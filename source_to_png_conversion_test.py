import cv2
from PIL import Image

video_path = r"%inputpath%"
cap = cv2.VideoCapture(video_path)

output_dir = r"%outputpath%"
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

if not cap.isOpened():
    print("Error: Unable to open video file.")
    exit()

for i in range(100):  # Save the first 10 frames
    ret, frame = cap.read()
    if not ret:
        print(f"Error: Could not read frame {i + 1}")
        break
    
    frame_path = f"{output_dir}/frame_{i + 1}.png"
    Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).save(frame_path)
    print(f"Saved frame {i + 1} to {frame_path}")

cap.release()
