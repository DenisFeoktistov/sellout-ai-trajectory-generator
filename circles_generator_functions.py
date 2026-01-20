import random
import time


def generate_t(cnt):
    ts = [13, 14, 15, 16, 17, 18, 19, 20, 21]
    prob = [1, 2, 3, 4, 5, 4, 3, 2, 1]

    t = random.choices(ts, weights=prob, k=cnt)

    return t


def generate_sp(cnt):
    s = list()

    current_value = 0.11 + random.random() / 100

    for _ in range(cnt - 10):
        values = [0.11 + random.random() / 100 for __ in range(3)]
        abs1 = [abs(value - current_value) for value in values]
        ind = abs1.index(min(abs1))

        current_value = values[ind]
        s.append(current_value)

    for i in range(18):
        values = [0.11 - 0.005 * i + random.random() / 100 for __ in range(3)]
        abs1 = [abs(value - current_value) for value in values]
        ind = abs1.index(min(abs1))

        current_value = values[ind]
        s.append(current_value)

    return s


def generate_trajectory(goal_degrees):
    start_x = random.randint(54 + 20, 120 + 54 - 20)
    goal_x = start_x + goal_degrees * 852 // 360

    # print(start_x, goal_x)

    x_array, x_linear = generate_x(goal_x, start_x)
    cnt = len(x_array)
    y_array, y_linear = generate_y(cnt)
    t_array = generate_t(cnt)
    s_array = generate_sp(cnt)
    p_array = s_array[::]

    t_array[0] = time.time_ns() // 10 ** 6 + 500

    data = {
        "x": x_array,
        "x_linear": x_linear,
        "y": y_array,
        "y_linear": y_linear,
        "t": t_array,
        "s": s_array,
        "p": p_array
    }

    return data


def generate_x(goal_x, start_x):
    after_point = float(str(random.random())[:7])

    x_array = list()
    x_array.append(start_x + after_point)
    vx = 7
    deltas_vx = [-1, 0, 1]
    prob = [1, 2, 2]

    while x_array[-1] < start_x + (goal_x - start_x) * 0.25:
        delta_vx = random.choices(deltas_vx, weights=prob, k=1)[0]
        vx += delta_vx
        vx = max(vx, 5)
        vx = min(vx, 10)

        after_point = float(str(random.random())[:7])

        x_array.append(int(x_array[-1] + vx) + after_point)

    deltas_vx = [-1, 0, 1, 2]
    prob = [1, 2, 2, 1]

    while x_array[-1] < start_x + (goal_x - start_x) * 0.55:
        delta_vx = random.choices(deltas_vx, weights=prob, k=1)[0]
        vx += delta_vx
        vx = max(vx, 3)

        after_point = float(str(random.random())[:7])

        x_array.append(int(x_array[-1] + vx) + after_point)

    deltas_vx = [-2, -1, 0, 1, 2]
    prob = [2, 2, 1, 1, 1]

    while x_array[-1] < start_x + (goal_x - start_x) * 0.95:
        delta_vx = random.choices(deltas_vx, weights=prob, k=1)[0]
        vx += delta_vx
        vx = max(vx, 2)

        after_point = float(str(random.random())[:7])

        x_array.append(int(x_array[-1] + vx) + after_point)

    deltas_vx = [-2, -1, 0, 1]
    prob = [3, 4, 2, 1]

    while x_array[-1] < goal_x:
        delta_vx = random.choices(deltas_vx, weights=prob, k=1)[0]
        vx += delta_vx
        vx = max(vx, 1)

        after_point = float(str(random.random())[:7])

        x_array.append(int(x_array[-1] + vx) + after_point)

    x_linear = list()

    for x in x_array:
        x_linear.append((x - start_x) * 248 / (goal_x - start_x))

    return x_array, x_linear


def generate_y(steps, start_y=1475):
    y_array = list()
    y_array.append(start_y)
    vy = 0
    deltas_vy = [-1, 0, 1]
    prob = [3, 4, 4]

    cnt = 0

    while cnt < steps * 0.55:
        cnt += 1

        delta_vy = random.choices(deltas_vy, weights=prob, k=1)[0]
        vy += delta_vy
        vy = max(vy, -1)
        vy = min(vy, 1)

        after_point = float(str(random.random())[:7])

        y_array.append(int(y_array[-1] + vy) + after_point)

    deltas_vy = [-1, 0, 1]
    prob = [4, 4, 3]

    while cnt < steps - 1:
        cnt += 1

        delta_vy = random.choices(deltas_vy, weights=prob, k=1)[0]
        vy += delta_vy
        vy = max(vy, -1)
        vy = min(vy, 1)

        after_point = float(str(random.random())[:7])

        y_array.append(int(y_array[-1] + vy) + after_point)

    y_linear = list()
    y_min = min(y_array)
    y_max = max(y_array)

    for y in y_array:
        y_linear.append((y - y_min) / (y_max - y_min) * 2 - 1)

    return y_array, y_linear
