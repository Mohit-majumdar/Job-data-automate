from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import bs4
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import sys
import pandas as pd
import json
import matplotlib.pyplot as plt

# Create ChromeOptions object
chrome_options = Options()

# Add the headless argument
chrome_options.add_argument('--headless')

with open("./input_data.json","r") as j_data:
    site_data = json.load(j_data)

def get_data(job_title, timeout=10, num_page=10,query=""):
    """get data for nukari.com specific job"""
    print("Start getting data for you")
    
    driver = Chrome(service=ChromeService(ChromeDriverManager().install()))

    max_wait_time = timeout

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

def create_query(job_title,experience,ctc):
    
    query = f"k={job_title}"
    if experience != "":
        query = query + f"&experience={experience}"
    if ctc != "":
        query = query + f"&ctcFilter={site_data.get('ctc').get(ctc,'0to3')}"
    return query

def write_dataframe(df: pd.DataFrame, filename="data"):
    
    if filename == "":
        filename = "data"

    df.to_excel(f"./{filename}.xlsx",index=False)

def create_pie_chart(df,file_name):

    categories_df = df['Skill Tags'].str.split(',', expand=True).stack()
    category_counts = categories_df.value_counts()
    category_counts = category_counts[category_counts > 10]
    labels = category_counts.index
    sizes = category_counts.values
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal') 
    plt.savefig(f"{file_name}_pie.png")


if __name__ == "__main__":

    name_map = {
        "Job Name": [],
        "Experience": [],
        "Salary": [],
        "Skill Tags": [],
        "Location": [],
        "Company":[],
        "Job link": []

    }
    try:
        job_title = sys.argv[1]
        df = get_data(job_title)
        write_dataframe(df)
    except IndexError:
        job_title = input("Enter Job title: ")
        exp = input("Enter Your Exprience: ")
        ctc = input("Enter your CTC: ")
        img = input("want pie chart for skills? [Y/N]: ")
        file_name = input("Enter file name you want to save: ")
        query = create_query(job_title,exp,ctc)
        df = get_data(job_title,query=query)
        if img.upper() == "Y":
            create_pie_chart(df,file_name)
        write_dataframe(df, file_name)
