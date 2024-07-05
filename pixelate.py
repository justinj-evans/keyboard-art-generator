import streamlit as st
from PIL import Image, ImageDraw, ImageOps
from image import color_name_to_rgb, find_closest_color_name, PIL_to_PNG
from collections import Counter
import math

class ImageGridProcessor:
    def __init__(self, image_path, border_width=5, background_color='black', colors=['white','black','grey']):
        self.image_path = image_path
        self.border_width = border_width
        self.background_color = background_color
        self.colors = [color_name_to_rgb(i) for i in colors]  # Black, White, Grey - 0, 0, 0), (255, 255, 255), (128, 128, 128)
    
    def split_image_into_grid(self, grid_size):

        # Open the image
        image = Image.open(self.image_path)
        width, height = image.size
        
        height_width_min = min([width,height])
        self.square_dim = height_width_min
        
        # Calculate the size of each square
        square_width = height_width_min // grid_size
        square_height = height_width_min // grid_size
        
        # Split the image into grid squares
        grid_images = []
        for row in range(grid_size):
            for col in range(grid_size):
                left = col * square_width
                upper = row * square_height
                right = (col + 1) * square_width
                lower = (row + 1) * square_height
                grid_images.append(image.crop((left, upper, right, lower)))
        
        return grid_images, square_width, square_height
    
    @staticmethod
    def color_distance(c1, c2):
        return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5
    
    def closest_color(self, pixel):
        distances = [self.color_distance(pixel, color) for color in self.colors]
        return self.colors[distances.index(min(distances))]
    
    def convert_to_closest_color(self, grid_images):
        converted_images = []
        self.grid_color_names = []
        self.grid_colors = []

        for img in grid_images:
            # Convert image to a small thumbnail to calculate average color
            img_thumbnail = img.resize((1, 1))
            avg_color = img_thumbnail.getpixel((0, 0))[0:3]

            # Round RBG (0, 171, 0) -> (0, 170, 0) to nearest 5 value to normalize color outputs
            normalize = 5
            avg_color = tuple(5 * round(value / normalize) for value in avg_color)

            # If color list is not supplied, default to average color of grid square
            if not self.colors:
                closest = avg_color
            else:            
                # Determine the closest color from the list
                closest = self.closest_color(avg_color)
            
            # Convert RGB color to named color 
            color_name = find_closest_color_name(closest)

            # Track closest colors to summarize 
            self.grid_color_names.append(color_name)
            self.grid_colors.append(closest)

            # Create a new image with the closest color
            new_img = Image.new('RGB', img.size, closest)
            converted_images.append(new_img)
        return converted_images
    
    # Convert list to grid format
    def format_to_grid(self, flat_list):
        size = int(math.sqrt(len(flat_list)))
        grid = []
        index = 0
        for row in range(size):
            grid_row = []
            for col in range(size):
                grid_row.append((flat_list[index]))
                index += 1
            grid.append(grid_row)
        
        return grid

    def grid_color_order(self, matrix: list):
        matrix_grids = []
        for grid in matrix:
            result = []
            current_value = None
            current_count = 0

            for item in grid:
                if current_value is None:
                    current_value = item
                    current_count = 1
                elif current_value == item:
                    current_count += 1
                else:
                    result.append([current_value, current_count])
                    current_value = item
                    current_count = 1
            if current_value is not None:
                result.append([current_value, current_count])

            matrix_grids.append(result)

        return matrix_grids
    
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
        
        # Split images for conversion and return merged image
        grid_images, square_width, square_height = self.split_image_into_grid(grid_size)
        converted_images = self.convert_to_closest_color(grid_images)
        merged_image = self.remerge_grid_images(converted_images, grid_size, square_width, square_height)

        return merged_image
    
    def process_grid_colors(self):

        # Summarize grid colors
        self.grid_color_name_count = Counter(self.grid_color_names).most_common()
        self.grid_colors_count = Counter(self.grid_colors).most_common()

        # Format grid colors for export
        grid_color_matrix = self.format_to_grid(flat_list=self.grid_color_names)
        self.grid_color_matrix_count = self.grid_color_order(matrix=grid_color_matrix)






