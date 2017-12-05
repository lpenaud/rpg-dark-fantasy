# rpg-dark-fantasy

## Installation

### If you are on GNU/Linux
You should have the third version of python and GTK.
if it is not already installed :
* with apt-get : `sudo apt-get install python3-gi`
* with pacman :  `sudo pacman -S python-gobject`

Then to lanch main.py :
Eitcher you have to execute theses commands (in source folder) : `chmod +x main.py` next `./main.py`
Or type (in source folder) `python3 main.py`

### Or if you are on Windows
**If you have windows 7 64 bits**
You can download lottery-win.zip and lanch main.exe

**Else**

You have to install some stuff :
* [MSYS2](http://www.msys2.org/)

and when it's installed, theses commands on MSYS2 terminal :

| 64 bits | 32 bits |
| :------: | :-------: |
|`pacman -S mingw-w64-x86_64-gtk3` | `pacman -S mingw-w64-i686-gtk3` |
| `pacman -S mingw-w64-x86_64-python3-gobject` | `pacman -S mingw-w64-i686-python3-gobject` |

After you have to play with `cd` and `ls` commands to enter in rpg-dark-fantasy folder next launch the program with : `python3 main.py` or `./main.py`.
If it's not working, install python3 : `pacman -S python3`, then retry.

## TODO
- [x] Write a documentation
- [x] Write data/stuff.json
- [ ] Window to view the history
- [ ] Option to lock a rarity in Lottery
- [ ] Style of the launch button
- [ ] Slow down the interval just before final loot
- [ ] Play a sound which depend of the loot rarity
- [ ] Write "about"

## Images sources
Thank to [Teekatas Suwannakrua](https://raindropmemory.deviantart.com) for the icons.
* [Iconset: Legendora](http://www.iconarchive.com/show/legendora-icons-by-raindropmemory.html)
* [Iconset: Down To Earth Icons](http://www.iconarchive.com/show/down-to-earth-icons-by-raindropmemory.html)
    * [![RPG-icon.png](images/RPG-icon.png)](http://www.iconarchive.com/show/down-to-earth-icons-by-raindropmemory/G12-RPG-icon.html)
