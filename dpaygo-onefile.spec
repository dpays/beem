# -*- mode: python -*-

import os
import glob
import platform
from PyInstaller.utils.hooks import exec_statement
import websocket
from os.path import join, dirname, basename

block_cipher = None
os_name = platform.system()
binaries = []

websocket_lib_path = dirname(websocket.__file__)
websocket_cacert_file_path = join(websocket_lib_path, 'cacert.pem')
analysis_data = [
    # For websocket library to find "cacert.pem" file, it must be in websocket
    # directory inside of distribution directory.
    # This line can be removed once PyInstaller adds hook-websocket.py
    (websocket_cacert_file_path, join('.', basename(websocket_lib_path)))
]


a = Analysis(['dpaygo/cli.py'],
             pathex=['dpaygo'],
             binaries=binaries,
             datas=analysis_data,
             hiddenimports=['scrypt', 'websocket'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['matplotlib', 'scipy', 'pandas', 'numpy', 'PyQt5', 'tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='dpay',
          debug=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=True,
          icon='dpay.ico',
 )

if platform.system() == 'Darwin':
    info_plist = {'NSHighResolutionCapable': 'True', 'NSPrincipalClass': 'NSApplication'}
    app = BUNDLE(exe,
                 name='dpay.app',
                 icon='dpay.ico',
                 bundle_identifier=None
                )