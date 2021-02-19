import matplotlib.pyplot as plt


def get_coordinate_max(buildings):
    x_max = max([item[2][0] for item in buildings.values()])
    y_max = max([item[1][1] for item in buildings.values()])
    return max(x_max, y_max)


def get_coordinate_min(buildings):
    x_min = min([item[0][0] for item in buildings.values()])
    y_min = min([item[0][1] for item in buildings.values()])
    return min(x_min, y_min)


def draw_buildings(axes1, buildings):
    # 绘制建筑物
    for item in buildings:
        building = buildings[item]
        temp_building = [building[1], building[0], building[2], building[3]]
        plt.text(building[0][0], building[0][1], item)
        square = plt.Polygon(xy=temp_building, color='blue', alpha=0.5)
        axes1.add_patch(square)


def draw_bounds(axes1, bounds):
    # 绘制边界点
    axes1.scatter(x=[item[0] for item in bounds], y=[item[1] for item in bounds], s=5)
    # 绘制边界线
    x_bounds = [item[0] for item in bounds]
    y_bounds = [item[1] for item in bounds]
    x_bounds.append(bounds[0][0])
    y_bounds.append(bounds[0][1])
    axes1.plot(x_bounds, y_bounds)