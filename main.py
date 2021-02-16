import cv2


CAMERA_URL = 'rtsp://admin:@192.168.1.10'
CLOSING_KEY = 'q'


class Camera:
    def __init__(self, url):
        self.url = url
        self.capture = cv2.VideoCapture(self.url)

    def get_frame(self):
        ret, frame = self.capture.read()
        return ret, frame

    def show_frame(self, frame):
        cv2.imshow('frame', frame)

    def stop_condition(self):
        return cv2.waitKey(1) & 0xFF == ord(CLOSING_KEY)

    def close_windows_and_clean_memory(self):
        self.capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    pass
