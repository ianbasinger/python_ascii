import time
import shutil
import cv2
from PIL import Image
import os
import random
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init, Style
import sys

init()

vid_dir = input("Enter the video file path").strip()
out_dir = input("Enter the output directory path").strip()
os.makedirs(out_dir, exist_ok=True)
resolution = input("Select resolution (low, medium, high, or custom up to 200): ").strip().lower()
ascii_chars = input("Enter a custom ASCII character set (default is '@ '): ") or "@ "
random_colors = input("Enable random ASCII colors? (y/n): ").strip().lower() == 'y'
dbug = input("Enable debug mode? (y/n): ").strip().lower() == 'y'

color_options = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
ascii_colors = {char: random.choice(color_options) for char in ascii_chars} if random_colors else {char: Fore.CYAN for char in ascii_chars}
f_cached = []

def term_width():
    try:
        return shutil.get_terminal_size().columns
    except OSError:
        return 80

terminal_width = term_width()
frame_width = terminal_width

if resolution == "low":
    frame_width = min(40, terminal_width)
elif resolution == "medium":
    frame_width = min(80, terminal_width)
elif resolution == "high":
    frame_width = min(120, terminal_width)
else:
    try:
        frame_width = int(resolution)
        if frame_width < 1 or frame_width > terminal_width:
            raise ValueError
    except ValueError:
        print("Invalid custom resolution value. Using default resolution (80).")
        frame_width = min(80, terminal_width)

frame_data = {"processed": 0, "errors": 0}

def to_ascii(image, width):
    image = image.convert("L")
    aspect_ratio = image.height / image.width
    new_height = int(aspect_ratio * width * 0.55)
    image = image.resize((width, new_height))
    ascii_art = []
    for pixel in image.getdata():
        char = ascii_chars[min(len(ascii_chars) - 1, pixel // 25)]
        colored_char = ascii_colors.get(char, "") + char + Style.RESET_ALL
        ascii_art.append(colored_char)
    ascii_art = '\n'.join([''.join(ascii_art[i:i + width]) for i in range(0, len(ascii_art), width)])
    return ascii_art

def progress(current, total):
    bar_length = 50
    progress = int(bar_length * (current / total))
    bar = f"[{'=' * progress}{' ' * (bar_length - progress)}] {current}/{total} frames"
    sys.stdout.write(f"\r{bar}")
    sys.stdout.flush()

def f_proc(frame_number, frame):
    try:
        frame_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        ascii_frame = to_ascii(frame_image, frame_width)
        f_cached.append(ascii_frame)
        frame_data["processed"] += 1
        if dbug:
            print(f"\nFrame {frame_number} processed successfully.")
    except Exception as e:
        frame_data["errors"] += 1
        if dbug:
            print(f"\nError processing frame {frame_number}: {e}")

def anim(f_cached):
    frame_interval = 1 / 24  # Adjust frame rate here (e.g., 24 FPS)
    for frame in f_cached:
        sys.stdout.write("\033[H")  # Move cursor to the top
        sys.stdout.write(frame)
        sys.stdout.flush()
        time.sleep(frame_interval)

def main():
    if not os.path.isfile(vid_dir):
        print("Error: Video file not found. Check the path and try again!")
        return

    cap = cv2.VideoCapture(vid_dir)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames <= 0:
        print("Error: No frames detected in the video. Ensure the video is valid...")
        return

    print(f"Total Frames: {total_frames}")

    with ThreadPoolExecutor() as executor:
        for frame_number in range(total_frames):
            ret, frame = cap.read()
            if not ret:
                break
            executor.submit(f_proc, frame_number + 1, frame)
            if not dbug:
                progress(frame_number + 1, total_frames)

    cap.release()
    if not dbug:
        print("\nProcessing is complete!")
    print(f"Summary:\n- Total frames processed: {frame_data['processed']}\n- Errors: {frame_data['errors']}")

    if f_cached:
        input("Press enter to play the animation...")
        anim(f_cached)
    else:
        print("No frames were processed. Please check the input video and settings.")

if __name__ == "__main__":
    main()
