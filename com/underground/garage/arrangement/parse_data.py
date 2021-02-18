import numpy as np
import re
import matplotlib.pyplot as plt


def read_file_data(file_name):
    with open(file_name, "r") as f:  # 打开文件
        return f.read()
    return None


class ParseData:

    def __init__(self, file_name):
        self.file_data = read_file_data(file_name)

    def print_file_data(self):
        print(self.file_data)

    def parse_building(self):
        file_data = self.file_data.split('\n')
        file_data = [item for item in file_data if len(item) > 0]

        buildings = {}

        temp_item = file_data[0]
        for item in file_data:
            if item[0].isdigit():
                sub_items = re.split('{|,|}', item)
                buildings[temp_item].append((float(sub_items[1].strip()), float(sub_items[2].strip())))
            else:
                temp_item = item.strip()
                buildings[temp_item] = []

        for item in buildings:
            building = buildings[item]
            building.sort()

        return buildings

    def parse_bound(self):
        file_data = self.file_data.split('\n')
        file_data = [item for item in file_data if len(item) > 0]

        bound = []

        for item in file_data:
            if item[0].isdigit():
                sub_items = re.split('{|,|}', item)
                bound.append([float(sub_items[1].strip()), float(sub_items[2].strip())])
        return bound

    def calculate_build_gap(self):
        buildings = self.parse_building()
        build_gaps = {}
        for item in buildings:
            build_gap = calculate_build_y_gap(buildings[item], buildings.values())
            build_gaps[item] = build_gap

        return build_gaps


def calculate_buildings_x_gap(build_gaps, buildings):
    buildings_x_gap = {}
    for item in build_gaps:
        building_gap = build_gaps[item]['upper']
        if building_gap is None:
            continue

        build_gap = calculate_build_x_gap(building_gap, buildings.values())
        buildings_x_gap[item] = build_gap
    return buildings_x_gap


def calculate_build_x_gap(building_gap, buildings):
    y_min_building = building_gap[0][1]
    y_max_building = building_gap[1][1]

    x_min_building = building_gap[0][0]
    x_max_building = building_gap[2][0]

    x_upper_gap = 100000000
    x_lower_gap = 100000000

    upper_building = {'lower': None, 'upper': None}

    for item in buildings:
        if (y_min_building <= item[0][1] <= y_max_building) or (y_min_building <= item[1][1] <= y_max_building):
            if item[0][0] >= x_max_building:
                temp_x_upper_gap = item[2][0] - x_max_building
                if x_upper_gap > temp_x_upper_gap:
                    x_upper_gap = temp_x_upper_gap

                    temp_x_min = building_gap[0][0]
                    temp_x_max = item[0][0]

                    upper_building['upper'] = [(temp_x_min, y_max_building),
                                               (temp_x_min, y_min_building),
                                               (temp_x_max, y_min_building),
                                               (temp_x_max, y_max_building)]

            if item[2][0] <= x_min_building:
                temp_x_upper_gap = x_min_building - item[2][0]
                if x_lower_gap > temp_x_upper_gap:
                    x_lower_gap = temp_x_upper_gap

                    temp_x_min = item[2][0]
                    temp_x_max = building_gap[2][0]

                    upper_building['lower'] = [(temp_x_min, y_max_building),
                                               (temp_x_min, y_min_building),
                                               (temp_x_max, y_min_building),
                                               (temp_x_max, y_max_building)]

    if upper_building['lower'] is not None and upper_building['upper'] is not None:
        min_x = upper_building['lower'][0][0] if upper_building['lower'][0][0] < upper_building['upper'][0][0] else upper_building['upper'][0][0]
        max_x = upper_building['lower'][2][0] if upper_building['lower'][2][0] > upper_building['upper'][2][0] else upper_building['upper'][2][0]
        return {'upper': [(min_x, y_max_building),
                          (min_x, y_min_building),
                          (max_x, y_min_building),
                          (max_x, y_max_building)]}
    elif upper_building['lower'] is not None and upper_building['upper'] is None:
        return {'upper': upper_building['lower']}
    elif upper_building['upper'] is not None and upper_building['lower'] is None:
        return upper_building
    else:
        return {'upper': None}


