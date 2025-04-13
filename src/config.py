# src/config.py

DEFAULT_FPS = 30
BASE_RECORDING_DIR = "grabaciones"
CAMERA_DEVICE = "/dev/video0"
CAMERA_RESOLUTION = "640x480"
VIDEO_CODEC = "libx264"
AUDIO_CODEC = "aac"
FFMPEG_PRESET = "ultrafast"
DEFAULT_DISPLAY = ":0.0"
DEFAULT_VOLUME = "100%"
DATE_FORMAT = "%d-%m-%Y"

import os
from datetime import datetime

def get_recording_directory_path():
    today_str = datetime.now().strftime(DATE_FORMAT)
    final_dir = os.path.join(BASE_RECORDING_DIR, today_str)
    os.makedirs(final_dir, exist_ok=True)
    return final_dir
