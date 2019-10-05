import os
import time
from difflib import SequenceMatcher


mediapath = "/media/Movies/"
subpath = "./subtitles/"

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

def menu():
    print("AutoSync batch script.")
    while True:
        print("Select option:\n (1)Sync a Movies folder\n (2)Copy subtitles from temporary to definitive folder\n (3)Sync a Single Movie (q) Quit")
        option = input()
        if option == "1":
            print("Sync Full Movies Folder")
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
    files = get_files_list(path)
    #print(files["folders"][0])

    database = open("subtitles.txt", "a+")


    for k in files["folders"]:
        newpath = mediapath + k
        ff = os.listdir(newpath)
        #print(ff)
        for f in ff:
            if os.path.isfile(newpath + "/" + str(f)) and ("mkv" in f or "mp4" in f):
                print(f)
                reference = ""
                for i in ff:
                    if "srt" in i:
                        videosource = newpath + "/" + str(f)
                        subsource = newpath + "/" + str(i)
                        subdest = subpath + str(i)
                        with open("subtitles.txt") as j:
                            if i in j.read():
                                print(i + " is already sync. Skipping")
                            else:
                                if reference == "":
                                    command = "subsync \"%s\" -i \"%s\" > \"%s\" " %(videosource, subsource, subdest)
                                    print(command)
                                    os.system(command)
                                    database.write(i)
                                    reference = subsource
                                    time.sleep(10)
                                else:
                                    command = "subsync \"%s\" -i \"%s\" > \"%s\" " %(reference, subsource, subdest)
                                    print(command)
                                    os.system(command)
                                    database.write(i)
                                    time.sleep(10)

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