import os
import time
from difflib import SequenceMatcher


mediapath = "/media/Movies/"
subpath = "./subtitles/"

videoextensions = [".mp4",".mkv",".avi"]
subtitlesextensions = [".srt"]

def get_files_list(path, extension=[]):
    #Get everything in the directory provided
    content = os.listdir(path)

    #Empty dict to store data for the return
    list = {"files": [], "folders": []}

    for c in content:
        #Files
        if os.path.isfile(path + str(c)):
            for e in extension:
                if e in c:
                    list["files"].append(c)
        #Folders
        if os.path.isdir(path + str(c)):
            list["folders"].append(c)
    return list

def subsync(path):
    database = open("subtitles.txt", "a+")
    files = os.listdir(path)
    for video in files:
        for ve in videoextensions:
            if os.path.isfile(path + str(video)) and ve in video:
                print(video)
                reference = ""
                for subtitle in files:
                    for se in subtitlesextensions:
                        if se in subtitle:
                            videosource = path + video
                            subsource = path + subtitle
                            subdest = subpath + subtitle
                            with open("subtitles.txt") as j:
                                if subtitle in j.read():
                                    print(subtitle + " is already sync. Skipping")
                                else:
                                    if reference == "":
                                        command = "subsync \"%s\" -i \"%s\" > \"%s\" " %(videosource, subsource, subdest)
                                        print(command)
                                        #os.system(command)
                                        database.write(subtitle)
                                        reference = subsource
                                        time.sleep(10)
                                    else:
                                        command = "subsync \"%s\" -i \"%s\" > \"%s\" " %(reference, subsource, subdest)
                                        print(command)
                                        #os.system(command)
                                        database.write(subtitle)
                                        time.sleep(10)
    database.close()

def menu():
    print("AutoSync batch script.")
    while True:
        print("Select option:\n (1)Sync a Movies folder\n (2)Copy subtitles from temporary to definitive folder\n (3)Sync a Single Movie\n (q) Quit")
        option = input()
        if option == "1":
            print("Sync Full Movies Folder")
            subtitlessync()
        elif option == "2":
            print("Copy Subs to Movie Folder")
            copysubstofolder()
        elif option == "3":
            print("Sync a Single Movie")
            print("To Do")
        elif option.lower() == "q":
            print("Exit")
            break
        else:
            print("No valid option")

def subtitlessync():
    
    path = mediapath
    folders = get_files_list(path)["folders"]
    #print(files["folders"][0])

    for k in folders:
        if k[-1] == "/":
            subsync(k)
        else:
            subsync(k+"/")

def copysubstofolder():
    #path = input("Insert path:")
    while True:
        path = input("Insert Movies Folder:")
        if path == "":
            path = mediapath
        
        pathsubs = input("Insert Subtitles Folder:")
        
        if pathsubs == "":
            pathsubs = subpath
        try:
            folders = get_files_list(path, [".mkv",".avi",".mp4"])["folders"]
            subs = get_files_list(pathsubs, [".srt"])["files"]
            break
        except:
            print("Something wrong. Are the folders correct?")

    proced = input("Continue?")
    if proced == "y":
        print("Processing")
        for s in subs:
            ratio = 0.0
            more_similar = ""
            for f in folders:
                c = SequenceMatcher(None, s, f)
                calcratio = c.ratio()
                if calcratio > ratio:
                    ratio = calcratio
                    more_similar = f
                #else:
                    #print("Not")

            print(more_similar + " é mais igual a    " + s)

            commands = "mv \"%s%s\" \"%s%s/\"" %(pathsubs, s, path, more_similar)
            print(commands)
            os.system(commands)
    else:
        print("Returning Menu")


if __name__ == "__main__":
    menu()