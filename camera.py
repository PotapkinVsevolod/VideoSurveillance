from datetime import datetime, timedelta

import cv2


CAMERA_URL = 'rtsp://admin:@192.168.1.10'
VIDEO_FORMAT = 'XVID'
CLOSING_KEY = 'q'
FILE_OUTPUT = 'output.avi'

# Длина видео в минутах
VIDEO_LENGTH = 30


def get_filename():
    now_time = datetime.now().strftime('%d-%m-%Y %H-%M')
    return now_time + '.avi'


class Camera:
    def __init__(self, url):
        self.url = url

        # Класс, который позволяет захватывать видео с камеры.
        self.capture = cv2.VideoCapture(self.url)

        # Параметры размеров фрейма
        self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Задаем последовательность байтов для идентификации или записи данных
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

        self.video_writer = None

    def get_frame(self):
        # ret - True, если frame не битый, иначе false
        ret, frame = self.capture.read()
        return frame

    def show_frame(self, frame):
        # Показывает диалоговое окно с фреймом
        cv2.imshow('frame', frame)

    def get_video_writer(self, file_name):
        # Класс, который умеет записывать видео, 3 аргумент - фпс
        self.video_writer = cv2.VideoWriter(file_name, self.fourcc, 20.0, (self.width, self.height))

    def stop_condition(self):
        # Если нажмем на клавиатуре CLOSING_KEY, то True
        return cv2.waitKey(1) & 0xFF == ord(CLOSING_KEY)

    def close_windows_and_clean_memory(self):
        # Освобождение в памяти места, занимаемого захватчиком видео
        self.capture.release()
        # Закрытие всех окон
        cv2.destroyAllWindows()

    def clean_memory(self):
        # Освобождение в памяти места, занимаемого захватчиком видео
        if self.capture:
            self.capture.release()
        # Освобождение в памяти места, занимаемого писарем видео
        if self.video_writer:
            self.video_writer.release()

    def close_windows(self):
        # Закрытие всех окон
        cv2.destroyAllWindows()

    def save_frame(self, frame):
        if not self.video_writer:
            raise RuntimeError('Get video writer before save frame.')
        self.video_writer.write(frame)

    def show_video(self):
        now_frame = self.get_frame()
        self.show_frame(now_frame)
        if self.stop_condition():
            self.clean_memory()
            self.close_windows()

    def show_and_save_video(self):
        now_frame = self.get_frame()
        self.show_frame(now_frame)
        self.save_frame(now_frame)
        if self.stop_condition():
            self.clean_memory()
            self.close_windows()


if __name__ == '__main__':
    camera = Camera(CAMERA_URL)
    file_name = get_filename()
    camera.get_video_writer(file_name=file_name)
    while True:
        camera.show_and_save_video()
