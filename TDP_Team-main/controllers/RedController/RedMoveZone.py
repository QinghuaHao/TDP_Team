""" Red Team Strategies consts and common functions. """

""" The pitch of play divided into 18 zones. NAME: [[x1, y1], [x2, y2]] (left up, right down)"""
""" x = 9m, y = 6m """
ZONE = {
    1: [[-4.5, 3.0], [-3.0, 1.5]],
    2: [[-3.0, 3.0], [-1.5, 1.5]],
    3: [[-1.5, 3.0], [0.0, 1.5]],
    4: [[0.0, 3.0], [1.5, 1.5]],
    5: [[1.5, 3.0], [3.0, 1.5]],
    6: [[3.0, 3.0], [4.5, 1.5]],
    7: [[-4.5, 1.5], [-3.0, 0.0]],
    8: [[-3.0, 1.5], [-1.5, 0.0]],
    9: [[-1.5, 1.5], [0.0, 0.0]],
    10: [[0.0, 1.5], [1.5, 0.0]],
    11: [[1.5, 1.5], [3.0, 0.0]],
    12: [[3.0, 1.5], [4.5, 0.0]],
    13: [[-4.5, 0.0], [-3.0, -1.5]],
    14: [[-3.0, 0.0], [-1.5, -1.5]],
    15: [[-1.5, 0.0], [0.0, -1.5]],
    16: [[0.0, 0.0], [1.5, -1.5]],
    17: [[1.5, 0.0], [3.0, -1.5]],
    18: [[3.0, 0.0], [4.5, -1.5]],
    19: [[-4.5, -1.5], [-3.0, -3.0]],
    20: [[-3.0, -1.5], [-1.5, -3.0]],
    21: [[-1.5, -1.5], [0.0, -3.0]],
    22: [[0.0, -1.5], [1.5, -3.0]],
    23: [[1.5, -1.5], [3.0, -3.0]],
    24: [[3.0, -1.5], [4.5, -3.0]]
}


BLUE_GOAL = {
  "Left":   [-4.5, -1.50],
  "Middle": [-4.5,  0.00],
  "Right":  [-4.5,  1.50]
}

RED_GOAL = {
  "Left":   [4.5, -1.50],
  "Middle": [4.5,  0.00],
  "Right":  [4.5,  1.50]
}


def determine_ball_zone(coordinates):

  x, y = coordinates

  for key, coords in ZONE.items():
    # Extract the left-top and right-bottom coordinates
    lt = coords[0]
    rb = coords[1]

    # Check if the ball's coordinates are within the zone's coordinates
    if lt[0] <= x <= rb[0] and rb[1] <= y <= lt[1]:
        return key

  return None
