import numpy as np
import matplotlib.pyplot as plt

housing_estate = np.array([[-100, 200], [-100, 0], [100, 0], [100, 200]])
available_housing_estate = np.array([[-98, 198], [-98, 2], [98, 2], [98, 198]])
floors = np.array([
    [[60, 50], [60, 100], [80, 100], [80, 50]],
    [[-80, 29], [-80, 64], [-60, 64], [-60, 29]],
])


x_floors = np.array([[floor[0][0], floor[2][0]] for floor in floors])
y_floors = np.array([[floor[0][1], floor[1][1]] for floor in floors])

x_min = available_housing_estate[0][0]
x_max = available_housing_estate[2][0]

y_min = available_housing_estate[1][1]
y_max = available_housing_estate[0][1]

x_availables = []
y_availables = []
floors_size = floors.shape[0]


def get_y_floors(x1, x2):
    x_interval_floors = np.array([floor for floor in floors if floor[0][0] >= x1 and floor[2][0] <= x2])
    print(x_interval_floors)
    for y_floor in y_floors:
        for i, floor in enumerate(x_interval_floors):
            print(floor[0][0])
            if floor[0][0] >= y_floor[0] and floor[2][0] <= y_floor[1]:
                y_available = [x1, x2, x_floor[1], x_max]
                y_availables.append(y_available)
                if y_max > y_floor[0]:
                    y_max = y_floor[0]
                if i + 1 == floors_size:
                    y_availables.append([x1, x2, x_min, floor[0][0]])
    print('y_availables', y_availables)
    return y_availables


for x_floor in x_floors:
    for i, floor in enumerate(floors):
        if floor[0][0] >= x_floor[0] and floor[2][0] <= x_floor[1]:
            x_available = [x_floor[1], x_max]
            # get_y_floors(x_floor[0], x_max)
            x_availables.append(x_available)
            if x_max > x_floor[0]:
                x_max = x_floor[0]
            if i + 1 == floors_size:
                x_availables.append([x_min, floor[0][0]])

print(x_availables)
print(y_availables)


def main():
    fig1 = plt.figure(figsize=(14, 7))
    plt.xlim(housing_estate[0][0], housing_estate[2][0])
    plt.ylim(housing_estate[1][1], housing_estate[0][1])
    x_ticks = np.linspace(-100, 100, 1)
    y_ticks = np.linspace(0, 100, 1)
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)
    axes1 = fig1.add_subplot()
    available_housing = plt.Polygon(xy=available_housing_estate, alpha=0.0)
    axes1.add_patch(available_housing)
    for floor in floors:
        square = plt.Polygon(xy=floor, color='blue', alpha=1)
        axes1.add_patch(square)
    for x_floor in x_availables:
        floor = [[x_floor[0], 198], [x_floor[0], 2], [x_floor[1], 0], [x_floor[1], 198]]
        square = plt.Polygon(xy=floor, color='red', alpha=0.5)
        axes1.add_patch(square)
    plt.show()
