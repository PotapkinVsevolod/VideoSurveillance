import os
from datetime import datetime

import cv2


VIDEO_FORMAT = 'XVID'
VIDEO_DIR = 'video'
CLOSING_KEY = 'q'


def close_windows():
    # Закрытие всех окон
    cv2.destroyAllWindows()


def close_condition():
    # Если нажмем на клавиатуре CLOSING_KEY, то True
    return cv2.waitKey(1) & 0xFF == ord(CLOSING_KEY)


def show_frame(frame):
    # Показывает диалоговое окно с фреймом
    cv2.imshow('frame', frame)


class Camera:
    def __init__(self, url, length_of_video):
        self.time = None
        self.file_name = None
        self.get_filename()

        self.length_of_video = length_of_video
        self.url = url

        # Класс, который позволяет захватывать видео с камеры.
        self.capture = cv2.VideoCapture(self.url)

        # Параметры размеров фрейма
        self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Задаем последовательность байтов для идентификации или записи данных
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

        # Класс, который умеет записывать видео, 3 аргумент - фпс
        self.video_writer = None
        self.get_video_writer()

    def get_frame(self):
        # ret - True, если frame не битый, иначе false
        ret, frame = self.capture.read()
        return ret, frame

    def get_filename(self):
        self.time = datetime.now()
        name = self.time.strftime('%d-%m-%Y %H-%M') + '.avi'
        self.file_name = os.path.join(VIDEO_DIR, name)

    def get_video_writer(self):
        # Класс, который умеет записывать видео, 3 аргумент - фпс
        self.video_writer = cv2.VideoWriter(
            self.file_name, self.fourcc, 25.0, (self.width, self.height))

    def clean_memory(self):
        # Освобождение в памяти места, занимаемого захватчиком видео
        if self.capture:
            self.capture.release()
        # Освобождение в памяти места, занимаемого писарем видео
        if self.video_writer:
            self.video_writer.release()

    def save_frame(self, ret, frame):
        if not self.video_writer:
            raise RuntimeError('Get video writer before save frame.')
        if ret:
            self.video_writer.write(frame)

    def next_file_time(self):
        return datetime.now().minute // self.length_of_video != \
               self.time.minute // self.length_of_video

    def run(self):
        if self.next_file_time():
            # self.video_writer.release()
            self.get_filename()
            self.get_video_writer()

        ret, frame = self.get_frame()
        show_frame(frame)
        self.save_frame(ret, frame)

        if close_condition():
            self.clean_memory()
            close_windows()
