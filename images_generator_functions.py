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


def compress(arr, cnt):
    first_val = arr[0]
    last_val = arr[-1]

    coefficient = last_val / arr[cnt]

    new_arr = list()

    for i in range(cnt):
        after_point = float(str(random.random())[:7])

        value = arr[i] * (1 + (coefficient - 1) * i / cnt)
        new_arr.append(int(value) + after_point)

    return new_arr


def generate_trajectory(start_block, finish_block):
    start_x_indent = start_block % 3
    start_y_indent = start_block // 3

    finish_x_indent = finish_block % 3
    finish_y_indent = finish_block // 3

    x_point_into_block = random.randint(50, 298 - 50)
    y_point_into_block = random.randint(50, 298 - 50)

    start_x = 72 + start_x_indent * (298 + 18) + x_point_into_block
    start_y = 712 + start_y_indent * (298 + 20) + y_point_into_block

    finish_x = 72 + finish_x_indent * (298 + 18) + x_point_into_block + random.choice([-1, 1]) + random.randint(5, 10)
    finish_y = 712 + finish_y_indent * (298 + 20) + y_point_into_block + random.choice([-1, 1]) + random.randint(5, 10)

    # print("X:", start_x, finish_x)
    # print("Y:", start_y, finish_y)
    x_array = generate_x(start_x, finish_x)
    y_array = generate_y(start_y, finish_y)

    if abs(start_x - finish_x) <= 10:
        x_array = generate_line(start_x, finish_x, len(y_array))

    if abs(start_y - finish_y) <= 10:
        y_array = generate_line(start_y, finish_y, len(x_array))

    # print("len", len(x_array), len(y_array))
    cnt = min(len(x_array), len(y_array))

    if cnt < len(x_array):
        x_array = compress(x_array, cnt)
    if cnt < len(y_array):
        y_array = compress(y_array, cnt)

    print("X:", x_array[0], x_array[-1])
    print("Y:", y_array[0], y_array[-1])

    t_array = generate_t(cnt)
    s_array = generate_sp(cnt)
    p_array = s_array[::]

    t_array[0] = time.time_ns() // 10 ** 6 + 500

    data = {
        "x": x_array,
        "y": y_array,
        "t": t_array,
        "s": s_array,
        "p": p_array
    }

    return data


def sgn(value):
    return 1 if value > 0 else -1


def generate_line(start_value, finish_value, cnt):
    arr = [int(start_value + (finish_value - start_value) * i // cnt) for i in range(cnt)]

    for i in range(1, cnt - 1):
        deltas_vx = [-2, -1, 0, 1, 2]
        prob = [1, 3, 7, 3, 1]

        arr[i] += random.choices(deltas_vx, weights=prob, k=1)[0]

    for i in range(cnt):
        after_point = float(str(random.random())[:7])

        arr[i] += after_point

    return arr


def generate_x(start_x, finish_x):
    reverse = False

    if start_x > finish_x:
        reverse = True
        start_x *= -1
        finish_x *= -1

    after_point = float(str(random.random())[:7])

    x_array = list()
    x_array.append(start_x + after_point)
    vx = 7
    deltas_vx = [-1, 0, 1]
    prob = [1, 2, 2]

    while x_array[-1] < start_x + (finish_x - start_x) * 0.25:
        delta_vx = random.choices(deltas_vx, weights=prob, k=1)[0]
        vx += delta_vx
        vx = max(vx, 5)
        vx = min(vx, 10)

        after_point = float(str(random.random())[:7])

        x_array.append(int(x_array[-1] + vx) + after_point)

    deltas_vx = [-1, 0, 1, 2]
    prob = [1, 2, 2, 1]

    while x_array[-1] < start_x + (finish_x - start_x) * 0.55:
        delta_vx = random.choices(deltas_vx, weights=prob, k=1)[0]
        vx += delta_vx
        vx = max(vx, 3)

        after_point = float(str(random.random())[:7])

        x_array.append(int(x_array[-1] + vx) + after_point)

    deltas_vx = [-2, -1, 0, 1, 2]
    prob = [2, 2, 1, 1, 1]

    while x_array[-1] < start_x + (finish_x - start_x) * 0.95:
        delta_vx = random.choices(deltas_vx, weights=prob, k=1)[0]
        vx += delta_vx
        vx = max(vx, 2)

        after_point = float(str(random.random())[:7])

        x_array.append(int(x_array[-1] + vx) + after_point)

    deltas_vx = [-2, -1, 0, 1]
    prob = [3, 4, 2, 1]

    while x_array[-1] < finish_x:
        delta_vx = random.choices(deltas_vx, weights=prob, k=1)[0]
        vx += delta_vx
        vx = max(vx, 1)

        after_point = float(str(random.random())[:7])

        x_array.append(int(x_array[-1] + vx) + after_point)

    if reverse:
        x_array = [-x for x in x_array]

    # x_linear = list()
    #
    # for x in x_array:
    #     x_linear.append((x - start_x) * 248 / (finish_x - start_x))
    #
    # return x_array, x_linear

    return x_array


def generate_y(start_y, finish_y):
    reverse = False

    if start_y > finish_y:
        reverse = True
        start_y *= -1
        finish_y *= -1

    after_point = float(str(random.random())[:7])

    y_array = list()
    y_array.append(start_y + after_point)
    vy = 7
    deltas_vy = [-1, 0, 1]
    prob = [1, 2, 2]

    while y_array[-1] < start_y + (finish_y - start_y) * 0.25:
        delta_vy = random.choices(deltas_vy, weights=prob, k=1)[0]
        vy += delta_vy
        vy = max(vy, 5)
        vy = min(vy, 10)

        after_point = float(str(random.random())[:7])

        y_array.append(int(y_array[-1] + vy) + after_point)

    deltas_vy = [-1, 0, 1, 2]
    prob = [1, 2, 2, 1]

    while y_array[-1] < start_y + (finish_y - start_y) * 0.55:
        delta_vy = random.choices(deltas_vy, weights=prob, k=1)[0]
        vy += delta_vy
        vy = max(vy, 3)

        after_point = float(str(random.random())[:7])

        y_array.append(int(y_array[-1] + vy) + after_point)

    deltas_vy = [-2, -1, 0, 1, 2]
    prob = [2, 2, 1, 1, 1]

    while y_array[-1] < start_y + (finish_y - start_y) * 0.95:
        delta_vy = random.choices(deltas_vy, weights=prob, k=1)[0]
        vy += delta_vy
        vy = max(vy, 2)

        after_point = float(str(random.random())[:7])

        y_array.append(int(y_array[-1] + vy) + after_point)

    deltas_vy = [-2, -1, 0, 1]
    prob = [3, 4, 2, 1]

    while y_array[-1] < finish_y:
        delta_vy = random.choices(deltas_vy, weights=prob, k=1)[0]
        vy += delta_vy
        vy = max(vy, 1)

        after_point = float(str(random.random())[:7])

        y_array.append(int(y_array[-1] + vy) + after_point)

    if reverse:
        y_array = [-y for y in y_array]

    # y_linear = list()
    #
    # for y in y_array:
    #     y_linear.append((y - start_y) * 248 / (finish_y - start_y))

    # return y_array, y_linear

    return y_array