import loading
import matplotlib.pyplot as plt
import plotting
import numpy as np

degree = "\N{DEGREE SIGN}"


data2d = loading.load_pressures_from_file("2D/corr_test")
data3d = loading.load_pressures_from_file("3D/corr_test")


def cl_alpha(x, y, data, mode):
    data.plot(x=x, y=y)
    plt.title(f"{y} vs {x} [{degree}] {mode}")
    plt.xlim(-2.5, 18.5)
    plt.ylim(-0.25, 1)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(visible=True)
    plotting.format_plot()
    plt.show()


def cd_alpha(x, y, data, mode):
    data.plot(x=x, y=y)
    plt.title(f"{y} vs {x} [{degree}] {mode}")
    plt.xlim(-2.5, 18.5)
    plt.ylim(0, 0.25)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(visible=True)
    plotting.format_plot()
    plt.show()


def cm_alpha(x, y, data, mode):
    data.plot(x=x, y=y)
    plt.title(f"{y} vs {x} [{degree}] {mode}")
    plt.xlim(-2.5, 18.5)
    plt.ylim(-0.085, 0.035)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(visible=True)
    plotting.format_plot()
    plt.show()


def cl_cd(x, y, data, mode):
    data.plot(x=x, y=y)
    plt.title(f"{y} vs {x} in [{mode}]")
    plt.xlim(0, 0.25)
    plt.ylim(-0.25, 1)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(visible=True)
    plotting.format_plot()
    plt.show()


# cl_alpha('Alpha', 'Cl', data2d, '2D')
# cl_alpha('Alpha', 'Cl', data3d, '3D')

# cd_alpha('Alpha', 'Cd', data2d, '2D')
# cd_alpha('Alpha', 'Cd', data3d, '3D')

# cm_alpha('Alpha', 'Cm', data2d, '2D')
# cm_alpha('Alpha', 'Cm', data3d, '3D')

cl_cd("Cd", "Cl", data2d, "2D")
cl_cd("Cd", "Cl", data3d, "3D")
