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
from pathlib import Path
import cbz_file_data

# test deleting file from directory and opening it once the file's location is already saved in app json


# get folders
# from them, get files
    # on open run this func with previously saved folders, try not to freeze app, only save new ones and don't touch older ones


class Globals():

    array_of_valid_files = []
    main_menu_files_widgets_height = 1000 #None 
    main_menu_files_widgets_width = 600 #None
    main_menu_authors_tab_widgets_height = None
    main_menu_authors_tab_widgets_width = None

class Folder_To_Scan_Card():
    def __init__(self, app, directory): # this func is still unfinished
        card = MDCard(
            orientation = "vertical",
            size_hint = (1, None),
            radius = [0, 0, 0, 0],
            md_bg_color = (0, 0, 0, 1),
            pos_hint = {"center_x": 0.5, "top": 1}
        )
        folder_path_label = Label(
            text = directory
        )
        card.add_widget(folder_path_label)
        remove_folder_from_scan_list_button = KivyButton(
            on_press = lambda x: self.remove_folder_from_scan_list(app, card, directory),
            text = "X",
            size = (50, 50),
            pos_hint = {"top": 1, "right": 1} 
        )
        card.add_widget(remove_folder_from_scan_list_button)
        app.root.ids.local_folders_to_scan_expansion_panel.content.ids.local_folders_to_scan_expansion_panel_content_box_layout_folders_widget_list.add_widget(card)

        # this isn't really doing anything
        app.root.ids.local_folders_to_scan_expansion_panel.content.height = app.root.ids.local_folders_to_scan_expansion_panel.content.minimum_height
        app.root.ids.local_folders_to_scan_expansion_panel.content.bind(minimum_height = app.root.ids.local_folders_to_scan_expansion_panel.content.setter("height"))

        # the problem might be the first box view in 'content' kv, not the second one

        # app.root.ids.local_folders_to_scan_expansion_panel.close_panel(app.root.ids.local_folders_to_scan_expansion_panel, app.root.ids.local_folders_to_scan_expansion_panel)
        # # Exception has occurred: TypeError
        # # MDExpansionPanel.close_panel() missing 2 required positional arguments: 'instance_expansion_panel' and 'press_current_panel'
        # app.root.ids.local_folders_to_scan_expansion_panel.open_panel()

        # fix position in regards to expansion panel and it going up
        # maybe just fix height

        # it's fine on reopening the expansion panel, so maybe just do that? 
        # or just do minimal size?

    def remove_folder_from_scan_list(self, app, card, directory): # this func is still unfinished
        app.root.ids.local_folders_to_scan_expansion_panel.content.ids.local_folders_to_scan_expansion_panel_content_box_layout_folders_widget_list.remove_widget(card)
        # resize expansion panel
        app.root.ids.local_folders_to_scan_expansion_panel.content.height = app.root.ids.local_folders_to_scan_expansion_panel.content.minimum_height
        # which one of the next 2 lines should be executed first?
        self.remove_folder_from_list_of_folders_json(directory)
        self.remove_folder_files_from_file_dictionary_json(app, directory)
        # what if files has been removed but is still open in album viewer/file deatails/file reader screen?

    def remove_folder_from_list_of_folders_json(self, directory):   
        if exists(SaveFileManager.local_directories_to_scan_save_file_location):
            file = open(SaveFileManager.local_directories_to_scan_save_file_location, "r")
            json_file_data = file.read()
            file.close()
            if json_file_data != "":
                list_of_directories_to_scan = eval(json_file_data)
                if directory in list_of_directories_to_scan:
                    file = open(SaveFileManager.local_directories_to_scan_save_file_location, "w")
                    list_of_directories_to_scan.remove(directory)
                    file.write(json.dumps(list_of_directories_to_scan))
                    file.close()

    def remove_folder_files_from_file_dictionary_json(self, app, folder): # this func is still unfinished
        list_of_subfolders = [x[0] for x in os.walk(folder)]
        # as it stands, to remove folder you've gotta open the file bellow twice, cut down on that
        local_folders_to_scan = open(SaveFileManager.local_directories_to_scan_save_file_location, "r")
        string_of_local_folders_to_scan = local_folders_to_scan.read()
        local_folders_to_scan.close()
        list_of_local_folders_to_scan = eval(string_of_local_folders_to_scan)
        for folder_to_scan in list_of_local_folders_to_scan:
            folder_to_scan = folder_to_scan.replace("\\\\", "\\")
            folder_to_scan = folder_to_scan.replace("\\\\", "\\")
            folder_to_scan = re.sub("/+", "/", folder_to_scan)
        with open(SaveFileManager.array_of_local_files) as local_files_dictionary:
            try:
                local_folders_to_scan_dictionary = json.load(local_files_dictionary)
                for subfolder in list_of_subfolders:
                    subfolder_path = subfolder.replace("\\\\", "\\")
                    if subfolder_path not in list_of_local_folders_to_scan:
                        for file in local_folders_to_scan_dictionary[:]:
                            try:
                                if file["file_format"] in app.music_tag_compatible_file_formats:
                                    for album_track in file["album_tracks_dictionary"]:
                                        album_track_path = album_track["absolute_file_path"]
                                        file_absolute_path = album_track_path.replace("\\\\", "\\")
                                        file_absolute_path = file_absolute_path.replace("\\\\", "\\")
                                        if subfolder_path in file_absolute_path:
                                            local_folders_to_scan_dictionary.remove(file)  
                                            # why isn't nabokov audio book sample getting removed?
                                else:
                                    file_absolute_path = file["absolute_file_path"].replace("\\\\", "\\")
                                    file_absolute_path = file_absolute_path.replace("\\\\", "\\") 
                                    if subfolder_path in file_absolute_path:
                                        local_folders_to_scan_dictionary.remove(file)    
                            except TypeError:
                                print("TypeError, remove_folder_files_from_file_dictionary_json(", folder, ")", file["absolute_file_path"]) 
            except Exception:
                logging.error(traceback.format_exc())
            folder_path = folder.replace("\\\\", "\\")
            for file in local_folders_to_scan_dictionary[:]:
                try:
                    if file["file_format"] in app.music_tag_compatible_file_formats:
                        for album_track in file["album_tracks_dictionary"]:
                            album_track_path = album_track["absolute_file_path"]
                            file_absolute_path = album_track_path.replace("\\\\", "\\")
                            file_absolute_path = file_absolute_path.replace("\\\\", "\\")
                            if subfolder_path in file_absolute_path:
                                local_folders_to_scan_dictionary.remove(file)  
                    file_path = re.sub("/+", "/", file["absolute_file_path"])
                    file_path_without_folder = file_path.removeprefix(folder_path)
                    if file_path_without_folder[0] == "\\":
                        file_path_without_folder = file_path_without_folder[1:]
                    if ("/" not in file_path_without_folder) and ("\\" not in file_path_without_folder):
                        local_folders_to_scan_dictionary.remove(file)   
                except TypeError:
                    print("TypeError", file["absolute_file_path"])
                except AttributeError:
                    print("AttributeError", file["absolute_file_path"])
                except Exception:
                    logging.error(traceback.format_exc())
            if not local_folders_to_scan_dictionary:
                file = open(SaveFileManager.array_of_local_files, "w")
                file.close()  
            else:
                file = open(SaveFileManager.array_of_local_files, "w")
                file.write(json.dumps(local_folders_to_scan_dictionary))
                file.close()  
        app.local_folders_and_files_scan()

