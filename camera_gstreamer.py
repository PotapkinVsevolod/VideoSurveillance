import sys
import gi

gi.require_version("GLib", "2.0")
gi.require_version("GObject", "2.0")
gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib, GObject


# Initialize GStreamer
Gst.init(sys.argv[1:])


class RTSPCamera:
    def __init__(self, ip, login, password, port):
        self.url = f'rtsp://{login}:{password}@{ip}:{port}'
        self.pipeline = None

    def get_pipeline(self):
        pass

    def _start_playing(self):
        ret = self.pipeline.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            print("Unable to set the pipeline to the playing state.")
            sys.exit(1)

    def _stop_playing_if_EOS_or_error(self):
        bus = self.pipeline.get_bus()
        self.msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)

    def _parse_message(self):
        if self.msg:
            if self.msg.type == Gst.MessageType.ERROR:
                err, debug_info = self.msg.parse_error()
                print(f"Error received from element {self.msg.src.get_name()}: {err.message}")
                print(f"Debugging information: {debug_info if debug_info else 'none'}")
            elif self.msg.type == Gst.MessageType.EOS:
                print("End-Of-Stream reached.")
            else:
                # This should not happen as we only asked for ERRORs and EOS
                print("Unexpected message received.")

    def _free_up_resources(self):
        self.pipeline.set_state(Gst.State.NULL)

    def run(self):
        self.get_pipeline()

        if not self.pipeline:
            print("Pipeline is not created.")
            sys.exit()

        self._start_playing()
        self._stop_playing_if_EOS_or_error()
        self._parse_message()
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
