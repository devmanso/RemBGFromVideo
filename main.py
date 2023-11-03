import rembgfromvideo as rembgvid
import time
import sys
import signal
import threading
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import GUI

# if __name__ == '__main__':
#
#     # get fps of video (needed for recompilation)
#
#     fps = rembgvid.get_video_fps("video_from_yt.mp4")
#     print("reading video file...")
#     # decompile video into frames
#     rembgvid.decompileVideo("video_from_yt.mp4", "decomp")
#     print("Video decompiled into output folder")
#     print("recompiling frames (single-threaded)")
#     # modify frames and store inside a new folder using parallel processing
#     rembgvid.batch_remove_background_single("decomp", "recomp")
#     print("recompilation complete, assembling video")
#     # recompile frames into a video
#     rembgvid.create_video("recomp", "recompiled.mp4", fps)
#     print("process complete, you may now safely exit")

if __name__ == "__main__":
    GUI.start()
