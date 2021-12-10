import matplotlib.pyplot as plt
import numpy as np




def grab_values(filename, skip_begin, skip_end):
    """
    Function that grabs data from an XFLR5 file
    """

    # Get the useful lists of data
    y_lst = np.genfromtxt(str(filename),skip_header=skip_begin,skip_footer=skip_end,usecols=(0,))       # Generate list of y cords
    XTrtop_lst = np.genfromtxt(str(filename),skip_header=skip_begin,skip_footer=skip_end,usecols=(8,))       # Generate list of chord lengths

    # The last values are the actual total values! The sectional values are the lists!
    return y_lst, XTrtop_lst

# Plots without tip, LLT
plt.figure()

for i in np.arange(-3,19,0.5):
    y_lst, XTrtop_lst = grab_values(f"OP_points_tip\LLT\MainWing_a={i}0_v=44.00ms.txt", 30, 0)
    plt.plot(y_lst, XTrtop_lst)
    plt.ylim(-0.05, 0.3)
plt.plot((0,0),(0,0.24),linewidth = 6, color = "black")
plt.plot((0,0.64),(0.24,0.24),linewidth = 6,color = "black")
plt.plot((0.64,0.64),(0.24,0),linewidth = 6,color = "black")
plt.plot((0.64,0),(0.0,0.0),linewidth = 6,color = "black")
plt.title("Transition lines without tip, LLT")
plt.show()

# Plots without tip, VLM
plt.figure()

for i in np.arange(-3,19,0.5):
    y_lst, XTrtop_lst = grab_values(f"OP_points_tip\LLT\MainWing_a={i}0_v=44.00ms.txt", 30, 0)
    plt.plot(y_lst, XTrtop_lst)
    plt.ylim(-0.05, 0.3)
plt.plot((0,0),(0,0.24),linewidth = 6, color = "black")
plt.plot((0,0.64),(0.24,0.24),linewidth = 6,color = "black")
plt.plot((0.64,0.64),(0.24,0),linewidth = 6,color = "black")
plt.plot((0.64,0),(0.0,0.0),linewidth = 6,color = "black")
plt.title("Transition lines without tip, LLT")
plt.show()

# Plots with tip, LLT
plt.figure()

for i in np.arange(-3,19,0.5):
    y_lst, XTrtop_lst = grab_values(f"OP_points_tip\LLT\MainWing_a={i}0_v=44.00ms.txt", 30, 0)
    plt.plot(y_lst, np.multiply(XTrtop_lst,0.24))
    plt.ylim(-0.05, 0.3)

plt.plot((0,0),(0,0.24),linewidth = 6, color = "black")
plt.plot((0,0.64),(0.24,0.24),linewidth = 6,color = "black")
plt.plot((0.64,0.64),(0.24,0),linewidth = 6,color = "black")
plt.plot((0.64,0),(0.0,0.0),linewidth = 6,color = "black")
plt.title("Transition lines with tip, LLT")
plt.show()

# Plots with tip, VLM
plt.figure()

for i in np.arange(-3,14,0.5):
    y_lst, XTrtop_lst = grab_values(f"OP_points_tip\VLM\MainWing_a={i}0_v=44.00ms.txt", 76, 1544)
    plt.plot(y_lst, np.multiply(XTrtop_lst, 0.24))
    plt.ylim(-0.05, 0.3)
plt.plot((0,0),(0,0.24),linewidth = 6, color = "black")
plt.plot((0,0.64),(0.24,0.24),linewidth = 6,color = "black")
plt.plot((0.64,0.64),(0.24,0),linewidth = 6,color = "black")
plt.plot((0.64,0),(0.0,0.0),linewidth = 6,color = "black")
plt.title("Transition lines with tip, VLM")
plt.show()
