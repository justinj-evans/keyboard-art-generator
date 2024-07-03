from io import BytesIO

def PIL_to_PNG(img):

    buf = BytesIO()
    img.save(buf, format="JPEG")
    byte_im = buf.getvalue()
    return byte_im


import matplotlib.colors as mcolors

def color_name_to_rgb(color_name):
    # Convert color name to RGB tuple
    try:
        rgb = mcolors.to_rgb(color_name)
        # Convert float values to integers (0-255)
        rgb = tuple(int(c * 255) for c in rgb)
        return rgb
    except ValueError:
        # Handle case where color_name is not valid
        raise ValueError(f"Invalid color name: {color_name}")