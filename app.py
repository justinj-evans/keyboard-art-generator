import streamlit as st
from PIL import Image
from pixelate import ImageGridProcessor
from image import PIL_to_PNG

# # Streamlit app
st.title("Image Grid Processor")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# SideBar
# Dropdowns
colors = st.sidebar.multiselect("Standard KeyBoard Colors",options=['black','white','grey'],default=[],                             help='Leave blank to default to average color')
grid_size = st.sidebar.slider("Number of Keys (width)", min_value=10, max_value=100, value=10, step=5)

# Process Image
if uploaded_file is not None:
    #image = Image.open(uploaded_file)
    # Display uploaded image
    #st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Parameters
    grid_size_inches = 0.75  # Size of each grid in inches
    border_width = 5  # Width of the border between squares
    background_color = 'black'  # Background color ('white' or 'black')
    
    pixelater = ImageGridProcessor(image_path=uploaded_file, colors=colors)
    pixelated_image = pixelater.process_and_display(grid_size=grid_size)
    st.image(pixelated_image, caption='Pixelated image')

else:
    image = r'image/python.PNG'
    pixelater = ImageGridProcessor(image_path=image, colors=colors)
    pixelated_image = pixelater.process_and_display(grid_size=grid_size)
    st.image(pixelated_image, caption='Pixelated image')


# Download Button - Export Instructions
st.download_button(label='Download - Pixelated Image',data=PIL_to_PNG(pixelated_image), file_name='pixelated_image.png',mime='image/png')