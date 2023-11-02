import cv2
import os
import rembg
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from rembg import new_session, remove


def get_video_fps(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get the frames per second (fps) of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Release the video capture object
    cap.release()

    return fps


def decompileVideo(video_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Processing {total_frames} frames at {fps} frames per second.")

    # Read and save each frame
    for frame_num in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break

        # Save the frame as an image file
        frame_filename = os.path.join(output_folder, f"frame_{frame_num:04d}.jpg")
        cv2.imwrite(frame_filename, frame)

    # Release the video capture object
    cap.release()

    print("Frames extraction completed.")


def remove_background_parallel(input_path, output_path):
    with open(input_path, "rb") as input_file:
        input_data = input_file.read()

    # Use rembg library to remove the background
    output_data = rembg.remove(input_data)

    # Save the result to the output file
    with open(output_path, "wb") as output_file:
        output_file.write(output_data)

    print("RECOMPILED FRAME")


# THIS ONE WORKS BUT IS VERY SLOW
def batch_remove_background_parallel(input_folder, output_folder, num_threads=4):
    count = 0
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        print("RECOMP DIR NOT FOUND, MAKING RECOMP DIR")
        os.makedirs(output_folder)

    # Remove background in parallel
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for filename in os.listdir(input_folder):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, filename)

                # Remove background and save the edited image
                executor.submit(remove_background_parallel, input_path, output_path)
                count += 1
                print(f"RECOMPILED FRAMES COUNT {count}")

    print("RECOMPILATION COMPLETE")


def batch_remove_background_single(input_folder, output_folder):
    session = new_session()

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        print("OUTPUT DIR NOT FOUND, MAKING OUTPUT DIR")
        os.makedirs(output_folder)

    for file in Path(input_folder).glob('*.jpg'):
        input_path = str(file)
        output_filename = f"{file.stem}.jpg"  # Corrected extension to .jpg
        output_path = os.path.join(output_folder, output_filename)

        with open(input_path, 'rb') as i:
            with open(output_path, 'wb') as o:
                input_data = i.read()
                output_data = remove(input_data, session=session)
                o.write(output_data)

    print("RECOMPILATION COMPLETE")


def create_video(input_folder, output_video, fps=30.0):
    # Get the list of image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # Sort the image files based on their names
    image_files.sort()

    # Get the first image to determine the dimensions of the video
    first_image = cv2.imread(os.path.join(input_folder, image_files[0]))
    height, width, _ = first_image.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can try other codecs like 'XVID' or 'MJPG'
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    # Write each image to the video file
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        frame = cv2.imread(image_path)
        video_writer.write(frame)

    # Release the VideoWriter object
    video_writer.release()

    print(f"Video '{output_video}' created successfully.")