class SaveFileManager:

    save_folder_location = "save_files"
    local_directories_to_scan_save_file_location = save_folder_location + "/local_directories_to_scan.json"
    array_of_local_files = save_folder_location + "/array_of_local_files.json"

    def create_save_directory_and_save_files():
        if exists(SaveFileManager.local_directories_to_scan_save_file_location) == False:
            os.makedirs(os.path.dirname(SaveFileManager.local_directories_to_scan_save_file_location), exist_ok = True)
        # check if all other save files exist, else, create them

class AbstractScanDirectoryManager(ABC):

    @abstractmethod
    def scan_directory():
        raise NotImplementedError("Must override scan_local_dictionaries")

class ScanDirectoryManager(): 

    @staticmethod
    def scan_all_directories():
        LocalScanDirectory.scan_all_directories()

        # check if local json with directories exists
            # if it does, enter it, iterate it and for each directory call local scan func
            # else, create that file





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
        for cb7_file in cb7_files:
            pass
    
        for cbz_file in cbz_files:
            absolute_path_to_file = os.path.abspath(cbz_file)
            if not any(dictionary["absolute_file_path"] == absolute_path_to_file for dictionary in Globals.array_of_valid_files):
                file_title = cbz_file_data.get_cbz_file_title(absolute_path_to_file)
                file_cover = cbz_file_data.get_cbz_cover_image(absolute_path_to_file)
                Globals.array_of_valid_files.append({
                    "absolute_file_path" : absolute_path_to_file, 
                    "file_format" : "cbz", 
                    "file_name" : file_title, 
                    "file_author" : None,
                    "file_cover" : file_cover,
                    "release_date" : None,
                    "date_added" : None,
                    "publisher" : None, 
                    "genre" : None, # this could be an list?
                    "date_most_recently_opened" : None, 
                    "country_of_origin" : None,
                    "language" : None,
                    "file_size" : None})

        # cb_files = {"cbz_files" : cbz_files, "cbr_files" : cbr_files}

        # mp3_files = glob.glob(folders_to_scan + "/**/*.mp3", recursive = True)
        # wav_files = glob.glob(folders_to_scan + "/**/*.wav", recursive = True)
        # ogg_files = glob.glob(folders_to_scan + "/**/*.ogg", recursive = True)
        # aac_files = glob.glob(folders_to_scan + "/**/*.aac", recursive = True)
        # flac_files = glob.glob(folders_to_scan + "/**/*.flac", recursive = True)
        # music_tag_compatible_audio_files = []
        # music_tag_compatible_audio_files.extend(mp3_files)
        # music_tag_compatible_audio_files.extend(wav_files)
        # music_tag_compatible_audio_files.extend(ogg_files)
        # music_tag_compatible_audio_files.extend(aac_files)
        # music_tag_compatible_audio_files.extend(flac_files)
        # list_of_albums = []
        # list_of_tracks = []
        # for music_tag_compatible_audio_file in music_tag_compatible_audio_files:
        #     absolute_path_to_file = os.path.abspath(music_tag_compatible_audio_file)
        #     if absolute_path_to_file.endswith(".mp3"):
        #         file_format = "mp3"
        #     elif absolute_path_to_file.endswith(".wav"):
        #         file_format = "wav"
        #     elif absolute_path_to_file.endswith(".ogg"):
        #         file_format = "ogg"
        #     elif absolute_path_to_file.endswith(".aac"):
        #         file_format = "aac"
        #     elif absolute_path_to_file.endswith(".flac"):
        #         file_format = "flac"
        #     file_album_title = audio_file_data_music_tag.get_audio_file_data_music_tag_album_name(absolute_path_to_file)
        #     file_album_artist = audio_file_data_music_tag.get_audio_file_data_music_tag_album_artist(absolute_path_to_file)
        #     file_album_total_track_number = audio_file_data_music_tag.get_audio_file_data_music_tag_total_tracks(absolute_path_to_file)
        #     file_album_total_disk_number = audio_file_data_music_tag.get_audio_file_data_music_tag_total_discs(absolute_path_to_file)
        #     file_album_release_year = audio_file_data_music_tag.get_audio_file_data_music_tag_release_year(absolute_path_to_file)
        #     album_dictionary = {
        #         "file_album_title" : file_album_title,
        #         "file_album_artist" : file_album_artist,
        #         "file_album_total_track_number" : file_album_total_track_number,
        #         "file_album_total_disk_number" : file_album_total_disk_number,
        #         "file_album_release_year" : file_album_release_year}
        #     list_of_albums.append(album_dictionary)
        #     track_title = audio_file_data_music_tag.get_audio_file_data_music_tag_title(absolute_path_to_file)
        #     track_artist = audio_file_data_music_tag.get_audio_file_data_music_tag_artist(absolute_path_to_file)
        #     track_number = audio_file_data_music_tag.get_audio_file_data_music_tag_track_number(absolute_path_to_file)
        #     track_genre = audio_file_data_music_tag.get_audio_file_data_music_tag_genre(absolute_path_to_file)
        #     track_lenght = audio_file_data_music_tag.get_audio_file_data_music_tag_length(absolute_path_to_file)
        #     track_dictionary = {
        #         "track_album_title" : file_album_title,
        #         "file_album_artist" : file_album_artist,
        #         "file_album_total_track_number" : file_album_total_track_number,
        #         "file_album_total_disk_number" : file_album_total_disk_number,
        #         "file_album_release_year" : file_album_release_year,
        #         "track_title" : track_title,
        #         "track_artist" : track_artist,
        #         "track_number" : track_number,
        #         "track_genre" : track_genre,
        #         "track_lenght" : track_lenght,
        #         "absolute_file_path" : absolute_path_to_file,
        #         "file_format" : file_format}
        #     list_of_tracks.append(track_dictionary)
        # list_of_unique_albums = list(map(dict, set(tuple(sorted(sub.items())) for sub in list_of_albums)))
        # for album in list_of_unique_albums:
        #     album_genres = []
        #     album_tracks_dictionary = []
        #     for track in list_of_tracks:
        #         if album["file_album_title"] == track["track_album_title"] and album["file_album_artist"] == track["file_album_artist"]:
        #             if album["file_album_total_track_number"] == track["file_album_total_track_number"] and album["file_album_total_disk_number"] == track["file_album_total_disk_number"]:
        #                 album_tracks_dictionary.append(track)
        #                 album_genres.append(track["track_genre"])
        #                 album_genres = [*set(album_genres)]
        #                 album_file_format = track["file_format"] + "_album"
        #     array_of_valid_files.append({
        #         "absolute_file_path" : None, 
        #         "file_format" : album_file_format,
        #         "file_name" : album["file_album_title"], 
        #         "file_author" : album["file_album_artist"],
        #         "file_cover" : None,
        #         "release_date" : album["file_album_release_year"],
        #         "album_tracks_dictionary" : album_tracks_dictionary,
        #         "date_added" : None,
        #         "publisher" : None, 
        #         "album_genre" : album_genres,
        #         "date_most_recently_opened" : None, 
        #         "country_of_origin" : None,
        #         "language" : None,
        #         "file_size" : None})
            # mobi_files = glob.glob(folder + "/**/*.mobi", recursive = True)
            # for mobi_file in mobi_files:
    #             absolute_path_to_file = os.path.abspath(mobi_file)
    #             if array_or_mobi_files.count(absolute_path_to_file) == 0 :
    #                 array_or_mobi_files.append(absolute_path_to_file)
    #         pdf_files = glob.glob(folder + "/**/*.pdf", recursive = True)
    #         for pdf_file in pdf_files:
    #             absolute_path_to_file = os.path.abspath(pdf_file)
    #             if array_or_pdf_files.count(absolute_path_to_file) == 0 :
    #                 array_or_pdf_files.append(absolute_path_to_file)
    #         doc_files = glob.glob(folder + "/**/*.doc", recursive = True)
    #         for doc_file in doc_files:
    #             absolute_path_to_file = os.path.abspath(doc_file)
    #             if array_or_doc_files.count(absolute_path_to_file) == 0 :
    #                 array_or_doc_files.append(absolute_path_to_file)
    #         docx_files = glob.glob(folder + "/**/*.docx", recursive = True)
    #         for docx_file in docx_files:
    #             absolute_path_to_file = os.path.abspath(docx_file)
    #             if array_or_docx_files.count(absolute_path_to_file) == 0 :
    #                 array_or_docx_files.append(absolute_path_to_file)
    #         kpf_files = glob.glob(folder + "/**/*.kpf", recursive = True)
    #         for kpf_file in kpf_files:
    #             absolute_path_to_file = os.path.abspath(kpf_file)
    #             if array_or_kpf_files.count(absolute_path_to_file) == 0 :
    #                 array_or_kpf_files.append(absolute_path_to_file)
    #         cbr_files = glob.glob(folder + "/**/*.cbr", recursive = True)
    #         for cbr_file in cbr_files:
    #             absolute_path_to_file = os.path.abspath(cbr_file)
    #             if array_or_cbr_files.count(absolute_path_to_file) == 0 :
    #                 array_or_cbr_files.append(absolute_path_to_file)
        # epub_files = glob.glob(folder + "/**/*.epub", recursive = True)
        # for epub_file in epub_files:
        #     absolute_path_to_file = os.path.abspath(epub_file)
        #     if not any(dictionary["absolute_file_path"] == absolute_path_to_file for dictionary in array_of_valid_files):
        #         file_title = epub_file_data.get_epub_book_title(absolute_path_to_file)
        #         file_author = epub_file_data.get_epub_book_author(absolute_path_to_file)
        #         file_cover = epub_file_data.get_epub_cover_image_path(absolute_path_to_file)
        #         array_of_valid_files.append({
        #             "absolute_file_path" : absolute_path_to_file, 
        #             "file_format" : "epub", 
        #             "file_name" : file_title, 
        #             "file_author" : file_author,
        #             "file_cover" : file_cover,
        #             "release_date" : None,
        #             "date_added" : None,
        #             "publisher" : None, 
        #             "genre" : None, # this could be an list?
        #             "date_most_recently_opened" : None, 
        #             "country_of_origin" : None,
        #             "language" : None,
        #             "file_size" : None})
        # txt_files = glob.glob(folders_to_scan + "/**/*.txt", recursive = True)
        # for txt_file in txt_files:
        #     absolute_path_to_file = os.path.abspath(txt_file)
        #     if not any(dictionary["absolute_file_path"] == absolute_path_to_file for dictionary in array_of_valid_files):
        #         file_title = text_file_data.get_txt_file_name(absolute_path_to_file)
        #         array_of_valid_files.append({
        #             "absolute_file_path" : absolute_path_to_file, 
        #             "file_format" : "txt", 
        #             "file_name" : file_title, 
        #             "file_author" : None,
        #             "release_date" : None,
        #             "date_added" : None,
        #             "publisher" : None, 
        #             "genre" : None, # this could be an list?
        #             "date_most_recently_opened" : None, 
        #             "country_of_origin" : None,
        #             "language" : None,
        #             "file_size" : None}) 
        LocalScanDirectory.save_scanned_files_dictionary()
        
    @staticmethod
    def scan_all_directories():
        if exists(SaveFileManager.local_directories_to_scan_save_file_location):
            file = open(SaveFileManager.local_directories_to_scan_save_file_location, "r")
            json_file_data = file.read()
            file.close()
            if json_file_data != "":
                print(eval(json_file_data))


                # self.list_of_files = scan_folders.scan_folders(eval(json_file_data), False)


                # LocalScanDirectory.scan_directory(directory_string_posix)
                # MainMenuFilesWidget(app)

        # list_of_local_directories_to_scan = 
        # for directory in :
        #     LocalScanDirectory.scan_directory(directory)

    @staticmethod
    def save_scanned_files_dictionary():
        data = json.dumps(Globals.array_of_valid_files)
        file = open(SaveFileManager.array_of_local_files, "w")
        file.write(data)
        file.close()    

    @staticmethod
    def add_local_dictionary_to_scan_list(app, directory):
        directory_string_posix = Path(str(directory)[2:-2]).as_posix()
        unique_directory = True
        SaveFileManager.create_save_directory_and_save_files()
        try:
            if exists(SaveFileManager.local_directories_to_scan_save_file_location):
                file = open(SaveFileManager.local_directories_to_scan_save_file_location, "r+")
                json_file_data = file.read()
                if json_file_data != "":
                    list_of_folders_to_scan = eval(json_file_data)
                    if directory_string_posix in list_of_folders_to_scan:
                        unique_directory = False
                    else:
                        list_of_folders_to_scan.append(directory_string_posix)
                        with open(SaveFileManager.local_directories_to_scan_save_file_location, "w") as local_directories_to_scan_save_file:
                            json.dump(list_of_folders_to_scan, local_directories_to_scan_save_file)
                elif json_file_data == "":
                    folders_to_scan_list : list = []
                    folders_to_scan_list.append(directory_string_posix)
                    file.write(json.dumps(folders_to_scan_list))
                file.close() 
        except:
            traceback.print_exc()
        if unique_directory == True:
            Folder_To_Scan_Card(app, directory_string_posix)
        LocalScanDirectory.scan_directory(directory_string_posix)
        MainMenuFilesWidget(app)
        # self.create_authors_dictionary()
        # self.add_main_menu_widgets()

