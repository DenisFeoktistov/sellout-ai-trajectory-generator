from matplotlib import pyplot as plt

from images_generator_functions import generate_trajectory

input_data = open("pictures.txt").read().split("|")

data = dict()

for line in input_data:
    for key, value in [pair.split("=") for pair in line.split(",")]:
        if key in data:
            data[key].append(value)
        else:
            data[key] = [value]


data = generate_trajectory(2, 4)

data["x"] = list(map(float, data["x"]))[1:]
data["y"] = list(map(float, data["y"]))[1:]
data["t"] = list(map(int, data["t"]))[1:]
# print(data["t"][:40])
# print(generate_t(40))

data["t_accumulate"] = [0]
for t in data["t"]:
    data["t_accumulate"].append(data["t_accumulate"][-1] + t)

data["t_accumulate"] = data["t_accumulate"][1:]
# data["t"] = list(filter(lambda x: x < 30, data["t"]))

data["s"] = list(map(float, data["s"]))[1:]
data["p"] = list(map(float, data["p"]))[1:]

data["x_deltas"] = [0]
for i in range(1, len(data["x"])):
    data["x_deltas"].append(abs(data["x"][i] - data["x"][i - 1]))

data["y_deltas"] = [0]
for i in range(1, len(data["y"])):
    data["y_deltas"].append(abs(data["y"][i] - data["y"][i - 1]))

data["v_x"] = [x / t for x, t in zip(data["x_deltas"], data["t"])]
data["v_y"] = [y / t for y, t in zip(data["y_deltas"], data["t"])]

dt = list(filter(lambda t: t < 50, data["t"]))

fig, ax = plt.subplots()

# ax.plot(data["x"], "r-")
# ax.plot(data["y"], "b-")

ax.plot(data["x"], data["y"], "b-")
# ax.plot(data["t"][1:], "b-")
# ax.plot(data["s"], "b-")
# print(data["t"][0])
# # 1714258370591
# # 1714496205185
#
# plt.show()
#
# exit(0)
# x_list = generate_x(goal_x=1000, start_x=200)
# y_list = generate_y(len(x_list))
# s_list = generate_sp(len(x_list))

# sample_x = list()
# for x in data["x"]:
#     if x > 1000:
#         break
#
#     sample_x.append(x)
#
# print(x_list)
# ax.plot(x_list, "b-")
# ax.plot(sample_x, "r-")
# ax.plot(data["t_accumulate"], data["x"], "b-")
# ax.plot(data["t_accumulate"], data["y"], "r--")
# ax.plot(data["t_accumulate"], data["s"], "r-")
# ax.plot(data["t_accumulate"], data["p"], "g-")

# s_test = list(filter(lambda s: s > 0.10, data["s"]))
# print(sum(s_test) / len(s_test))
# ax.plot(s_test[:len(x_list)], "g--")
# ax.plot(s_list[:len(x_list)], "r--")

# ax.plot(data["y"][:len(x_list)], "r-")
# ax.plot(x_list, y_list, "b-")

# ax.plot(data["t_accumulate"], data["x_deltas"], "b-")
# ax.plot(data["t_accumulate"], data["y_deltas"], "r-")
# ax.plot(data["t_accumulate"], data["t"], "r-")

# ax.plot(data["t_accumulate"], data["v_x"], "r-")
# ax.plot(data["t_accumulate"], data["v_y"], "b-")
plt.show()

# print(*enumerate(data["x"]))
#
# data["x_deltas"] = list()
# for i in range(1, len(data["x"])):
#     data["x_deltas"].append(abs(data["x"][i] - data["x"][i - 1]))
#
# print(data["x_deltas"])
# print(sum(data["x_deltas"]) / len(data["x_deltas"]))
