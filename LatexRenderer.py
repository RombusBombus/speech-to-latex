import matplotlib.pyplot as plt
import io
from PIL import Image, ImageTk


def render_latex_to_image(latex_code):
    # strip the \[ and \] from the latex result
    if latex_code.startswith("\\[") and latex_code.endswith("\\]"):
        latex_code = latex_code[2:-2].strip()

    plt.rcParams['text.usetex'] = True
    fig = plt.figure()
    plt.text(0.5, 0.5, f"${latex_code}$", fontsize=20, ha='center', va='center')
    plt.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)
    buf.seek(0)
    img = Image.open(buf)
    img = ImageTk.PhotoImage(img)

    return img, latex_code