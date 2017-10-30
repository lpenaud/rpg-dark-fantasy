#!/usr/bin/env/python3
# coding: utf-8

from setInterval import ThreadJob
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk

class MyWindow(Gtk.Builder):

    def __init__(self, file):
        Gtk.Builder.__init__(self)

        fileList = file.split('/')

        self.add_from_file(file)
        self.connect_signals(self)

        self.name = fileList[len(fileList) - 1].split('.')[0]

    def getWindow(self):
        return self.get_object(self.name)

    def changeImage(self, imageId, file, width=64, height=64):
        image = GdkPixbuf.Pixbuf.new_from_file_at_size(file, width=width, height=height)

        self.get_object(imageId).set_from_pixbuf(image)

    def changeTextLabel(self, labelId, txt):
        self.get_object(labelId).set_text(txt)

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

class LotteryWindow(MyWindow):

    def __init__(self, lottery):
        MyWindow.__init__(self, '../glade/Lottery.glade')
        self.lottery = lottery
        self.interval = 0.25
        self.times = 50

    def randomise(self, *args):
        def loopDisplayLoot():
            for i in range(1, 4):
                self.displayLoot(i, self.lottery.loot())

        k = ThreadJob(loopDisplayLoot, self.interval, self.times - 1)
        k.start()


    def displayLoot(self, numLabel, loot):
        label = self.get_object('label-item-' + str(numLabel))
        label.set_width_chars(50)
        label.set_line_wrap(True)
        label.set_margin_left(50)
        label.set_markup('<span color="' + loot['options']['color'] + '">' + self.lottery.displayLoot(loot) + '</span>')



def load(window, title="None"):
    if title != "None":
        window.set_title(title)

    window.show_all()
    Gtk.main()
