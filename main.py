from camera_gstreamer import RTSPCameraWriterMKV
from config import REMOTE_CAMERA


if __name__ == '__main__':
    camera = RTSPCameraWriterMKV(**REMOTE_CAMERA)
    camera.run()
