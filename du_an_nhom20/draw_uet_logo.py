"""Generate a clean vector-rendered UET emblem PNG for the report cover page."""
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Rectangle

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    fig, ax = plt.subplots(figsize=(2.4, 2.4), dpi=300)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect("equal")
    ax.axis("off")

    blue = "#0B4B8C"
    # Outer white/blue ring + inner solid blue circle
    outer = Circle((0, 0), 1.0, facecolor="white", edgecolor=blue, linewidth=4.0, zorder=1)
    inner = Circle((0, 0), 0.90, facecolor=blue, edgecolor=blue, linewidth=1.0, zorder=2)
    ax.add_patch(outer)
    ax.add_patch(inner)

    # Stylized white geometric motif (arc + horizontal bars inspired by UET emblem)
    arc = Wedge((-0.12, 0.15), 0.62, 65, 255, width=0.11, facecolor="white", edgecolor="none", zorder=3)
    ax.add_patch(arc)
    for idx, y_pos in enumerate([0.38, 0.24, 0.10, -0.04]):
        bar = Rectangle((-0.10, y_pos), 0.66 - idx * 0.04, 0.065, facecolor="white", edgecolor="none", zorder=3)
        ax.add_patch(bar)

    ax.text(0.14, -0.34, "ĐẠI HỌC", ha="center", va="center", fontsize=8.5, fontweight="bold", color="white", zorder=4)
    ax.text(0.14, -0.53, "CÔNG NGHỆ", ha="center", va="center", fontsize=8.5, fontweight="bold", color="white", zorder=4)

    out_path = os.path.join(OUT_DIR, "uet_logo.png")
    plt.savefig(out_path, bbox_inches="tight", transparent=True, pad_inches=0.02)
    plt.close()
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
