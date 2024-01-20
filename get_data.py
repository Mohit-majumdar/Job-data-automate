import sys
import pandas as pd
import json
import bs4
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import matplotlib.pyplot as plt
from pathlib import Path
from .utils import *
from urllib.parse import quote

# Global veribles
max_wait_time = 10
num_page = 2
OUTPUT_DIR = Path("./output")
EXCEL_DIR = OUTPUT_DIR / "excel_files"
PIE_DIR = OUTPUT_DIR / "piechart"
# Creating directory if not exist
OUTPUT_DIR.mkdir(exist_ok=True)
EXCEL_DIR.mkdir(exist_ok=True)
PIE_DIR.mkdir(exist_ok=True)


# reading config json file for all needed data
with open("./input_data.json", "r") as j_data:
    site_data = json.load(j_data)


def get_naukri_data(job_title, query="") -> pd.DataFrame:
    """getting data from naukri.com"""
    name_map = {
        "Job Name": [],
        "Experience": [],
        "Salary": [],
        "Skill Tags": [],
        "Location": [],
        "Company": [],
        "Job link": []

    }

    # initializing  chrome driver
    driver = Chrome(service=ChromeService(ChromeDriverManager().install()))
    for i in range(1, num_page+1):

        url = f"https://www.naukri.com/{job_title}-jobs-{i}?{query}"
        driver.get(url)

        try:
            element_present = EC.presence_of_element_located(
                (By.CLASS_NAME, 'srp-jobtuple-wrapper'))
            WebDriverWait(driver, max_wait_time).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
            continue

        source = driver.find_element(By.ID, "root").get_attribute("outerHTML")
        soup = bs4.BeautifulSoup(source, "html.parser")
        for el in soup.css.select(".srp-jobtuple-wrapper"):
            try:
                name = el.css.select_one(".title").getText()
                name_map["Job Name"].append(name)
            except:
                name_map["Job Name"].append(None)
            try:
                exp = el.css.select_one(".expwdth").getText()
                name_map["Experience"].append(exp)
            except:
                name_map["Experience"].append(None)
            try:
                location = el.css.select_one(".locWdth").getText()
                name_map["Location"].append(location)
            except:
                name_map["Location"].append(None)
            try:
                job_tags = ",".join([i.getText()
                                    for i in el.css.select("ul.tags-gt >li")])
                name_map["Skill Tags"].append(job_tags)
            except:
                name_map["Skill Tags"].append(None)
            try:
                job_link = el.find("a").get("href")
                name_map["Job link"].append(job_link)
            except:
                name_map["Job link"].append(None)
            try:
                salary = el.css.select_one(".sal-wrap").get_text()
                name_map["Salary"].append(salary)
            except:
                name_map["Salary"].append(None)

            try:
                company = el.css.select_one(".comp-name").getText()
                name_map["Company"].append(company)
            except:
                name_map["Company"].append(None)

        print(f"page {i} is completed.....")

    return pd.DataFrame(name_map)

# TODO: complete this


def get_linkedin_data() -> pd.DataFrame:
    name_map = {
        "Job Name": [],
        "Experience": [],
        "Salary": [],
        "Skill Tags": [],
        "Location": [],
        "Company": [],
        "Job link": []

    }

    pass

# TODO: complete this


def get_indded_data() -> pd.DataFrame:
    name_map = {
        "Job Name": [],
        "Experience": [],
        "Salary": [],
        "Skill Tags": [],
        "Location": [],
        "Company": [],
        "Job link": []

    }

    pass


