import numpy as np

import quaternion
from scipy import optimize


def packStateVector(pos, quat):
    """
    Packs the position and orientation data into a single array so that
    scipy.optimize can use it properly.
    Inverse to unpackStateVector()

    Args:
        pos (np.array)
        quat (np.quaternion)

    Returns:
        state (np.array): a length-7 state for the optimizer
    """
    return np.array(tuple(pos) + tuple(quaternion.as_float_array(quat).ravel()))


def unpackStateVector(state):
    """
    Unpacks the length-7 array into its position and orientation components
    Inverse of packStateVector()

    Args:
        state (np.array): a length-7 state for the optimizer

    Returns:
        pos (np.array)
        quat (np.quaternion)

    """
    position = np.array(state[:3])
    quat = np.quaternion(*state[3:])
    return position, quat


def getDistFunc(spheres, foundCircles):
    """
    Returns a function for use with scipy.optimize. The two arguments must be
    equal-length lists of paired 3D and 2D features
    """

    assert len(spheres) == len(foundCircles)

    def distFunc(state):
        position, quat = unpackStateVector(state)
        """
        Takes a list of 7 numbers. The first three represent translational
        position, and the last four form a rotation quaternion.
        Returns a list of error values.
        """
        matrix = quaternion.as_rotation_matrix(quat)

        errors = [c.distance(s.project(position, matrix).center)
                  for s, c in zip(spheres, foundCircles)
                  if c.confidence == True]

        # Flatten the resulting 2-deep list
        errors = [e for l in errors for e in l]

        # Even if we have insufficient data, we want the optimizer
        # to find a reasonably close solution to our initial guess.
        # Adding extra "0"'s suppresses the error, and allows that to happen.
        return errors + [quat.norm() - 1] + [0] * 6

    return distFunc


# TODO: massive speed boosts should come from computing the Jacobian more sensibly
def findPose(spheres, circles, pos, quat, verbose=False):
    """
    Finds a possible pose of the camera near (pos, quat) that
    projects as closely as possible the spheres onto their corresponding circles

    Args:
        spheres (list of Sphere3D):
        circles (list of Circle2D):
        pos (np.array):
        quat (np.quaternion):
        verbose (bool):

    Returns:
        pos
        quat

    """
    p, cov, infodict, mesg, ier = optimize.leastsq(
        getDistFunc(spheres, circles),
        packStateVector(pos, quat),
        xtol=5e-3,
        full_output=True)
    if verbose:
        print '{} evaluations needed, final error {}'.format(infodict['nfev'], infodict['fvec'])
    return unpackStateVector(p)
