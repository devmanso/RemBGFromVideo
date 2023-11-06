import tkinter as tk

from rembg import new_session
from tkinterdnd2 import TkinterDnD, DND_FILES
import rembgfromvideo as rembgvid
import onnxruntime as ort

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Remove Background from video")

        # Create a canvas for the rectangle (drop region)
        self.canvas = tk.Canvas(root, width=600, height=600, bg="lightgray")
        self.canvas.pack(padx=10, pady=10)

        # Register the canvas for drag-and-drop functionality
        self.canvas.drop_target_register(DND_FILES)
        self.canvas.dnd_bind('<<Drop>>', self.handle_drop)
        text = "DROP A VIDEO HERE"
        font_size = 30
        self.canvas.create_text(
            self.canvas.winfo_reqwidth() / 2,
            self.canvas.winfo_reqheight() / 2,
            text=text,
            font=("Arial", font_size, "bold"),
            fill="blue"
        )

    def handle_drop(self, event):
        # Get the file path from the dropped data
        file_path = event.data

        text = "STARTING"
        font_size = 30
        self.canvas.create_text(
            self.canvas.winfo_reqwidth() / 2,
            self.canvas.winfo_reqheight() / 2,
            text=text,
            font=("Arial", font_size, "bold"),
            fill="blue"
        )
        # Check if the dropped file is a video file (you may need to add more file types)
        if file_path.lower().endswith(('.mp4', '.avi', '.mkv')):
            print(f"Video file dropped: {file_path}")

            text = f"Video file dropped: {file_path}"
            font_size = 30
            self.canvas.create_text(
                self.canvas.winfo_reqwidth() / 2,
                self.canvas.winfo_reqheight() / 2,
                text=text,
                font=("Arial", font_size, "bold"),
                fill="blue"
            )

            fps = rembgvid.get_video_fps(file_path)
            print("decompiling video...")

            text = "decompiling video..."
            font_size = 30
            self.canvas.create_text(
                self.canvas.winfo_reqwidth() / 2,
                self.canvas.winfo_reqheight() / 2,
                text=text,
                font=("Arial", font_size, "bold"),
                fill="blue"
            )

            # decompile video into frames
            rembgvid.decompile_video(file_path, "decomp")
            print("Video decompiled into output folder")

            text = "Video decompiled into output folder"
            font_size = 30
            self.canvas.create_text(
                self.canvas.winfo_reqwidth() / 2,
                self.canvas.winfo_reqheight() / 2,
                text=text,
                font=("Arial", font_size, "bold"),
                fill="blue"
            )

            print("recompiling frames (multi-threaded)")

            text = "recompiling frames (multi-threaded)"
            font_size = 30
            self.canvas.create_text(
                self.canvas.winfo_reqwidth() / 2,
                self.canvas.winfo_reqheight() / 2,
                text=text,
                font=("Arial", font_size, "bold"),
                fill="blue"
            )

            # modify frames and store inside a new folder using parallel processing
            # rembgvid.process_images_parallel("decomp", "recomp", threads=12)
            onnx_model_path = 'models/u2net.onnx'
            session = ort.InferenceSession(onnx_model_path, providers=['CUDAExecutionProvider'])

            rembgvid.process_images_gpu("decomp", "recomp", session)
            print("recompilation complete, assembling video")

            text = "recompilation complete, assembling video"
            font_size = 30
            self.canvas.create_text(
                self.canvas.winfo_reqwidth() / 2,
                self.canvas.winfo_reqheight() / 2,
                text=text,
                font=("Arial", font_size, "bold"),
                fill="blue"
            )

            # recompile frames into a video
            rembgvid.create_video("recomp", "recompiled.mp4", fps)
            print("process complete, you may now safely exit")

            text = "process complete, you may now safely exit"
            font_size = 30
            self.canvas.create_text(
                self.canvas.winfo_reqwidth() / 2,
                self.canvas.winfo_reqheight() / 2,
                text=text,
                font=("Arial", font_size, "bold"),
                fill="blue"
            )




def start():
    root = TkinterDnD.Tk()
    app = GUI(root)
    root.mainloop()