class MainMenuFilesWidget():
    def __init__(self, app):
        for file in Globals.array_of_valid_files:
            self.create_main_menu_files_widget(app, file)

    def create_main_menu_files_widget(self, app, file):
        if file["file_format"] == "txt":
            file_title = file["file_name"]
            card = MDCard(
                    orientation = "vertical",
                    size_hint = (None, None),
                    height = Globals.main_menu_files_widgets_height,
                    width = Globals.main_menu_files_widgets_width,
                    radius = [0, 0, 0, 0],
                    md_bg_color = (0, 0, 0, 0)
                )
            app.root.ids.main_menu_grid_layout.add_widget(card)
            if file_title != None:
                file_title_button = KivyButton(
                        on_press = lambda x: app.change_screen("Read Currently Open File Screen", False),
                        text = file_title,
                        color = (0, 0, 0, 1),
                        size_hint = (1, None),
                        height = 50,
                        # width = 300,
                    )
            else:
                file_title_button = KivyButton(
                    on_press = lambda x: app.change_screen("Read Currently Open File Screen", False),
                    text = "File Title Not Found",
                    color = (0, 0, 0, 1),
                    size_hint = (1, None),
                    height = 50,
                    # width = 300,
                )
            file_title_button.bind(on_press = lambda x: app.load_file_read_screen(file))  
            card.add_widget(file_title_button)   
        elif file["file_format"] == "epub":
            file_title = file["file_name"]
            file_author = file["file_author"]
            file_cover = zipfile.ZipFile(file["absolute_file_path"]).read(file["file_cover"])
            card = MDCard(
                    orientation = "vertical",
                    size_hint = (None, None),
                    height = Globals.main_menu_files_widgets_height,
                    width = Globals.main_menu_files_widgets_width,
                    radius = [0, 0, 0, 0],
                    md_bg_color = (0, 0, 0, 0)
                )
            app.root.ids.main_menu_grid_layout.add_widget(card)
            if file_cover != None:
                cover_image = CoreImage(io.BytesIO(file_cover), ext = "jpg")
                file_cover_button = KivyButton(
                    background_color = (0, 0, 0, 0),
                    pos_hint = {"bottom": 1}
                    )
                file_cover_image = Image(
                    texture = CoreImage(cover_image).texture,
                    allow_stretch = True,
                    keep_ratio = True,
                    pos_hint = {"bottom": 1},
                    )
                file_cover_button.bind(size = file_cover_image.setter("size"))
                file_cover_button.bind(pos = file_cover_image.setter("pos"))
                file_cover_button.add_widget(file_cover_image)
            else:
                file_cover_button = KivyButton(
                    on_press = lambda x: app.change_screen("Read Currently Open File Screen", False),
                    text = "File Cover Image Not Found",
                    color = (0, 0, 0, 1),
                    size_hint = (1, None),
                    height = 50,
                    # width = 300,
                )
            file_cover_button.bind(on_press = lambda button: app.main_menu_file_widget_pressed(file, button))
            card.add_widget(file_cover_button)                         
            if file_title != None:
                file_title_button = KivyButton(
                    on_press = lambda x: app.change_screen("Read Currently Open File Screen", False),
                    text = file_title,
                    color = (0, 0, 0, 1),
                    size_hint = (1, None),
                    height = 50,
                    # width = 300,
                )
            else:
                file_title_button = KivyButton(
                on_press = lambda x: app.change_screen("Read Currently Open File Screen", False),
                text = "File Title Not Found",
                color = (0, 0, 0, 1),
                size_hint = (1, None),
                height = 50,
                # width = 300,
                )
            file_title_button.bind(on_press = lambda x: app.load_file_read_screen(file))  
            card.add_widget(file_title_button)
            if file_author != None:
                file_author_button = KivyButton(
                    text = file_author,
                    color = (0, 0, 0, 1),
                    size_hint = (1, None),
                    height = 50,
                    # width = 300,
                    )
                file_author_button.bind(on_press = lambda button: app.main_menu_author_widget_pressed(button, app.authors_dictionary[file_author]))
            else:
                file_author_button = KivyButton(
                text = "File Author Not Found",
                color = (0, 0, 0, 1),
                size_hint = (1, None),
                height = 50,
                # width = 300,
                ) 
            card.add_widget(file_author_button)
        elif file["file_format"] == "cbz":
            file_title = cbz_file_data.get_cbz_file_title(file["absolute_file_path"])
            file_author = file["file_author"]
            file_cover = zipfile.ZipFile(file["absolute_file_path"]).read(file["file_cover"])
            card = MDCard(
                    orientation = "vertical",
                    size_hint = (None, None),
                    height = Globals.main_menu_files_widgets_height,
                    width = Globals.main_menu_files_widgets_width,
                    radius = [0, 0, 0, 0],
                    md_bg_color = (0, 0, 0, 0)
                )
            app.root.ids.main_menu_files_tab_grid_layout.add_widget(card)
            if file_cover != None:
                cover_image = CoreImage(io.BytesIO(file_cover), ext = "jpg")
                file_cover_button = KivyButton(
                    background_color = (0, 0, 0, 0),
                    pos_hint = {"bottom": 1}
                    )
                file_cover_image = Image(
                    texture = CoreImage(cover_image).texture,
                    allow_stretch = True,
                    keep_ratio = True,
                    pos_hint = {"bottom": 1},
                    )
                file_cover_button.bind(size = file_cover_image.setter("size"))
                file_cover_button.bind(pos = file_cover_image.setter("pos"))
                file_cover_button.add_widget(file_cover_image)
            else:
                file_cover_button = KivyButton(
                    on_press = lambda x: app.change_screen("Read Currently Open File Screen", False),
                    text = "File Cover Image Not Found",
                    color = (0, 0, 0, 1),
                    size_hint = (1, None),
                    height = 50,
                    # width = 300,
                )
            file_cover_button.bind(on_press = lambda button: app.main_menu_file_widget_pressed(file, button))
            card.add_widget(file_cover_button)                       
            if file_title != None:
                file_title_button = KivyButton(
                    on_press = lambda x: app.change_screen("Read Currently Open File Screen", False),
                    text = file_title,
                    color = (0, 0, 0, 1),
                    size_hint = (1, None),
                    height = 50,
                    # width = 300,
                    )
            else:
                file_title_button = KivyButton(
                on_press = lambda x: app.change_screen("Read Currently Open File Screen", False),
                text = "File Title Not Found",
                color = (0, 0, 0, 1),
                size_hint = (1, None),
                height = 50,
                # width = 300,
                )
            file_title_button.bind(on_press=lambda x: app.load_file_read_screen(file))  
            card.add_widget(file_title_button)
        elif file["file_format"] == "cbr":
            file_title = cbr_file_data.get_cbr_file_title(file["absolute_file_path"])
            file_author = file["file_author"]
            print(file["file_cover"], type(file["file_cover"]))
            # cbr_file_data.get_cbr_file_content(file["absolute_file_path"])
            # file_cover = rarfile.RarFile(file["absolute_file_path"])
            # file_cover.read(file["file_cover"])
            # print(file_cover, type(file_cover))
            file_cover = None
            card = MDCard(
                    orientation = "vertical",
                    size_hint = (None, None),
                    height = Globals.main_menu_files_widgets_height,
                    width = Globals.main_menu_files_widgets_width,
                    radius = [0, 0, 0, 0],
                    md_bg_color = (0, 0, 0, 0)
                )
            app.root.ids.main_menu_grid_layout.add_widget(card)
            if file_cover != None:
                cover_image = CoreImage(io.BytesIO(file_cover), ext = "jpg")
                file_cover_button = KivyButton(
                    background_color = (0, 0, 0, 0),
                    pos_hint = {"bottom": 1}
                    )
                file_cover_image = Image(
                    texture = CoreImage(cover_image).texture,
                    allow_stretch = True,
                    keep_ratio = True,
                    pos_hint = {"bottom": 1},
                    )
                file_cover_button.bind(size = file_cover_image.setter("size"))
                file_cover_button.bind(pos = file_cover_image.setter("pos"))
                file_cover_button.add_widget(file_cover_image)
            else:
                file_cover_button = KivyButton(
                    on_press = lambda x: app.change_screen("Read Currently Open File Screen", False),
                    text = "File Cover Image Not Found",
                    color = (0, 0, 0, 1),
                    size_hint = (1, None),
                    height = 50,
                    # width = 300,
                )
            file_cover_button.bind(on_press = lambda button: app.main_menu_file_widget_pressed(file, button))
            card.add_widget(file_cover_button)                       
            if file_title != None:
                file_title_button = KivyButton(
                    on_press = lambda x: app.change_screen("Read Currently Open File Screen", False),
                    text = file_title,
                    color = (0, 0, 0, 1),
                    size_hint = (1, None),
                    height = 50,
                    # width = 300,
                    )
            else:
                file_title_button = KivyButton(
                on_press = lambda x: app.change_screen("Read Currently Open File Screen", False),
                text = "File Title Not Found",
                color = (0, 0, 0, 1),
                size_hint = (1, None),
                height = 50,
                # width = 300,
                )
            file_title_button.bind(on_press=lambda x: app.load_file_read_screen(file))  
            card.add_widget(file_title_button)
        elif file["file_format"] in app.music_tag_compatible_file_formats:
            album_title = file["file_name"]
            album_author = file["file_author"]
            file_cover = audio_file_data_music_tag.get_audio_file_data_music_tag_artwork(file["album_tracks_dictionary"][0]["absolute_file_path"])
            card = MDCard(
                    orientation = "vertical",
                    size_hint = (None, None),
                    height = Globals.main_menu_files_widgets_height,
                    width = Globals.main_menu_files_widgets_width,
                    radius = [0, 0, 0, 0],
                    md_bg_color = (0, 0, 0, 0)
                )
            app.root.ids.main_menu_grid_layout.add_widget(card)
            if file_cover != None:
                cover_image = CoreImage(io.BytesIO(file_cover), ext = "jpg")
                file_cover_button = KivyButton( 
                    background_color = (0, 0, 0, 0),
                    pos_hint = {"bottom": 1}
                    )
                file_cover_image = Image(
                    texture = CoreImage(cover_image).texture,
                    allow_stretch = True,
                    keep_ratio = True,
                    pos_hint = {"bottom": 1},
                    y = 0
                    )
                file_cover_button.bind(size = file_cover_image.setter("size"))
                file_cover_button.bind(pos = file_cover_image.setter("pos"))
                file_cover_button.add_widget(file_cover_image)
            else:
                file_cover_button = KivyButton(
                    on_press = lambda x: app.change_screen("Album Inspector Screen", False),
                    text = "File Cover Image Not Found",
                    color = (0, 0, 0, 1),
                    size_hint = (1, None),
                    height = 50,
                    # width = 300,
                )
            file_cover_button.bind(on_press = lambda button: app.main_menu_file_widget_pressed(file, button))
            card.add_widget(file_cover_button)                        
            if album_title != None:
                file_title_button = KivyButton(
                    on_press = lambda x: app.change_screen("Album Inspector Screen", False),
                    text = album_title,
                    color = (0, 0, 0, 1),
                    size_hint = (1, None),
                    height = 50,
                    # width = 300,
                )
            else:
                file_title_button = KivyButton(
                on_press = lambda x: app.change_screen("Album Inspector Screen", False),
                text = "File Title Not Found",
                color = (0, 0, 0, 1),
                size_hint = (1, None),
                height = 50,
                # width = 300,
                )
            file_title_button.bind(on_press = lambda x: app.load_album_inspector_screen(file))  
            card.add_widget(file_title_button)
            if album_author != None:
                file_author_button = KivyButton(
                    text = album_author,
                    color = (0, 0, 0, 1),
                    size_hint = (1, None),
                    height = 50,
                    # width = 300,
                    )
            else:
                file_author_button = KivyButton(
                text = "File Author Not Found",
                color = (0, 0, 0, 1),
                size_hint = (1, None),
                height = 50,
                # width = 300,
                ) 
            card.add_widget(file_author_button)

