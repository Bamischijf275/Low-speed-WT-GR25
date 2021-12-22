import loading
import matplotlib.pyplot as plt
import plotting
import matplotlib.lines as mlines

# Load datasets
data_Actual_2D, hys2d, data_Actual_2D_hys = loading.load_pressures_from_file("2D/corr_test")
data_Actual_3D, hys3d, data_Actual_3D_hys = loading.load_pressures_from_file("balance/corr_test")
data_VLM_tip, _ = loading.load_pressures_from_file_simulated("3D/OP_points_tip/VLM")
data_VLM_notip, _ = loading.load_pressures_from_file_simulated("3D/OP_points_no_tip/VLM")
data_LLT_tip, _ = loading.load_pressures_from_file_simulated("3D/OP_points_tip/LLT")
data_LLT_notip, _ = loading.load_pressures_from_file_simulated("3D/OP_points_no_tip/LLT")
data_XFOIL, _ = loading.load_polars_from_xfoil("141viscnew")


# Some information for datasets
Actual_2D = ("2D Measurements", "2D")
Actual_3D = ("3D Measurements", "3D")
VLM_tip = ("VLM with tip", "3D")
VLM_notip = ("VLM without tip", "3D")
LLT_tip = ("LLT with tip", "3D")
LLT_notip = ("LLT without tip", "3D")
XFOIL = ("XFOIL", "2D")
Actual_2D_hys = ("2D Measurements", "2D")
Actual_3D_hys = ("3D Measurements", "3D")


# Dictionary that connects the data set and information
dic = {
    Actual_2D: data_Actual_2D,
    Actual_3D: data_Actual_3D,
    VLM_notip: data_VLM_notip,
    VLM_tip: data_VLM_tip,
    LLT_notip: data_LLT_notip,
    LLT_tip: data_LLT_tip,
    XFOIL: data_XFOIL,
    Actual_2D_hys: data_Actual_2D_hys,
    Actual_3D_hys: data_Actual_3D_hys,
}


def convert_list(input):  # Convert into list if not
    if not isinstance(input, list):
        input = [input]
    return input


def x_alpha(y, info, hys=[], arrow=False):  # X vs Alpha plots
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
        if "2D" in tags:
            label.append("${}_{}$".format(y[i][0], y[i][1]))
        else:
            label.append("${}_{}$".format(y[i][0], y[i][1].upper()))
    plt.figure(figsize=(12, 6))
    if len(y) != 1 and len(data) == 1 and len(mode) == 1:
        multi_plot(y, data[0], mode, label, hys)  # Plot with varying y-axes
    else:
        for i in range(len(y)):  # Plot all the lines
            for j in range(len(data)):  # 2D/3D/Both
                # plt.plot(data[j][x], data[j][i], label=(f"{i} in {mode[j]}"), marker=".")
                plt.plot(
                    data[j][x], data[j][y[i]], label=r"{}, {}".format(label[i], mode[j]), marker="."
                )

                if len(hys) == 1:  # plot hysteresis with different color
                    plt.plot(
                        hys[j][x],
                        hys[j][y[i]],
                        label=r"{} hysteresis, {}".format(label[i], mode[j]),
                        marker=".",
                    )

                if len(hys) == 2:
                    plt.plot(
                        hys[j][x], hys[j][y[i]], marker=".", color=plt.gca().lines[-1].get_color()
                    )

        if arrow:  # add arrow symbol to legend
            plt.arrow(
                3.833,
                0.3602,
                0.927,
                0,
                head_width=0.026,
                head_length=0.2,
                width=0.01,
                color="gold",
                ec="k",
            )

            handles, labels = plt.gca().get_legend_handles_labels()  # get current legends
            arrow_shape = mlines.Line2D(
                [],
                [],
                marker=r"$\rightarrow$",  # arrow legend
                linestyle="None",
                color="gold",
                markersize=25,
                label="$\u03B1_{ind}$",
            )

            handles.extend([arrow_shape])  # add arrow legend to current legends
            plt.legend(handles=handles)

        elif (len(mode) != 1) or (len(hys) != 0):  # if only one curve, don't include legend
            plt.legend()

        plt.xlabel("\u03B1 (deg)")
        plt.ylabel(r", ".join(label))
        plotting.format_plot()

        plotting.save_plot(r"{} vs {} (deg) - {}".format(", ".join(y), f"\u03B1", ", ".join(mode)))


