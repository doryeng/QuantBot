from pymongo import MongoClient
from pymongo.cursor import CursorType
import configparser

class MongoDBHandler:
    """
    MongoDB를 Python에서 사용하기 위해 작성한 클래스입니다.
    """
    def __init__(self):
        """
        mongoDB의 접속 정보를 로딩하고 _client에 저장합니다.
        """
        config = configparser.ConfigParser()
        config.read('C:\\Users\\mskwon\\Documents\\GitHub\\QuantBot\\conf\\config.ini')
        host = config['MONGODB']['host']
        port = config['MONGODB']['port']
        self._client = MongoClient(host, int(port))

    def insert_item_one(self, data, db_name=None, collection_name=None):
        """
        MongoDB의 insertOne()을 실행하는 함수입니다.

        :param datas:dict: 저장할 문서
        :param db_name:str
        :param collection_name:str
        :return inserted_id:str: 입력 완료된 문서의 ObjectId를 반환합니다.
        :raises Exception: data가 없거나 type이 dict이 아니면 예외(Exception)을 발생시킵니다.
        :raises Exception: 매개변수 db_name과 collection_name이 없으면 예외(Exception)을 발생시킵니다.
        """
        if not isinstance(data, dict):
            raise Exception("data type should be dict")
        if db_name is None or collection_name is None:
            raise Exception("Need to param db_name, collection_name")
        return self._client[db_name][collection_name].insert_one(data).inserted_id

    def insert_item_many(self, datas, db_name=None, collection_name=None):
        """
        MongoDB의 insertMany()를 실행하는 함수입니다.

        :param datas:list
        :param db_name:str
        :param collection_name:str
        :return inserted_ids: 입력 완료된 문서의 ObjectId list를 반환합니다.
        :raises Exception: datas가 없거나 type이 list가 아니면 예외(Exception)을 발생시킵니다.
        :raises Exception: 매개변수 db_name과 collection_name이 없으면 예외(Exception)을 발생시킵니다.
        """
        if not isinstance(datas, list):
            raise Exception("datas type should be list")
        if db_name is None or collection_name is None:
            raise Exception("Need to param db_name, collection_name")
        return self._client[db_name][collection_name].insert_many(datas).inserted_ids

    def find_item(self, condition=None, db_name=None, collection_name=None):
        """
        MongoDB의 find()를 실행하는 함수입니다.

        :param condition:dict: 검색 조건을 dictionary 형태로 받습니다.
        :param db_name:str
        :param collection_name:str
        :return Cursor: Cursor를 반환합니다.
        :raises Exception: 매개변수 db_name과 collection_name이 없으면 예외(Exception)을 발생시킵니다.
        """
        if condition is None or not isinstance(condition, dict):
            condition = {}
        if db_name is None or collection_name is None:
            raise Exception("Need to param db_name, collection_name")
        return self._client[db_name][collection_name].find(condition, {"_id": False}, no_cursor_timeout=True, cursor_type=CursorType.EXHAUST)

    def find_item_one(self, condition=None, db_name=None, collection_name=None):
        """
        MongoDB의 findOne()을 실행하는 함수입니다.

        :param condition:dict: 검색 조건을 dictionary 형태로 받습니다.
        :param db_name:str
        :param collection_name:str
        :return document:dict: 검색된 문서가 있으면 문서의 내용을 반환합니다.
        :raises Exception: 매개변수 db_name과 collection_name이 없으면 예외(Exception)을 발생시킵니다.
        """
        if condition is None or not isinstance(condition, dict):
            condition = {}
        if db_name is None or collection_name is None:
            raise Exception("Need to param db_name, collection_name")
        return self._client[db_name][collection_name].find_one(condition, {"_id": False})

    def delete_item_many(self, condition=None, db_name=None, collection_name=None):
        """
        MongoDB의 deleteMany()를 실행하는 함수입니다.

        :param condition:dict: 삭제 조건을 dictionary 형태로 받습니다.
        :param db_name:str
        :param collection_name:str
        :return DeleteResult:obj: PyMongo의 문서의 삭제 결과 객체 DeleteResult가 반환됩니다.
        :raises Exception: condition이 없거나 type이 dict이 아니면 예외(Exception)을 발생시킵니다.
        :raises Exception: 매개변수 db_name과 collection_name이 없으면 예외(Exception)을 발생시킵니다.
        """
        if condition is None or not isinstance(condition, dict):
            raise Exception("Need to condition")
        if db_name is None or collection_name is None:
            raise Exception("Need to param db_name, collection_name")
        return self._client[db_name][collection_name].delete_many(condition)

    def update_item_many(self, condition=None, update_value=None, db_name=None, collection_name=None):
        """
        MongoDB의 updateMany()를 실행하는 함수입니다.

        :param condition:dict: 갱신 조건을 dictionary 형태로 받습니다.
        :param update_value:dict: 갱신하고자 하는 값을 dictionary 형태로 받습니다.
        :param db_name:str
        :param collection_name:str
        :return UpdateResult:obj: PyMongo의 문서의 갱신 결과 객체 UpdateResult가 반환됩니다.
        :raises Exception: condition이 없거나 type이 dict이 아니면 예외(Exception)을 발생시킵니다.
        :raises Exception: update_value가 없으면 예외(Exception)을 발생시킵니다.
        :raises Exception: 매개변수 db_name과 collection_name이 없으면 예외(Exception)을 발생시킵니다.
        """
        if condition is None or not isinstance(condition, dict):
            raise Exception("Need to condition")
        if update_value is None:
            raise Exception("Need to update value")
        if db_name is None or collection_name is None:
            raise Exception("Need to param db_name, collection_name")
        return self._client[db_name][collection_name].update_many(filter=condition, update=update_value)

    def update_item_one(self, condition=None, update_value=None, db_name=None, collection_name=None):
        """
        MongoDB의 updateOne()을 실행하는 함수입니다.

        :param condition:dict: 갱신 조건을 dictionary 형태로 받습니다.
        :param update_value:dict: 갱신하고자 하는 값을 dictionary 형태로 받습니다.
        :param db_name:str
        :param collection_name:str
        :return UpdateResult:obj: PyMongo의 문서의 갱신 결과 객체 UpdateResult가 반환됩니다.
        :raises Exception: condition이 없거나 type이 dict이 아니면 예외(Exception)을 발생시킵니다.
        :raises Exception: update_value가 없으면 예외(Exception)을 발생시킵니다.
        :raises Exception: 매개변수 db_name과 collection_name이 없으면 예외(Exception)을 발생시킵니다.
        """
        if condition is None or not isinstance(condition, dict):
            raise Exception("Need to condition")
        if update_value is None:
            raise Exception("Need to update value")
        if db_name is None or collection_name is None:
            raise Exception("Need to param db_name, collection_name")
        return self._client[db_name][collection_name].update_one(filter=condition, update=update_value)

    def aggregate(self, pipeline=None, db_name=None, collection_name=None):
        """
        MongoDB의 aggregate()를 실행하는 함수입니다.
        :param pipeline:list: 갱신 조건을 dictionary의 리스트 형태로 받습니다.
        :param db_name:str
        :param collection_name:str
        :return CommandCursor:obj: PyMongo의 CommandCursor가 반환됩니다.
        :raises Exception: pipeline이 없거나 type이 list가 아니면 예외(Exception)을 발생시킵니다.
        :raises Exception: 매개변수 db_name과 collection_name이 없으면 예외(Exception)을 발생시킵니다.
        """
        if pipeline is None or not isinstance(pipeline, list):
            raise Exception("Need to pipeline")
        if db_name is None or collection_name is None:
            raise Exception("Need to param db_name, collection_name")
        return self._client[db_name][collection_name].aggregate(pipeline)

    def text_search(self, text=None, db_name=None, collection_name=None):
        """
        MongoDB의 text search를 위한 함수입니다.
        :param text:str: 검색할 문자
        :param db_name:str
        :param collection_name:str
        :return Cursor: Cursor를 반환합니다.
        """
        if text is None or not isinstance(text, str):
            raise Exception("Need to text")
        if db_name is None or collection_name is None:
            raise Exception("Need to param db_name, collection_name")
        return self._client[db_name][collection_name].find({"$text": {"$search": text}})
