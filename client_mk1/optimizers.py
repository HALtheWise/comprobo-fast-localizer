import numpy as np

import quaternion
from scipy import optimize


def packStateVector(pos, quat):
    return np.array(tuple(pos) + tuple(quaternion.as_float_array(quat).ravel()))


def unpackStateVector(state):
    position = np.array(state[:3])
    quat = np.quaternion(*state[3:])
    return position, quat


def getDistFunc(spheres, foundCircles):
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

        # Note that scipy leastsq requires sufficient number of outputs,
        # hacked here by feeding extra '0's
        return errors + [quat.norm() - 1] + [0] * 6

    return distFunc


# TODO: massive speed boosts should come from computing the Jacobian more sensibly
def findPose(spheres, circles, pos, quat, verbose=False):
    p, cov, infodict, mesg, ier = optimize.leastsq(
        getDistFunc(spheres, circles),
        packStateVector(pos, quat),
        xtol=5e-3,
        full_output=True)
    if verbose:
        print '{} evaluations needed, final error {}'.format(infodict['nfev'], infodict['fvec'])
    return unpackStateVector(p)
