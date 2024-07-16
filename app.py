import streamlit as st
from PIL import Image, ImageOps
from pixelate import ImageGridProcessor
from image import PIL_to_PNG

# # Streamlit app
st.title("Keyboard Art Generator")

# Example
with st.expander('Example'):
    e1, e2, e3, e4, e5 = st.columns(5,gap='large')
    with e1: st.image("docs/landscape.PNG",width=100, caption='Choose an Image')
    with e2: st.image("docs/inputs.PNG",width=100, caption='Select Inputs')
    with e3: st.image("docs/landscape-keyboard-generator.PNG",width=100, caption='Pixelate Your Image')
    with e4: st.image("docs/keyboard.PNG",width=100, caption='Recycle Keycaps from Keyboard')
    with e5: st.image("docs/landscape-keys.PNG",width=100, caption='Keyboard Artwork')

# Upload image
container = st.container(border=True)
uploaded_file = container.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# SideBar
# Dropdowns
st.sidebar.title("Select Inputs")
colors = st.sidebar.multiselect("Standard Keyboard Colors",options=['black','white','grey'],default=[],                             help='Leave blank to default to average color')
grid_size = st.sidebar.slider("Keycap Width", min_value=10, max_value=100, value=10, step=5)

# Process Image
with st.container(border=True):

    if uploaded_file is not None:
        pixelater = ImageGridProcessor(image_path=uploaded_file, colors=colors)
    else:
        image = 'image/python.PNG'
        pixelater = ImageGridProcessor(image_path=image, colors=colors)

    pixelated_image = pixelater.process_and_display(grid_size=grid_size)
    pixelater.process_grid_colors()
    grid_color_matrix_count_export = '\n'.join(str(row) for row in pixelater.grid_color_matrix_count)

    # Metrics
    m1, m2, m3 = st.columns(3,gap='large')
    with m1: st.metric(label='Grid Keys', value=grid_size*grid_size)
    with m2: st.metric(label='Colors', value=len(pixelater.grid_colors_count))
    with m3: st.metric(label="Width (inches)", value=(grid_size*0.75))

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
