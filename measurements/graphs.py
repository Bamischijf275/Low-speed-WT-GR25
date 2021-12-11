import loading
import matplotlib.pyplot as plt
import plotting
from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes


degree = "\N{DEGREE SIGN}"


data2d, hys2d = loading.load_pressures_from_file("2D/corr_test")
data3d, hys3d = loading.load_pressures_from_file("3D/corr_test")


def convert_list(input):  # Convert into list if not
    if not isinstance(input, list):
        input = [input]
    return input


def x_alpha(y, data, mode, hys=[]):
    x = "Alpha"
    y = convert_list(y)
    data = convert_list(data)
    mode = convert_list(mode)
    hys = convert_list(hys)

    if len(y) != 1 and len(data) == 1 and len(mode) == 1:
        multi_plot(y, data[0], mode[0], hys)
    else:
        for i in y:  # Plot all the lines
            for j in range(len(data)):  # 2D/3D/Both
                plt.plot(data[j][x], data[j][i], label=(f"{i} in {mode[j]}"), marker=".")

                if len(hys) != 0:
                    plt.plot(hys[j][x], hys[j][i], marker=".")

        plt.title(f"{', '.join(y)} vs {x} [{degree}] in {', '.join(mode)}")
        plt.xlim(-2.5, 18.5)

        if len(mode) != 1:
            plt.legend()

        plt.xlabel(x)
        plt.ylabel(", ".join(y))
        plt.grid(visible=True)
        plotting.format_plot()
        # plt.show()


def cl_cd(data, mode, hys=[]):
    data = convert_list(data)
    mode = convert_list(mode)
    hys = convert_list(hys)

    x, y = "Cd", "Cl"
    for i in range(len(data)):
        plt.plot(data[i][x], data[i][y], label=mode[i], marker=".")

        if len(hys) != 0:
            plt.plot(hys[i][x], hys[i][y], marker=".")

    if len(mode) != 1:
        plt.legend()
    plt.title(f"{y} vs {x} in [{', '.join(mode)}]")
    plt.xlim(0, 0.25)
    plt.ylim(-0.25, 1)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(visible=True)
    plotting.format_plot()
    # plt.show()


def multi_plot(y, data, mode, hys=[]):

    fig = plt.figure()
    if len(y) == 3:
        bool3 = True
    else:
        bool3 = False
    limits = {"Cl": [-0.25, 1], "Cd": [-0.25 / 2, 0.25 * 2], "Cm": [-0.125 * 2 / 3, 0.5 * 2 / 3]}

    host = fig.add_axes([0.15, 0.1, 0.6, 0.8], axes_class=HostAxes)
    par1 = ParasiteAxes(host, sharex=host)
    if bool3:
        par2 = ParasiteAxes(host, sharex=host)
    host.parasites.append(par1)
    if bool3:
        host.parasites.append(par2)

    host.axis["right"].set_visible(False)

    par1.axis["right"].set_visible(True)
    par1.axis["right"].major_ticklabels.set_visible(True)
    par1.axis["right"].label.set_visible(True)

    plt.title(f"{', '.join(y)} vs Alpha [{degree}] in {mode}")
    if bool3:
        par2.axis["right2"] = par2.new_fixed_axis(loc="right", offset=(60, 0))

    (p1,) = host.plot(data["Alpha"], data[y[0]], label=y[0], marker=".")
    # host.plot(hys[0]['Alpha'], hys[0][y[0]], marker='.')

    (p2,) = par1.plot(data["Alpha"], data[y[1]], label=y[1], marker=".")
    if bool3:
        (p3,) = par2.plot(data["Alpha"], data[y[2]], label=y[2], marker=".")

    host.set_xlim(-2.5, 18.5)

    host.set_ylim(limits[y[0]])
    par1.set_ylim(limits[y[1]])
    if bool3:
        par2.set_ylim(limits[y[2]])

    host.set_xlabel(f"Alpha [{degree}]")
    host.set_ylabel(y[0])
    par1.set_ylabel(y[1])
    if bool3:
        par2.set_ylabel(y[2])

    host.legend()

    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["right"].label.set_color(p2.get_color())
    if bool3:
        par2.axis["right2"].label.set_color(p3.get_color())

    plt.grid(visible=True)
    plotting.format_plot()
    # plt.show()


x_alpha(["Cl", "Cd"], data2d, "2D", hys2d)
plt.show()

