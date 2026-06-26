import pandas as pd

import utils

course_key = utils.load_file()

done = "y"
result_list = []

while done.lower() != "n":
    course, course_id, course_abbr = utils.getSubjectIdAndAbbrivation(course_key)
    done = utils.validator(input("Do you want to add another subject? (Y/n): "))
    course_stats = utils.get_course_stats(course_id)
    if course_stats:
        res = utils.average_stat(course_stats)

    else:
        print("Some Error occured")
        if done == "n":
            done = utils.validator(input("Do you want to retry? (Y/n): "))
        break
    if res:
        res = utils.add_parameters(res, course, course_abbr)
        result_list.append(res)
    else:
        print("Not enough Data...Try re-entering the course...")
        if done == "n":
            done = utils.validator(input("Do you want to retry? (Y/n): "))
        break


if done.lower() == "n":
    df = pd.DataFrame(result_list)
    df.rename(columns={"index": "Subject"}, inplace=True)

    utils.save_to_excel(df)
    utils.plot(df)
