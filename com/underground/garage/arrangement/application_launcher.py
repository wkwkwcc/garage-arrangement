import matplotlib.pyplot as plt
from com.underground.garage.arrangement.parse_data import ParseData
from com.underground.garage.arrangement.draw_utils \
    import draw_bounds, draw_buildings, get_coordinate_max, get_coordinate_min
from com.underground.garage.arrangement.caculate_core import calculate_available_areas


def calculate_main():
    parseBuildingData = ParseData('./resources/test-project-1-building.txt')
    buildings = parseBuildingData.parse_building()

    parseBoundData = ParseData('./resources/test-project-1-bound.txt')
    bounds = parseBoundData.parse_bound

    fig1 = plt.figure(figsize=(16, 8))

    coordinate_max = get_coordinate_max(buildings)
    coordinate_min = get_coordinate_min(buildings)
    plt.xlim(coordinate_min - 10, coordinate_max + 10)
    plt.ylim(coordinate_min - 10, coordinate_max + 10)

    axes1 = fig1.add_subplot()
    draw_buildings(axes1, buildings)
    draw_bounds(axes1, bounds)

    calculate_available_areas(axes1, bounds, buildings)
    plt.show()


if __name__ == '__main__':
    calculate_main()
