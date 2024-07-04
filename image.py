from io import BytesIO
import matplotlib.colors as mcolors
import math

def PIL_to_PNG(img):

    buf = BytesIO()
    img.save(buf, format="JPEG")
    byte_im = buf.getvalue()
    return byte_im


# Convert color name to RGB tuple
def color_name_to_rgb(color_name):
    try:
        rgb = mcolors.to_rgb(color_name)
        # Convert float values to integers (0-255)
        rgb = tuple(int(c * 255) for c in rgb)
        return rgb
    except ValueError:
        # Handle case where color_name is not valid
        raise ValueError(f"Invalid color name: {color_name}")

# Create a dictionary mapping RGB values to color names
rgb_to_name = {tuple(int(c * 255) for c in mcolors.to_rgb(name)): name for name in mcolors.CSS4_COLORS}

def color_distance(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

def find_closest_color_name(rgb):
    if not isinstance(rgb, tuple) or len(rgb) != 3 or not all(isinstance(c, int) and 0 <= c <= 255 for c in rgb):
        raise ValueError("RGB must be a tuple of three integers in the range 0-255")

    closest_color = min(rgb_to_name.keys(), key=lambda color: color_distance(rgb, color))
    return rgb_to_name[closest_color]