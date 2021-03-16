import gi
gi.require_version("Gtk", "3.0")
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gst
Gst.init(None)
Gst.init_check(None)


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self):
        super().__init__()
        self.maximize()


class CameraWidget(Gtk.Box):
    def __init__(self, pipeline):
        super().__init__()
        # Only setup the widget after the window is shown.
        self.connect('realize', self._on_realize)

        # Parse a gstreamer pipeline and create it.
        self._bin = Gst.parse_bin_from_description(pipeline, True)

    def _on_realize(self, widget):
        pipeline = Gst.Pipeline()
        factory = pipeline.get_factory()
        gtk_sink = factory.make('gtksink')
        pipeline.add(self._bin)
        pipeline.add(gtk_sink)
        # Link the pipeline to the sink that will display the video.
        self._bin.link(gtk_sink)
        self.pack_start(gtk_sink.props.widget, True, True, 0)
        gtk_sink.props.widget.show()
        # Start the video
        pipeline.set_state(Gst.State.PLAYING)


if __name__ == '__main__':
    main_window = MainWindow()
    camera_widget = CameraWidget('videotestsrc')
    main_window.add(camera_widget)
    main_window.connect("destroy", Gtk.main_quit)  # Закрывает приложение при закрытии окна
    main_window.show_all()
    Gtk.main()
