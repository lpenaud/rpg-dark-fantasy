#!/usr/bin/env/python3
# coding: utf-8

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

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
    
    def __init__(self):
        MyWindow.__init__(self, '../glade/Lottery.glade')

    

def load(window, title="None"):    
    if title != "None":
        window.set_title(title)
    
    window.show_all()
    Gtk.main()
