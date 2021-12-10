import matplotlib.pyplot as plt
import numpy as np

def grab_values(filename, skip_begin):
    """
    Function that grabs data from an XFLR5 file
    """

    # Get the useful lists of data
    y_lst = np.genfromtxt(str(filename),skip_header=skip_begin,skip_footer=0,usecols=(0,))       # Generate list of y cords
    XTrtop_lst = np.genfromtxt(str(filename),skip_header=skip_begin,skip_footer=0,usecols=(8,))       # Generate list of chord lengths

    # The last values are the actual total values! The sectional values are the lists!
    return y_lst, XTrtop_lst

plt.figure()

# for i in np.arange(-2,19,0.5):
    # y_lst, XTrtop_lst = grab_values(f"OP_points_no_tip\LLT\MainWing_a={i}.00_v=44.00ms.txt", 30)
    # plt.plot(y_lst, XTrtop_lst)

for i in np.arange(-2,19,0.5):
    y_lst, XTrtop_lst = grab_values(f"OP_points_tip\LLT\MainWing_a={i}0_v=44.00ms.txt", 30)
    plt.plot(y_lst, XTrtop_lst)


plt.show()