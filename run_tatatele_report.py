import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def generate_tatatele_image(landed, answered, missed):
    fig, ax = plt.subplots(figsize=(8, 1.4), dpi=300)
    ax.axis('off')

    # Draw table for 2 rows: Header & Data
    cell_text = [
        ["Agent", "Landed Call", "Answered", "Missed"],
        ["Amaresh Kumar & Soumyajith", str(landed), str(answered), str(missed)]
    ]

    cell_colors = [
        ["#FCE5CD"]*4,
        ["#FFFFFF"]*4
    ]

    table = ax.table(
        cellText=cell_text,
        cellColours=cell_colors,
        cellLoc='center',
        colWidths=[0.46, 0.18, 0.18, 0.18],
        loc='bottom',
        bbox=[0, 0, 1.0, 0.62]
    )

    table.auto_set_font_size(False)
    table.set_fontsize(13)

    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor('black')
        cell.set_linewidth(1.5)
        if r == 0:
            cell.get_text().set_weight('bold')

    # Draw single merged grey header box at top
    rect = patches.Rectangle((0, 0.62), 1.0, 0.38, facecolor='#C0C0C0', edgecolor='black', linewidth=1.5, transform=ax.transAxes)
    ax.add_patch(rect)

    # Place single centered "Lux" text
    ax.text(0.5, 0.81, "Lux", fontsize=15, fontweight='bold', ha='center', va='center', transform=ax.transAxes)

    plt.tight_layout()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "tatatele_lux_report.png")
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()

    return image_path

if __name__ == "__main__":
    generate_tatatele_image(19, 12, 7)
