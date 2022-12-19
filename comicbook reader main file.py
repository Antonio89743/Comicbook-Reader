import glob
import string
import os
from abc import ABC, abstractmethod
from cProfile import label
from logging import root
from msilib.schema import File
from kivy.config import Config
Config.set("input", "mouse", "mouse,multitouch_on_demand")
Config.set("graphics", "minimum_width", "700")
Config.set("graphics", "minimum_height", "400")
Config.set("kivy", "exit_on_escape", "0")
# config kivy window_icon
# graphics:
#  window_state 
# height
# width
# left
# position
# top
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.uix.card import MDCard
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDIconButton
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.image import Image as CoreImage
from kivy.uix.button import Button as KivyButton
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivy.core.window import Window
import os, string
from os.path import sep, expanduser, isdir, dirname, exists
import sys
import re
from glob import glob
import json
from io import StringIO 
import traceback
import logging
import imghdr
import sys
from zipfile import ZipFile
import io
import zipfile
import rarfile
from itertools import cycle
import kivy_garden.contextmenu as ContextMenu
from kivy.factory import Factory
import kivy as kivyscript

# test deleting file from directory and opening it once the file's location is already saved in app json



# get folders
# from them, get files
    # on open run this func with previously saved folders, try not to freeze app, only save new ones and don't touch older ones







class AbstractScanDirectoryManager(ABC):

    @abstractmethod
    def scan_local_directories():
        raise NotImplementedError("Must override scan_local_dictionaries")






class ScanDirectoryManager(): 

    @staticmethod
    def scan_all_directories():
        LocalScanDirectory.scan_local_directories()
        CloudScanDirectory.scan_local_directories()






class LocalScanDirectory(AbstractScanDirectoryManager):

    @staticmethod
    def scan_local_directories():
        print("am in methodB")

    @staticmethod
    def add_local_dictionary_to_scan_list():
        pass

    @staticmethod
    def remove_local_dictionary_from_scan_list():
        pass





class CloudScanDirectory(AbstractScanDirectoryManager):

    @staticmethod
    def scan_local_directories():
        print("am in meth")

    @staticmethod
    def add_local_dictionary_to_scan_list():
        pass

    @staticmethod
    def remove_local_dictionary_from_scan_list():
        pass


# only have one json file, in it save data about app, save local folders, cloud folders to scan


class ComicbookReaderGUI(MDApp):
    def build(self):
        self.title = "Comicbook Reader"
        # Window.bind(on_resize = self.window_resized)
        # Window.bind(on_restore = self.responsive_grid_layout)
        # Window.bind(on_maximize = self.responsive_grid_layout)
        # Window.bind(on_request_close = self.on_request_close)
        # Window.bind(on_key_down = self.on_key_down)
        # Window.bind(on_mouse_down = self.on_mouse_down)
        # Window.bind(mouse_pos = self.on_mouse_position_changed)
        return Builder.load_file("kivy.kv")
    
    def on_start(self):
        ScanDirectoryManager.scan_all_directories()
        # self.load_last_used_settings()
        # self.responsive_grid_layout()
        # self.create_local_folders_to_scan_expansion_panel()
        # self.local_folders_and_files_scan()
        # print(Config.get("graphics", "window_state"), Config.get("graphics", "fullscreen"))
        # Config.set("graphics", "window_state", "hidden")


ComicbookReaderGUI().run()






