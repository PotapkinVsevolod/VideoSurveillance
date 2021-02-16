import unittest

from cv2 import VideoCapture

from main import Camera, CAMERA_URL


class TestCamera(unittest.TestCase):
    def setUp(self) -> None:
        self.camera = Camera(url=CAMERA_URL)

    def test_capture(self):
        self.assertEqual(type(self.camera.capture), VideoCapture)

    def test_not_empty_frame(self):
        ret, frame = self.camera.get_frame()
        self.assertTrue(ret)
        self.assertIsNotNone(frame)
