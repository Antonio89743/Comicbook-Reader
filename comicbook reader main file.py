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
        print(directory, "gogogo")






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
    def add_local_dictionary_to_scan_list(directory):
        unique_folder = True
        folder_selected_string = str(directory)
        if exists("Book Worm\Book Worm\local_folders_to_scan.json"):
            file = open("Book Worm\Book Worm\local_folders_to_scan.json", "r")
            json_file_data = file.read()
            file.close()
            if json_file_data != "":
                list_of_folders_to_scan = eval(json_file_data)
                folder_selected_string_path = re.sub("/+", "/", folder_selected_string[2:-2])
                for folder in list_of_folders_to_scan:
                    folder_path = re.sub("/+", "/", folder)
                    if folder_path == folder_selected_string_path:
                        unique_folder = False

                        
        # if unique_folder == True:
        #     self.Folder_To_Scan_Card(self, directory)
        # self.list_of_files = scan_folders.scan_folders(folder_selected_string, unique_folder)
        # self.create_authors_dictionary()
        # self.add_main_menu_widgets()
        LocalScanDirectory.scan_directory(directory)

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



class LocalFolderPopUp(Popup):
    class DriveButton():
        def __init__(self, app, drive):
            app.ids.folder_chooser_box_layout_vertical.add_widget(
            KivyButton(
                text = drive,
                pos_hint = {"top": 1},
                size_hint = (1, None),
                height = 70,
                on_press = lambda x: app.drive_chosen(app, drive)
                )
            )

    def drive_chosen(self, app, drive):
        app.ids.folder_chooser.rootpath = drive

    def add_drives(self):
        available_drives = ["%s:" % d for d in string.ascii_uppercase if os.path.exists("%s:" % d)]
        for drive in available_drives:
            self.DriveButton(self, drive)

class AddLocalFolderToScanDialog():
    '''AddLocalFolderToScanDialog'''

class LocalFoldersExpansionPanelContent(BoxLayout):
    '''LocalFoldersExpansionPanelContent'''
        
class ScreenManager():

    app = None
    screen_currently_in_use :int = 0
    previous_screens_and_tabs_list = ["Main Menu"]

    def __init__(self, app):
        self.app = app

    def go_forward_to_next_tab_or_screen(self):
        self.change_screen(self.previous_screens_and_tabs_list[self.screen_currently_in_use + 1], True)

    def return_to_previous_tab_or_screen(self):
        self.screen_currently_in_use -= 1
        self.change_screen(self.previous_screens_and_tabs_list[self.screen_currently_in_use], True)
    
    def change_screen(self, screen, using_return_bool):
        self.app.root.ids.screen_manager.current = screen
        self.previous_screens_and_tabs_list.append(screen)
        if using_return_bool == False:
            self.screen_currently_in_use += 1

class WidgetManager():

    reading_sign_collections_navbar_card_pulled_out = None

    def __init__(self, app):
        self.app = app

    def change_widget_height(self, widget_id, new_value):
        animation = Animation(height = new_value)
        if widget_id == self.app.root.ids.toolbar:
            if self.app.root.ids.toolbar.height != new_value:
                animation.start(self.app.root.ids.toolbar)
        elif widget_id == self.app.root.ids.reading_sign_collections_navbar_card:
            if self.app.root.ids.reading_sign_collections_navbar_card.height != new_value:
                animation.start(self.app.root.ids.reading_sign_collections_navbar_card)

    def change_widget_width(self, widget_id, new_value):
        animation = Animation(width = new_value, duration = 0.3)
        try:
            if widget_id == self.app.root.ids.reading_sign_collections_navbar_card:
                if self.app.root.ids.reading_sign_collections_navbar_card.width != new_value:
                    animation.start(self.app.root.ids.reading_sign_collections_navbar_card, )
                    if new_value != 0:
                        self.reading_sign_collections_navbar_card_pulled_out = True #####################################
            elif widget_id == self.app.root.ids.navbar:
                    if self.app.root.ids.navbar.width != new_value:
                        animation.start(self.app.root.ids.navbar)            
        except AttributeError:
            print("AttributeError, change_widget_width", widget_id)

    def change_widget_opacity(self, widget_id, new_value):
        animation = Animation(opacity = new_value)
        if widget_id == self.app.root.ids.toolbar:
            if self.app.root.ids.toolbar.opacity != new_value:
                animation.start(self.app.root.ids.toolbar)

