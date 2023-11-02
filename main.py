import rembgfromvideo as rembgvid

if __name__ == '__main__':
    # get fps of video (needed for recompilation)
    fps = rembgvid.get_video_fps("video_from_yt.mp4")

    # decompile video into frames
    rembgvid.decompileVideo("video_from_yt.mp4", "decomp")

    # modify frames and store inside a new folder using parallel processing
    rembgvid.batch_remove_background_single_better("decomp", "recomp")

    # recompile frames into a video
    rembgvid.create_video("recomp", "recompiled.mp4", fps)