from camera import Camera


CAMERA_URL = 'rtsp://admin:@192.168.1.10'
VIDEO_LENGTH = 30

if __name__ == '__main__':
    camera = Camera(CAMERA_URL, VIDEO_LENGTH)

    while True:
        camera.run()
