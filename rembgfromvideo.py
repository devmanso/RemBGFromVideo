import cv2
import os
import onnxruntime as ort
import numpy as np
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


def decompile_video(video_path, output_folder):
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


# tbh IDK what I did here
# def process_image_gpu(input_path, output_path, session):
#     # Read the input image
#     with open(input_path, "rb") as input_file:
#         input_data = input_file.read()
#
#     # Use Rembg library with GPU support to remove the background
#     input_array = np.frombuffer(input_data, dtype=np.uint8)
#     input_array = input_array.reshape((1, len(input_array)))
#     output_array = session.run([], {"input": input_array.astype(np.float32)})[0]
#
#     # Save the result to the output file
#     with open(output_path, "wb") as output_file:
#         output_file.write(output_array.tobytes())
#
#     print("RECOMPILED FRAME")
#
#
# def initialize_onnx_session():
#     # Provide the path to the ONNX model file for GPU
#     onnx_model_path = "path/to/your/rembg_gpu_model.onnx"
#
#     # Create an ONNX Runtime session with GPU support
#     options = onnxruntime.SessionOptions()
#     options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_EXTENDED
#     options.execution_mode = onnxruntime.ExecutionMode.ORT_SEQUENTIAL
#     providers = ['CUDAExecutionProvider']
#     session = onnxruntime.InferenceSession(onnx_model_path, providers=providers, sess_options=options)
#
#     return session

def process_image(file, input_folder, output_folder, session):
    input_path = str(file)
    output_filename = f"{file.stem}.jpg"
    output_path = os.path.join(output_folder, output_filename)

    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input_data = i.read()
            output_data = remove(input_data, session=session)
            o.write(output_data)


def process_image_gpu(file, output_folder, session):
    input_path = str(file)
    output_filename = f"{file.stem}.jpg"
    output_path = os.path.join(output_folder, output_filename)

    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input_data = i.read()

            # Use onnxruntime for GPU acceleration
            input_array = np.frombuffer(input_data, dtype=np.uint8)
            input_array = cv2.imdecode(input_array, cv2.IMREAD_COLOR)
            input_array = cv2.cvtColor(input_array, cv2.COLOR_BGR2RGB)
            input_array = input_array.astype(np.float32) / 255.0  # Normalize pixel values
            input_array = cv2.resize(input_array, (320, 320))  # Resize to match expected dimensions
            input_array = np.transpose(input_array, (2, 0, 1))  # Transpose to (3, 320, 320)
            input_array = np.expand_dims(input_array, axis=0)  # Add batch dimension
            input_tensor = session.get_inputs()[0].name
            output = session.run(None, {input_tensor: input_array})

            o.write(output[0].tobytes())


def process_images_gpu(input_folder, output_folder, session):
    # Create the output folder if it doesn't exist
    if not Path(output_folder).exists():
        Path(output_folder).mkdir()

    # Iterate through every jpg file in the input folder
    for file_path in Path(input_folder).glob('*.jpg'):
        process_image_gpu(file_path, output_folder, session)


def process_images_parallel(input_folder, output_folder, threads=12):
    session = new_session()

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        print("OUTPUT DIR NOT FOUND, MAKING OUTPUT DIR")
        os.makedirs(output_folder)

    files = list(Path(input_folder).glob('*.jpg'))

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(lambda file: process_image(file, input_folder, output_folder, session), files)

    print("RECOMPILATION COMPLETE")


def process_images_single(input_folder, output_folder):
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
