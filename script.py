# keys = [
#     "Enrolled",
#     "Registered",
#     "Certified",
#     "Gold",
#     "Silver",
#     "Elite",
#     "Success",
#     "Participation",
#     "Toppers",
#     "Minimum Mark",
#     "Maximum Mark",
#     "Average Mark",
#     "Standard Deviation"
# ]                                    -> Column Headers
# data_string = "43871371949510736147630849179255.3312.93"       ->   Example Input

# Enrolled >= Registered >= Certified
# Certified = Gold + Silver + Elite + Success
# Maximum Mark <= 100

# '.' appeas for Average Mark and Standard Deviation in the form of 'dd.ff'

data_string = "43871371949510736147630849179255.3312.93"
data = data_string.split(".")
if len(data) != 3:
    raise ValueError("Unintended data format")

std_dev = float(data[1][-2:] + "." + data[2])
average = float(data[0][-2:] + "." + data[1][:-2])

data_part = data[0][:-2]

# 438713719495107361476308491792
# Maximum Mark = 92
# Minimum Mark = 17
# Max != Min => min < average < max

max_mark = int(data_part[-2:])
min_mark = int(data_part[-4:-2])
if max_mark == 0:
    max_mark = 100
    min_mark = int(data_part[-5:-3])
if min_mark == max_mark or not (min_mark < average < max_mark):
    if average != min_mark:
        min_mark = min_mark % 10
        if max_mark == 100:
            data_part = data_part[:-4]
        else:
            data_part = data_part[:-3]
else:
    if max_mark == 100:
        data_part = data_part[:-5]
    else:
        data_part = data_part[:-4]

# data_part = 43871371949510736147630849
# Enrolled Registered Certified Gold Silver Elite Success Participation Toppers
# Certified = Gold + Silver + Elite + Success
# Enrolled >= Registered >= Certified


def crack(dataString, cracked_code):
    if len(cracked_code) == 9:
        if not dataString:
            if cracked_code:
                if cracked_code[0] >= cracked_code[1] >= cracked_code[2]:
                    if (
                        cracked_code[3]
                        + cracked_code[4]
                        + cracked_code[5]
                        + cracked_code[6]
                        == cracked_code[2]
                    ):
                        return cracked_code
        return None

    for i in range(1, min(len(dataString) + 1, 6)):
        curr = int(dataString[:i])
        rem = dataString[i:]

        res = crack(rem, cracked_code + [curr])
        if res:
            return res


cracked = crack(data_part, [])

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

result = {}
for i in range(len(cracked)):
    result[header[i]] = cracked[i]

result["Maximum Mark"] = max_mark
result["Minimum Mark"] = min_mark
result["Average Mark"] = average
result["Standard Deviation"] = std_dev

print(result)
