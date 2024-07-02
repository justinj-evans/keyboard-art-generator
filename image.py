from PIL import Image

def split_image_into_grid(image_path, grid_size):
    # Open the image
    image = Image.open(image_path)
    width, height = image.size

    height_width_min = min([width,height])
    
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


def remerge_grid_images(grid_images, grid_size, square_width, square_height, border_width, background_color):
    # Calculate the size of the new image
    new_width = grid_size * (square_width + border_width) + border_width
    new_height = grid_size * (square_height + border_width) + border_width
    
    # Create a new image with the specified background color
    new_image = Image.new('RGB', (new_width, new_height), background_color)
    
    # Paste the grid images into the new image with the border
    for index, img in enumerate(grid_images):
        row = index // grid_size
        col = index % grid_size
        left = col * (square_width + border_width) + border_width
        upper = row * (square_height + border_width) + border_width
        new_image.paste(img, (left, upper))
    
    return new_image