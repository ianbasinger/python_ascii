import cv2
from PIL import Image
import os

# Parameters
video_path = r"%inputpath%"
output_dir = r"%inputpath%"
ascii_chars = "@%#*+=-:. "
frame_width = 80  # Width of ASCII output

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

def image_to_ascii(image, width):
    """Convert an image to ASCII art."""
    image = image.convert("L")  # Convert to grayscale
    aspect_ratio = image.height / image.width
    new_height = int(aspect_ratio * width * 0.55)
    image = image.resize((width, new_height))

    ascii_art = ""
    for pixel in image.getdata():
        pixel = max(0, min(255, pixel))  # Clamp pixel values
        ascii_art += ascii_chars[min(len(ascii_chars) - 1, pixel // 25)]

    ascii_art = '\n'.join(
        [ascii_art[i:i+width] for i in range(0, len(ascii_art), width)]
    )
    return ascii_art

# Process video
cap = cv2.VideoCapture(video_path)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"Total Frames: {frame_count}")

current_frame = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame (BGR to RGB)
    frame_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    try:
        # Convert frame to ASCII
        ascii_frame = image_to_ascii(frame_image, frame_width)

        # Save ASCII art to a text file
        output_file = os.path.join(output_dir, f"frame_{current_frame + 1}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(ascii_frame)
        print(f"Processed Frame {current_frame + 1}/{frame_count}")
    except Exception as e:
        print(f"Error processing frame {current_frame + 1}: {e}")
        continue

    current_frame += 1

cap.release()
print("All frames processed and saved.")
