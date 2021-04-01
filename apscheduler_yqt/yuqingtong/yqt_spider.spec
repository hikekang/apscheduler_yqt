# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['yqt_spider.py','config.py',
        'F:\项目\sina_yuqing\apscheduler_yqt\utils\file_helper.py',
        'F:\项目\sina_yuqing\apscheduler_yqt\utils\my_logger.py',
        'F:\项目\sina_yuqing\apscheduler_yqt\utils\my_pyautogui.py',
        'F:\项目\sina_yuqing\apscheduler_yqt\utils\mylogger.py',
        'F:\项目\sina_yuqing\apscheduler_yqt\utils\spider_helper.py',
        'F:\项目\sina_yuqing\apscheduler_yqt\utils\sql_helper.py',
        'F:\项目\sina_yuqing\apscheduler_yqt\utils\webdriverhelper.py',
],

             pathex=['F:\\项目\\sina_yuqing\\apscheduler_yqt\\yuqingtong'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='yqt_spider',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='yqt_spider')
