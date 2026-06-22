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
