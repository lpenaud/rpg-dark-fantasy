#!/usr/bin/env python3
# coding: utf-8

import os
from setInterval import ThreadJob
import utils
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Pango
from gi.repository.GdkPixbuf import Pixbuf

class MyWindow(Gtk.Builder):
    """
    A class which add some useful methods

    :param f: A relative or absolute path of glade file
    :type f: str
    """

    def __init__(self, f):
        fileList = f.split('/')
        Gtk.Builder.__init__(self)
        self.add_from_file(f)
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
        image = Pixbuf.new_from_file_at_size(file, width=width, height=height)
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
        MyWindow.__init__(self, utils.resolvePath('glade/Lottery.glade'))
        img = Pixbuf.new_from_file_at_size(utils.resolvePath('images/RPG-icon.png'), width=128, height=128)
        self.getWindow().set_icon(img)
        self.getWindow().set_title("Loterie")
        self.lottery = lottery
        self.interval = 0.1
        self.times = 50
        self.handlerItemIdItem = 0
        self.handlerItemIdRand = self.addEvent('button-launch', 'clicked', self.randomise)
        self.catImg = {
            "parchment":utils.resolvePath("images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Document.png"),
            "book":utils.resolvePath("images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Ebook.png"),
            "stick":utils.resolvePath("images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Stick.png"),
            "sword":utils.resolvePath("images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/sword.png"),
            "axe":utils.resolvePath("images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Axe.png"),
            "att":utils.resolvePath("images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/SwordAxe.png"),
            "shoe":utils.resolvePath("images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Pegasus-Boot.png"),
            "helmet":utils.resolvePath("images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Music-4.png"),
            "shield":utils.resolvePath("images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Shield-Security.png"),
            "armor":utils.resolvePath("images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Armor.png"),
            "unknown":utils.resolvePath("images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Storage.png")
        }
        self.changeImage("image-give-me-your-money", utils.resolvePath('images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Gold.png'), width=96, height=96)
        self.changeTextLabel("label-name-lottery", "Le loto de Ginette")
        self.changeImage('image-arrow', utils.resolvePath('images/Legendora-Icon-Set-by-Raindropmemory/Legendora-Icon-Set/Icon/Download.png'), width=96, height=96)
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
            if self.threadJobRandom.currentTimes + 10 >= self.times:
                self.threadJobRandom.interval += 0.015
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
        markupTemplate = '<span color="' + loot['options']['color'] + '">{}</span>'
        marginLeft = 15

        labelDescTitle = self.get_object('label-desc-title-2')
        labelDescTitle.set_markup(markupTemplate.format("Description :"))

        labelDesc = self.get_object('label-desc-2')
        labelDesc.set_line_wrap(True)
        labelDesc.set_margin_left(marginLeft)
        labelDesc.set_markup(markupTemplate.format(loot['item']['desc']))

        labelEffectTitle = self.get_object('label-effect-title-2')
        labelEffectTitle.set_markup(markupTemplate.format("Effet :"))

        labelEffect = self.get_object('label-effect-2')
        labelEffect.set_line_wrap(True)
        labelEffect.set_margin_left(marginLeft)
        labelEffect.set_markup(markupTemplate.format(loot['item']['effet']))

        labelClass = self.get_object('label-class-2')
        labelClass.set_markup(markupTemplate.format(
            "Classe : " + loot['item']['classe']
        ))
        self.get_object('box-item-desc-2').show()

    def displayHistory(self, *args):
        dialog = History(self.getWindow(), self.lottery, self.catImg)
        response = dialog.run()
        dialog.destroy()

    def displayPreference(self, *args):
        lotteryMinRarity = self.lottery.minRarity
        lotteryMaxRarity = self.lottery.maxRarity
        dialog = Preference(self.getWindow(), self.lottery)
        response = dialog.run()

        if response != Gtk.ResponseType.OK:
            self.lottery.minRarity = lotteryMinRarity
            self.lottery.maxRarity = lotteryMaxRarity
        dialog.destroy()

    def displayAbout(self, *args):
        about = About(self.getWindow())
        about.run()
        about.destroy()


class History(Gtk.Dialog):
    def __init__(self, parent, lottery, icons):
        Gtk.Dialog.__init__(
            self,
            "Historique",
            parent,
            0,
            (Gtk.STOCK_OK, Gtk.ResponseType.OK)
        )

        contentArea = self.get_content_area()
        if len(lottery.history) > 0:
            scrolled = Gtk.ScrolledWindow()
            scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            scrolled.set_size_request(500, 300)
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            for loot in lottery.history:
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
                hbox.set_size_request(300, -1)
                hbox.set_halign(Gtk.Align.START)
                label = Gtk.Label()
                label.set_markup(
                """
<span color="{color}">
Nom : <span weight="bold">{name}</span>
Description : {desc}
Effet : {effect}
Rareté : {rarity}
</span>
                """.format(
                        color = loot['options']['color'],
                        name = loot['item']['nom'],
                        desc = loot['item']['desc'],
                        effect = loot['item']['effet'],
                        rarity = loot['options']['rarity']
                    )
                )
                label.set_halign(Gtk.Justification.LEFT)
                label.set_max_width_chars(100)
                label.set_ellipsize(Pango.EllipsizeMode.END)
                # label.set_size_request(100, -1)
                label.set_line_wrap(True)
                if loot['item']['categorie'] in icons.keys():
                    icon = icons[loot['item']['categorie']]
                else:
                    icon = icons['unknown']
                pixbufImg = Pixbuf.new_from_file_at_size(icon, width=96, height=96)
                img = Gtk.Image()
                img.set_from_pixbuf(pixbufImg)
                hbox.pack_start(img, True, True, 0)
                hbox.pack_start(label, True, True, 0)
                vbox.pack_start(hbox, True, True, 0)
            scrolled.add(vbox)
            contentArea.add(scrolled)
        else:
            contentArea.add(Gtk.Label("Vous n'avez pas encore utilisé la loterie."))
        self.show_all()

