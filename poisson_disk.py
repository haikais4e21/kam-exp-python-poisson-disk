import random
import math
import svgwrite

def poisson_disk_sampling(width, height, radius, k=30):
    cell_size = radius / math.sqrt(2)
    grid_width = math.ceil(width / cell_size)
    grid_height = math.ceil(height / cell_size)
    grid = [[None for _ in range(grid_width)] for _ in range(grid_height)]
    points = []
    queue = []

    def get_neighbors(point):
        neighbors = []
        x, y = point
        for i in range(max(0, math.floor(x / cell_size) - 2), min(grid_width, math.ceil(x / cell_size) + 3)):
            for j in range(max(0, math.floor(y / cell_size) - 2), min(grid_height, math.ceil(y / cell_size) + 3)):
                if grid[j][i]:
                    neighbors.append(grid[j][i])
        return neighbors

    def is_valid(point):
        for neighbor in get_neighbors(point):
            if math.dist(point, neighbor) < radius:
                return False
        return True

    def random_point_around(point):
        for _ in range(k):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(radius, 2 * radius)
            candidate = (point[0] + distance * math.cos(angle), point[1] + distance * math.sin(angle))
            if 0 <= candidate[0] < width and 0 <= candidate[1] < height and is_valid(candidate):
                return candidate
        return None

    first_point = (random.uniform(0, width), random.uniform(0, height))
    grid[math.floor(first_point[1] / cell_size)][math.floor(first_point[0] / cell_size)] = first_point
    points.append(first_point)
    queue.append(first_point)

    while queue:
        current_point = queue.pop(0)
        for _ in range(k):
            new_point = random_point_around(current_point)
            if new_point:
                grid[math.floor(new_point[1] / cell_size)][math.floor(new_point[0] / cell_size)] = new_point
                points.append(new_point)
                queue.append(new_point)

    return points

def export_svg(points, width, height, filename):
    dwg = svgwrite.Drawing(filename, profile='tiny', size=(f'{width}px', f'{height}px'))
    for point in points:
        dwg.add(dwg.circle(center=point, r=1, fill='black'))
    dwg.save()

if __name__ == '__main__':
    points = poisson_disk_sampling(100, 100, 5)
    export_svg(points, 100, 100, 'poisson_disk.svg')