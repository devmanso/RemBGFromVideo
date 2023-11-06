import GUI
import torch
import onnxruntime as ort
import rembgfromvideo as rembgvid
from pathlib import Path

if __name__ == "__main__":

    print(torch.cuda.is_available())

    print(torch.cuda.current_device())

    print(torch.cuda.get_device_name(0))

    onnx_model_path = 'models/u2net.onnx'
    session = ort.InferenceSession(onnx_model_path, providers=['CUDAExecutionProvider'])

    # # Specify input and output folders
    # input_folder = "decomp"
    # output_folder = "test"

    # # Create the output folder if it doesn't exist
    # if not Path(output_folder).exists():
    #     Path(output_folder).mkdir()
    #
    # # Iterate through every jpg file in the input folder
    # for file_path in Path(input_folder).glob('*.jpg'):
    #     rembgvid.process_image_gpu(file_path, output_folder, session)
    #GUI.start()
