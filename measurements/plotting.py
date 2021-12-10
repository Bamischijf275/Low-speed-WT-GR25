import os

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sb

sb.set(
    context="paper",
    style="ticks",
    font_scale=1.6,
    font="sans-serif",
    rc={
        "lines.linewidth": 1.2,
        "axes.titleweight": "bold",
    },
)


def format_plot(
    xlocator=matplotlib.ticker.AutoMinorLocator(), ylocator=matplotlib.ticker.AutoMinorLocator()
):
    fig = plt.gcf()
    for ax in fig.axes[:1]:
        ax.get_xaxis().set_minor_locator(xlocator)
        ax.get_yaxis().set_minor_locator(ylocator)

        ax.grid(b=True, which="major", linewidth=1.0)
        ax.grid(b=True, which="minor", linewidth=0.5, linestyle="-.")

    fig.tight_layout(pad=0.1, h_pad=0.4, w_pad=0.4)


def save_plot(name: str, type="pdf"):
    os.makedirs("plots", exist_ok=True)
    name = name.replace(".", "-")
    plt.savefig(
        f"plots/plot_{name}.{type}",
        dpi=300,
        bbox_inches="tight",
        pad_inches=0,
    )
    plt.close()
