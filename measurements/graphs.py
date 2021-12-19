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


data_Actual_2D, hys2d = loading.load_pressures_from_file("2D/corr_test")
data_Actual_3D, hys3d = loading.load_pressures_from_file("balance/corr_test")
data_VLM_tip, trash = loading.load_pressures_from_file_simulated("3D/OP_points_tip/VLM")
data_VLM_notip, trash = loading.load_pressures_from_file_simulated("3D/OP_points_no_tip/VLM")
data_LLT_tip, trash = loading.load_pressures_from_file_simulated("3D/OP_points_tip/LLT")
data_LLT_notip, trash = loading.load_pressures_from_file_simulated("3D/OP_points_no_tip/LLT")

Actual_2D = ('2D Measurements', '2D')
Actual_3D = ('3D Measurements', '3D')
VLM_tip = ('VLM with tip', '3D')
VLM_notip = ('VLM without tip', '3D')
LLT_tip = ('LLT with tip', '3D')
LLT_notip = ('LLT without tip', '3D')

dic = {Actual_2D: data_Actual_2D,
       Actual_3D: data_Actual_3D,
       VLM_notip: data_VLM_notip,
       VLM_tip: data_VLM_tip,
       LLT_notip: data_LLT_notip,
       LLT_tip: data_LLT_tip}


def convert_list(input):  # Convert into list if not
    if not isinstance(input, list):
        input = [input]
    return input


def x_alpha(y, info, hys=[]):  # X vs Alpha plots
    x = "Alpha"

    info = convert_list(info)
    hys = convert_list(hys)
    mode, tags, data = [], [], []
    for pack in info:
        mode.append(pack[0])
        tags.append(pack[1])
        data.append(dic[pack])

    label = []
    for i in range(len(y)):
        if '2D' in tags:
            label.append("${}_{}$".format(y[i][0], y[i][1]))
        else:
            label.append("${}_{}$".format(y[i][0], y[i][1].upper()))

    if len(y) != 1 and len(data) == 1 and len(mode) == 1:
        multi_plot(y, data[0], mode[0], label, hys)  # Plot with varying y-axes
    else:
        for i in y:  # Plot all the lines
            for j in range(len(data)):  # 2D/3D/Both
                # plt.plot(data[j][x], data[j][i], label=(f"{i} in {mode[j]}"), marker=".")
                plt.plot(data[j][x], data[j][i], label=r'{}, {}'.format(label[i], mode[j]), marker=".")
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
        plt.show()


def drag_polar(info, hys=[]):  # drag polar graph
    info = convert_list(info)
    hys = convert_list(hys)
    mode, tags, data = [], [], []
    for pack in info:
        mode.append(pack[0])
        tags.append(pack[1])
        data.append(dic[pack])



    x, y = "Cd", "Cl"

    title = 'Drag polar in ' + ', '.join(mode)

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

    # plt.xlim(0, 0.25)
    # plt.ylim(-0.25, 1)
    plt.xlabel(r'{}'.format(label[0]))
    plt.ylabel(r'{}'.format(label[1]))
    plotting.format_plot()
    plt.show()


def multi_plot(y, data, mode, label, hys=[]):  # graphs for multiple y-axes


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
    }  # Set limits of curves so they don't intersect a lot


    p1, = ax.plot(data["Alpha"], data[y[0]], "b-", label=label[0], marker=".")
    p2, = twin1.plot(data["Alpha"], data[y[1]], "r-", label=label[1], marker=".")
    if bool3:
        p3, = twin2.plot(data["Alpha"], data[y[2]], "g-",  label=label[2], marker=".")

    # ax.set_xlim(0, 2)
    ax.set_ylim(limits[y[0]])
    twin1.set_ylim(limits[y[1]])
    twin2.set_ylim(limits[y[2]])

    ax.set_xlabel('\u03B1 (deg)')
    ax.set_ylabel(label[0])
    twin1.set_ylabel(label[1])
    twin2.set_ylabel(label[2])

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
    plt.show()

def analyse(data, hys=[]):
    data = convert_list(data)

    x_alpha(['Cl', 'Cd', 'Cm'], data, hys)
    x_alpha(['Cl'], data, hys)
    x_alpha(['Cd'], data, hys)
    x_alpha(['Cm'], data, hys)


analyse([Actual_2D, Actual_3D])