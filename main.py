import cv2


CAMERA_URL = 'rtsp://admin:@192.168.1.10'
CLOSING_KEY = 'q'


def start_camera():
    capture = cv2.VideoCapture(CAMERA_URL)

    while True:
        ret, frame = capture.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord(CLOSING_KEY):
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    start_camera()
