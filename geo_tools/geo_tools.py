import json
import requests
import pandas as pd
from threading import Lock
from math import sin, cos, sqrt, atan2, radians
from concurrent.futures import ThreadPoolExecutor


class Geotools:
    """
    this module is built to execute the task given by Dokka and to hold functions related to geographical oriented methods.
    """
    def __init__(self, df):
        self.df = df
        self.lock = Lock()
        self.res = {'links': [],
                    'points': []}

    def _validate_geo_df(self):
        """
        the purpose of this function is to check that the following df contains the following columns.
        :param df: a pandas.DataFrame datatype
        return: boolean
        """
        return 'Point' in self.df.keys() and 'Latitude' in self.df.keys() and 'Longitude' in self.df.keys()

    def _get_address(self, args):
        point, x, y = args
        geocode_service = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/reverseGeocode"
        geocode_params = {'location': f'{float(x)},{float(y)}', 'langCode': 'en', 'outSR': '', 'forStorage': 'false', 'f': 'pjson'}

        res = requests.get(geocode_service, params=geocode_params)
        with self.lock:
            try:
                self.res['points'].append({'name': point, 'address': json.loads(res.text)['address']['Address']})
            except KeyError:
                self.res['points'].append({'name': point, 'address': ""})

    @staticmethod
    def _get_distance(point, point2):
        """
        :param point: tuple which holds (lat, lon)
        :param point2: tuple which holds (lat, lon)
        :return the distance between two coordinates
        """
        # approximate radius of earth in km
        R = 6373.0
        x1, y1 = point
        x2, y2 = point2
        lat1 = radians(float(x1))
        lon1 = radians(float(y1))
        lat2 = radians(float(x2))
        lon2 = radians(float(y2))

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        #distance in meters
        distance = R * c * 1000
        return distance
    
    def _create_links(self, args):
        """
        this function takes a tuple of tuples as an argument.
        each tuple inside the tuple should contain [POINT, LAT, LON]
        this function links all the points in the tuples together and calls the _get_distance method to calculate
        the distance between the points
        this function uses links as a hash table to document each insertion into the self.res['links'] list
        :param args:
        :return:
        """
        links = {}
        for i_point, i_lat, i_lon in args:
            for j_point, j_lat, j_lon in args:
                if i_point == j_point:
                    continue
                elif f'{i_point}{j_point}' in links or f'{j_point}{i_point}' in links:
                    continue
                else:
                    self.res['links'].append({'name': f'{i_point}{j_point}',
                                              'distance': self._get_distance([i_lat, i_lon], [j_lat, j_lon])})
                    links[f'{i_point}{j_point}'] = True

    def dokka_task(self):
        """
        this function executes all the above functions to answer to Dokka's mission
        :return: dictionary which contains an error if the csv is not valid else dictionary containing links and points
        """
        if not self._validate_geo_df():
            return {'error': {'status_code': 405, 'description': 'the csv you entered is not valid'}}

        args = [[row['Point'], row['Latitude'], row['Longitude']] for index, row in self.df.iterrows()]

        with ThreadPoolExecutor() as executor:
            executor.map(self._get_address, args)
        self._create_links(args)

        return self.res


if __name__ == '__main__':
    df = pd.read_csv('/Users/YanivAkiva/Desktop/dokka_test.csv')
    print(Geotools(df).dokka_task())
