# MDP Project problem
# Kyrolos Melek
# Intended outcome = 0.8, 0.2 for other two options
# Collision with walls = no movement
# Terminal states = +1 and -1
# Other states reward = -0.04
# max iterations = 20, discount factor lambda = 0.95
import sys
import pandas as pd

# Given variables
reward = float(sys.argv[1])
policyFile = sys.argv[2]
#reward = -0.04
#policyFile = "case1.csv"
iterations = 19
discountFactor = 0.95
intendedDirection = 0.80
slip90 = 0.1
slipNeg90 = 0.1

# Read in Policy
df = pd.read_csv(policyFile, header=None)
policy = df.values.tolist()  # make it a list
numOfRows = len(policy)
numOfCol = len(policy[0])
stoneLocation = (1, 1)
terminalPos1 = (0, 3)
terminalneg1 = (1, 3)

# Current iteration (future)
V = [[0 for col in range(4)] for row in range(3)]
# Next iteration (past)
V_next = [[0 for col in range(4)] for row in range(3)]


# First check if wall is hit, if so return reward + V of current state
# Then check if we have landed in a special state (ie. stone location or terminal states)
def rewardCalcution(row, col, direction):
  # Bounds checking, if wall is hit, no movement occurs
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
      if (policy[row][col] == 1):
        V_next[row][col] = intendedDirection * (rewardCalcution(row - 1, col, 1)) + slip90 * (
          rewardCalcution(row, col + 1, 2)) + slipNeg90 * (rewardCalcution(row, col - 1, -2))
      # going down
      elif (policy[row][col] == -1):
        V_next[row][col] = intendedDirection * (rewardCalcution(row + 1, col, -1)) + slip90 * (
          rewardCalcution(row, col + 1, 2)) + slipNeg90 * (rewardCalcution(row, col - 1, -2))
      # going right
      elif (policy[row][col] == 2):
        V_next[row][col] = intendedDirection * (rewardCalcution(row, col + 1, 2)) + slip90 * (
          rewardCalcution(row - 1, col, 1)) + slipNeg90 * (rewardCalcution(row + 1, col, -1))
      # going left
      elif (policy[row][col] == -2):
        V_next[row][col] = intendedDirection * (rewardCalcution(row, col - 1, -2)) + slip90 * (
          rewardCalcution(row - 1, col, 1)) + slipNeg90 * (rewardCalcution(row + 1, col, -1))
  V = V_next
  for row in V:
    print(row)
  print('\n')


print(V[2][0])
