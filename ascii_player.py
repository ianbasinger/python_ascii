import os
import time
from colorama import Fore, init

init()

directory = r"C:\Users\ianba\Desktop\Python Projects\res"
file_prefix = "frame_"
file_extension = ".txt"
total_frames = 6577
wait_time = 1 / 30
debug = True

ascii_colors = {
	'@': Fore.CYAN,
	'%': Fore.CYAN,
	'#': Fore.CYAN,
	'*': Fore.CYAN,
	'+': Fore.CYAN,
	'=': Fore.CYAN,
	'-': Fore.CYAN,
	':': Fore.CYAN,
	'.': Fore.CYAN,
	' ': Fore.CYAN,
}

def apply_colors_to_frame(frame):
	colored_frame = ""
	for char in frame:
		colored_frame += ascii_colors.get(char, Fore.RESET) + char
	return colored_frame + Fore.RESET

def read_frame(file_path):
	try:
		with open(file_path, "r", encoding="utf-8") as f:
			return f.read()
	except FileNotFoundError:
		print(f"Error: {file_path} not found.")
		return None

def play_frames(directory, total_frames):
	for frame_number in range(1, total_frames + 1):
		file_path = os.path.join(directory, f"{file_prefix}{frame_number}{file_extension}")
		frame = read_frame(file_path)
		if frame is None:
			continue
		if debug:
			print(f"(frame: {frame_number}/{total_frames})")
		print("\033[H\033[J", end="")
		print(apply_colors_to_frame(frame))
		time.sleep(wait_time)

def main():
	print("C Project - '[Touhou] Bad Apple!! PV [Shadow] - [ASCII]'")
	input("Press Enter to start playback...")
	print(f"Total frames: {total_frames}")
	input("Press Enter to play...")
	play_frames(directory, total_frames)
	print("Animation playback completed.")

if __name__ == "__main__":
	main()