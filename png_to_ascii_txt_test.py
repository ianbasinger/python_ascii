from PIL import Image

ascii_chars = "@%#*+=-:. "
frame_path = r"%inputpath%\frame_94.png" 

def image_to_ascii(image, width):
    """Convert an image to ASCII art."""
    image = image.convert("L")
    aspect_ratio = image.height / image.width
    new_height = int(aspect_ratio * width * 0.55)
    image = image.resize((width, new_height))

    ascii_art = ""
    for pixel in image.getdata():
        pixel = max(0, min(255, pixel))
        ascii_art += ascii_chars[min(len(ascii_chars) - 1, pixel // 25)]

    ascii_art = '\n'.join(
        [ascii_art[i:i+width] for i in range(0, len(ascii_art), width)]
    )
    return ascii_art

image = Image.open(frame_path)
ascii_result = image_to_ascii(image, 80)
print(ascii_result)
