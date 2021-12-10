import loading
import matplotlib.pyplot as plt
import plotting


from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA


degree = "\N{DEGREE SIGN}"


data2d = loading.load_pressures_from_file("2D/corr_test")
data3d = loading.load_pressures_from_file("3D/corr_test")

def convertList(input):  # Convert into list if not
    if not isinstance(input, list):
        input = [input]

    return input

def x_alpha(y, data, mode):
    x = 'Alpha'
    y = convertList(y)
    data = convertList(data)
    mode = convertList(mode)
    print(data)
    for i in y:  # Plot all the lines
        k = 0
        for j in data:  # 2D/3D/Both
            plt.plot(j[x], j[i], label=(f"{i} in {mode[k]}"), marker='D')
            k += 1

    plt.title(f"{', '.join(y)} vs {x} [{degree}] in {', '.join(mode)}")
    plt.xlim(-2.5, 18.5)

    # if y == 'Cl':
    #     plt.ylim(-0.25, 1)
    # elif y == 'Cd':
    #     plt.ylim(0, 0.25)
    # else:
    #     plt.ylim(-0.085, 0.035)

    plt.legend()
    plt.xlabel(x)
    plt.ylabel(', '.join(y))
    plt.grid(visible=True)
    plotting.format_plot()
    plt.show()


def cl_cd(data, mode):
    x, y = 'Cd', 'Cl'
    data.plot(x=x, y=y, marker='D')
    plt.title(f"{y} vs {x} in [{mode}]")
    plt.xlim(0, 0.25)
    plt.ylim(-0.25, 1)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(visible=True)
    plotting.format_plot()
    plt.show()

def multiy(y_parameters):
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)
    par1 = host.twinx()
    par2 = host.twinx()
    offset = 60
    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    par2.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par2,
                                        offset=(offset, 0))
    par2.axis["right"].toggle(all=True)

    host.set_xlim(-2.5, 18.5)  # Alpha range

    host.set_ylim(-0.5, 1)

    host.set_xlabel("Alpha")
    host.set_ylabel("Cl")
    par1.set_ylabel("Cd")
    par2.set_ylabel("Cm")

    p1, = host.plot(data2d['Alpha'], data2d['Cl'], label="Cl")
    p2, = par1.plot(data2d['Alpha'], data2d['Cd'], label="Cd")
    p3, = par2.plot(data2d['Alpha'], data2d['Cm'], label="Cm")

    par1.set_ylim(0, 0.25)
    par2.set_ylim(-0.25, 25)

    host.legend()

    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["right"].label.set_color(p2.get_color())
    par2.axis["right"].label.set_color(p3.get_color())

    plt.draw()
    plt.show()

# multiy()

# x_alpha('Cl', data2d, '2D')
# x_alpha('Cl', data3d, '3D')

# x_alpha('Cd', data2d, '2D')
# x_alpha('Cd', data3d, '3D')
#
# x_alpha('Cm', data2d, '2D')
# x_alpha('Cm', data3d, '3D')
#
# cl_cd(data2d, "2D")
# cl_cd(data3d, "3D")

x_alpha('Cl', [data2d, data3d], ['2D', '3D'])
x_alpha(['Cl', 'Cd', 'Cm'], [data2d, data3d], ['2D', '3D'])

#different color for hysteresis