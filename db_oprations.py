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
        self.job_collection = self.db.job_data
        self.queue_job_collection = self.db.search_queue

    def create_db_key(self, job_title, job_exp, ctc, app) -> str:
        common_words = ["developer", "engineer"]
        job_title = job_title.lower()
        for word in common_words:
            job_title = job_title.replace(word, "")

        job_title = job_title.replace("+", "").replace(" ", "")

        key = "_".join([job_title, job_exp, ctc, app.lower()])
        return key

    def write_to_db(
        self,
        job_title,
        incoming_data,
        job_exp="",
        ctc="",
        app="",
        key=None,
        pie_data=None,
    ):
        if not key:
            key = self.create_db_key(job_title, job_exp, ctc, app)
        time_now = datetime.now()
        data = {
            "key": key,
            "data": incoming_data.to_dict(orient="records"),
            "pie_data": pie_data,
            "created_at": time_now,
            "updated_at": time_now,
        }
        self.job_collection.insert_one(data)

    def read_from_db(self, job_title, job_exp, ctc, app):
        key = self.create_db_key(job_title, job_exp, ctc, app)
        data = self.job_collection.find_one({"key": key})

        return data

    def add_to_search_queue(self, job_title, job_exp, ctc, app):
        key = self.create_db_key(job_title, job_exp, ctc, app)
        obj = self.queue_job_collection.find_one({"key": key})
        if not obj:
            self.queue_job_collection.insert_one({"key": key})

    def pending_jobs_in_queue(self):
        return self.queue_job_collection.find()

    def remove_jobs_from_queue(self, job_key):
        self.queue_job_collection.find_one_and_delete({"key": job_key})

    def older_job(self, filter_time):
        return self.job_collection.find({"updated_at": {"$lt": filter_time}})

    def update_job(self, job_key, incoming_data, pie_data):
        data = incoming_data.to_dict(orient="records")
        self.job_collection.find_one_and_update(
            {"key": job_key},
            {
                "$set": {
                    "data": data,
                    "pie_data": pie_data,
                    "updated_at": datetime.now(),
                }
            },
        )
