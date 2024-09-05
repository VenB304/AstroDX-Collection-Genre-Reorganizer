import os
import json
import urllib.request
import shutil

def unknownHandler(title_value, folder_path, catcode):
    chosen = False
    print(f"unable to determine genre for {title_value} in {folder_path}")
    while not chosen:
        print("Choices:")
        print("[1] Copy to unidentified folder")
        print("[2] Choose Manually")
        print("[3] Log to unidentifiedCharts.txt and Ignore")
        choice = str(input("Enter the number of your choice: "))
        match choice:
            case "1":
                chosen = True
                os.makedirs(root_path + "/levels/Unidentified/" + os.path.basename(folder_path), exist_ok=True)
                try:
                    shutil.copytree(folder_path, root_path + "/levels/Unidentified/" + os.path.basename(folder_path), dirs_exist_ok=True)
                except:
                    print(f"Error: Copy failed: {folder_path}")
                    debugging.write(f"Error: Copy failed: {folder_path} to Output folder\n")
                print(f"copied to output: {folder_path}")
                
            case "2":
                chosen = True
                print("Choices:")
                print("[1] POPS＆アニメ")
                print("[2] niconico＆ボーカロイド")
                print("[3] 東方Project")
                print("[4] ゲーム＆バラエティ")
                print("[5] maimai")
                print("[6] オンゲキ＆CHUNITHM")
                print("[7] 宴会場")
                print("[8] 中国流行乐")
                print("[9] Unidentified")
                manualChosen = False
                while not manualChosen:
                    manualChoice = str(input("Enter the number of your choice: "))
                    if manualChoice in ["1","2","3","4","5","6","7","8","9"]:
                        os.makedirs(root_path + "/levels/" + catcode[int(manualChoice)-1] + "/" + os.path.basename(folder_path), exist_ok=True)
                        try:
                            shutil.copytree(folder_path, root_path + "/levels/" + catcode[int(manualChoice)-1] + "/" + os.path.basename(folder_path), dirs_exist_ok=True)
                        except:
                            print(f"Error: Copy failed: {folder_path}")
                            debugging.write(f"Error: Copy failed: {folder_path} to Output folder\n")
                        print(f"copied to output: {folder_path}")
                        manualChosen = True
                    else:
                        print("Invalid choice, please try again")
                        manualChosen = False
                        continue
            case "3":
                chosen = True
                print(f"IGNORED: {title_value} in {folder_path}")
                unidentifiedChartsDebug.write(f"IGNORED: {title_value} in {folder_path}\n")
                
            case "_":
                print("Invalid choice, please try again")
                chosen = False
                continue

def parse_JSON_Database():
    try:
        response = urllib.request.urlopen(maimai_JP_songlist_URL)
        if response.status == 200:
            maimaiSongInfoJSON = json.loads(response.read())
        else:
            print(f"Failed to fetch data, status code: {response.status}")
            maimaiSongInfoJSON = []
    except Exception as e:
        print(f"Error fetching or parsing JSON: {e}")
        maimaiSongInfoJSON = []

    try:
        response = urllib.request.urlopen(manualCheckURL)
        if response.status == 200:
            manualCheckJSON = json.loads(response.read())
        else:
            print(f"Failed to fetch data, status code: {response.status}")
            manualCheckJSON = []
    except Exception as e:
        print(f"Error fetching or parsing JSON: {e}")
        manualCheckJSON = []

    for item in maimaiSongInfoJSON:
        if item.get('catcode') == 'maimai':
            maimai.append(item.get('title'))
        elif item.get('catcode') == 'POPS＆アニメ':
            popAndAnime.append(item.get('title'))
        elif item.get('catcode') == 'ゲーム＆バラエティ':
            gameAndVariety.append(item.get('title'))
        elif item.get('catcode') == '東方Project':
            touhouProject.append(item.get('title'))
        elif item.get('catcode') == 'niconico＆ボーカロイド':
            niconicoAndVocaloid.append(item.get('title'))
        elif item.get('catcode') == 'オンゲキ＆CHUNITHM':
            ongekiAndChunithm.append(item.get('title'))

    return maimaiSongInfoJSON, manualCheckJSON


def parse_maidata(filepath):
    lv_7_value = None
    title_value = None
    
    with open(filepath, 'r', encoding='utf-8-sig') as file:
        for line in file:
            if line.startswith("&title="):
                title_value = line.strip().split('=')[1]
                if not title_value:  # If title is somehow empty
                    print(f"Warning: Title is empty in file {filepath}")
            elif line.startswith("&lv_7="):
                lv_7_value = line.strip().split('=')[1]
    
    return lv_7_value, title_value

