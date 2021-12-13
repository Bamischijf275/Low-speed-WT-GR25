import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from measurements.plotting import save_plot

plots  = False

def grab_values(filename, skip_begin, skip_end):
    """
    Function that grabs data from an XFLR5 file
    """

    # Get the useful lists of data
    y_lst = np.genfromtxt(
        str(filename), skip_header=skip_begin, skip_footer=skip_end, usecols=(0,)
    )  # Generate list of y cords
    XTrtop_lst = np.genfromtxt(
        str(filename), skip_header=skip_begin, skip_footer=skip_end, usecols=(8,)
    )  # Generate list of chord lengths

    # The last values are the actual total values! The sectional values are the lists!
    return y_lst, XTrtop_lst


def plot_config(title):
    """
    Contains the configuration for the plots
    """
    line_thickness = 6
    line_color = "#000000"

    plt.ylim(0.0, 0.7)
    plt.xlim(-0.1, 0.3)
    plt.plot((0, 0), (0, 0.64), linewidth=line_thickness, color=line_color)
    plt.plot((0, 0.24), (0.64, 0.64), linewidth=line_thickness, color=line_color)
    plt.plot((0.24, 0.24), (0.64, 0), linewidth=line_thickness, color=line_color)
    plt.plot((0.24, 0), (0.0, 0.0), linewidth=line_thickness, color=line_color)
    plt.title(title)
    plt.gca().invert_yaxis()


colors = [
    "#38f523",
    "#38f523",
    "#4cf107",
    "#5bed00",
    "#68e900",
    "#73e500",
    "#7ce100",
    "#85dd00",
    "#85dd00",
    "#8dd900",
    "#94d500",
    "#9bd100",
    "#a1cc00",
    "#a7c800",
    "#adc400",
    "#b2bf00",
    "#b8bb00",
    "#bdb600",
    "#c1b100",
    "#c6ac00",
    "#caa700",
    "#cea300",
    "#d29d00",
    "#d59800",
    "#d99300",
    "#dc8e00",
    "#df8800",
    "#e28300",
    "#e57d00",
    "#e77700",
    "#e97100",
    "#eb6b00",
    "#ed6400",
    "#ef5e00",
    "#f05700",
    "#f15000",
    "#f24800",
    "#f34000",
    "#f43600",
    "#f43600",
    "#f42c00",
    "#f41f00",
    "#f41f00",
    "#f40909",
    "#f40909",
]

if plots:
    # Plots without tip, LLT
    plt.figure()

    k = 2
    for i in np.arange(-2, 18, 0.5):
        y_lst, XTrtop_lst = grab_values(f"OP_points_no_tip\LLT\MainWing_a={i}0_v=44.00ms.txt", 30, 0)
        k += 1
        average = round(np.average(XTrtop_lst),2)
        plt.plot(np.multiply(XTrtop_lst, 0.24),y_lst,  color=colors[k])
        plot_config(f"Transition lines without tip, LLT [AOA={i} X/C ={average}]")
        save_plot(f"Transition lines without tip, LLT AOA= {i}")



    # Plots without tip, VLM
    plt.figure()
    k = 6
    for i in np.arange(-0.5, 14.5, 0.5):
        k += 1
        y_lst, XTrtop_lst = grab_values(f"OP_points_no_tip\VLM\MainWing_a={i}0_v=44.00ms.txt", 40, 536)
        average = round(np.average(XTrtop_lst), 2)
        plt.plot(np.multiply(XTrtop_lst, 0.24),y_lst,  color=colors[k])
        plot_config(f"Transition lines without tip, VLM [AOA={i} X/C ={average}]")
        save_plot(f"Transition lines without tip, VLM AOA= {i}")



    # Plots with tip, LLT
    plt.figure()
    k = 0
    for i in np.arange(-3, 19, 0.5):
        k += 1
        y_lst, XTrtop_lst = grab_values(f"OP_points_tip\LLT\MainWing_a={i}0_v=44.00ms.txt", 30, 0)
        average = round(np.average(XTrtop_lst), 2)
        plt.plot(np.multiply(XTrtop_lst, 0.24),y_lst,  color=colors[k])
        plot_config(f"Transition lines with tip, LLT [AOA={i} X/C ={average}]")
        save_plot(f"Transition lines with tip, LLT AOA= {i}")



    # Plots with tip, VLM
    plt.figure()
    k = 3
    for i in np.arange(-3, 14, 0.5):
        k += 1
        y_lst, XTrtop_lst = grab_values(f"OP_points_tip\VLM\MainWing_a={i}0_v=44.00ms.txt", 76, 1544)
        average = round(np.average(XTrtop_lst), 2)
        plt.plot(np.multiply(XTrtop_lst, 0.24),y_lst,  color=colors[k])
        plot_config(f"Transition lines with tip, VLM [AOA={i} X/C ={average}]")
        save_plot(f"Transition lines with tip, VLM AOA= {i}")


