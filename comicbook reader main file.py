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
    def scan_directory():
        raise NotImplementedError("Must override scan_local_dictionaries")

class ScanDirectoryManager(): 

    @staticmethod
    def scan_all_directories():
        # for directory in 
        # LocalScanDirectory.scan_directory(directory)
        # CloudScanDirectory.scan_directory()

        # at the end call func to create all the widgets for authors and files
        pass


class LocalScanDirectory(AbstractScanDirectoryManager):

    @staticmethod
    def scan_directory(directory):
        cba_files = glob(directory + "/**/*.cba", recursive = True)
        cbr_files = glob(directory + "/**/*.cbr", recursive = True)
        cbz_files = glob(directory + "/**/*.cbz", recursive = True)
        cb7_files = glob(directory + "/**/*.cb7", recursive = True)

        for cba_file in cba_files:
            pass
        for cbr_file in cbr_files:
            pass

        for cbz_file in cbz_files:
            # save cover photo, title
            pass

        for cb7_file in cb7_files:
            pass

        # here create a dir of files
        
        LocalScanDirectory.save_scanned_files_dictionary()
        
    @staticmethod
    def save_scanned_files_dictionary():
        pass


    @staticmethod
    def add_local_dictionary_to_scan_list():
        pass

    @staticmethod
    def remove_local_dictionary_from_scan_list():
        pass





# class CloudScanDirectory(AbstractScanDirectoryManager):

#     @staticmethod
#     def scan_directory():
#         print("am in meth")

#     @staticmethod
#     def add_local_dictionary_to_scan_list():
#         pass

#     @staticmethod
#     def remove_local_dictionary_from_scan_list():
#         pass






















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

print(LocalScanDirectory.scan_directories(r"E:\Comic Books, Manga & Visual Novels"))

ComicbookReaderGUI().run()