class Preference(Gtk.Dialog):
    def __init__(self, parent, lottery):
        Gtk.Dialog.__init__(
            self,
            "Préférence",
            parent,
            0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)
        )
        contentArea = self.get_content_area()
        self.lottery = lottery
        self.set_default_size(150, 100)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        minRarityStore = Gtk.ListStore(int, str)
        self.defaultMinRarityIndex = -1
        maxRarityStore = Gtk.ListStore(int, str)
        self.defaultMaxRarityIndex = -1
        rendererText = Gtk.CellRendererText()
        i = 0
        for key in sorted(self.lottery.items.keys(), reverse=True):
            obj = self.lottery.items[key]
            if key[1] == self.lottery.minRarity:
                self.defaultMinRarityIndex = i
            if key[0] == self.lottery.maxRarity:
                self.defaultMaxRarityIndex = i
            minRarityStore.append([key[1], obj['options']['rarity']])
            maxRarityStore.append([key[0], obj['options']['rarity']])
            i += 1

        minRarityComboBox = Gtk.ComboBox.new_with_model(minRarityStore)
        minRarityComboBox.pack_start(rendererText, True)
        minRarityComboBox.add_attribute(rendererText, "text", 1)
        minRarityComboBox.connect("changed", self.on_min_rarity_changed)
        minRarityComboBox.set_active(self.defaultMinRarityIndex)
        minRarityVbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        minRarityVbox.pack_start(Gtk.Label("Rareté minimum"), True, True, 0)
        minRarityVbox.pack_start(minRarityComboBox, True, True, 0)

        maxRarityComboBox = Gtk.ComboBox.new_with_model(maxRarityStore)
        maxRarityComboBox.pack_start(rendererText, True)
        maxRarityComboBox.add_attribute(rendererText, "text", 1)
        maxRarityComboBox.connect("changed", self.on_max_combo_changed)
        maxRarityComboBox.set_active(self.defaultMaxRarityIndex)
        maxRarityVbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        maxRarityVbox.pack_start(Gtk.Label("Rareté maximun"), True, True, 0)
        maxRarityVbox.pack_start(maxRarityComboBox, True, True, 0)

        self.labelErr = Gtk.Label()
        contentArea.add(self.labelErr)
        hbox.pack_start(minRarityVbox, True, True, 0)
        hbox.pack_start(maxRarityVbox, True, True, 0)
        contentArea.add(hbox)
        self.show_all()

    def on_max_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        model = combo.get_model()
        try:
            self.lottery.maxRarity = model[tree_iter][0]
            self.defaultMaxRarityIndex = combo.get_active()
        except ValueError as e:
            self.labelErr.set_markup('<span color="red">La rareté maximun est inférieur à la rareté minimum</span>')
            combo.set_active(self.defaultMaxRarityIndex)


    def on_min_rarity_changed(self, combo):
        tree_iter = combo.get_active_iter()
        model = combo.get_model()
        try:
            self.lottery.minRarity = model[tree_iter][0]
            self.defaultMinRarityIndex = combo.get_active()
        except ValueError as e:
            self.labelErr.set_markup('<span color="red">La rareté minimum est supérieur à la rareté maximun</span>')
            combo.set_active(self.defaultMaxRarityIndex)

class About(Gtk.AboutDialog):
    """docstring for About."""
    def __init__(self, parent):
        img = utils.resolvePath('images/RPG-icon.png')
        logo = Pixbuf.new_from_file_at_size(img, width=128, height=128)
        super(About, self).__init__(
            parent = parent,
            artists = ['Teekatas Suwannakrua'],
            authors = ['Loïc Penaud', 'Erwan Bourhis'],
            comments = "A RPG Lottery",
            copyright = "Loïc Penaud",
            documenters = ['Loïc Penaud'],
            license_type = Gtk.License.GPL_3_0_ONLY,
            logo = logo,
            program_name = "Lottery",
            version = '1.2',
            website = 'https://github.com/lpenaud/rpg-dark-fantasy',
            website_label = 'Github'
        )



def load(window):
    """
    Show main GtkWindow

    :param window: Gtk main window to display it
    :type window: Gtk.Window
    """
    window.show_all()
    Gtk.main()
