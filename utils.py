import json
import re

import requests
from bs4 import BeautifulSoup


# Don't use this function directly in script.py. Use load_file() instead...
def get_courses():
    res = requests.get("https://nptel.ac.in/courses/")
    soup = BeautifulSoup(res.content, "html.parser")
    content = soup.find("script")
    if content:
        pattern = r'id:(\d+),\s*title:"([^"]+)".*?instituteName:"([^"]+)"'
        pairs = re.findall(pattern, content.text)
        if pairs:
            course_map = {}
            for course_id, title, institute in pairs:
                title = title.replace("NOC:", "").strip()
                if title not in course_map:
                    course_map[title] = []
                course_map[title].append({"id": int(course_id), "institute": institute})

            with open("courses.json", "w", encoding="utf-8") as f:
                json.dump(course_map, f, indent=4, ensure_ascii=False)
            return course_map
        else:
            print("Error loading data... :(")
            return None
    else:
        print("Error loading data... :(")
        return None


# This is to load the scrapped data of course-id pair from NPTEL web page.
def load_file():
    try:
        with open("courses.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return get_courses()
    except Exception as e:
        print(f"Error loading data... :({e}")
        return None


# Don't use this in script.py.
def abbrivate_subject(subject_name):
    words = [
        w
        for w in subject_name.split()
        if w.lower() not in ["and", "to", "for", "of", "in"]
    ]
    if len(words) >= 2:
        return "".join([word[0].upper() for word in words])
    else:
        return subject_name


# This is to get subject of intrest input from the user.
def getSubjectIdAndAbbrivation(courses):
    checker = {sub.lower(): (sub, info) for sub, info in courses.items()}
    while True:
        try:
            subject = input("Enter subject: ").strip()
            if not subject:
                print("Skipping subject...")
                return None, None, None
            if subject.lower() in checker:
                subject_name, info_list = checker[subject.lower()]
                if len(info_list) == 1:
                    course_id = info_list[0]["id"]
                    return subject_name, course_id, abbrivate_subject(subject_name)
                else:
                    institutes_offering = []
                    for x in info_list:
                        if x["institute"].startswith("IIT "):
                            institute_abbr = "IIT " + x["institute"][4]
                        elif x["institute"].startswith("IITT "):
                            institute_abbr = "IIIT " + x["institute"][5]
                        elif x["institute"].startswith("IISc "):
                            institute_abbr = "IISc Banglore"
                        else:
                            institute_abbr = x["institute"]
                        institutes_offering.append(institute_abbr)
                    state = False
                    print(f"Institute Code : Institute Offering {subject}")
                    for i in range(len(institutes_offering)):
                        print(f"{i + 1}: {institutes_offering[i]}")
                    institute_code = input(
                        f"Choose your institute code for your institute of interest from the above institutes offering {subject}"
                    )
                    if institute_code.isdigit() and int(institute_code) in range(
                        1, len(institutes_offering) + 1
                    ):
                        state = True
                    while state == False:
                        institute_code = input(
                            f"Choose a valid institute offering {subject}"
                        )
                        if institute_code.isdigit() and int(institute_code) in range(
                            1, len(institutes_offering) + 1
                        ):
                            state = True
                    course_id = info[int(institute_code) - 1]["id"]
                    return subject_name, course_id, abbrivate_subject(subject_name)
            raise ValueError("Subject not found. Please enter a valid subject.")
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid subject.")
        except Exception:
            print("Please enter a valid subject.")


# Don't use this in script.py.
def abbrivate_subject(subject_name):
    words = [
        w
        for w in subject_name.split()
        if w.lower() not in ["and", "to", "for", "of", "in"]
    ]
    if len(words) >= 2:
        return "".join([word[0].upper() for word in words])
    else:
        return subject_name


# This is to get subject of intrest input from the user.
def getSubjectIdAndAbbrivation(courses):
    checker = {sub.lower(): (sub, info) for sub, info in courses.items()}
    while True:
        try:
            subject = input("Enter subject: ").strip()
            if not subject:
                print("Skipping subject...")
                return None, None, None
            if subject.lower() in checker:
                subject_name, info_list = checker[subject.lower()]
                if len(info_list) == 1:
                    course_id = info_list[0]["id"]
                    return subject_name, course_id, abbrivate_subject(subject_name)
                else:
                    institutes_offering = []
                    for x in info_list:
                        if x["institute"].startswith("IIT "):
                            institute_abbr = "IIT " + x["institute"][4]
                        elif x["institute"].startswith("IITT "):
                            institute_abbr = "IIIT " + x["institute"][5]
                        elif x["institute"].startswith("IISc "):
                            institute_abbr = "IISc Banglore"
                        else:
                            institute_abbr = x["institute"]
                        institutes_offering.append(institute_abbr)
                    state = False
                    print(f"Institute Code : Institute Offering {subject}")
                    for i in range(len(institutes_offering)):
                        print(f"{i + 1}: {institutes_offering[i]}")
                    institute_code = input(
                        f"Choose your institute code for your institute of interest from the above institutes offering {subject}"
                    )
                    if institute_code.isdigit() and int(institute_code) in range(
                        1, len(institutes_offering) + 1
                    ):
                        state = True
                    while state == False:
                        institute_code = input(
                            f"Choose a valid institute offering {subject}"
                        )
                        if institute_code.isdigit() and int(institute_code) in range(
                            1, len(institutes_offering) + 1
                        ):
                            state = True
                    course_id = info[int(institute_code) - 1]["id"]
                    return subject_name, course_id, abbrivate_subject(subject_name)
            raise ValueError("Subject not found. Please enter a valid subject.")
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid subject.")
        except Exception:
            print("Please enter a valid subject.")


def get_course_stats(course_id):
    url = f"https://nptel.ac.in/api/stats/{course_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
