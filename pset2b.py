###########################
# 6.0002 Problem Set 1b: Space Change
# Name: Awoninyam Kojo Stephen
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    # TODO: Your code here
    # initialization of n
    n = 0
    # sort the elements in the tuple in descending order
    egg_weights = sorted(egg_weights,reverse=True)
    # loop through the element in the tuple
    for weight in egg_weights:
        # take the nearest division to the mod variable
        mod = int(target_weight/weight)
        # if the mod is equal to zero continue the process
        if mod == 0:
            continue
        # multiply the mod to the element from the tuple and subtract it from weight and assign it to the weight variable
        target_weight = target_weight-mod*weight
        # add up the mod
        n += mod
        # return the add up modes
    return n    
    pass

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()