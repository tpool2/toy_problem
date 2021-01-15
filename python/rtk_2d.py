import unittest
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Circle

def get_unit_vectors(receiver_from_satellite):
    """Returns i along the path of the receiver from satellite,
    j rotated 90 degrees clockwise from it
    Ex: get_unit_vectors(np.array([1,0])) returns
    i: np.array([1,0])
    j: np.array([0,1])
    """
    R = np.array([ [np.cos(np.pi/2.0), -np.sin(np.pi/2.0)], [np.sin(np.pi/2.0), np.cos(np.pi/2.0)] ])
    normalized_i = receiver_from_satellite/np.linalg.norm(receiver_from_satellite)
    return normalized_i, R@normalized_i

def get_angle_between(vector1, vector2):
    """Returns the angle between two vectors"""
    return np.arccos(np.dot(vector1/np.linalg.norm(vector1), vector2/np.linalg.norm(vector2)))

class GetAngleBetweenTest(unittest.TestCase):
    def test_north_east(self):
        theta = get_angle_between(np.array([1,0]), np.array([0,1]))
        self.assertAlmostEqual(theta, np.pi/2.0, 5)

    def test_east_north(self):
        theta = get_angle_between(np.array([0,1]), np.array([1,0]))
        self.assertAlmostEqual(theta, np.pi/2.0, 10)

class UnitVectorsTest(unittest.TestCase):

    def test_north_of_satellite(self):
        satellite_location = np.array([-1,0])
        receiver_location = np.array([1,0])
        i, j = get_unit_vectors(receiver_location-satellite_location)
        self.assertAlmostEqual(i[0], 1, 10)
        self.assertEqual(i[1], 0)
        self.assertAlmostEqual(j[0], 0, 10)
        self.assertAlmostEqual(j[1], 1, 10)

    def test_east_of_satellite(self):
        i, j = get_unit_vectors(np.array([0, 10]))
        self.assertAlmostEqual(i[0], 0, 10)
        self.assertEqual(i[1], 1)
        self.assertEqual(j[0], -1)
        self.assertAlmostEqual(j[1], 0, 10)

    def test_south_of_satellite(self):
        i, j = get_unit_vectors(np.array([-5,0]))
        self.assertAlmostEqual(i[0], -1, 10)
        self.assertAlmostEqual(i[1], 0, 10)
        self.assertAlmostEqual(j[0], 0, 10)
        self.assertAlmostEqual(j[1], -1, 10)

    def test_west_of_satellite(self):
        i, j = get_unit_vectors(np.array([0,-2]))
        self.assertAlmostEqual(i[0], 0, 10)
        self.assertEqual(i[1], -1)
        self.assertEqual(j[0], 1)
        self.assertAlmostEqual(j[1], 0, 10)

if __name__ == '__main__':
    fig, ax = plt.subplots()
    origin = np.array([0,0])
    ax.plot([0,0], [0,1], c='k')
    h1 = np.sqrt(2)
    h2 = np.sqrt(2)
    satellite_1 = np.array([0,1])
    satellite_2 = np.array([2,-1])
    # satellite_3 = np.array([1,1])
    circle_1 = Circle((satellite_1[1],satellite_1[0]), radius=np.linalg.norm(satellite_1), color='b', fill=False, visible=True)
    ax.add_patch(circle_1)
    circle_2 = Circle((satellite_2[1],satellite_2[0]), radius=np.linalg.norm(satellite_2), color='g', fill=False, visible=True)
    ax.add_patch(circle_2)
    circle_1_prime = Circle((satellite_1[1],satellite_1[0]), radius=np.sqrt(2), color='b', fill=False, visible=True)
    ax.add_patch(circle_1_prime)
    circle_2_prime = Circle((satellite_2[1],satellite_2[0]), radius=np.sqrt(2), color='g', fill=False, visible=True)
    ax.add_patch(circle_2_prime)
    # circle_3 = Circle((satellite_3[1],satellite_3[0]), radius=np.linalg.norm(satellite_3), color='r', fill=False, visible=True)
    # ax.add_patch(circle_3)
    # circle_3_prime = Circle((satellite_3[1],satellite_3[0]), radius=np.linalg.norm(np.array([1,0])-satellite_3), color='r', fill=False, visible=True)
    # ax.add_patch(circle_3_prime)
    ax.scatter(satellite_1[1], satellite_1[0], c='b', s=2)
    ax.scatter(satellite_2[1], satellite_2[0], c='g', s=2)
    # ax.scatter(satellite_3[1], satellite_3[0], c='r', s=2)
    i1,j1 = get_unit_vectors(origin-satellite_1)
    print(i1,j1)
    ax.plot([satellite_1[1], satellite_1[1]+i1[1]], [satellite_1[0], satellite_1[0]+i1[0]], c='m')
    ax.plot([satellite_1[1], satellite_1[1]+j1[1]], [satellite_1[0], satellite_1[0]+j1[0]], c='m')
    i2,j2 = get_unit_vectors(origin-satellite_2)
    print(i2,j2)
    ax.plot([satellite_2[1], satellite_2[1]+i2[1]], [satellite_2[0], satellite_2[0]+i2[0]], c='m')
    ax.plot([satellite_2[1], satellite_2[1]+j2[1]], [satellite_2[0], satellite_2[0]+j2[0]], c='m')
    alpha = get_angle_between(i1, i2)
    print(alpha)
    p = h1/np.sin(alpha)*j2-h2/np.sin(alpha)*j1
    print(p)
    ax.plot([0, p[1]], [0, p[0]], 'r')
    plt.show()
    unittest.main()