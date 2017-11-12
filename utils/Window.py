#!/usr/bin/env python3
# coding: utf-8

from setInterval import ThreadJob
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GObject

class MyWindow(Gtk.Builder):
    """
    A class which add some useful methods

    :param file: A relative or absolute path of glade file
    :type file: str
    """

    def __init__(self, file):
        Gtk.Builder.__init__(self)
        fileList = file.split('/')
        self.add_from_file(file)
        self.connect_signals(self)
        self.name = fileList[len(fileList) - 1].split('.')[0]

    def getWindow(self):
        """
        Get window object in the glade file

        :return: Window object
        :rtype: Gtk.Window
        """
        return self.get_object(self.name)

    def changeImage(self, imageId, file, width=64, height=64):
        """
        Set source of a GtkImage with its id

        :param imageId: Id of a GtkImage
        :type imageId: str
        :param file: Absolute or relative path of the image source
        :type file: str
        :param width: Width in pixel of the image by default 64
        :type width: int
        :param height: Height in pixel of the image by default 64
        :type height: int
        """
        image = GdkPixbuf.Pixbuf.new_from_file_at_size(file, width=width, height=height)
        self.get_object(imageId).set_from_pixbuf(image)

    def changeTextLabel(self, labelId, txt):
        """
        Set text of a GtkLabel with its id

        :param labelId: Id of a GtkLabel
        :type labelId: str
        :param txt: Text to put into the GtkLabel
        :type txt: str
        """
        self.get_object(labelId).set_text(txt)

    def addEvent(self, objectId, event, callback, *dataCallback):
        """
        Connect a signal a gtkObject

        :param objectId: Id of the gtkObject
        :type objectId: str
        :param event: Gtk event of the signal compatible with the selected object
        :type event: str
        :param callback: Function invoked when the event is triggered
        :type callback: function
        :return: Handler id to disconnect him
        :rtype: int
        """
        obj = self.get_object(objectId)
        handlerId = obj.connect(event, callback, dataCallback)
        return handlerId

    def onDeleteWindow(self, *args):
        """
        Procedure triggered when the user left the main window
        """
        Gtk.main_quit(*args)

class LotteryWindow(MyWindow):
    """
    Create a new Window to the class Lottery

    :param lottery: Lottery to use in the window
    :type lottery: Lottery.Lottery
    """

    def __init__(self, lottery):
        MyWindow.__init__(self, '../glade/Lottery.glade')
        img = GdkPixbuf.Pixbuf.new_from_file_at_size('../images/RPG-icon.png', width=128, height=128)
        self.getWindow().set_icon(img)
        self.lottery = lottery
        self.interval = 0.1
        self.times = 50
        self.handlerItemId = 0

    def randomise(self, *args):
        """
        A procedure to launch x times Lottery.Loot() in Thread and display the loots (self.displayRandom())
        """
        def workingThreadRandomise():
            GObject.idle_add(self.displayRandom)

        self.threadJobRandom = ThreadJob(workingThreadRandomise, self.interval, self.times)
        self.threadJobRandom.currentTimes = 0
        self.threadJobRandom.start()

    def displayRandom(self):
        """
        A procedure to display name of the loots obtained by the thread triggered by self.randomise procedure
        """
        for number in range(1, 4):
            keepHistory = number == 2 and self.threadJobRandom.currentTimes == self.times
            loot = self.lottery.loot(keepHistory=keepHistory)
            label = self.get_object('label-item-' + str(number))
            label.set_width_chars(50)
            label.set_line_wrap(True)
            label.set_margin_left(50)
            self.changeImage('image-item-' + str(number), '../images/rarity/128x128/' + loot['options']['rarity'] + '.png', width=64, height=64)
            label.set_markup('<span weight="bold" color="' + loot['options']['color'] + '">' + loot['item']['nom'] + '</span>')
            if keepHistory:
                self.addEventItem(number, **loot)


    def addEventItem(self, number, **dataCallback):
        """
        A procedure to connect the signal of the object looted

        :param number: number (1 to 3) of eventbox-item
        :type number: int
        :param dataCallback: Arguments of the callback function
        :type dataCallback: dict
        """
        idObject = "eventbox-item-" + str(number)
        if self.handlerItemId != 0:
            self.get_object(idObject).disconnect(self.handlerItemId)
        self.handlerItemId = self.addEvent(idObject, 'enter-notify-event', self.displayLoot, dataCallback)


    def displayLoot(self, *args):
        """
        A procedure to display more informations of the obtained loot (effect and description)

        :param args: Data : Gtk.Object, Gtk.Event,<tuple (loot (item, options))>
        :type args: tuple
        """
        loot = args[2][0]
        label = self.get_object('label-item-2')
        markup = '<span color="' + loot['options']['color'] + '">'
        markup += '<span weight=' + '"bold"' + '>' + loot['item']['nom'] + '</span>'
        markup += "\nDescription : " + loot['item']['desc']
        markup += "\nEffet : " + loot['item']['effet']
        markup += '</span>'
        label.set_markup(markup) #To get markup : get_label()

def load(window, title="None"):
    """
    Show main GtkWindow

    :param window: Gtk main window to display it
    :type window: Gtk.Window
    """
    if title != "None":
        window.set_title(title)

    window.show_all()
    Gtk.main()
