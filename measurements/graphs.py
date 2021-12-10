import loading
import matplotlib.pyplot as plt
import plotting
import numpy as np

degree = "\N{DEGREE SIGN}"


data2d = loading.load_pressures_from_file("2D/corr_test")
data3d = loading.load_pressures_from_file("3D/corr_test")


def x_alpha(y, data, mode):
    x = 'Alpha'
    data.plot(x=x, y=y)
    plt.title(f"{y} vs {x} [{degree}] {mode}")
    plt.xlim(-2.5, 18.5)

    if y == 'Cl':
        plt.ylim(-0.25, 1)
    elif y == 'Cd':
        plt.ylim(0, 0.25)
    else:
        plt.ylim(-0.085, 0.035)

    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(visible=True)
    plotting.format_plot()
    plt.show()


def cl_cd(data, mode):
    x, y = 'Cd', 'Cl'
    data.plot(x=x, y=y)
    plt.title(f"{y} vs {x} in [{mode}]")
    plt.xlim(0, 0.25)
    plt.ylim(-0.25, 1)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(visible=True)
    plotting.format_plot()
    plt.show()


x_alpha('Cl', data2d, '2D')
x_alpha('Cl', data3d, '3D')

x_alpha('Cd', data2d, '2D')
x_alpha('Cd', data3d, '3D')

x_alpha('Cm', data2d, '2D')
x_alpha('Cm', data3d, '3D')

cl_cd(data2d, "2D")
cl_cd(data3d, "3D")
