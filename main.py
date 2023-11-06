import GUI
import torch
import onnxruntime as ort
import rembgfromvideo as rembgvid
from pathlib import Path


if __name__ == "__main__":
    print("TORCH CUDA TEST")
    print(torch.cuda.is_available())

    print(torch.cuda.current_device())

    print(torch.cuda.get_device_name(0))

    onnx_model_path = 'models/u2net.onnx'
    session = ort.InferenceSession(onnx_model_path, providers=['CUDAExecutionProvider'])
    provider = session.get_providers()
    fps = rembgvid.get_video_fps("video_from_yt.mp4")
    rembgvid.decompile_video("video_from_yt.mp4", "decomp")

    rembgvid.process_images_gpu_test("decomp", "recomp", provider)
    rembgvid.create_video("recomp", "recompiled.mp4", fps)
    #GUI.start()