def calculate_build_y_gap(building, buildings):
    x_min_building = building[0][0]
    x_max_building = building[2][0]

    y_min_building = building[0][1] if building[0][1] < building[1][1] else building[1][1]
    y_max_building = building[0][1] if building[0][1] > building[1][1] else building[1][1]

    y_lower_gap = 100000000
    y_upper_gap = 100000000

    lower_building = None
    upper_building = None

    for item in buildings:
        temp_y_min = item[0][1] if item[0][1] < item[1][1] else item[1][1]
        temp_y_max = item[0][1] if item[0][1] > item[1][1] else item[1][1]

        if (x_min_building < item[0][0] < x_max_building) or (x_min_building < item[2][0] < x_max_building):
            if temp_y_min < y_min_building:
                temp_y_lower_gap = y_min_building - temp_y_min
                if y_lower_gap > temp_y_lower_gap:
                    y_lower_gap = temp_y_lower_gap

                    temp_x_min = building[0][0] if building[0][0] > item[0][0] else item[0][0]
                    temp_x_max = building[2][0] if building[2][0] < item[2][0] else item[2][0]

                    lower_building = [(temp_x_min, y_min_building),
                                      (temp_x_min, temp_y_max),
                                      (temp_x_max, temp_y_max),
                                      (temp_x_max, y_min_building)]

            if temp_y_max > y_max_building:
                temp_y_upper_gap = temp_y_max - y_max_building
                if y_upper_gap > temp_y_upper_gap:
                    y_upper_gap = temp_y_upper_gap

                    temp_x_min = building[0][0] if building[0][0] > item[0][0] else item[0][0]
                    temp_x_max = building[2][0] if building[2][0] < item[2][0] else item[2][0]

                    upper_building = [(temp_x_min, y_max_building),
                                      (temp_x_min, temp_y_min),
                                      (temp_x_max, temp_y_min),
                                      (temp_x_max, y_max_building)]

    return {'lower': lower_building, 'upper': upper_building}


def draw_spesial(building, axes1, color='red'):
    if building is None:
        return

    temp_building = [building[1], building[0], building[2], building[3]]
    square = plt.Polygon(xy=temp_building, color=color, alpha=0.3)
    axes1.add_patch(square)


def draw(building, axes1, color='red'):
    if building is None:
        return

    square = plt.Polygon(xy=building, color=color, alpha=0.3)
    axes1.add_patch(square)


parseBuildingData = ParseData('./test-project-1-building.txt')
buildings = parseBuildingData.parse_building()
build_gaps = parseBuildingData.calculate_build_gap()
buildings_x_gap = calculate_buildings_x_gap(build_gaps, buildings)
parseBoundData = ParseData('./test-project-1-bound.txt')
bounds = parseBoundData.parse_bound()

fig1 = plt.figure(figsize=(16, 8))

plt.xlim(-480, -220)
plt.ylim(-260, 150)

axes1 = fig1.add_subplot()
for item in build_gaps:
    building_gap = build_gaps[item]
    # building = building_gap['lower']
    # draw(building, axes1, 'red')

    building = building_gap['upper']
    draw(building, axes1, 'red')

for item in buildings_x_gap:
    building = buildings_x_gap[item]['upper']
    draw(building, axes1, 'green')

for item in buildings:
    building = buildings[item]
    temp_building = [building[1], building[0], building[2], building[3]]
    square = plt.Polygon(xy=temp_building, color='blue', alpha=0.5)
    axes1.add_patch(square)

axes1.scatter(x=[item[0] for item in bounds], y=[item[1] for item in bounds], s=1)

x_bounds = [item[0] for item in bounds]
y_bounds = [item[1] for item in bounds]
x_bounds.append(bounds[0][0])
y_bounds.append(bounds[0][1])
axes1.plot(x_bounds, y_bounds)
plt.show()
