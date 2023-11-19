from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import bs4
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import sys
import pandas as pd

# Create ChromeOptions object
chrome_options = Options()

# Add the headless argument
chrome_options.add_argument('--headless')


def get_data(job_title, timeout=10, num_page=10):
    """get data for nukari.com specific job"""
    print("Start getting data for you")
    driver = Chrome()

    max_wait_time = timeout

    for i in range(1, num_page+1):

        url = f"https://www.naukri.com/{job_title}-jobs-{i}?k={job_title}&experience=3&ctcFilter=6to10&ctcFilter=10to15&ctcFilter=15to25"
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


def write_dataframe(df: pd.DataFrame, filename="data"):
    
    if filename == "":
        filename = "data"

    df.to_excel(f"./{filename}.xlsx")


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
        file_name = input("Enter file name you want to save: ")
        df = get_data(job_title)
        write_dataframe(df, file_name)
