import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

# Инициализация библиотеки Gstreamer
Gst.init(None)


class RTSPCamera:
    def __init__(self, ip, login, password, port):
        self.url = f'rtsp://{login}:{password}@{ip}:{port}'
        self.pipeline = None

    def get_pipeline(self):
        pass

    def _start_playing(self):
        self.pipeline.set_state(Gst.State.PLAYING)

    def _stop_playing_if_EOS_or_error(self):
        bus = self.pipeline.get_bus()
        msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)

    def _free_up_resources(self):
        self.pipeline.set_state(Gst.State.NULL)

    def run(self):
        self.get_pipeline()
        self._start_playing()
        self._stop_playing_if_EOS_or_error()
        self._free_up_resources()


class RTSPCameraMonitor(RTSPCamera):
    def get_pipeline(self):
        description = 'rtspsrc name=rtspsrc ! decodebin ! autovideosink'
        self.pipeline = Gst.parse_launch(description)
        rtsp_src = self.pipeline.get_by_name("rtspsrc")
        rtsp_src.set_property('location', self.url)
        rtsp_src.set_property('latency', 0)  # Количество буфферизируемых миллисекунд видео
        rtsp_src.set_property('drop-on-latency', True)  # Сообщает джиттербуферу не превышать задержку


class RTSPCameraWriterMKV(RTSPCamera):
    def get_pipeline(self):
        description = 'rtspsrc name=rtspsrc ! rtph264depay ! h264parse ! matroskamux ! filesink location=file.mkv'
        self.pipeline = Gst.parse_launch(description)
        rtsp_src = self.pipeline.get_by_name("rtspsrc")
        rtsp_src.set_property('location', self.url)
