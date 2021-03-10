import os
from datetime import datetime

import cv2


class Camera:
    def __init__(self, url, fps, length_of_video=60, directory='video'):
        self.fps = fps
        self.directory = directory
        self.url = url if url else 0
        self.capture = cv2.VideoCapture(self.url)

        # Извлекает разрешение видео из камеры
        self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.length_of_video = length_of_video
        self.get_path_to_video()
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.get_video_writer()

    def get_frame(self):
        # ret - True, если frame не битый, иначе false
        ret, frame = self.capture.read()
        return ret, frame

    def get_path_to_video(self):
        self.time = datetime.now()
        self.file_name = self.time.strftime('%d-%m-%Y %H:%M:%S') + '.avi'
        self.path_to_video = os.path.join(self.directory, self.file_name)

    def get_video_writer(self):
        self.video_writer = cv2.VideoWriter(
            self.path_to_video,
            self.fourcc,
            self.fps,
            (self.width, self.height)
        )

    def clean_memory(self):
        self.capture.release()
        self.video_writer.release()

    def save_frame(self, ret, frame):
        if not self.video_writer:
            raise RuntimeError('Get video writer before save frame.')
        self.video_writer.write(frame)

    def next_file_time(self):
        return datetime.now().minute // self.length_of_video != \
               self.time.minute // self.length_of_video

    def run(self):

        if self.next_file_time():
            self.get_path_to_video()
            self.get_video_writer()

        ret, frame = self.get_frame()

        if ret:
            """ Blocking function. Opens OpenCV window to display stream. """
            cv2.imshow(self.url, frame)

            self.save_frame(ret, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.clean_memory()
            cv2.destroyAllWindows()
