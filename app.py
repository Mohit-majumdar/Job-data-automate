from flask import Flask, render_template, request
from .get_data import get_data, create_pie_chart, create_query
import json


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_data", methods=["POST"])
def generate_data():
    """generate data from input"""
    query_prams = json.loads(request.data)
    app_name = query_prams.get("app", "")
    salary = query_prams.get("salary", "")
    experience = query_prams.get("experience", "")
    job_title = query_prams.get("job-title", "")

    query = create_query(job_title, experience, salary, app_name)

    data = get_data(job_title, query, app_name)
    return data.to_dict(orient="records")
