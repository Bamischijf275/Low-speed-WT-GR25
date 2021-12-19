import loading
import matplotlib.pyplot as plt
import plotting
from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes

# degree symbol
degree = "\N{DEGREE SIGN}"

# Load files
# loading.load_pressures_from_file("2D/corr_test")   # 2D actual measurements
# loading.load_pressures_from_file("3D/corr_test")   # 3D actual measurements
# loading.load_pressures_from_file("balance/corr_test") # 3D Balance measurements

# loading.load_pressures_from_file_simulated("3D/OP_points_tip/LLT")   # 3D LLT simulation measurements
# loading.load_pressures_from_file_simulated("3D/OP_points_tip/VLM")   # 3D VLM simulation measurements


data2d, hys2d = loading.load_pressures_from_file("2D/corr_test")
data3d, hys3d = loading.load_pressures_from_file("balance/corr_test")
datavlm, trash = loading.load_pressures_from_file_simulated("3D/OP_points_tip/VLM")


print(max(datavlm['Cm']))
print(min(datavlm['Cm']))
def convert_list(input):  # Convert into list if not
    if not isinstance(input, list):
        input = [input]
    return input


def x_alpha(y, data, mode, tags, hys=[]):  # X vs Alpha plots
    x = "Alpha"
    y = convert_list(y)
    data = convert_list(data)
    mode = convert_list(mode)
    hys = convert_list(hys)
    tags = convert_list(tags)

    label = []
    for k in y:
        if mode[0]:
            label.append("${}_{}$".format(k[0], k[1]))

    if len(y) != 1 and len(data) == 1 and len(mode) == 1:
        multi_plot(y, data[0], mode[0], hys)  # Plot with varying y-axes
    else:
        for i in y:  # Plot all the lines
            for j in range(len(data)):  # 2D/3D/Both
                # plt.plot(data[j][x], data[j][i], label=(f"{i} in {mode[j]}"), marker=".")
                plt.plot(data[j][x], data[j][i], label=r'${}_{}$, {}'.format(i[0], i[1], mode[j]), marker=".")
                if len(hys) != 0:  # plot hysteresis with different color
                    plt.plot(hys[j][x], hys[j][i], marker=".")

        # plt.title(r"{} vs {} (deg) in {}".format(', '.join(label), f'\u03B1', ', '.join(mode)))  # title
        # plt.xlim(-2.5, 18.5)  # x limit

        if len(mode) != 1:  # if only one curve, don't include legend
            plt.legend()


        plt.xlabel('\u03B1 (deg)')
        plt.ylabel(r', '.join(label))
        plt.grid(visible=True)
        plotting.format_plot()
        # plt.show()


def drag_polar(data, mode, tags, hys=[]):  # drag polar graph
    data = convert_list(data)
    mode = convert_list(mode)
    hys = convert_list(hys)
    tags = convert_list(tags)

    x, y = "Cd", "Cl"

    title = 'Drag polar in ' + ', '.join(mode)

    if len(hys) != 0: # include hysteresis in title
        title += ' (with hysteresis)'

    if '2D' in tags:  # set x, y labels
        label = ['$C_d$', '$C_l$']
    else:
        label = ['$C_D$', '$C_L$']

    for i in range(len(data)):
        plt.plot(data[i][x], data[i][y], label=mode[i], marker=".")
        # hys_color = np.array((p[0].get_color()))
        # hys_color[0] = 1

        if len(hys) != 0:
            plt.plot(hys[i][x], hys[i][y], marker=".")

    if len(mode) != 1:
        plt.legend()

    # plt.title(f"{y} vs {x} in [{', '.join(mode)}]")

    # plt.title(r"$C_D$ vd $C_L$" + ', '.join(mode))

    # plt.title(title)

    # plt.xlim(0, 0.25)
    # plt.ylim(-0.25, 1)
    plt.xlabel(r'{}'.format(label[0]))
    plt.ylabel(r'{}'.format(label[1]))
    plt.grid(visible=True)
    plotting.format_plot()
    # plt.show()