# x_alpha('Cl', data2d, '2D')
# plotting.save_plot("Cl-Alpha 2D")
#
# x_alpha('Cl', data3d, '3D')
# plotting.save_plot("Cl-Alpha 3D")
#
# x_alpha('Cl', data2d, '2D', hys2d)
# plotting.save_plot("Cl-Alpha 2D with hysteresis")
#
# x_alpha('Cl', data3d, '3D', hys3d)
# plotting.save_plot("Cl-Alpha 3D with hysteresis")
#
#
# x_alpha('Cd', data2d, '2D')
# plotting.save_plot("Cd-Alpha 2D")
#
# x_alpha('Cd', data3d, '3D')
# plotting.save_plot("Cd-Alpha 3D")
#
# x_alpha('Cd', data2d, '2D', hys2d)
# plotting.save_plot("Cd-Alpha 2D with hysteresis")
#
# x_alpha('Cd', data3d, '3D', hys3d)
# plotting.save_plot("Cd-Alpha 3D with hysteresis")
#
#
# x_alpha('Cm', data2d, '2D')
# plotting.save_plot("Cm-Alpha 2D")
#
# x_alpha('Cm', data3d, '3D')
# plotting.save_plot("Cm-Alpha 3D")
#
# x_alpha('Cm', data2d, '2D', hys2d)
# plotting.save_plot("Cm-Alpha 2D with hysteresis")
#
# x_alpha('Cm', data3d, '3D', hys3d)
# plotting.save_plot("Cm-Alpha 3D with hysteresis")
#
# cl_cd(data2d, "2D")
# plotting.save_plot("Cl-Cd 2D")
#
# cl_cd(data3d, "3D")
# plotting.save_plot("Cl-Cd 3D")
#
# cl_cd(data2d, "2D", hys2d)
# plotting.save_plot("Cl-Cd 2D with hysteresis")
#
# cl_cd(data3d, "3D", hys3d)
# plotting.save_plot("Cl-Cd 3D with hysteresis")
#
# cl_cd([data2d, data3d], ["2D", '3D'])
# plotting.save_plot("Cl-Cd 2D & 3D")
#
# cl_cd([data2d, data3d], ["2D", '3D'], [hys2d, hys3d])
# plotting.save_plot("Cl-Cd 2D & 3D with hysteresis")
#
#
# x_alpha('Cl', [data2d, data3d], ['2D', '3D'])
# plotting.save_plot("Cl-Alpha 2D & 3D")
#
# x_alpha('Cl', [data2d, data3d], ['2D', '3D'], [hys2d, hys3d])
# plotting.save_plot("Cl-Alpha 2D & 3D with hysteresis")
#
#
# x_alpha('Cd', [data2d, data3d], ['2D', '3D'])
# plotting.save_plot("Cd-Alpha 2D & 3D")
#
#
# x_alpha('Cd', [data2d, data3d], ['2D', '3D'], [hys2d, hys3d])
# plotting.save_plot("Cd-Alpha 2D & 3D with hysteresis")
#
# x_alpha('Cm', [data2d, data3d], ['2D', '3D'])
# plotting.save_plot("Cm-Alpha 2D & 3D")
#
# x_alpha('Cm', [data2d, data3d], ['2D', '3D'], [hys2d, hys3d])
# plotting.save_plot("Cm-Alpha 2D & 3D with hysteresis")
#
#
# x_alpha(['Cl', 'Cd', 'Cm'], [data2d], ['2D'])
# plotting.save_plot("Cl,Cd,Cm-Alpha 2D")
#
#
# x_alpha(['Cl', 'Cd', 'Cm'], [data2d], ['2D'], [hys2d])
# plotting.save_plot("Cl,Cd,Cm-Alpha 2D with hysteresis")
#
# x_alpha(['Cl', 'Cd', 'Cm'], [data2d], ['3D'])
# plotting.save_plot("Cl,Cd,Cm-Alpha 3D")
#
# x_alpha(['Cl', 'Cd', 'Cm'], [data2d], ['3D'], [hys3d])
# plotting.save_plot("Cl,Cd,Cm-Alpha 3D with hysteresis")
#
# x_alpha(['Cl', 'Cd', 'Cm'], [data2d, data3d], ['2D', '3D'])
# plotting.save_plot("Cl,Cd,Cm-Alpha 2D & 3D")
#
# x_alpha(['Cl', 'Cd', 'Cm'], [data2d, data3d], ['2D', '3D'], [hys2d, hys3d])
# plotting.save_plot("Cl,Cd,Cm-Alpha 2D & 3D with hysteresis")


# slope calculation
