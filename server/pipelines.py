from server.models import Results
from sqlalchemy import create_engine
from sqlalchemy.pool import SingletonThreadPool
from sqlalchemy.orm import sessionmaker

#, poolclass=SingletonThreadPool


class ResultsPipelines:
    def __init__(self):
        engine = create_engine('sqlite:///dokka.db', connect_args={"check_same_thread": False}, poolclass=SingletonThreadPool)
        self.Session = sessionmaker(bind=engine)

    def insert_item(self, item):
        """
        this function takes a Table Object as an argument and inserts it into the database
        :param item:
        :return:
        """
        try:
            session = self.Session()
            session.add(item)
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            session.close()

    def insert_uuid(self, uuid, links, points):
        """
        this function takes the parameters and creates a Results Object and inserts the item into the database
        :param uuid:
        :param links:
        :param points:
        :return:
        """
        result = Results(uuid=str(uuid), links=str(links), points=str(points))
        self.insert_item(result)

    def check_uuid(self, uuid):
        """
        this function takes a uuid as a parameter and returns the first row it appears on the database
        :param uuid:
        :return:
        """
        session = self.Session()
        return session.query(Results).filter(Results.uuid == uuid).first()


if __name__ == '__main__':
    pass