def drag_polar(info, hys=[]):  # drag polar graph
    info = convert_list(info)
    hys = convert_list(hys)
    mode, tags, data = [], [], []
    for pack in info:
        mode.append(pack[0])
        tags.append(pack[1])
        data.append(dic[pack])

    plt.figure(figsize=(12, 6))

    x, y = "Cd", "Cl"

    if "2D" in tags:  # set x, y labels
        label = ["$C_d$", "$C_l$"]
    else:
        label = ["$C_D$", "$C_L$"]

    for i in range(len(data)):
        plt.plot(data[i][x], data[i][y], label=mode[i], marker=".")
        # hys_color = np.array((p[0].get_color()))
        # hys_color[0] = 1

        if len(hys) == 1:
            plt.plot(hys[i][x], hys[i][y], label="hysteresis, " + mode[i], marker=".")
        if len(hys) == 2:
            plt.plot(hys[i][x], hys[i][y], marker=".", color=plt.gca().lines[-1].get_color())
    if (len(mode) != 1) or (len(hys) != 0):
        plt.legend()

    # plt.xlim(0, 0.25)
    # plt.ylim(-0.25, 1)
    plt.xlabel(r"{}".format(label[0]))
    plt.ylabel(r"{}".format(label[1]))
    plotting.format_plot()
    plotting.save_plot("Drag polar - " + ", ".join(mode))


def multi_plot(y, data, mode, label, hys=[]):  # graphs for multiple y-axes

    fig, ax = plt.subplots()

    fig.subplots_adjust(right=0.75)
    fig.set_figheight(6)
    fig.set_figwidth(12)

    if len(y) == 3:  # check if input has three items
        bool3 = True
    else:
        bool3 = False

    twin1 = ax.twinx()
    if bool3:
        twin2 = ax.twinx()
        twin2.spines.right.set_position(("axes", 1.2))

    limits = {
        "Cl": [min(data["Cl"] - 0.1), max(data["Cl"]) + 0.1],
        "Cd": [min(data["Cd"] - 0.2), max(data["Cd"]) + 0.6],
        "Cm": [min(data["Cm"] - 0.4), max(data["Cm"]) + 1],
    }  # Set limits of curves so they don't intersect a lot

    (p1,) = ax.plot(data["Alpha"], data[y[0]], "b-", label=label[0], marker=".")
    (p2,) = twin1.plot(data["Alpha"], data[y[1]], "r-", label=label[1], marker=".")
    if bool3:
        (p3,) = twin2.plot(data["Alpha"], data[y[2]], "g-", label=label[2], marker=".")

    # ax.set_xlim(0, 2)
    ax.set_ylim(limits[y[0]])
    twin1.set_ylim(limits[y[1]])
    if bool3:
        twin2.set_ylim(limits[y[2]])

    ax.set_xlabel("\u03B1 (deg)")
    ax.set_ylabel(label[0])
    twin1.set_ylabel(label[1])
    if bool3:
        twin2.set_ylabel(label[2])

    ax.yaxis.label.set_color(p1.get_color())
    twin1.yaxis.label.set_color(p2.get_color())
    if bool3:
        twin2.yaxis.label.set_color(p3.get_color())

    tkw = dict(size=4, width=1.5)
    ax.tick_params(axis="y", colors=p1.get_color(), **tkw)
    twin1.tick_params(axis="y", colors=p2.get_color(), **tkw)
    if bool3:
        twin2.tick_params(axis="y", colors=p3.get_color(), **tkw)
    ax.tick_params(axis="x", **tkw)

    if bool3:
        ax.legend(handles=[p1, p2, p3])
    else:
        ax.legend(handles=[p1, p2])

    plotting.format_plot()
    plotting.save_plot(r"{} vs {} (deg) - {}".format(", ".join(y), f"\u03B1", ", ".join(mode)))


# analyse and export plots, passing hysteresis datasets in a list plots hysteresis, detailed=True returns more plots,
# arrow=True makes an arrow for alpha induced only for 2D vs 3D experimental results
def analyse(
    data, hys=[], detailed=False, arrow=False
):  # To plot and save, call this function and give the data points in a list
    data = convert_list(data)

    x_alpha(["Cl", "Cd", "Cm"], data, hys)
    x_alpha(["Cl"], data, hys, arrow)
    x_alpha(["Cd"], data, hys)
    x_alpha(["Cm"], data, hys)
    drag_polar(data, hys)

    if detailed:
        x_alpha(["Cl", "Cd"], data, hys)
        x_alpha(["Cd", "Cm"], data, hys)
        x_alpha(["Cl", "Cm"], data, hys)


analyse([VLM_notip])
