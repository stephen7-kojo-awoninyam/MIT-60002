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
    # sort and list the egg weight in descending order and assign it to variable weights
    weights = sorted(list(egg_weights),reverse=True)
    # initialize the results variable
    results = 0
    # initialize the n variable
    n = 0
    # loop through the listed egg weight
    for weight in weights:
        # take the exact division of each egg weight with respect to the target weight
        mod = int(target_weight/weight)
        # if the product and the weight yields zero continue looping 
        if mod*weight == 0:
            continue
        # else check inside the memo dict to return our results
        try:
            return memo[target_weight]
        # if our results is not found
        except KeyError:
            # take the resulting weight after taking the number of the heaviest egg
            target_weight = target_weight-mod*weight
            # remove the heaviest egg
            del(weights[n])
            # increase the n variable
            n+=1
            # continue adding up the exact division and assign it to the initialized results variable
            results = mod + dp_make_weight(tuple(weights),target_weight,memo)
            # add the value of results to memo dict with a key of target_weight 
            memo[target_weight] = results
    # return results        
    return results        
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