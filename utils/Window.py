#!/usr/bin/env python3
# coding: utf-8

from setInterval import ThreadJob
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GObject

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

    def addEvent(self, objectId, event, callback, *dataCallback):
        obj = self.get_object(objectId)
        handlerId = obj.connect(event, callback, dataCallback)
        return handlerId

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

class LotteryWindow(MyWindow):

    def __init__(self, lottery):
        MyWindow.__init__(self, '../glade/Lottery.glade')
        img = GdkPixbuf.Pixbuf.new_from_file_at_size('../images/RPG-icon.png', width=128, height=128)
        self.getWindow().set_icon(img)
        self.lottery = lottery
        self.interval = 0.1
        self.times = 50
        self.handlerItemId = 0

    def randomise(self, *args):
        def workingThreadRandomise():
            GObject.idle_add(self.displayRandom)

        self.threadJobRandom = ThreadJob(workingThreadRandomise, self.interval, self.times)
        self.threadJobRandom.currentTimes = 0
        self.threadJobRandom.start()

    def displayRandom(self):
        for number in range(1, 4):
            keepHistory = number == 2 and self.threadJobRandom.currentTimes == self.times
            loot = self.lottery.loot(keepHistory=keepHistory)
            label = self.get_object('label-item-' + str(number))
            label.set_width_chars(50)
            label.set_line_wrap(True)
            label.set_margin_left(50)
            self.changeImage('image-item-' + str(number), '../images/rarety/128x128/' + loot['options']['rarety'] + '.png', width=64, height=64)
            label.set_markup('<span weight="bold" color="' + loot['options']['color'] + '">' + loot['item']['nom'] + '</span>')
            if keepHistory:
                self.addEventItem(number, **loot)


    def addEventItem(self, number, **dataCallback):
        idObject = "eventbox-item-" + str(number)
        if self.handlerItemId != 0:
            self.get_object(idObject).disconnect(self.handlerItemId)
        self.handlerItemId = self.addEvent(idObject, 'enter-notify-event', self.displayLoot, dataCallback)


    def displayLoot(self, *args):
        loot = args[2][0]
        label = self.get_object('label-item-2')
        markup = '<span color="' + loot['options']['color'] + '">'
        markup += '<span weight=' + '"bold"' + '>' + loot['item']['nom'] + '</span>'
        markup += "\nDescription : " + loot['item']['desc']
        markup += "\nEffet : " + loot['item']['effet']
        markup += '</span>'
        label.set_markup(markup) #To get markup : get_label()



def load(window, title="None"):
    if title != "None":
        window.set_title(title)

    window.show_all()
    Gtk.main()