class LocalFolderPopUp(Popup):
    class DriveButton():
        def __init__(self, app, drive):
            app.ids.folder_chooser_box_layout_vertical.add_widget(
            KivyButton(
                text = drive,
                pos_hint = {"top": 1},
                size_hint = (None, None),
                height = 60,
                width = 60,
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
        
class ScreenManager(): # needs some fixing
    def __init__(self, app):
        self.app = app
        self.screen_currently_in_use :int = 0
        self.previous_screens_and_tabs_list = ["Main Menu"]

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
                        self.app.reading_sign_collections_navbar_card_pulled_out = True
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
        self.keyboard_ctrl_button_pressed = False

    def on_mouse_down(self, *args):
        # print("Mouse input:", args)
        if args[3] == "mouse5":
            self.app.screen_manager_object.go_forward_to_next_tab_or_screen()
        if args[3] == "mouse4":
            self.app.screen_manager_object.return_to_previous_tab_or_screen()

        if args[3] == "scrollup":
            self.mouse_button_and_keayboard_input(args[3])
        if args[3] == "scrolldown":
            self.mouse_button_and_keayboard_input(args[3])

    def on_key_down(self, *args):
        # print("Keyboard input:", args)
        if args[3] == "y" and str(args[4]) == "['ctrl']":
            pass
        if args[3] == "z" and str(args[4]) == "['ctrl']":
            pass
        if str(args[4]) == "['ctrl']":
            self.keyboard_ctrl_button_pressed = True
        else:
            self.keyboard_ctrl_button_pressed = False
        if args[1] == 27:
            self.app.screen_manager_object.change_screen("Settings Screen", False)

    def on_mouse_position_changed(self, window_object, mouse_position):
        self.check_mouse_position_on_navbar(mouse_position)

    def check_mouse_position_on_navbar(self, mouse_position):
        if self.app.root.ids.screen_manager.current == "Read Currently Open File Screen":
            if self.app.root.ids.navbar.width < 50:
                if mouse_position[0] <= self.root.ids.navbar.pos[0] + self.navbar_width_max:
                    self.widget_manager_object.change_widget_width(self.root.ids.navbar, 50)
            elif self.root.ids.navbar.width == 50:
                if mouse_position[0] > 50:
                    self.widget_manager_object.change_widget_width(self.root.ids.navbar, 0)
        if self.app.reading_sign_collections_navbar_card_pulled_out == True:
            # if mouse_position[0] isnt between widget width
            #     and if mouse_position[1] isnt between widget height
            #     self.change_widget_width(self.root.ids.reading_sign_collections_navbar_card, 0)
            pass

    def mouse_button_and_keayboard_input(self, mouse_wheel_input):
        # check current screen, if main menu, if files tab, chage size of widgets by some increment, same if authors tab
        if self.keyboard_ctrl_button_pressed == True:
            if mouse_wheel_input == "scrollup":
                if self.app.root.ids.screen_manager.current == "Main Menu":
                    if self.app.root.ids.main_menu_tabbed_panel.current_tab.text == "Files":
                        self.app.root.ids.main_menu_file_widget_size_slider.value -= 10
                        self.on_slider_value_changed(self.root.ids.main_menu_file_widget_size_slider)
                    elif self.app.root.ids.main_menu_tabbed_panel.current_tab.text == "Authors":
                        self.app.root.ids.main_menu_authors_tab_widget_size_slider.value -= 10
                        self.on_slider_value_changed(self.root.ids.main_menu_authors_tab_widget_size_slider)
                        # [WARNING] <kivy.uix.gridlayout.GridLayout object at 0x000002C0FF490350> have no cols or rows set, layout is not triggered.
                    elif self.app.root.ids.main_menu_tabbed_panel.current_tab == "Authors":
                        pass
                elif self.app.root.ids.screen_manager.current == "Read Currently Open File Screen":
                    pass
            elif mouse_wheel_input == "scrolldown":
                pass

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
        if exists(SaveFileManager.local_directories_to_scan_save_file_location):    
            file = open(SaveFileManager.local_directories_to_scan_save_file_location, "r") 
            json_file_data = file.read()
            file.close()
            if json_file_data != "":
                list_of_folders_to_scan = eval(json_file_data)
                for folder in list_of_folders_to_scan:
                    Folder_To_Scan_Card(self.app, folder)

class ComicbookReaderGUI(MDApp):

    def on_slider_value_changed(self, id):
        if id == self.root.ids.main_menu_file_widget_size_slider:
            self.main_menu_files_widgets_height = 1000 * id.value
            self.main_menu_files_widgets_width = 600 * id.value
            for child in self.root.ids.main_menu_grid_layout.children:
                child.height = self.main_menu_files_widgets_height
                child.width = self.main_menu_files_widgets_width
            self.responsive_grid_layout()
        if id == self.root.ids.main_menu_authors_tab_widget_size_slider:
            self.main_menu_authors_tab_widgets_height = 1000 * id.value
            self.main_menu_authors_tab_widgets_width = 600 * id.value
            for child in self.root.ids.main_menu_authors_tab_grid_layout.children:
                child.height = self.main_menu_authors_tab_widgets_height
                child.width = self.main_menu_authors_tab_widgets_width
            self.responsive_grid_layout()

    def responsive_grid_layout(self, *args):
        self.root.ids.main_menu_files_tab_grid_layout.cols = int(self.root.ids.main_menu_files_tab_grid_layout.width / (Globals.main_menu_files_widgets_width + 20))
        # self.root.ids.main_menu_authors_tab_grid_layout.cols = int(self.root.ids.main_menu_authors_tab_grid_layout.width / (Globals.main_menu_authors_tab_widgets_width + 20))

    def build(self):
        self.title = "Comicbook Reader"
        # Window.bind(on_resize = self.window_resized)
        # Window.bind(on_restore = self.responsive_grid_layout)
        # Window.bind(on_maximize = self.responsive_grid_layout)
        # Window.bind(on_request_close = self.on_request_close)
        self.local_scan_directory_class = LocalScanDirectory
        self.reading_sign_collections_navbar_card_pulled_out = False
        self.screen_manager_object = ScreenManager(MDApp.get_running_app())
        self.widget_manager_object = WidgetManager(MDApp.get_running_app())
        self.input_manager_object = InputManager(MDApp.get_running_app())
        self.md_widget_manager_object = MDWidgetManager(MDApp.get_running_app())
        Window.bind(on_key_down = self.input_manager_object.on_key_down)
        Window.bind(on_mouse_down = self.input_manager_object.on_mouse_down)
        Window.bind(mouse_pos = self.input_manager_object.on_mouse_position_changed)
        return Builder.load_file("kivy_gui.kv")
    
    def on_start(self):
        # self.load_last_used_settings()
        self.responsive_grid_layout()
        self.md_widget_manager_object.create_local_folders_to_scan_expansion_panel()
        # ScanDirectoryManager.scan_all_directories()
        # self.local_folders_and_files_scan()
        # print(Config.get("graphics", "window_state"), Config.get("graphics", "fullscreen"))
        # Config.set("graphics", "window_state", "hidden")
        # ScanDirectoryManager.scan_all_directories() #first create all the main menu widgets, then scan folders, make sure this doesn't freeze the device

ComicbookReaderGUI().run()

# when and where will file dict json be called from?

# should this be written in file class?
    # in that case, what to do with authors tab
    # should authors tab json be a thing?