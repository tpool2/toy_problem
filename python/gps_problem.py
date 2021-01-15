from matplotlib import pyplot as plt
import numpy as np

import unittest

def gps_algorithm(initial_point, satellites, pseudoranges, tolerance = 0.001):
    k = 0
    receiver_location = initial_point
    new_location = receiver_location
    clock_bias = 0
    while  (abs(new_location-receiver_location) > tolerance).any() or k==0:
        receiver_location = new_location
        new_location, clock_bias = position_determiner(receiver_location, satellites, pseudoranges)
        k += 1

    return new_location, clock_bias, k

def position_determiner(receiver_point, satellites, pseudoranges):

    H = np.hstack((-(satellites-receiver_point)/(np.linalg.norm(satellites-receiver_point, axis=1).reshape((4,1))), np.ones((4,1))))
    pseudoranges_0 = np.array([np.linalg.norm(receiver_point - satellite) for satellite in satellites])
    delta_x, residuals, rank, s = np.linalg.lstsq(H, (pseudoranges-pseudoranges_0).T)
    # print(delta_x)
    return receiver_point + delta_x[:3], delta_x[3]

class TestGPS(unittest.TestCase):
    def test_1(self):
        sv_2 = np.array([7766188.44, -21960535.34, 12522838.56])
        sv_26 = np.array([-25922679.66, -6629461.28, 31864.37])
        sv_4 = np.array([-5743774.02, -25828319.92, 1692757.72])
        sv_7 = np.array([-2786005.69, -15900725.80, 21302003.49])
        p1 = 22228206.42
        p2 = 24096139.11
        p3 = 21729070.63
        p4 = 21259581.09
        satellites = np.array([sv_2, sv_26, sv_4, sv_7])
        pseudoranges = np.array([p1, p2, p3, p4])
        position = np.array([0,0,0])
        position, receiver_clock_bias, k = gps_algorithm(np.zeros((3)), satellites, pseudoranges, 3)
        print(position, receiver_clock_bias, k)

if __name__=='__main__':
    sv_2 = np.array([7766188.44, -21960535.34, 12522838.56])
    sv_26 = np.array([-25922679.66, -6629461.28, 31864.37])
    sv_4 = np.array([-5743774.02, -25828319.92, 1692757.72])
    sv_7 = np.array([-2786005.69, -15900725.80, 21302003.49])
    satellites = np.array([sv_2, sv_26, sv_4, sv_7])
    p1 = 22228206.42
    p2 = 24096139.11
    p3 = 21729070.63
    p4 = 21259581.09
    psuedoranges = np.array([p1, p2, p3, p4])

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(satellites[0], satellites[1], satellites[2], color='b')
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    r = 6.371*10**6
    x = r*np.cos(u)*np.sin(v)
    y = r*np.sin(u)*np.sin(v)
    z = r*np.cos(v)
    ax.plot_wireframe(x, y, z,color='g')
    receiver_position, receiver_clock_bias, k = gps_algorithm(np.zeros((3)), satellites, psuedoranges)
    ax.scatter(receiver_position[0], receiver_position[1], receiver_position[2], color='r')
    print(receiver_position)
    plt.show()
    unittest.main()