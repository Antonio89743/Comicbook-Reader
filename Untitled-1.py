import glob
import string
import os
from abc import ABC, abstractmethod

# test deleting file from directory and opening it once the file's location is already saved in app json

# getting all files takes way too long, old method is good



# get folders
# from them, get files
    # on open run this func with previously saved folders, try not to freeze app, only save new ones and don't touch older ones



class DirectoriesToScan():
    pass

class LocalDirectoriesToScan():
    pass


# you should be able to call dictionaries to scan, scan func for all dictionaries, wheather or not





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

