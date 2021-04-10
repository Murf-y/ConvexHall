import pygame
import random
from pygame_widgets import Button, Slider, TextBox

pygame.init()
pygame.font.init()

# COLORS
white = (230, 230, 230)
black = (0, 0, 0)
grey = (20, 20, 20)
red = (255, 0, 0)
green = (34, 204, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
purple = (166, 77, 255)
orange = (255, 162, 0)

# constants
WIDTH = 600
HEIGHT = 600
BUFFER = 50
LOWERGAP = 50

# variables

point_normal_raduis = 5


# arrays


class Point:
    def __init__(self, x, y, color, raduis):
        self.x = x
        self.y = y
        self.color = color
        self.raduis = raduis

    def get_raduis(self):
        return self.raduis

    def set_raduis(self, raduis):
        self.raduis = raduis

    def get_pos(self):
        return (self.x, self.y)

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color


def vector_from_points(a, b):
    return [b.x - a.x, b.y - a.y, 0]


def cross_product(a, b):
    return (a[0] * b[1]) - (a[1] * b[0])


def draw_point(display, point):
    pygame.draw.circle(display, point.get_color(), point.get_pos(), point.get_raduis())
    pygame.display.update()


def draw_points(display, number_of_points, points):
    for i in range(number_of_points + 1):
        x = random.randint(BUFFER, WIDTH - BUFFER)
        y = random.randint(BUFFER, HEIGHT - BUFFER - LOWERGAP)
        point = Point(x, y, white, point_normal_raduis)
        points.append(point)
        draw_point(display, point)


def update_diplay(display, points):
    for point in points:
        draw_point(display, point)


def sort_points(points):
    points.sort(key=lambda point: point.x)


def check_Zcrossproduct(a, b, c):
    ab = vector_from_points(a, b)
    ac = vector_from_points(a, c)
    return cross_product(ab, ac)


def draw_line(display, a, b, color, width=2):
    pygame.draw.line(display, color, a.get_pos(), b.get_pos(), width)
    pygame.display.update()


def algo(display, number_of_points):
    points = []
    hull = []
    draw_points(display, number_of_points, points)

    sort_points(points)

    leftmost_point = points[0]
    leftmost_point.set_color(green)
    leftmost_point.set_raduis(10)

    current_point = leftmost_point

    def get_random_point_except_current():
        point = points[random.randint(0, len(points) - 1)]
        if point != current_point:
            return point
        else:
            return get_random_point_except_current()

    while True:
        hull.append(current_point)
        next_point = get_random_point_except_current()
        for check_point in points:
            draw_line(display, current_point, check_point, grey, 1)
            if (check_Zcrossproduct(current_point, next_point, check_point) > 0):
                next_point = check_point
        draw_line(display, current_point, next_point, blue, 5)
        current_point = next_point
        current_point.set_color(green)
        current_point.set_raduis(10)
        update_diplay(display, points)
        if (current_point == hull[0]):
            break
    for index, point in enumerate(hull):
        curr = hull[index]
        if (index + 1 == len(hull)):
            next = hull[0]
        else:
            next = hull[index + 1]
        draw_line(display, curr, next, red, 5)
        point.set_color(green)
    update_diplay(display, points)


def main():
    font = pygame.font.SysFont("Arial", 32)
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ConvexHull")

    slider = Slider(display, 25, HEIGHT - 40, 300, 30, min=4, max=10000, step=1, handleColour=grey)

    def start():
        pygame.draw.rect(display, black, (0, 0, WIDTH, HEIGHT - BUFFER - LOWERGAP + 20))
        number_of_points = slider.getValue()
        algo(display, number_of_points)

    button = Button(
        display, WIDTH - 150, HEIGHT - 50, 125, 50, text='Start',
        fontSize=50, margin=20,
        inactiveColour=grey,
        pressedColour=green, radius=20,
        onClick=lambda: start()
    )
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        if (running):
            button.listen(events)
            button.draw()
            slider.listen(events)
            slider.draw()

            textsurface = font.render(f"{slider.getValue()}", False, blue)
            pygame.draw.circle(display, black, (WIDTH - 200, HEIGHT - 25), 45)
            display.blit(textsurface, (WIDTH - 230, HEIGHT - 40))
            pygame.display.update()


if __name__ == '__main__':
    main()
