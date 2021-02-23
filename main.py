from camera import Camera

HOME_CAMERA = 'rtsp://admin:@192.168.1.10'

CAMERA_FPS = 25.0
VIDEO_DIR = 'video'
VIDEO_LENGTH = 60


if __name__ == '__main__':
    camera = Camera(HOME_CAMERA, fps=CAMERA_FPS)

    while True:
        camera.run()
