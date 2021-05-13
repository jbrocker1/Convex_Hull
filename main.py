import math
import random

import pygame
import time
from random import randint
from sys import exit

pygame.init()
pygame.display.init()
pygame.mixer.quit()

win_width = 1000
win_height = 750

num_points = 500

background = (0, 0, 0)
point_color = (255, 255, 255)
curr_point_color = (255, 255, 255)
outer_most_color = (0, 255, 0)
hull_color = (0, 0, 255)

point_size = 1
line_size = 2

buffer = 40

fps = 60

class Point:
  def __init__(self, x_val: int, y_val: int):
    self.x = x_val
    self.y = y_val

  def point(self) -> tuple:
    return self.x, self.y

  def __str__(self):
    return "({}, {})".format(self.x, self.y)


def angle(base: Point, p1: Point, p2: Point) -> float:
  # sqrt((y2 - y1)**2 + (x2 - x1)**2)
  a = math.sqrt(math.pow((base.y - p1.y), 2) + math.pow((base.x - p1.x), 2))
  b = math.sqrt(math.pow((base.y - p2.y), 2) + math.pow((base.x - p2.x), 2))
  c = math.sqrt(math.pow((p1.y - p2.y), 2) + math.pow((p1.x - p2.x), 2))

  return math.degrees(math.acos((math.pow(a, 2) + math.pow(b, 2) - math.pow(c, 2)) / (2 * a * b)))

def draw_points(win: pygame.Surface, points: [Point]):
  for point in points:
    pygame.draw.circle(win, point_color, point.point(), point_size)

def draw_hull(win: pygame.Surface, hull:  [Point], points: [Point], draw_ps: bool = True) -> None:
  win.fill(background)
  if draw_ps:
    draw_points(win, points)
  else:
    draw_points(win, hull)
  for i in range(len(hull) - 1):
    pygame.draw.line(win, hull_color, hull[i].point(), hull[i + 1].point(), line_size)


def get_quit():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()


def main() -> None:
  # setup
  clock = pygame.time.Clock()
  win = pygame.display.set_mode((win_width, win_height))

  # gets random points
  points: [Point] = []
  for i in range(num_points):
    points.append(Point(randint(buffer, win_width - buffer), randint(buffer, win_height - buffer)))

  # gets left most point
  start_point = points[0]
  for point in points[1:]:
    if point.x < start_point.x:
      start_point = point

  # points of that makeup the convex hull
  hull: [Point] = [start_point]

  curr_point_index = 0
  outer_most = random.choice(points)

  # game loop
  while True:
    win.fill(background)

    # drawing every point
    draw_points(win, points)

    # get point of curr point and random outer most point
    curr_point = points[curr_point_index]
    if curr_point_index == 0:
      outer_most = random.choice(points)
      while outer_most == start_point:
        outer_most = random.choice(points)


    # if we are just starting we check against the center
    center = Point(win_width // 2, win_height // 2)
    # don't check against itself
    if curr_point != start_point:
      if len(hull) == 1:
        outer_most_gamma = angle(start_point, outer_most, center)
        gamma = angle(start_point, curr_point, center)
        if gamma > outer_most_gamma:
          outer_most = curr_point
      # check against the last point we added to the hull
      else:
        # cant check against the other part of our triangle
        if curr_point != hull[-2]:
          outer_most_gamma = angle(start_point, outer_most, hull[-2])
          gamma = angle(start_point, curr_point, hull[-2])
          if gamma > outer_most_gamma:
            outer_most = curr_point


    # check if we have checked all of the components and add left most to hull
    if curr_point_index == (len(points) - 1):
      hull.append(outer_most)
      start_point = outer_most
      curr_point_index = 0
      # check if we are done
      if outer_most == hull[0]:
        while pygame.display.get_active():
          get_quit()
          draw_hull(win, hull, points)
          pygame.display.flip()
          time.sleep(.5)
    else:
      curr_point_index += 1

    # draw hull
    if len(hull) > 1:
      draw_hull(win, hull, points)

    # draw left most point and checking point
    pygame.draw.line(win, curr_point_color, start_point.point(), curr_point.point(), line_size)
    pygame.draw.line(win, outer_most_color, start_point.point(), outer_most.point(), line_size)

    get_quit()

    pygame.display.flip()
    clock.tick(fps)

if __name__ == "__main__":
  main()