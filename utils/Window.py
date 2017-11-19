#!/usr/bin/env python3
# coding: utf-8

import os
from setInterval import ThreadJob
import utils
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

    def __init__(self, lottery, **args):
        rootFolder = utils.realPathDir()
        MyWindow.__init__(self, rootFolder + '../glade/Lottery.glade')
        img = GdkPixbuf.Pixbuf.new_from_file_at_size(rootFolder + '../images/RPG-icon.png', width=128, height=128)
        self.getWindow().set_icon(img)
        self.getWindow().set_title("Loterie")
        self.lottery = lottery
        self.interval = 0.1
        self.times = 50
        self.handlerItemIdItem = 0
        self.handlerItemIdRand = self.addEvent('button-launch', 'clicked', self.randomise)
        self.catImg = {
            "parchment":rootFolder+"../images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Document.png",
            "book":rootFolder+"../images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Ebook.png",
            "stick":rootFolder+"../images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Stick.png",
            "sword":rootFolder+ "../images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/sword.png",
            "axe":rootFolder+"../images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Axe.png",
            "att":rootFolder+"../images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/SwordAxe.png",
            "shoe":rootFolder+"../images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Pegasus-Boot.png",
            "helmet":rootFolder+"../images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Music-4.png",
            "shield":rootFolder+"../images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Shield-Security.png",
            "armor":rootFolder+"../images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Armor.png",
            "unknown":rootFolder+"../images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Storage.png"
        }
        self.changeImage("image-give-me-your-money", rootFolder+'../images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Gold.png', width=96, height=96)
        self.changeTextLabel("label-name-lottery", "Le loto de Ginette")
        self.changeImage('image-arrow', rootFolder+'../images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Download.png', width=96, height=96)
        self.threadJobRandom = ThreadJob(self.displayRandom, 0.01, 1)
        self.threadJobRandom.start()
        load(self.getWindow())

    def randomise(self, *args):
        """
        A procedure to launch x times Lottery.Loot() in Thread and display the loots (self.displayRandom())
        """
        def workingThreadRandomise():
            GObject.idle_add(self.displayRandom)

        self.get_object('box-item-desc-2').hide()
        if self.handlerItemIdItem != 0:
            self.get_object("eventbox-item-2").disconnect(self.handlerItemIdItem)
        self.get_object('button-launch').disconnect(self.handlerItemIdRand)
        self.threadJobRandom = ThreadJob(workingThreadRandomise, self.interval, self.times)
        self.threadJobRandom.currentTimes = 0
        self.threadJobRandom.start()

    def displayRandom(self, keep=True):
        """
        A procedure to display name of the loots obtained by the thread triggered by self.randomise procedure
        """
        for number in range(1, 4):
            keepHistory = number == 2 and self.threadJobRandom.currentTimes == self.times and self.times > 1
            loot = self.lottery.loot(keepHistory=keepHistory)
            if loot['item']['categorie'] in self.catImg.keys():
                img = self.catImg[loot['item']['categorie']]
            else:
                img = self.catImg['unknown']
            label = self.get_object('label-rarity-' + str(number))
            title = self.get_object('label-title-' + str(number))
            title.set_markup('<span weight="bold" color="' + loot['options']['color'] + '">' + loot['item']['nom'].capitalize() + '</span>')
            label.set_width_chars(50)
            label.set_markup('<span weight="bold" color="' + loot['options']['color'] + '">' + loot['options']['rarity'].capitalize() + '</span>')
            self.changeImage('image-item-' + str(number), img, width=96, height=96)
            if keepHistory:
                self.addEventItem(number, **loot)
                self.handlerItemIdRand = self.addEvent('button-launch', 'clicked', self.randomise)


    def addEventItem(self, number, **dataCallback):
        """
        A procedure to connect the signal of the object looted

        :param number: number (1 to 3) of eventbox-item
        :type number: int
        :param dataCallback: Arguments of the callback function
        :type dataCallback: dict
        """
        idObject = "eventbox-item-" + str(number)
        self.handlerItemIdItem = self.addEvent(idObject, 'enter-notify-event', self.displayLoot, dataCallback)


    def displayLoot(self, *args):
        """
        A procedure to display more informations of the obtained loot (effect and description)

        :param args: Data : Gtk.Object, Gtk.Event,<tuple (loot (item, options))>
        :type args: tuple
        """
        loot = args[2][0]
        markupList = ['<span color="' + loot['options']['color'] + '">',"</span>"]
        marginLeft = 15

        labelDescTitle = self.get_object('label-desc-title-2')
        markupListDescTitle = markupList.copy()
        markupListDescTitle.insert(1, "Description :")
        labelDescTitle.set_markup("".join(markupListDescTitle))

        labelDesc = self.get_object('label-desc-2')
        markupListDesc = markupList.copy()
        markupListDesc.insert(1, loot['item']['desc'])
        labelDesc.set_line_wrap(True)
        labelDesc.set_margin_left(marginLeft)
        labelDesc.set_markup("".join(markupListDesc))

        labelEffectTitle = self.get_object('label-effect-title-2')
        markupListEffectTitle = markupList.copy()
        markupListEffectTitle.insert(1, "Effet :")
        labelEffectTitle.set_markup("".join(markupListEffectTitle))

        labelEffect = self.get_object('label-effect-2')
        markupListEffect = markupList.copy()
        markupListEffect.insert(1, loot['item']['effet'])
        labelEffect.set_line_wrap(True)
        labelEffect.set_margin_left(marginLeft)
        labelEffect.set_markup("".join(markupListEffect))

        labelClass = self.get_object('label-class-2')
        markupListClass = markupList.copy()
        markupListClass.insert(1, "Classe : ")
        markupListClass.insert(2, loot['item']['classe'])
        labelClass.set_markup("".join(markupListClass))
        self.get_object('box-item-desc-2').show()

def load(window):
    """
    Show main GtkWindow

    :param window: Gtk main window to display it
    :type window: Gtk.Window
    """
    window.show_all()
    Gtk.main()
