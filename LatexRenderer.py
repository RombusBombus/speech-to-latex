from PIL import Image, ImageTk
import subprocess


def render_latex_to_image(latex_code):
    tex_file = f"temp.tex"

    latex_document = rf"""
        \documentclass[preview,border=2pt]{{standalone}}
        \usepackage{{amsmath}}
        \begin{{document}}
        {latex_code}
        \end{{document}}
    """

    with open(tex_file, "w") as f:
        f.write(latex_document)

    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", tex_file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    subprocess.run(
        ["pdftoppm", "-png", f"temp.pdf", "temp"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    img = Image.open(f"temp-1.png")
    tk_img = ImageTk.PhotoImage(img)

    return tk_img, latex_code