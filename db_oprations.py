from pymongo import MongoClient
from datetime import datetime
from decouple import config


class Db_oprations:
    """all db oprations are perfom eg: Insert, Read, Update"""

    def __init__(self) -> None:
        user_name = config("DB_USERNAME")
        password = config("DB_PASSWORD")
        address = config("IP_ADDRESS")
        self.connection_string = f"mongodb://{user_name}:{password}@{address}"
        self.client = MongoClient(self.connection_string)
        self.db = self.client.jobData
        self.collection = self.db.job_data

    def create_db_key(self, job_title, job_exp, ctc, app) -> str:
        common_words = ["developer", "engineer"]
        job_title = job_title.lower()
        for word in common_words:
            job_title = job_title.replace(word, "")

        job_title = job_title.replace("+", "").replace(" ", "")

        key = "_".join([job_title, job_exp, ctc, app.lower()])
        return key

    def write_to_db(
        self, job_title, incoming_data, job_exp="", ctc="", app="", key=None
    ):
        if not key:
            key = self.create_db_key(job_title, job_exp, ctc, app)
        time_now = datetime.now()
        data = {
            "key": key,
            "data": incoming_data.to_dict(orient="records"),
            "created_at": time_now,
            "updated_at": time_now,
        }
        self.collection.insert_one(data)

    def read_from_db(self, job_title, job_exp, ctc, app):
        key = self.create_db_key(job_title, job_exp, ctc, app)
        data = self.collection.find_one({"key": key})

        return data

    def add_to_search_queue(self, job_title, job_exp, ctc, app):
        collection = self.db.search_queue
        key = self.create_db_key(job_title, job_exp, ctc, app)
        obj = collection.find_one({"key": key})
        if not obj:
            collection.insert_one({"key": key})
