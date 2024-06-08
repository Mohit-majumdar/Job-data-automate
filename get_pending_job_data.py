from get_data import get_data, create_query, create_pie_chart
from db_oprations import Db_oprations
from datetime import datetime, timedelta

DB = Db_oprations()


def get_data_for_job_queue():
    all_jobs = DB.pending_jobs_in_queue()
    for job in all_jobs:
        job_key = job.get("key")
        DB.remove_jobs_from_queue(job_key)
        print(job_key)
        job_title, exp, ctc, app = job_key.split("_")
        query = create_query(job_title, exp, ctc, app)
        data = get_data(job_title, query, app)
        pie_data = ""
        if not data.empty:
            pie_data = create_pie_chart(data, "")
        DB.write_to_db(job_title, data, key=job_key, pie_data=pie_data)


def update_jobs():
    filer_time = datetime.now() - timedelta(days=5)
    jobs = DB.older_job(filer_time)
    for job in jobs:
        print(job.get("key"), job.get("updated_at"))
        job_key = job.get("key")
        job_title, exp, ctc, app = job_key.split("_")
        query = create_query(job_title, exp, ctc, app)
        data = get_data(job_title, query, app)
        pie_data = ""
        if not data.empty:
            pie_data = create_pie_chart(data, "")
        print(pie_data)
        DB.update_job(job_key, data, pie_data)


get_data_for_job_queue()
update_jobs()
