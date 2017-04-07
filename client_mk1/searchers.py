import numpy as np


def do_linear_search(image, color, start, end,
                     num_steps=None, tol=0, verbose=False):
    """
    Runs a linear search between start and end,
    both specified as iterables of length 2
    (x, y) where start must match color and end must not.
    Tolerates stretches of incorrect pixel color up to tol long without
    returning wildly incorrect results.

    Returns a np array of the coordinates of the transition found
    """
    end = np.array(end)

    start = np.array(start)
    if num_steps is None:
        num_steps = max(np.abs(end - start))

    step_size = (end - start) / float(num_steps)
    if verbose:
        print "stepsize={}".format(step_size)

    miss_count = 0
    for i in range(num_steps):
        point = np.array(start + i * step_size, dtype=np.int32)
        if not color.matches(image.getHSV(*point)):
            miss_count += 1
        else:
            miss_count = 0

        if miss_count > tol:
            result = np.array(start + (i - tol) * step_size, dtype=np.int32)
            if verbose:
                print "Search end found after {} steps at {}".format(i, result)
            break

    return result


def do_binary_search(image, color, start, end,
                     numSteps=float('inf'), verbose=False):
    """
    Runs a binary search between start and end,
    both specified as iterables of length 2
    (x, y) where start must match color and end must not.

    Returns a np array of the coordinates of the transition found
    """
    lower = np.array(start, dtype=np.float64)
    upper = np.array(end, dtype=np.float64)

    i = 0
    while i < numSteps and max(np.abs(upper - lower)) > 1:
        point = (upper + lower) / 2

        if color.matches(image.getHSV(*point)):
            lower = point
        else:
            upper = point

    return np.array((upper + lower) / 2, dtype=np.int32)
