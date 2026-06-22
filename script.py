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

max = int(data_part[-2:])
min = int(data_part[-4:-2])
if max == 0:
    max = 100
    min = int(data_part[-5:-3])
if min == max or not (min < average < max):
    if average != min:
        min = min % 10
        if max == 100:
            data_part = data_part[:-4]
        else:
            data_part = data_part[:-3]
else:
    if max == 100:
        data_part = data_part[:-5]
    else:
        data_part = data_part[:-4]

# data_part = 43871371949510736147630849
# Enrolled Registered Certified Gold Silver Elite Success Participation Toppers
# Certified = Gold + Silver + Elite + Success
# Enrolled >= Registered >= Certified


def crack(dataString, cracked_code):
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


cracked = crack(data_string, [])

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

res = {}
for i in range(len(cracked)):
    res[header[i]] = cracked[i]

res["Maximum Mark"] = max
res["Minimum Mark"] = min
res["Average Mark"] = average
res["Standard Deviation"] = std_dev

print(res)
