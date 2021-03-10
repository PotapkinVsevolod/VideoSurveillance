import os
import sys
import unittest
from datetime import datetime

from cv2 import VideoCapture, VideoWriter

sys.path.append(os.path.join(os.getcwd(), '..'))

from camera_opencv import Camera


# CAMERA_URL = 'rtsp://admin:@192.168.1.10'
CAMERA_URL = 'test_url'
CAMERA_FPS = 25.0
VIDEO_LENGTH = 60
VIDEO_DIRECTORY = 'test_directory'


class TestCamera(unittest.TestCase):
    def setUp(self) -> None:
        self.camera = Camera(
            url=CAMERA_URL,
            fps=CAMERA_FPS,
            length_of_video=VIDEO_LENGTH,
            directory=VIDEO_DIRECTORY,
        )

    def test_init(self):
        self.assertIsInstance(self.camera, Camera)
        self.assertIsInstance(self.camera.time, datetime)
        self.assertIsInstance(self.camera.video_writer, VideoWriter)
        self.assertIsInstance(self.camera.capture, VideoCapture)
        self.assertIsInstance(self.camera.width, int)
        self.assertIsInstance(self.camera.height, int)
        self.assertIsInstance(self.camera.fourcc, int)
        self.assertTrue(self.camera.path_to_video.startswith(VIDEO_DIRECTORY))
        self.assertEqual(self.camera.file_name, self.camera.time.strftime('%d-%m-%Y %H:%M:%S') + '.avi')
        self.assertEqual(self.camera.url, CAMERA_URL)
        self.assertEqual(self.camera.fps, CAMERA_FPS)
        self.assertEqual(self.camera.length_of_video, VIDEO_LENGTH)
        self.assertEqual(self.camera.directory, VIDEO_DIRECTORY)
