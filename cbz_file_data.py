import zipfile
import os.path
from datetime import datetime

def get_cbz_file_modified_time(file_path):
    unix_time = os.path.getmtime(file_path)
    return datetime.fromtimestamp(unix_time).strftime("%d/%m/%Y %H:%M:%S")

def get_cbz_file_title(file_path):
    file_name = None
    with zipfile.ZipFile(file_path) as z:
        folder_list = [info.filename for info in z.infolist() if info.is_dir()]
        if len(folder_list) == 1:
            file_name = folder_list[0]
            if file_name.endswith("/"):
                file_name = file_name[:-1]
        elif len(folder_list) == 0:
            file_name = os.path.basename(file_path)
        elif len(folder_list) > 1:
            file_name = folder_list[0]
            if file_name.endswith("/"):
                file_name = file_name[:-1]
    return file_name
    
def get_cbz_file_metadata(file_path):
    pass

def get_cbz_file_content(file_path):
    list_of_images = []
    file_number :int = 0
    with zipfile.ZipFile(file_path) as z:
        file_list = z.namelist()
        for file in file_list:
            if file.endswith(".jpeg"):
                file_info = {"file" : z.read(file), "file_format" : "jpeg"}
                list_of_images.append(file_info)
                file_number += 1
            elif file.endswith(".jpg"):
                file_info = {"file" : z.read(file), "file_format" : "jpg"}
                list_of_images.append(file_info)
                file_number += 1
            elif file.endswith(".png"):
                file_info = {"file" : z.read(file), "file_format" : "png"}
                list_of_images.append(file_info)
                file_number += 1
            elif file.endswith(".gif"):
                file_info = {"file" : z.read(file), "file_format" : "gif"}
                list_of_images.append(file_info)
                file_number += 1         
            elif file.endswith(".tiff"):
                file_info = {"file" : z.read(file), "file_format" : "tiff"}
                list_of_images.append(file_info)
                file_number += 1    
            elif file.endswith(".bmp"):
                file_info = {"file" : z.read(file), "file_format" : "bmp"}
                list_of_images.append(file_info)
                file_number += 1    
            elif file.endswith(".jpe"):
                file_info = {"file" : z.read(file), "file_format" : "jpe"}
                list_of_images.append(file_info)
                file_number += 1    
            elif file.endswith(".lbm"):
                file_info = {"file" : z.read(file), "file_format" : "lbm"}
                list_of_images.append(file_info)
                file_number += 1  
            elif file.endswith(".pcx"):
                file_info = {"file" : z.read(file), "file_format" : "pcx"} 
                list_of_images.append(file_info)
                file_number += 1    
            elif file.endswith(".pnm"):
                file_info = {"file" : z.read(file), "file_format" : "pnm"}
                list_of_images.append(file_info)
                file_number += 1  
            elif file.endswith(".webp"):
                file_info = {"file" : z.read(file), "file_format" : "webp"}
                list_of_images.append(file_info)
                file_number += 1    
            elif file.endswith(".tga"):
                file_info = {"file" : z.read(file), "file_format" : "tga"}
                list_of_images.append(file_info)
                file_number += 1  
            elif file.endswith(".xcf"):
                file_info = {"file" : z.read(file), "file_format" : "xcf"}
                list_of_images.append(file_info)
                file_number += 1  
            elif file.endswith(".xpm"):
                file_info = {"file" : z.read(file), "file_format" : "xpm"}
                list_of_images.append(file_info)
                file_number += 1    
            elif file.endswith(".xv"):
                file_info = {"file" : z.read(file), "file_format" : "xv"}
                list_of_images.append(file_info)
                file_number += 1  
    return list_of_images

def get_cbz_cover_image(file_path):
    file_info = None
    with zipfile.ZipFile(file_path) as z:
        file_list = z.namelist()
        while file_info == None:
            for file in file_list:
                if file.endswith(".jpeg"):
                    file_info = {"file" : file, "file_format" : "jpeg"}
                    break
                elif file.endswith(".jpg"):
                    file_info = {"file" : file, "file_format" : "jpg"}
                    break
                elif file.endswith(".png"):
                    file_info = {"file" : file, "file_format" : "png"}
                    break
                elif file.endswith(".gif"):
                    file_info = {"file" : file, "file_format" : "gif"}      
                    break
                elif file.endswith(".tiff"):
                    file_info = {"file" : file, "file_format" : "tiff"}  
                    break
                elif file.endswith(".bmp"):
                    file_info = {"file" : file, "file_format" : "bmp"} 
                    break
                elif file.endswith(".jpe"):
                    file_info = {"file" : file, "file_format" : "jpe"}
                    break
                elif file.endswith(".lbm"):
                    file_info = {"file" : file, "file_format" : "lbm"}
                    break
                elif file.endswith(".pcx"):
                    file_info = {"file" : file, "file_format" : "pcx"} 
                    break
                elif file.endswith(".pnm"):
                    file_info = {"file" : file, "file_format" : "pnm"}
                    break
                elif file.endswith(".webp"):
                    file_info = {"file" : file, "file_format" : "webp"}
                    break
                elif file.endswith(".tga"):
                    file_info = {"file" : file, "file_format" : "tga"}
                    break
                elif file.endswith(".xcf"):
                    file_info = {"file" : file, "file_format" : "xcf"}
                    break
                elif file.endswith(".xpm"):
                    file_info = {"file" : file, "file_format" : "xpm"}
                    break  
    return file_info["file"]