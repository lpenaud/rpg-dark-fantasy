# -*- mode: python -*-

import os
import site


gnome_path = os.path.join(site.getsitepackages()[1], 'gnome')
typelib_path = os.path.join(gnome_path, 'lib', 'girepository-1.0')
missing_files = []

for tl in ["GdkPixbuf-2.0.typelib", "GModule-2.0.typelib"] :
    missing_files.append((os.path.join(typelib_path, tl), "./gi_typelibs"))


block_cipher = None

added_files = [
    ('data','data'),
    ('glade', 'glade'),
    ('images', 'images'),
    ('README.md', '.'),
    ('LICENSE', '.')
]


a = Analysis(['main.py'],
             pathex=['utils', 'C:\\Users\\loic\\Documents\\git\\rpg-dark-fantasy'],
             binaries=missing_files,
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
	  icon='images/RPG-icon.ico',
          exclude_binaries=True,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Lottery')
