from flask import Flask, render_template, request, jsonify
import json
from .db_oprations import Db_oprations


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_data", methods=["POST"])
def generate_data():
    """generate data from input"""
    query_prams = json.loads(request.data)
    app_name = query_prams.get("app", "")
    salary = query_prams.get("salary", "0")
    experience = query_prams.get("experience", "0")
    job_title = query_prams.get("job-title", "")

    db = Db_oprations()
    data = db.read_from_db(job_title, experience, salary, app_name)

    if not data:
        db.add_to_search_queue(job_title, experience, salary, app_name)
        return jsonify(message="We will get data shorty for you"), 300
    return {"data": data.get("data"), "pie_data": data.get("pie_data")}
