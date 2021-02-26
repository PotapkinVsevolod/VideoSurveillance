# from pprint import pprint

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

# initialize GStreamer
Gst.init(None)

# build the pipeline
pipeline = Gst.parse_launch('rtspsrc name=rtspsrc ! decodebin ! autovideosink')

rtsp_src = pipeline.get_by_name("rtspsrc")
rtsp_src.set_property('location', "rtsp://admin:@192.168.1.10:554")  # home ip camera
# rtsp_src.set_property('location', "rtsp://admin:AdminF13@178.176.243.64:8011")  # remote ip camera
rtsp_src.set_property('latency', 0)  # Amount of ms to buffer
rtsp_src.set_property('drop-on-latency', True)  # Tells the jitterbuffer to never exceed the given latency in size

# start playing
pipeline.set_state(Gst.State.PLAYING)

# wait until EOS or error
bus = pipeline.get_bus()
msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)

# free resources
pipeline.set_state(Gst.State.NULL)
