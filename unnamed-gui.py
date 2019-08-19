#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Gdk, Vte, GObject, Gio, GLib

provider = Gtk.CssProvider()

Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

settings = Gtk.Settings.get_default()
settings.set_property("gtk-theme-name", "Adwaita")
settings.set_property("gtk-application-prefer-dark-theme", True)

builder = Gtk.Builder()
GObject.type_register(Vte.Terminal)
builder.add_from_file("gtk/unnamed-bot-main.glade")

class SignalHandler:
    def quit(self, *args):
        Gtk.main_quit()
    def start(self, *args):
        global builder
        terminal = builder.get_object("terminal")
        startbtn = builder.get_object("start")
        stopbtn = builder.get_object("stop")
        startbtn.set_sensitive(False)
        stopbtn.set_sensitive(True)
        terminal.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            None,
            ["./unnamed-bot.py"],
            None,
            GLib.SpawnFlags.DEFAULT,
            None,
            None,
            None
        )
    def stop(self, *args):
        terminal = builder.get_object("terminal")
        terminal.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            None,
            ["/usr/bin/tput", "reset"],
            None,
            GLib.SpawnFlags.DEFAULT,
            None,
            None,
            None
        )
        startbtn = builder.get_object("start")
        stopbtn = builder.get_object("stop")
        startbtn.set_sensitive(True)
        stopbtn.set_sensitive(False)
        return

builder.connect_signals(SignalHandler())

window = builder.get_object("MainWindow")
window.maximize()
window.show_all()

terminal = builder.get_object("terminal")
bg = Gdk.RGBA()
bg.parse("#353535")
terminal.set_color_background(bg)

Gtk.main()