# -*- mode: python -*-

block_cipher = None

added_files = [
    ('data','data'),
    ('glade', 'glade'),
    ('images', 'images'),
    ('README.md', '.'),
    ('LICENSE', '.')
]

a = Analysis(['main.py'],
             pathex=['utils', '/data/home/loic/Documents/git/rpg-dark-fantasy'],
             binaries=[],
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
          icon='images/RPG-icon.png',
          exclude_binaries=True,
          name='Lottery',
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
               name='Lottery-linux')
