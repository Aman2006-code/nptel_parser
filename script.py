import pandas as pd

import utils

course_key = utils.load_file()


result_list = []


def main(subject, is_doc):
    res = None
    if is_doc:
        course, course_id, course_abbr = utils.getSubjectIdAndAbbrivation(
            course_key, True, subject
        )
    else:
        course, course_id, course_abbr = utils.getSubjectIdAndAbbrivation(
            course_key, False, None
        )
        done_not = utils.validator(
            input("Do you want to add another subject? (Y/n): "), True
        )
    course_stats = utils.get_course_stats(course_id)
    if course_stats:
        res = utils.average_stat(course_stats)
    else:
        if is_doc:
            print(f"Some Error occured..({course})")
        if not is_doc:
            if done_not == "n":
                print("Some inputs encountered error...")
                done_not = utils.validator(input("Do you want to retry? (Y/n): "))
                return done_not
    if res:
        res = utils.add_parameters(res, course, course_abbr)
        result_list.append(res)
    else:
        print("Not enough Data...Try re-entering the course...")
        if is_doc:
            print(f"Some inputs encountered error.({course})...")
        else:
            done_not = utils.validator(input("Do you want to retry? (Y/n): "))
            return done_not
    if not is_doc:
        return done_not
    else:
        return None


is_doc = utils.validator(
    input("Do you have a subject list in .txt format ? (Y/n): "), True
)
if is_doc == "n":
    is_doc = False
else:
    is_doc = True
if is_doc:
    with open("subject.txt", "r") as f:
        for line in f:
            subject = line.strip()
            temp = main(subject, True)
    f.close()
    isMore = utils.validator(input("Do you want to add more subjects? (y/N): "), False)
    if isMore.lower() == "n":
        done_not = "n"
    else:
        done_not = "y"
        while done_not.lower() != "n":
            done_not = main(None, False)

else:
    done_not = "y"
    while done_not.lower() != "n":
        done_not = main(None, False)

utils.save_results(result_list)
