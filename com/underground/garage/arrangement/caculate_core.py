import matplotlib.pyplot as plt
from com.underground.garage.arrangement.parse_data \
    import ParseData, calculate_buildings_x_gap, draw, handle_x_bounds


def calculate_available_areas(axes1, bounds, buildings):
    # 绘制建筑物相交部分
    build_gaps = ParseData.calculate_build_gap(buildings)
    for item in build_gaps:
        building_gap = build_gaps[item]
        building = building_gap['upper']
        draw(building, axes1, 'red')
    # 绘制建筑物相交部分的眼延伸
    buildings_x_gap = calculate_buildings_x_gap(build_gaps, buildings)
    bounds_size = len(bounds)
    bound_lines = []
    for i, bound in enumerate(bounds):
        line = (bound, bounds[bounds_size - 1]) if 0 == i else (bound, bounds[i - 1])
        bound_lines.append(line)
    for bound_line in bound_lines:
        if bound_line[0][0] == bound_line[1][0]:
            handle_x_bounds(bound_line, buildings_x_gap)
    for item in buildings_x_gap:
        building = buildings_x_gap[item]['upper']
        draw(building, axes1, 'green')
