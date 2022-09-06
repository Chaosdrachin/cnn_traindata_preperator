#################################
#   DEV     : Chaosdrachin
#   Year    : 2022 Sep
#   Version : 1.1.0
#   State   : Beta
#################################
import os
from glob import glob
import shutil
from PIL import Image, ImageOps
import re

Image.LOAD_TRUNCATED_IMAGES = True

# CSV Data with folder Stucture and Data Count
train_data_info_csv = ["folder,file,\n", "test,test.jpg"]
train_data_count_csv = ["folder,file_count,\n"]
all_data = 0

def resize_and_greyscale(file, size_w, size_h, greyscale):
    try:
        image = Image.open(file)
        new_image = image.resize((size_w, size_h))
        image.close()
        if greyscale:
            gray_image = ImageOps.grayscale(new_image)
            gray_image.save(file)
        else:
            new_image.save(file)
        return True
    except:
        # if file is broken in someway
        return False

def add_to_label_file(label_file_path, train_file, label):
    label = "".join(label)
    label = re.sub(r"[0-9$&+,:;=?@#|'<>.^*()%!-]", "", label)

    if os.path.exists(label_file_path):
        with open(label_file_path, "a") as f:
            f.write(str(train_file) + "," + label + ",\n")
    else:
        with open(label_file_path, "w+") as f:
            f.writelines(["folder,label,\n", str(train_file) + "," + label + ",\n"])

def rename_and_move(base_folder='./Pictures/*', prepared_data_path="prepared_data/Pictures/", copy_testfolder=False,
                    resize=True, height=128, width=128, greyscale=True):
    global all_data
    resized = True  # Default

    prepared_folders = prepared_data_path.split("/")
    for folder in prepared_folders:
        if folder != "":
            if not os.path.exists(folder):
                os.mkdir(folder)

    base_folders = glob(base_folder, recursive=True)
    foldernames = [prepared_data_path]
    subfolders = {}

    print("[+] Getting Sub-folders of Pictures")
    for folder in base_folders:
        if not copy_testfolder:
            if "test" not in folder:
                subfolders[folder] = glob(folder + r"\*", recursive=True)
        else:
            if "test" not in folder:
                subfolders[folder] = glob(folder + r"\*", recursive=True)

    print("[+] Start Scanning...")
    for folder in subfolders:
        foldernames.append(prepared_data_path + folder.replace("./Pictures\\", ""))
        for subfolder in subfolders[folder]:
            i = 0
            files = glob(subfolder + "/*")
            foldernames.append(prepared_data_path + subfolder.replace("./Pictures\\", ""))


            for existing_folder in foldernames:
                if not os.path.exists(existing_folder):
                    os.mkdir(existing_folder)

            target_folder = subfolder.replace("./Pictures\\", "")

            for file in files:
                all_data += len(files)
                save_path = str(prepared_data_path + target_folder + "\\")
                label_folder = target_folder.split("\\")
                label_file_path = "prepared_data/" + subfolder.split("\\")[0] + "/" + subfolder.split("\\")[1] \
                                  + "/labels.csv"

                if ".jpg" in file or ".jpeg" in file:
                    shutil.copy(file, save_path + str(i) + ".jpg")
                    if resize:
                        resized = resize_and_greyscale(save_path + str(i) + ".jpg", height, width, greyscale)
                    if resized:
                        add_to_label_file(label_file_path.replace("./", ""), save_path + str(i) + ".jpg",
                                          label_folder[1:])
                        train_data_info_csv.append(
                            str(prepared_data_path + target_folder + "\\" + "," + str(i) + ".jpg" + ",\n"))
                        i += 1
                    if not resized:
                        os.remove(file)
                elif ".png" in file:
                    shutil.copy(file, save_path + str(i) + ".png")
                    if resize:
                        resized = resize_and_greyscale(save_path + str(i) + ".png", height, width, greyscale)
                    if resized:
                        add_to_label_file(label_file_path.replace("./", ""), save_path + str(i) + ".jpg",
                                          label_folder[1:])
                        train_data_info_csv.append(
                            str(prepared_data_path + target_folder + "\\" + "," + str(i) + ".png" + ",\n"))
                        i += 1
                elif ".bmp" in file:
                    shutil.copy(file, save_path + str(i) + ".bmp")
                    if resize:
                        resized = resize_and_greyscale(save_path + str(i) + ".bmp", height, width, greyscale)
                    if resized:
                        add_to_label_file(label_file_path.replace("./", ""), save_path + str(i) + ".jpg",
                                          label_folder[1:])
                        train_data_info_csv.append(
                            str(prepared_data_path + target_folder + "\\" + "," + str(i) + ".bmp" + ",\n"))
                        i += 1

                train_data_count_csv.append(f"{subfolder}, {len(files)},\n")

    print("[+] Save Collected Data while Processing as CSV")
    with open("prepared_data/pictures/train_data_info.csv", "w+") as f:
        f.writelines(train_data_info_csv)
    with open("prepared_data/pictures/train_data_count.csv", "w+") as f:
        f.writelines(train_data_count_csv)

# Example Usage | And for Testing
print("[+] Start Image Processing")
rename_and_move()
print("[+] Done")
