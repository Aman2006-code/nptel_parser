import matplotlib.pyplot as plt
import pandas as pd


def validator(parameter):
    if parameter.lower() == "n" or parameter.lower() == "":
        return "n"
    elif parameter.lower() == "y":
        return "y"
    else:
        parameter = input("Invalid input. Please enter a valid option (y/N): ")
        return validator(parameter)


def get_subject():
    while True:
        sub = input("Enter subject: ")
        sub_abbr = sub.split()
        try:
            for x in sub_abbr:
                if x.isnumeric():
                    raise ValueError("Subject abbreviation must be alphabetic")
            if len(sub_abbr) >= 3:
                sub_abbr = (
                    "".join([sub_abbr[x][0] for x in range(len(sub_abbr) - 2)])
                    + ", "
                    + sub_abbr[-2]
                    + sub_abbr[-1][0]
                )
                return sub, sub_abbr
            elif sub == "":
                print("Skipping subject...")
                return None, None
            else:
                raise ValueError(
                    "Subject abbreviation must have at least 3 words.Leave empty to skip."
                )
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid subject.")
        except Exception:
            print("Please enter a valid subject.")


def get_data():
    while True:
        data_string = input("Enter data string: ")
        data = data_string.split()
        try:
            if len(data) == 13:
                [float(x) for x in data]
                return data
            elif len(data) == 0:
                print("Skipping data...")
                return None
            else:
                raise ValueError(
                    "Lacks enough data...Try again... or leave empty to skip."
                )
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid data string.")
        except Exception:
            print("Please enter a valid data string.")


done = "n"

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
    "Minimum Mark",
    "Maximum Mark",
    "Average Mark",
    "Standard Deviation",
]


result_list = {}
while done.lower() != "y":
    subject, subject_abbr = get_subject()
    data = get_data()
    if not data or not subject:
        continue
    res = {}
    for i in range(len(data)):
        res[header[i]] = float(data[i])

    registered = res["Registered"]

    res["cert_percent"] = (res["Certified"] / registered) * 100
    res["gold_percent"] = (res["Gold"] / registered) * 100
    res["performance_percent"] = (
        (res["Gold"] + res["Silver"] + res["Elite"]) / registered
    ) * 100
    res["success_percent"] = (res["Success"] / registered) * 100

    base_score = (
        (res["cert_percent"] * 0.85)
        + (res["performance_percent"] * 0.70)
        + (res["gold_percent"] * 0.50)
        + (res["Average Mark"] * 1.00)
    )

    std_dev_penalty = res["Standard Deviation"] * 1.5
    enrollment_penalty = min(20, res["Enrolled"] * 0.005)

    final_score = base_score - std_dev_penalty - enrollment_penalty
    res["score"] = max(0, round(final_score, 2))
    res["Subject Abbreviation"] = subject_abbr

    if subject in result_list:
        print("Recheck Entry!! Possible duplication")
    else:
        result_list[subject] = res

    done = input("Is this the last subject? (y/N): ")
    done = validator(done)

if done.lower() == "y":
    df = pd.DataFrame.from_dict(result_list, orient="index").reset_index()
    df.rename(columns={"index": "Subject"}, inplace=True)

    calculated_columns = [
        col
        for col in df.columns
        if col not in ["Subject", "Subject Abbreviation"] + header
    ]
    columns_order = ["Subject", "Subject Abbreviation"] + header + calculated_columns
    df = df[columns_order]

    df.to_excel("nptel_statistics.xlsx", index=False)
    print("Statistics saved to nptel_statistics.xlsx")

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10))

    subjects = df["Subject Abbreviation"].tolist()

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
                    fontweight="semibold",
                )

    df.plot(
        x="Subject",
        y="Standard Deviation",
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
                    fontweight="semibold",
                )

    plt.tight_layout()
    plt.savefig("nptel_charts.png", dpi=300)
    plt.show()