class InputManager:
    def __init__(self, app):
        self.app = app

    def on_mouse_down(self, *args):
        print("Mouse input:", args)
        if args[3] == "mouse5":
            self.go_forward_to_next_tab_or_screen()
        if args[3] == "mouse4":
            self.return_to_previous_tab_or_screen()

        if args[3] == "scrollup":
            self.mouse_button_and_keayboard_input(args[3])
        if args[3] == "scrolldown":
            self.mouse_button_and_keayboard_input(args[3])

    def on_key_down(self, *args):
        print("Keyboard input:", args)
        if args[3] == "y" and str(args[4]) == "['ctrl']":
            pass
        if args[3] == "z" and str(args[4]) == "['ctrl']":
            pass
        if str(args[4]) == "['ctrl']":
            self.keyboard_ctrl_button_pressed = True
        else:
            self.keyboard_ctrl_button_pressed = False
        if args[1] == 27:
            self.change_screen("Settings Screen", False)
        if args[1] == 1073742085:
            self.on_pause_resume_audio_file_button_pressed()

class MDWidgetManager:
    def __init__(self, app):
        self.app = app

    def create_local_folders_to_scan_expansion_panel(self):
        local_folders_to_scan_expansion_panel = MDExpansionPanel(
                content = LocalFoldersExpansionPanelContent(),
                panel_cls = MDExpansionPanelOneLine(
                    text = "Local Folders To Scan",
                    size_hint = (1, None)
                    )
                )   
        self.app.root.ids["local_folders_to_scan_expansion_panel"] = local_folders_to_scan_expansion_panel
        self.app.root.ids.settings_scanning_local_folders_tab_box_layout.add_widget(local_folders_to_scan_expansion_panel)
        # if exists("Book Worm\Book Worm\local_folders_to_scan.json"):
        #     file = open("Book Worm\Book Worm\local_folders_to_scan.json", "r")
        #     json_file_data = file.read()
        #     file.close()
        #     if json_file_data != "":
        #         list_of_folders_to_scan = eval(json_file_data)
        #         for folder in list_of_folders_to_scan:
        #             self.Folder_To_Scan_Card(self, folder)

class ComicbookReaderGUI(MDApp):

    local_scan_directory_class = LocalScanDirectory





    def on_mouse_position_changed(self, window_object, mouse_position):
        # self.check_mouse_position_on_navbar(mouse_position)
        pass

    # def check_mouse_position_on_navbar(self, mouse_position):
    #     if self.root.ids.screen_manager.current == "Read Currently Open File Screen":
    #         if self.root.ids.navbar.width < 50:
    #             if mouse_position[0] <= self.root.ids.navbar.pos[0] + self.navbar_width_max:
    #                 self.change_widget_width(self.root.ids.navbar, 50)
    #         elif self.root.ids.navbar.width == 50:
    #             if mouse_position[0] > 50:
    #                 self.change_widget_width(self.root.ids.navbar, 0)
    #     if self.reading_sign_collections_navbar_card_pulled_out == True:
    #         # if mouse_position[0] isnt between widget width
    #             # and if mouse_position[1] isnt between widget height
    #             # self.change_widget_width(self.root.ids.reading_sign_collections_navbar_card, 0)
    #         pass

    def build(self):
        self.title = "Comicbook Reader"
        # Window.bind(on_resize = self.window_resized)
        # Window.bind(on_restore = self.responsive_grid_layout)
        # Window.bind(on_maximize = self.responsive_grid_layout)
        # Window.bind(on_request_close = self.on_request_close)
        Window.bind(mouse_pos = self.on_mouse_position_changed)
        self.screen_manager_object = ScreenManager(MDApp.get_running_app())
        self.widget_manager_object = WidgetManager(MDApp.get_running_app())
        self.input_manager_object = InputManager(MDApp.get_running_app())
        self.md_widget_manager_object = MDWidgetManager(MDApp.get_running_app())
        Window.bind(on_key_down = self.input_manager_object.on_key_down)
        Window.bind(on_mouse_down = self.input_manager_object.on_mouse_down)
        return Builder.load_file("kivy.kv")
    
    def on_start(self):
        ScanDirectoryManager.scan_all_directories()
        # self.load_last_used_settings()
        # self.responsive_grid_layout()
        self.md_widget_manager_object.create_local_folders_to_scan_expansion_panel()
        # self.local_folders_and_files_scan()
        # print(Config.get("graphics", "window_state"), Config.get("graphics", "fullscreen"))
        # Config.set("graphics", "window_state", "hidden")

ComicbookReaderGUI().run()






