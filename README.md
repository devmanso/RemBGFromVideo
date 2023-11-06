# RemBGFromVideo
A tool to remove backgrounds from videos, WIP

THIS IS A WORK-IN-PROGRESS

## Requirements
- opencv-python
- rembg
- pathlib
- tkinter
- tkintertable
- tkinterdnd2

## Benchmarks

### Relevant System specs
- RAM: 16gb DDR4 2666mhz
- CPU: i7-9750h 6 core 12 threads
- GPU: GTX 1650 4gb

### Video details
- 240p video ripped from YouTube
- mpeg4 format
- 2372 frames
- 1-min, 34-second video
- Description: an angry newsman loses his mind in front of the camera

### Dedicated Graphics Card
- 3 min, 38 seconds
- very minimal GPU usage, too negligable to be noticed in task manager
- 

### Multithreaded
- 12 min, 46.120 seconds
- 100 percent CPU usage, using 12 threads among 6 cores
- 5Gb memory usage

(second test, this time I cleaned out my laptop to prevent thermal throttling)
- ~5 minutes
- 40-70% percent CPU usage, using 12 threads among 6 cores
- 2Gb memory usage

### Single-threaded
- 22 minutes and 36.893 seconds
- 45 to 70 percent CPU usage
- 800 to 900mb memory usage