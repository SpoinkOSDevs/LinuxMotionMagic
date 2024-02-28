import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject

class Sprite:
    def __init__(self, filename):
        self.filename = filename
        self.x = 0
        self.y = 0
        self.angle = 0

class Frame:
    def __init__(self, frame_id):
        self.frame_id = frame_id
        self.sprites = []

class Handle:
    def __init__(self):
        self.frames = [Frame(1)]
        self.current_frame_index = 0

    def add_sprite_from_dialog(self, button):
        dialog = Gtk.FileChooserDialog("Select an image file", None,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        filter_image = Gtk.FileFilter()
        filter_image.set_name("Image files")
        filter_image.add_pattern("*.png")
        filter_image.add_pattern("*.jpg")
        dialog.add_filter(filter_image)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            dialog.destroy()
            self.frames[self.current_frame_index].sprites.append(Sprite(filename))
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def save_project_from_dialog(self, button):
        dialog = Gtk.FileChooserDialog("Save project", None,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        filter_lmmp = Gtk.FileFilter()
        filter_lmmp.set_name("Linux Motion Magic Projects")
        filter_lmmp.add_pattern("*.lmmp")
        dialog.add_filter(filter_lmmp)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            dialog.destroy()

            with open(filename, 'w') as file:
                for frame in self.frames:
                    file.write(f"Frame {frame.frame_id}:\n")
                    for sprite in frame.sprites:
                        file.write(f"  Sprite: {sprite.filename} at ({sprite.x}, {sprite.y}) with angle {sprite.angle}\n")
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def load_project_from_dialog(self, button):
        dialog = Gtk.FileChooserDialog("Open project", None,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        filter_lmmp = Gtk.FileFilter()
        filter_lmmp.set_name("Linux Motion Magic Projects")
        filter_lmmp.add_pattern("*.lmmp")
        dialog.add_filter(filter_lmmp)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            dialog.destroy()

            self.frames = []
            current_frame_id = -1

            with open(filename, 'r') as file:
                for line in file:
                    if line.startswith("Frame"):
                        _, current_frame_id = line.split()
                        current_frame_id = int(current_frame_id[:-1])
                        self.frames.append(Frame(current_frame_id))
                    elif line.startswith("  Sprite"):
                        _, sprite_filename, _, sprite_x, _, sprite_y, _, sprite_angle = line.split()
                        sprite = Sprite(sprite_filename)
                        sprite.x, sprite.y, sprite.angle = float(sprite_x), float(sprite_y), float(sprite_angle[:-1])
                        self.frames[-1].sprites.append(sprite)

    def play_frames(self, button):
        for frame in self.frames:
            print(f"Frame {frame.frame_id}:")
            for sprite in frame.sprites:
                print(f"  Sprite: {sprite.filename} at ({sprite.x}, {sprite.y}) with angle {sprite.angle}")

    def go_to_previous_frame(self, button):
        if self.current_frame_index > 0:
            self.current_frame_index -= 1

class AnimationWindow(Gtk.Window):
    def __init__(self, handle):
        Gtk.Window.__init__(self, title="Linux Motion Magic Animation")
        self.handle = handle
        self.connect("destroy", Gtk.main_quit)

        self.animation_area = Gtk.DrawingArea()
        self.animation_area.connect("draw", self.on_draw)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.add(hbox)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        hbox.pack_start(vbox, True, True, 0)

        vbox.pack_start(self.animation_area, True, True, 0)

        previous_button = Gtk.Button.new_with_label("Previous Frame")
        previous_button.connect("clicked", handle.go_to_previous_frame)
        vbox.pack_start(previous_button, False, False, 0)

    def on_draw(self, widget, cr):
        # Clear the area
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(0, 0, self.get_allocated_width(), self.get_allocated_height())
        cr.fill()

        # Draw sprites
        for sprite in self.handle.frames[self.handle.current_frame_index].sprites:
            self.draw_sprite(cr, sprite)

    def draw_sprite(self, cr, sprite):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(sprite.filename)
        cr.save()
        cr.translate(sprite.x, sprite.y)
        cr.rotate(sprite.angle)
        Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
        cr.paint()
        cr.restore()

class LinuxMotionMagicApp(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self, application_id="org.gtk.LinuxMotionMagic")

    def do_activate(self):
        handle = Handle()
        animation_window = AnimationWindow(handle)
        animation_window.show_all()

if __name__ == "__main__":
    app = LinuxMotionMagicApp()
    app.run(None)
