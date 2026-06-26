import json
import re

import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup

# For Excel
header = [
    "Enrolled",
    "Registered",
    "Certified",
    "Gold",
    "Silver",
    "Elite",
    "Success",
    "Participation",
    "Toppers",
    "max_mark",
    "min_mark",
    "average",
    "standard_deviation",
]


# To create a loop to ask for as many as input as user wishes.
def validator(parameter, defaultYes):
    if defaultYes:
        defaultKey = "y"
        oppositeKey = "n"
    else:
        defaultKey = "n"
        oppositeKey = "y"
    if parameter.lower() == defaultKey or parameter.lower() == "":
        return defaultKey
    elif parameter.lower() == oppositeKey:
        return oppositeKey
    else:
        parameter = input("Invalid input. Please enter a valid option (y/N): ")
        return validator(parameter, defaultYes)


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
def getSubjectIdAndAbbrivation(courses, is_doc, subject):
    checker = {sub.lower(): (sub, info) for sub, info in courses.items()}
    while True:
        try:
            if not is_doc:
                subject = input("Enter subject: ").strip()
            else:
                subject = subject
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
                        f"Choose your institute code for your institute of interest from the above institutes offering {subject} : "
                    )
                    if institute_code.isdigit() and int(institute_code) in range(
                        1, len(institutes_offering) + 1
                    ):
                        state = True
                    while state == False:
                        institute_code = input(
                            f"Choose a valid institute offering {subject} : "
                        )
                        if institute_code.isdigit() and int(institute_code) in range(
                            1, len(institutes_offering) + 1
                        ):
                            state = True
                    course_id = info_list[int(institute_code) - 1]["id"]
                    return subject_name, course_id, abbrivate_subject(subject_name)
            if is_doc:
                print(f"Subject '{subject}' not found in database. Skipping...")
                return None, None, None
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


# For calculating the mean in case of data from multiple years available
def average_stat(stat):
    if not stat.get("data") or len(stat["data"]) == 0:
        print("No statistical data available for this course on NPTEL.")
        return None
    # Cleaning
    course_stats = stat["data"][0]["run_wise_stats"]
    # Mean calculation
    df = pd.DataFrame(course_stats)
    df = df.drop(columns=["Timeline", "noc_courseid"]).astype(float)
    df = df.mean().to_dict()
    if df:
        return df
    else:
        print("Corrupt data")
        return None


# To add helper parameters to the subject's stat list (calculated from existing data)
def add_parameters(result, subject, abbr):
    res = result.copy()
    registered = res["Registered"]

    res["cert_percent"] = (res["Certified"] / registered) * 100
    res["gold_percent"] = (res["Gold"] / registered) * 100
    res["performance_percent"] = ((res["Elite"]) / registered) * 100
    res["success_percent"] = ((res["Success"] + res["Elite"]) / registered) * 100

    base_score = (
        (res["cert_percent"] * 0.85)
        + (res["performance_percent"] * 0.70)
        + (res["gold_percent"] * 0.50)
        + (res["average"] * 1.00)
    )

    std_dev_penalty = res["standard_deviation"] * 1.5
    enrollment_penalty = min(20, res["Enrolled"] * 0.005)
    final_score = base_score - std_dev_penalty - enrollment_penalty
    res["score"] = max(0, round(final_score, 2))
    res["Subject Abbreviation"] = abbr
    res["Subject"] = subject

    return res


# To save the list of selected subject as excel sheet
def save_to_excel(df):
    calculated_columns = [
        col
        for col in df.columns
        if col not in ["Subject", "Subject Abbreviation"] + header
    ]
    columns_order = ["Subject", "Subject Abbreviation"] + header + calculated_columns
    df = df[columns_order]
    df = df.round(2)

    df.to_excel("nptel_statistics.xlsx", index=False)
    print("Statistics saved to nptel_statistics.xlsx")


# To plot the data and save as png for chosen subject


def plot(df):
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10))
    subjects = df["Subject Abbreviation"].tolist()
    calculated_columns = [
        col
        for col in df.columns
        if col
        in [
            "min_mark",
            "max_mark",
            "average",
            "standard_deviation",
            "cert_percent",
            "gold_percent",
            "performance_percent",
            "success_percent",
            "score",
        ]
    ]

    df.plot(
        x="Subject",
        y=calculated_columns,
        kind="line",
        marker="o",
        ax=axes[0],
        colormap="viridis",
    )
    axes[0].set_title(
        "Calculated Metrics & Score by Subject", fontsize=14, fontweight="bold"
    )
    axes[0].set_ylabel("Value", fontsize=12)
    axes[0].legend(loc="upper right")

    axes[0].tick_params(axis="x", which="both", bottom=False, labelbottom=False)
    axes[0].set_xlabel("")

    for line in axes[0].lines:
        for x_val, y_val in zip(line.get_xdata(), line.get_ydata()):
            idx = int(x_val)
            if 0 <= idx < len(subjects):
                axes[0].annotate(
                    subjects[idx],
                    xy=(x_val, y_val),
                    xytext=(0, 6),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                )

    df.plot(
        x="Subject",
        y="standard_deviation",
        kind="line",
        marker="o",
        color="tomato",
        ax=axes[1],
        legend=False,
    )
    axes[1].set_title("Standard Deviation by Subject", fontsize=14, fontweight="bold")
    axes[1].set_ylabel("Standard Deviation", fontsize=12)

    axes[1].tick_params(axis="x", which="both", bottom=False, labelbottom=False)
    axes[1].set_xlabel("")

    for line in axes[1].lines:
        for x_val, y_val in zip(line.get_xdata(), line.get_ydata()):
            idx = int(x_val)
            if 0 <= idx < len(subjects):
                axes[1].annotate(
                    subjects[idx],
                    xy=(x_val, y_val),
                    xytext=(0, 6),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                )

    plt.tight_layout()
    plt.savefig("nptel_plot.png", bbox_inches="tight")
    print("Plot saved as nptel_plot.png")


def save_results(result_list):
    df = pd.DataFrame(result_list)
    df.rename(columns={"index": "Subject"}, inplace=True)

    save_to_excel(df)
    plot(df)
