# rpg-dark-fantasy

## Requirements
The third version of python and GTK.

### Then if you are on GNU/Linux
If it is not already installed : 
* with apt-get : `sudo apt-get install python3-gi`
* with pacman :  `sudo pacman -S python-gobject`

Then, before to launch main.py, type this command `chmod +x main.py`, after `./main.py`, 
or type `python3 main.py` directly.

### Or if you are on Windows
You have to install some stuff :
* [MSYS2](http://www.msys2.org/)

and when it's installed, theses commands on MSYS2 terminal :

| 64 bits | 32 bits |
| :------: | :-------: |
|`pacman -S mingw-w64-x86_64-gtk3` | `pacman -S mingw-w64-i686-gtk3` |
| `pacman -S mingw-w64-x86_64-python3-gobject` | `pacman -S mingw-w64-i686-python3-gobject` |

After you have to play with `cd` and `ls` commands to enter in rpg-dark-fantasy folder next launch the program with : `python3 main.py`.
If it's not working, install python3 : `pacman -S python3`, then retry.

## TODO
- [x] Write a documentation
- [ ] Create some settings windows

## Images sources
Thank to [Teekatas Suwannakrua](https://raindropmemory.deviantart.com) for the icons.
* [Iconset: Legendora](http://www.iconarchive.com/show/legendora-icons-by-raindropmemory.html)
* [Iconset: Down To Earth Icons](http://www.iconarchive.com/show/down-to-earth-icons-by-raindropmemory.html)
    * [![RPG-icon.png](images/RPG-icon.png)](http://www.iconarchive.com/show/down-to-earth-icons-by-raindropmemory/G12-RPG-icon.html)
    
