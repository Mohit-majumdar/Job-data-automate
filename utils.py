import re


def remove_special_characters(input_string):
    # Define a regular expression pattern to match special characters
    # This pattern allows alphanumeric characters and spaces
    pattern = r'[^a-zA-Z0-9\s]'

    # Use re.sub to replace matched characters with an empty string
    result = re.sub(pattern, ' ', input_string)

    return result


def get_monster_job_link(job_title, company, location, el_id):
    s = "-".join([job_title, company, location.split(",")[0], el_id])
    s = remove_special_characters(s)
    return "https://www.foundit.in/job/" + s.replace(" ", "-").lower()
