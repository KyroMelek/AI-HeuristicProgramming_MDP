# MDP Project Part 2
# Kyrolos Melek
import sys
import csv

# Given variables
intendedDirection = float(sys.argv[1])
reward = float(sys.argv[2])
iterations = 19
discountFactor = 0.95
slip90 = (1.0 - intendedDirection) / 2.0
slipNeg90 = slip90

# Working policy
policy = [[0 for col in range(4)] for row in range(3)]
# Current iteration (future)
V = [[0 for col in range(4)] for row in range(3)]
# Next iteration (past)
V_next = [[0 for col in range(4)] for row in range(3)]

numOfRows = len(policy)
numOfCol = len(policy[0])

stoneLocation = (1, 1)
terminalPos1 = (0, 3)
terminalneg1 = (1, 3)


# First check if wall is hit, if so return reward + V of current state
# Then check if we have landed in a special state (ie. stone location or terminal states)
def rewardCalcution(row, col, direction):
  # Bounds checking, if wall is hit, no movement occurs therefore
  # no reward is given for the current iteration(ex: -0.04), just the discounted future reward associated with that state
  if (row > numOfRows - 1):
    return reward + discountFactor * V[row - 1][col]
  elif (row < 0):
    return reward + discountFactor * V[row + 1][col]
  elif (col > numOfCol - 1):
    return reward + discountFactor * V[row][col - 1]
  elif (col < 0):
    return reward + discountFactor * V[row][col + 1]

  # If stone is hit, no movement occurs, return reward + discounted reward for current state
  elif (row == stoneLocation[0] and col == stoneLocation[1]):
    if (direction == 1):
      return reward + discountFactor * V[row + 1][col]
    if (direction == -1):
      return reward + discountFactor * V[row - 1][col]
    if (direction == 2):
      return reward + discountFactor * V[row][col - 1]
    if (direction == -2):
      return reward + discountFactor * V[row][col + 1]

  # If terminal state reached, reward associated with terminal state given, and no discounted future reward is given
  elif (row == terminalPos1[0] and col == terminalPos1[1]):
    return 1
  elif (row == terminalneg1[0] and col == terminalneg1[1]):
    return -1

  # This is the default case, going to a state that is valid (i.e. not a wall or stone) and not a terminal state
  else:
    return reward + discountFactor * V[row][col]


for i in range(iterations):
  for row in range(numOfRows):
    for col in range(numOfCol):
      if ((row, col) == stoneLocation or (row, col) == terminalPos1 or (row, col) == terminalneg1):
        continue
      # going up
      V_Up = intendedDirection * (rewardCalcution(row - 1, col, 1)) + slip90 * (
        rewardCalcution(row, col + 1, 2)) + slipNeg90 * (rewardCalcution(row, col - 1, -2))
      # going down
      V_Down = intendedDirection * (rewardCalcution(row + 1, col, -1)) + slip90 * (
        rewardCalcution(row, col + 1, 2)) + slipNeg90 * (rewardCalcution(row, col - 1, -2))
      # going right
      V_right = intendedDirection * (rewardCalcution(row, col + 1, 2)) + slip90 * (
        rewardCalcution(row - 1, col, 1)) + slipNeg90 * (rewardCalcution(row + 1, col, -1))
      # going left
      V_left = intendedDirection * (rewardCalcution(row, col - 1, -2)) + slip90 * (
        rewardCalcution(row - 1, col, 1)) + slipNeg90 * (rewardCalcution(row + 1, col, -1))
      V_next[row][col] = max(V_Up, V_right, V_Down, V_left)
      if (V_next[row][col] == V_Up):
        policy[row][col] = 1
      elif (V_next[row][col] == V_Down):
        policy[row][col] = -1
      elif (V_next[row][col] == V_right):
        policy[row][col] = 2
      elif (V_next[row][col] == V_left):
        policy[row][col] = -2
  V = V_next


for row in policy:
  print(row)

with open("expectimax.csv", "w", newline="") as f:
  writer = csv.writer(f)
  writer.writerows(policy)