def multi_plot(y, data, mode, tags, hys=[]):  # graphs for multiple y-axes
    label = []
    for element in y:
        if mode == '2D':
            label.append(element)
        elif mode == '3D':
            pass

    fig, ax = plt.subplots()
    fig.subplots_adjust(right=0.75)

    if len(y) == 3:  # check if input has three items
        bool3 = True
    else:
        bool3 = False

    twin1 = ax.twinx()
    twin2 = ax.twinx()
    twin2.spines.right.set_position(("axes", 1.2))

    limits = {
        "Cl": [min(data["Cl"] - 0.1), max(data["Cl"]) + 0.1],
        "Cd": [min(data["Cd"] - 0.2), max(data["Cd"]) + 0.6],
        "Cm": [min(data["Cm"] - 0.4), max(data["Cm"]) + 1],
    }  # Change until the 3 curves look nice and readable

    # limits = {'Cl': [],
    #           'Cd': [],
    #           'Cm': []}

    p1, = ax.plot(data["Alpha"], data[y[0]], "b-", label=y[0], marker=".")
    p2, = twin1.plot(data["Alpha"], data[y[1]], "r-", label=y[1], marker=".")
    if bool3:
        p3, = twin2.plot(data["Alpha"], data[y[2]], "g-",  label=y[2], marker=".")

    # ax.set_xlim(0, 2)
    ax.set_ylim(limits[y[0]])
    twin1.set_ylim(limits[y[1]])
    twin2.set_ylim(limits[y[2]])

    ax.set_xlabel('\u03B1 (deg)')
    ax.set_ylabel(y[0])
    twin1.set_ylabel(y[1])
    twin2.set_ylabel(y[2])

    ax.yaxis.label.set_color(p1.get_color())
    twin1.yaxis.label.set_color(p2.get_color())
    twin2.yaxis.label.set_color(p3.get_color())

    tkw = dict(size=4, width=1.5)
    ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
    twin1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    twin2.tick_params(axis='y', colors=p3.get_color(), **tkw)
    ax.tick_params(axis='x', **tkw)

    ax.legend(handles=[p1, p2, p3])

    plotting.format_plot()

# x_alpha(['Cl', 'Cm', 'Cd'], [data3d], ['3D'])
# plt.show()

# drag_polar([data2d, data3d], ["2D", "3D"], [hys2d, hys3d])
# plt.show()
drag_polar([data2d, data3d], ["Measurements", ""], "2D")
plt.show()
# 
# x_alpha('Cl', [datavlm, data3d], ['VLM', 'Measurement'])
# plt.show()
# plotting.save_plot("Cl-Alpha 2D")
# #
# x_alpha('Cl', data3d, '3D')
# plotting.save_plot("Cl-Alpha 3D")
# #
# x_alpha('Cl', data2d, '2D', hys2d)
# plotting.save_plot("Cl-Alpha 2D with hysteresis")
# 
# x_alpha('Cl', data3d, '3D', hys3d)
# plotting.save_plot("Cl-Alpha 3D with hysteresis")
# #
# 
# x_alpha('Cd', data2d, '2D')
# plotting.save_plot("Cd-Alpha 2D")
# #
# x_alpha('Cd', data3d, '3D')
# plotting.save_plot("Cd-Alpha 3D")
# #
# x_alpha('Cd', data2d, '2D', hys2d)
# plotting.save_plot("Cd-Alpha 2D with hysteresis")
# 
# x_alpha('Cd', data3d, '3D', hys3d)
# plotting.save_plot("Cd-Alpha 3D with hysteresis")
# #
# #
# x_alpha('Cm', data2d, '2D')
# plotting.save_plot("Cm-Alpha 2D")
# #
# x_alpha('Cm', data3d, '3D')
# plotting.save_plot("Cm-Alpha 3D")
# #
# x_alpha('Cm', data2d, '2D', hys2d)
# plotting.save_plot("Cm-Alpha 2D with hysteresis")
# 
# x_alpha('Cm', data3d, '3D', hys3d)
# plotting.save_plot("Cm-Alpha 3D with hysteresis")
# #
# drag_polar(data2d, "2D")
# plotting.save_plot("Cl-Cd 2D")
# #
# drag_polar(data3d, "3D")
# plotting.save_plot("Cl-Cd 3D")
# #
# drag_polar(data2d, "2D", hys2d)
# plotting.save_plot("Cl-Cd 2D with hysteresis")
# 
# drag_polar(data3d, "3D", hys3d)
# plotting.save_plot("Cl-Cd 3D with hysteresis")
# 
# drag_polar([data2d, data3d], ["2D", '3D'])
# plotting.save_plot("Cl-Cd 2D & 3D")
# 
# drag_polar([data2d, data3d], ["2D", '3D'], [hys2d, hys3d])
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
# #
# x_alpha(['Cl', 'Cd', 'Cm'], [data3d], ['3D'])
# plotting.save_plot("Cl,Cd,Cm-Alpha 3D")
# # #
# x_alpha(['Cl', 'Cd', 'Cm'], [data3d], ['3D'], [hys3d])
# plotting.save_plot("Cl,Cd,Cm-Alpha 3D with hysteresis")
# 
# x_alpha(['Cl', 'Cd', 'Cm'], [data2d, data3d], ['2D', '3D'])
# plotting.save_plot("Cl,Cd,Cm-Alpha 2D & 3D")
# 
# x_alpha(['Cl', 'Cd', 'Cm'], [data2d, data3d], ['2D', '3D'], [hys2d, hys3d])
# plotting.save_plot("Cl,Cd,Cm-Alpha 2D & 3D with hysteresis")


# slope calculation
