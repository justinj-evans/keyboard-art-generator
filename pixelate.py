import streamlit as st
from PIL import Image, ImageDraw, ImageOps

class ImageGridProcessor:
    def __init__(self, image, dpi=300, grid_size_inches=0.75, border_width=5, background_color='black'):
        self.image = image
        self.dpi = dpi
        self.grid_size_inches = grid_size_inches
        self.border_width = border_width
        self.background_color = background_color
        self.colors = [(0, 0, 0), (255, 255, 255), (128, 128, 128)]  # Black, White, Grey
    
    def split_image_into_grid(self, grid_size):
        # Open the image
        width, height = self.image.size
        
        # Calculate the size of each square in pixels
        square_size_pixels = int(self.grid_size_inches * self.dpi)
        
        # Split the image into grid squares
        grid_images = []
        for row in range(grid_size):
            for col in range(grid_size):
                left = col * square_size_pixels
                upper = row * square_size_pixels
                right = left + square_size_pixels
                lower = upper + square_size_pixels
                grid_images.append(self.image.crop((left, upper, right, lower)))
        
        return grid_images, square_size_pixels, square_size_pixels
    
    @staticmethod
    def color_distance(c1, c2):
        return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5
    
    def closest_color(self, pixel):
        distances = [self.color_distance(pixel, color) for color in self.colors]
        return self.colors[distances.index(min(distances))]
    
    def convert_to_closest_color(self, grid_images):
        converted_images = []
        for img in grid_images:
            # Convert image to a small thumbnail to calculate average color
            img_thumbnail = img.resize((1, 1))
            avg_color = img_thumbnail.getpixel((0, 0))
            
            # Determine the closest color from the list
            closest = self.closest_color(avg_color)
            
            # Create a new image with the closest color
            new_img = Image.new('RGB', img.size, closest)
            converted_images.append(new_img)
        return converted_images
    
    def remerge_grid_images(self, grid_images, grid_size, square_width, square_height):
        # Calculate the size of the new image
        new_width = grid_size * (square_width + self.border_width) + self.border_width
        new_height = grid_size * (square_height + self.border_width) + self.border_width
        
        # Create a new image with the specified background color
        new_image = Image.new('RGB', (new_width, new_height), self.background_color)
        
        # Paste the grid images into the new image with the border
        for index, img in enumerate(grid_images):
            row = index // grid_size
            col = index % grid_size
            left = col * (square_width + self.border_width) + self.border_width
            upper = row * (square_height + self.border_width) + self.border_width
            new_image.paste(img, (left, upper))
        
        return new_image
    
    def process_and_display(self, grid_size):
        grid_images, square_width, square_height = self.split_image_into_grid(grid_size)
        converted_images = self.convert_to_closest_color(grid_images)
        merged_image = self.remerge_grid_images(converted_images, grid_size, square_width, square_height)
        
        # Display the merged image
        st.image(merged_image)
        
        # Print the size of each grid image in inches
        st.write(f"Each grid image size: {self.grid_size_inches} inches x {self.grid_size_inches} inches")

# Streamlit app
st.title("Image Grid Processor")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Display uploaded image
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Parameters
    dpi = 300  # Dots per inch
    grid_size_inches = 0.75  # Size of each grid in inches
    border_width = 5  # Width of the border between squares
    background_color = 'black'  # Background color ('white' or 'black')
    
    # Grid size slider
    grid_size = st.slider("Grid Size", min_value=2, max_value=10, value=4, step=1)
    
    processor = ImageGridProcessor(image, dpi, grid_size_inches, border_width, background_color)
    processor.process_and_display(grid_size)

