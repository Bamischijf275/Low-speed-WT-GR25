import loading
import matplotlib.pyplot as plt


data = loading.load_pressures_from_file("2D/corr_test")


def plotter(x, y):
    data.plot(x=x, y=y)
    plt.title(x + " vs " + y)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()


data.plot(x="Alpha", y="Cl")
plt.show()