def get_monster_data(query="") -> pd.DataFrame:
    name_map = {
        "Job Name": [],
        "Experience": [],
        "Salary": [],
        "Skill Tags": [],
        "Location": [],
        "Company": [],
        "Job link": []

    }

    driver = Chrome(service=ChromeService(ChromeDriverManager().install()))
    for limit in range(0, 200, 100):
        url = f"https://www.foundit.in/srp/results?{query}&start={limit}&limit=100"
        driver.get(url)
        try:
            element_present = EC.presence_of_element_located(
                (By.CLASS_NAME, 'srpResultCardContainer'))
            WebDriverWait(driver, max_wait_time).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
            continue

        source = driver.find_element(
            By.TAG_NAME, "body").get_attribute("outerHTML")
        soup = bs4.BeautifulSoup(source, "html.parser")
        els = soup.find_all("div", {"class": "srpResultCardContainer"})
        for el in els:
            try:
                job_title = el.find(
                    "div", {"class": "jobTitle"}).get_text(strip=True)
                name_map["Job Name"].append(job_title)
            except:
                name_map["Job Name"].append(None)

            try:
                company = el.find(
                    "div", {"class": "companyName"}).get_text(strip=True)
                name_map["Company"].append(company)
            except:
                name_map["Company"].append(None)

            try:
                skill = el.find("div", {"class": "skillDetails"}).get_text(
                    strip=True, separator=",")
                name_map["Skill Tags"].append(skill)
            except:
                name_map["Skill Tags"].append(None)
            try:
                details = el.find_all("div", {"class": "details"})
                for i in range(1, len(details)):
                    if i == 1:
                        location = details[i].get_text(strip=True)
                        name_map["Location"].append(location)
                    if i == 2:
                        exp = details[i].get_text(strip=True)
                        name_map["Experience"].append(exp)
                if len(details) == 4:
                    name_map["Salary"].append(details[3].get_text(strip=True))
                else:
                    name_map["Salary"].append(None)

            except:
                name_map["Location"].append(None)
                name_map["Experience"].append(None)
                name_map["Salary"].append(None)

            try:
                el_id = el.next_element.attrs.get("id")
                job_link = get_monster_job_link(
                    job_title, company, location, el_id)
                name_map["Job link"].append(job_link)
            except:
                name_map["Job link"].append(None)

    return pd.DataFrame(name_map)


def get_data(job_title, query="", app=""):
    """get data for specific job"""

    print("Start getting data for you")
    app = app.lower()
    if app == "naukri":
        return get_naukri_data(job_title, query)
    if app == "foundit":
        return get_monster_data(query)

    return pd.DataFrame()


def create_query(job_title, experience, ctc, app=""):
    d = site_data.get(app.lower())
    if not d:
        print("Entered wrong app name")
        sys.exit(1)
    q, exp, salary, ctc_map = d.values()

    query = f"{q}={job_title}"
    if experience != "":
        query = query + f"&{exp}={experience}"
    if ctc != "":
        query = query + f"&{salary}={ctc_map.get(ctc,'0to3')}"

    return query


def write_dataframe(df: pd.DataFrame, filename="data"):

    if filename == "":
        filename = "data"

    df.to_excel(f"{EXCEL_DIR}/{filename}.xlsx", index=False)


def create_pie_chart(df, file_name):

    categories_df = df['Skill Tags'].str.split(',', expand=True).stack()
    category_counts = categories_df.value_counts()
    category_counts = category_counts[category_counts > 10]
    labels = category_counts.index
    sizes = category_counts.values
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.savefig(f"{PIE_DIR}/{file_name}_pie.png")


if __name__ == "__main__":

    try:
        job_title = sys.argv[1]
        df = get_data(job_title)
        write_dataframe(df)
    except IndexError:
        job_title = input("Enter Job title: ").replace(" ", "+")
        exp = input("Enter Your Experience: ")
        ctc = input("Enter your CTC: ")
        img = input("want pie chart for skills? [Y/N]: ")
        app = input("Select app from want data? ['Naukri','Foundit']: ")
        file_name = input("Enter file name you want to save: ")
        query = create_query(job_title, exp, ctc, app)
        df = get_data(job_title, app=app, query=query)
        if img.upper() == "Y":
            create_pie_chart(df, file_name)
        write_dataframe(df, file_name)
