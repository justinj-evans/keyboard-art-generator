import streamlit as st
from PIL import Image, ImageOps
from pixelate import ImageGridProcessor
from image import PIL_to_PNG

# # Streamlit app
st.title("Keyboard Art Generator")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# SideBar
# Dropdowns
colors = st.sidebar.multiselect("Standard KeyBoard Colors",options=['black','white','grey'],default=[],                             help='Leave blank to default to average color')
grid_size = st.sidebar.slider("Number of Keys (width)", min_value=10, max_value=100, value=10, step=5)

# Process Image
if uploaded_file is not None:
    pixelater = ImageGridProcessor(image_path=uploaded_file, colors=colors)
else:
    image = r'image/python.PNG'
    pixelater = ImageGridProcessor(image_path=image, colors=colors)

pixelated_image = pixelater.process_and_display(grid_size=grid_size)
pixelater.process_grid_colors()
grid_color_matrix_count_export = '\n'.join(str(row) for row in pixelater.grid_color_matrix_count)

# Metrics
m1, m2 = st.columns(2,gap='small')
with m1: st.metric(label='Keys', value=grid_size*grid_size)
with m2: st.metric(label='Colors', value=len(pixelater.grid_colors_count))

# Display Grid Color Counts in a row
color_grids = 10
cols = st.columns(len(pixelater.grid_colors_count[0:color_grids]), gap='small')
for i, (color, count) in enumerate(pixelater.grid_colors_count[0:color_grids][0:color_grids]):
    with cols[i]:
        image = Image.new('RGB', size=(50, 50), color=color)
        # Add a black border
        border_color = (0, 0, 0)
        border_size = 1  # Change this value to adjust the border size
        image_with_border = ImageOps.expand(image, border=border_size, fill=border_color)
        st.image(image_with_border,width=50, caption=f'x {count}')

# Display Pixelated Image
st.image(pixelated_image, caption='Pixelated image', use_column_width=True)

# Download Button - Export Instructions
d1, d2 = st.columns(2,gap='small')
with d1: st.download_button(label='Download - Pixelated Image',data=PIL_to_PNG(pixelated_image), file_name='pixelated_image.png',mime='image/png')
with d2: st.download_button(label='Download - Pixelated Grid Instructions',data=grid_color_matrix_count_export, file_name='grid_color_order.txt',mime="text/plain")
