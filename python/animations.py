from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib import pyplot as plt
import Parameters as P
def sine_animation():

    g = P.G*P.earth_mass/(P.orbital_radius**2)

    time = np.linspace(0, 200, 20000)
    x0 = np.array([0, P.orbital_radius])
    x_dot0 = np.array([-np.sqrt(P.G*P.earth_mass/P.orbital_radius), 0])
    x = .5*g*time**2

    fig = plt.figure()
    plt.xlim(-2.2, 2.2)
    plt.ylim(-2.2, 2.2)

    satellite_1, = plt.plot([],[])

    def update(index):

        satellite_1.set_data(x1[index-2:index], y1[index-2:index])
        return satellite_1, satellite_2,

    a = FuncAnimation(fig, update, frames=len(x1), interval=10)
    plt.show()