def check_only_folders(root_path,maimaiSongInfoJSON,manualCheckJSON):
    for root, dirs, files in os.walk(root_path):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            maidata_path = os.path.join(folder_path, 'maidata.txt')
            
            if os.path.isfile(maidata_path):
                lv_7_value, title_value = parse_maidata(maidata_path)
                print(f"&title:\t\t{title_value}")

                if lv_7_value:
                    print(f"matched to in maimaiJSON: \tutage")

                elif title_value in popAndAnime or folder in popAndAnime:
                    print(f"matched to maimaiJSON: \tpop and anime")

                elif title_value in niconicoAndVocaloid or folder in niconicoAndVocaloid:
                    print(f"matched to maimaiJSON: \tniconico and vocaloid")

                elif title_value in touhouProject or folder in touhouProject:
                    print(f"matched to maimaiJSON: \ttouhou project")

                elif title_value in gameAndVariety or folder in gameAndVariety:
                    print(f"matched to maimaiJSON: \tgame and variety")

                elif title_value in maimai or folder in maimai:
                    print(f"matched to maimaiJSON: \tmaimai")
                
                elif title_value in ongekiAndChunithm or folder in ongekiAndChunithm:
                    print(f"matched to maimaiJSON: \tongeki and chunithm")
                
                else:
                    if title_value in manualCheckJSON:
                        if manualCheckJSON[title_value] == "POPS＆アニメ":
                            print(f"matched to manualCheckJSON: \tpop and anime")

                        elif manualCheckJSON[title_value] == "niconico＆ボーカロイド":
                            print(f"matched to manualCheckJSON: \tniconico and vocaloid")

                        elif manualCheckJSON[title_value] == "東方Project":
                            print(f"matched to manualCheckJSON: \ttouhou project")

                        elif manualCheckJSON[title_value] == "ゲーム＆バラエティ":
                            print(f"matched to manualCheckJSON: \tgame and variety")

                        elif manualCheckJSON[title_value] == "maimai":
                            print(f"matched to manualCheckJSON: \tmaimai")

                        elif manualCheckJSON[title_value] == "オンゲキ＆CHUNITHM":
                            print(f"matched to manualCheckJSON: \tongeki and chunithm")

                        elif manualCheckJSON[title_value] == "中国流行乐":
                            print(f"matched to manualCheckJSON: \tchinese pop")

                        elif manualCheckJSON[title_value] == "宴会場":
                            print(f"matched to manualCheckJSON: \tutage")

                        else:
                            print(f"{title_value} found in manual check, value empty, @venb304 please update manualCheck.json")
                            # move or copy to unidentified folder
                    else:
                        if title_value:
                            print(title_value + " not match, Unidentified genre")
                        else:
                            print(f"No title found, Unidentified genre in {folder_path}")
                
            else:
                print(f"{folder_path} is empty, moving on")

def proces_toGenre(root_path, maimaiSongInfoJSON, manualCheckJSON):
    savedFolderPaths = [[],[],[],[],[],[],[],[],[]]
    catcode = ["POPS＆アニメ", "niconico＆ボーカロイド", "東方Project", "ゲーム＆バラエティ", "maimai", "オンゲキ＆CHUNITHM", "宴会場", "中国流行乐","Unidentified"]

    if os.path.isdir(root_path + "/levels/"):
        if not os.listdir(root_path + "/levels/"):
            print(f"{root_path}/levels/ is empty")
        else:
            print(f"{root_path}/levels/ is not empty")
            print(f"deleting {root_path}/levels/")
            shutil.rmtree(root_path + "/levels/")

    for root, dirs, files in os.walk(root_path):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            maidata_path = os.path.join(folder_path, 'maidata.txt')
            
            if os.path.isfile(maidata_path):
                lv_7_value, title_value = parse_maidata(maidata_path)
                print(f"Folder: {folder_path}")
                
                if lv_7_value:
                    print(f"{title_value} has utage difficulty | matched to in maimaiJSON: utage")
                    savedFolderPaths[6].append(folder_path)

                elif title_value in popAndAnime or folder in popAndAnime:
                    print(f"{title_value} matched to maimaiJSON: pop and anime")
                    savedFolderPaths[0].append(folder_path)

                elif title_value in niconicoAndVocaloid or folder in niconicoAndVocaloid:
                    print(f"{title_value} matched to maimaiJSON: niconico and vocaloid")
                    savedFolderPaths[1].append(folder_path)

                elif title_value in touhouProject or folder in touhouProject:
                    print(f"{title_value} matched to maimaiJSON: touhou project")
                    savedFolderPaths[2].append(folder_path)

                elif title_value in gameAndVariety or folder in gameAndVariety:
                    print(f"{title_value} matched to maimaiJSON: game and variety")
                    savedFolderPaths[3].append(folder_path)

                elif title_value in maimai or folder in maimai:
                    print(f"{title_value} matched to maimaiJSON: maimai")
                    savedFolderPaths[4].append(folder_path)
                
                elif title_value in ongekiAndChunithm or folder in ongekiAndChunithm:
                    print(f"{title_value} matched to maimaiJSON: ongeki and chunithm")
                    savedFolderPaths[5].append(folder_path)
                
                else:
                    if title_value in manualCheckJSON:
                        if manualCheckJSON[title_value] == "POPS＆アニメ":
                            print(f"{title_value} matched to manualCheckJSON: pop and anime")
                            savedFolderPaths[0].append(folder_path)

                        elif manualCheckJSON[title_value] == "niconico＆ボーカロイド":
                            print(f"{title_value} matched to manualCheckJSON: niconico and vocaloid")
                            savedFolderPaths[1].append(folder_path)

                        elif manualCheckJSON[title_value] == "東方Project":
                            print(f"{title_value} matched to manualCheckJSON: touhou project")
                            savedFolderPaths[2].append(folder_path)

                        elif manualCheckJSON[title_value] == "ゲーム＆バラエティ":
                            print(f"{title_value} matched to manualCheckJSON: game and variety")
                            savedFolderPaths[3].append(folder_path)

                        elif manualCheckJSON[title_value] == "maimai":
                            print("title matched in manual check: maimai list")
                            savedFolderPaths[4].append(folder_path)

                        elif manualCheckJSON[title_value] == "オンゲキ＆CHUNITHM":
                            print("title matched in manual check: ongeki and chunithm list")
                            savedFolderPaths[5].append(folder_path)

                        elif manualCheckJSON[title_value] == "中国流行乐":
                            print("title matched in manual check: chinese pop list")
                            savedFolderPaths[7].append(folder_path)

                        elif manualCheckJSON[title_value] == "宴会場":
                            print("title matched in manual check: utage list")
                            savedFolderPaths[6].append(folder_path)

                        else:
                            print(title_value + " found in manual check, value empty, @venb304 please update manualCheck.json")
                    else:
                        if title_value:
                            print(title_value + " not match, Unidentified genre")
                        else:
                            print("No title found, Unidentified genre") 
                        
                        savedFolderPaths[8].append(folder_path)
            else:
                print(f"{folder_path} is empty, moving on")

    for category in savedFolderPaths:
        match savedFolderPaths.index(category):
            case 0:
                print("\ncurrent category: pop and anime\n")
            case 1:
                print("\ncurrent category: niconico and vocaloid\n")
            case 2:
                print("\ncurrent category: touhou project\n")
            case 3:
                print("\ncurrent category: game and variety\n")
            case 4:
                print("\ncurrent category: maimai\n")
            case 5:
                print("\ncurrent category: ongeki and chunithm\n")
            case 6:
                print("\ncurrent category: utage\n")
            case 7:
                print("\ncurrent category: chinese pop\n")
            case 8:
                print("\ncurrent category: unidentified\n")
            case _:
                print("\ncurrent category: how? there should not be another category, how did this return to 8\n")
        
        for savedPaths in category:
            if savedFolderPaths.index(category) == 8:
                unknownHandler(os.path.basename(savedPaths), savedPaths, catcode)
                continue
            else:
                os.makedirs(root_path+"/levels/" + catcode[savedFolderPaths.index(category)] + "/" + os.path.basename(savedPaths), exist_ok=True)
                try:
                    shutil.copytree(savedPaths, root_path + "/levels/" + catcode[savedFolderPaths.index(category)] + "/" + os.path.basename(savedPaths), dirs_exist_ok=True)
                except:
                    print(f"Error: Copy failed: {savedPaths}")
                    debugging.write(f"Error: Copy failed: {savedPaths} to Output folder\n")
                print(f"copied to output: {savedPaths}")

debugging = open("debugging.txt","w", encoding="utf-8-sig")
unidentifiedChartsDebug = open("unidentifiedCharts.txt","w", encoding="utf-8-sig")
popAndAnime = []
niconicoAndVocaloid = []
touhouProject = []
gameAndVariety = []
maimai = []
ongekiAndChunithm = []

manualCheckURL = "https://raw.githubusercontent.com/VenB304/AstroDX-Collection-Genre-Reorganizer/main/manualCheck.json"
maimai_JP_songlist_URL = "https://maimai.sega.jp/data/maimai_songs.json"
maimaiSongInfoJSON = []
manualCheckJSON = []
maimaiSongInfoJSON, manualCheckJSON = parse_JSON_Database()

running = True

while running:
    print("\nMenu\n")
    print("[1] Check folders only for GENRE grouping")
    print("[2] Check folders for GENRE grouping and copy to Output folder")
    print("[3] Generate collection.json files")
    print("[0] Exit")

    choice = str(input("Enter the number you wanna do: "))

    match choice:
        case "1":
            print("Checking folders only for GENRE grouping")
            print("this will not copy to levels folder")
            print("Sample path: C:/Users/username/Downloads/maisquared/")
            root_path = input("Enter the root directory path: ").strip()
            check_only_folders(root_path,maimaiSongInfoJSON,manualCheckJSON)
        case "2":
            print("Checking folders for GENRE grouping and copy to Output folder")
            print("this will copy to levels folder within the same root directory/path you input")
            print("Sample path: C:/Users/username/Downloads/maisquared/")
            root_path = input("Enter the root directory path: ").strip()
            proces_toGenre(root_path,maimaiSongInfoJSON,manualCheckJSON)
        case "3":
            print("Not implemented yet")
        case "0":
            running = False
        case _:
            print("Invalid choice, please try again")
            continue