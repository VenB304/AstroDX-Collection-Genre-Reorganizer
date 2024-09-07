import os
import json
import urllib.request
import shutil
import uuid
import argparse
import zipfile

def zip_folder(folder_path, zip_name):
    # Specify the full path where you want to save the zip file
    zip_file_path = os.path.join(folder_path, zip_name)

    # Create the ZipFile object and specify where to save it
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_STORED) as zipf:
        # Walk through the folder
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)  # Store relative path in the zip
                zipf.write(file_path, arcname=arcname)

def generate_manifest(root_path, replace_files, append_guid):
    # original code by @castierook in the AstroDX Discord Server
    def generate_guid():
        return str(uuid.uuid4())

    def create_manifest(directory, sub_dirs):
        manifest = {
            "name": os.path.basename(directory), 
            "id": None,
            "serverUrl": None,
            "levelIds": sub_dirs
        }
        return manifest

    def process_directories(path, replace_files=False, append_guid=False):
        root_dir = os.path.abspath(path)  # Use the specified path
        output_dir = os.path.join(root_dir, 'output')
        collections_dir = os.path.join(output_dir, 'collections')
        levels_dir = os.path.join(output_dir, 'levels')

        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(collections_dir)
        os.makedirs(levels_dir)

        for root, dirs, files in os.walk(root_dir):
            if root == root_dir or output_dir in root:
                continue

            relative_root = os.path.relpath(root, root_dir)
            if os.path.basename(relative_root) == "output":
                continue

            sub_dirs = []
            for dir_name in dirs:
                if append_guid:
                    new_dir_name = f"{dir_name}-{generate_guid()}"
                    sub_dirs.append(new_dir_name)
                else:
                    sub_dirs.append(dir_name)

            manifest = create_manifest(root, sub_dirs)
            manifest_path = os.path.join(collections_dir, relative_root, 'manifest.json')
            os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
            
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)

            for original_dir_name, dir_name in zip(dirs, sub_dirs):
                src_dir = os.path.join(root, original_dir_name)
                dst_dir = os.path.join(levels_dir, dir_name)
                if replace_files:
                    shutil.move(src_dir, dst_dir)
                else:
                    shutil.copytree(src_dir, dst_dir)

            if replace_files:
                shutil.rmtree(root)

            dirs.clear()  # prevent descending into subdirectories
    process_directories(root_path, replace_files, append_guid)

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
                print(f"[1] {catcode[0]}")
                print(f"[2] {catcode[1]}")
                print(f"[3] {catcode[2]}")
                print(f"[4] {catcode[3]}")
                print(f"[5] {catcode[4]}")
                print(f"[6] {catcode[5]}")
                print(f"[7] {catcode[6]}")
                print(f"[8] {catcode[7]}")
                print(f"[9] {catcode[8]}")
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
    maimaisongInfoJSON_hasLoaded = False
    zetaraku_maimai_songlist_JSON_hasLoaded = False
    genre_manualCheckJSON_hasLoaded = False
    version_manualCheckJSON_hasLoaded = False

    try:
        response = urllib.request.urlopen(maimai_JP_songlist_URL)
        if response.status == 200:
            maimaiSongInfoJSON = json.loads(response.read())
            print("online official maimai song information loaded")
        else:
            response = urllib.request.urlopen(maimai_JP_songlist_other_URL)
            if response.status == 200:
                maimaiSongInfoJSON = json.loads(response.read())
                print("Fallback: online other official maimai song information loaded")
            else:
                
                print(f"maimaisongInfoJSON: Failed to fetch data, status code: {response.status}")
                print("Fallback: loading from local database")
                fallback = open("AstroDX-Collection-Genre-Reorganizer/data/maimai_songs.json", 'r', encoding='utf-8-sig')
                maimaiSongInfoJSON = json.load(fallback)
                print("Fallback: offline official maimai song information loaded")
        maimaisongInfoJSON_hasLoaded = True
    except Exception as e:
        print(f"maimaisongInfoJSON: Error fetching or parsing JSON: {e}")
        try:
            fallback = open("AstroDX-Collection-Genre-Reorganizer/data/maimai_songs.json", 'r', encoding='utf-8-sig')
            print("Fallback: loading from local database")
            maimaiSongInfoJSON = json.load(fallback)
            print("Fallback offline official maimai song information loaded")
            maimaisongInfoJSON_hasLoaded = True
        except:
            maimaiSongInfoJSON = []
            print("Failed to load maimai song information")
            maimaisongInfoJSON_hasLoaded = False

    try:
        response = urllib.request.urlopen(zetaraku_maimai_songlist_URL)
        if response.status == 200:
            zetaraku_maimai_songlist_JSON = json.loads(response.read())
            zetaraku_maimai_songlist_JSON_hasLoaded = True
            print("zetaraku's online song information loaded")
        else:
            print(f"zetaraku song information JSON: Failed to fetch data, status code: {response.status}")
            fallback = open("AstroDX-Collection-Genre-Reorganizer/data/zetaraku_maimai_songlist.json", 'r', encoding='utf-8-sig')
            print("Fallback: loading from local database")
            zetaraku_maimai_songlist_JSON = json.load(fallback)
            print("Fallback: zetaraku's song information loaded")
            zetaraku_maimai_songlist_JSON_hasLoaded = True
        
    except Exception as e:
        print(f"zetaraku song information JSON: Error fetching or parsing JSON: {e}")
        try:
            print("Fallback: loading from local database")
            fallback = open("AstroDX-Collection-Genre-Reorganizer/data/zetaraku_maimai_songlist.json", 'r', encoding='utf-8-sig')
            zetaraku_maimai_songlist_JSON = json.load(fallback)
            print("Fallback: zetaraku's song information loaded")
            zetaraku_maimai_songlist_JSON_hasLoaded = True
        except:
            zetaraku_maimai_songlist_JSON = []
            print("Failed to load zetaraku's maimai song information")
            zetaraku_maimai_songlist_JSON_hasLoaded = False

    try:
        response = urllib.request.urlopen(genre_manualCheckURL)
        if response.status == 200:
            genre_manualCheckJSON = json.loads(response.read())
            print("online manual checking json for genre loaded")
        else:
            print(f"genre manual check json: Failed to fetch data, status code: {response.status}")
            print("Fallback: loading from local database")
            fallback = open("AstroDX-Collection-Genre-Reorganizer/data/genre_manualCheck.json", 'r', encoding='utf-8-sig')
            genre_manualCheckJSON = json.load(fallback)
            print("Fallback: offline manual checking json for genre loaded")
        genre_manualCheckJSON_hasLoaded = True
        
    except Exception as e:
        print(f"genre manual check json: Error fetching or parsing JSON: {e}")
        try:
            print("Fallback: loading from local database")
            fallback = open("AstroDX-Collection-Genre-Reorganizer/data/genre_manualCheck.json", 'r', encoding='utf-8-sig')
            genre_manualCheckJSON = json.load(fallback)
            print("Fallback: offline genre to title list loaded")
            genre_manualCheckJSON_hasLoaded = True
        except:
            genre_manualCheckJSON = []
            print("Failed to load genre to title information")
            genre_manualCheckJSON_hasLoaded = False

    try:
        response = urllib.request.urlopen(version_manualCheckURL)
        if response.status == 200:
            version_manualCheckJSON = json.loads(response.read())
            print("online manual checking json for version loaded")
        else:
            print(f"version manual check JSON: Failed to fetch data, status code: {response.status}")
            print("Fallback: loading from local database")
            fallback = open("AstroDX-Collection-Genre-Reorganizer/data/version_manualCheck.json", 'r', encoding='utf-8-sig')
            version_manualCheckJSON = json.load(fallback)
            print("Fallback: offline manual checking json for version loaded")
        version_manualCheckJSON_hasLoaded = True
        print("manual checking json for version loaded")
    except Exception as e:
        print(f"version manual check JSON: Error fetching or parsing JSON: {e}")
        try:
            print("loading from local database")
            fallback = open("AstroDX-Collection-Genre-Reorganizer/data/version_manualCheck.json", 'r', encoding='utf-8-sig')
            version_manualCheckJSON = json.load(fallback)
            print("Fallback: offline version to title list loaded")
            version_manualCheckJSON_hasLoaded = True
        except:
            version_manualCheckJSON = []
            print("Failed to load version to title information")
            version_manualCheckJSON_hasLoaded = False
       

    if not maimaisongInfoJSON_hasLoaded or not zetaraku_maimai_songlist_JSON_hasLoaded or not genre_manualCheckJSON_hasLoaded or not version_manualCheckJSON_hasLoaded:
        print("Failed to load all JSON files, please check your internet connection or the files in the directory")
        print(f"maimaisongInfoJSON: {maimaisongInfoJSON_hasLoaded}\n zetaraku_maimai_songlist_JSON: {zetaraku_maimai_songlist_JSON_hasLoaded}\n genre_manualCheckJSON: {genre_manualCheckJSON_hasLoaded}\n version_manualCheckJSON: {version_manualCheckJSON_hasLoaded}")
        exit()

    elif maimaisongInfoJSON_hasLoaded and zetaraku_maimai_songlist_JSON_hasLoaded and genre_manualCheckJSON_hasLoaded and version_manualCheckJSON_hasLoaded:
        print("All JSON files loaded successfully")
        print("Parsing genre and version information")

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
            else:
                if item.get('catcode') == '宴会場':
                    continue
                else:
                    debugging.write(f"Unknown catcode: {item.get('catcode')}\n Title: {item.get('title')}")
        print("Genre information parsed")

        for item in zetaraku_maimai_songlist_JSON["songs"]:
            if item.get('version') == 'maimai':
                maimai.append(item.get('songId'))
            elif item.get('version') == 'maimai PLUS':
                maimai_PLUS.append(item.get('songId'))
            elif item.get('version') == 'GreeN':
                GreeN.append(item.get('songId'))
            elif item.get('version') == 'GreeN PLUS':
                GreeN_PLUS.append(item.get('songId'))
            elif item.get('version') == 'ORANGE':
                ORaNGE.append(item.get('songId'))
            elif item.get('version') == 'ORANGE PLUS':
                ORaNGE_PLUS.append(item.get('songId'))
            elif item.get('version') == 'PiNK':
                PiNK.append(item.get('songId'))
            elif item.get('version') == 'PiNK PLUS':
                PiNK_PLUS.append(item.get('songId'))
            elif item.get('version') == 'MURASAKi':
                MURASAKi.append(item.get('songId'))
            elif item.get('version') == 'MURASAKi PLUS':
                MURASAKi_PLUS.append(item.get('songId'))
            elif item.get('version') == 'MiLK':
                MiLK.append(item.get('songId'))
            elif item.get('version') == 'MiLK PLUS':
                MiLK_PLUS.append(item.get('songId'))
            elif item.get('version') == 'FiNALE':
                FiNALE.append(item.get('songId'))
            elif item.get('version') == 'maimaiでらっくす':
                Deluxe.append(item.get('songId'))
            elif item.get('version') == 'maimaiでらっくす PLUS':
                Deluxe_PLUS.append(item.get('songId'))
            elif item.get('version') == 'Splash':
                Splash.append(item.get('songId'))
            elif item.get('version') == 'Splash PLUS':
                Splash_PLUS.append(item.get('songId'))
            elif item.get('version') == 'UNiVERSE':
                UNiVERSE.append(item.get('songId'))
            elif item.get('version') == 'UNiVERSE PLUS':
                UNiVERSE_PLUS.append(item.get('songId'))
            elif item.get('version') == 'FESTiVAL':
                FESTiVAL.append(item.get('songId'))
            elif item.get('version') == 'FESTiVAL PLUS':
                FESTiVAL_PLUS.append(item.get('songId'))
            elif item.get('version') == 'BUDDiES':
                BUDDiES.append(item.get('songId'))
            elif item.get('version') == 'BUDDiES PLUS':
                BUDDiES_PLUS.append(item.get('songId'))
            else:
                if item.get('version') == '':
                    continue
                else:
                    debugging.write(f"parse_JSON_Database() Unknown version: {item.get('version')} Title: {item.get('title')}\n")
        print("Version information parsed")
        print("Parsing complete")

    return maimaiSongInfoJSON, zetaraku_maimai_songlist_JSON, genre_manualCheckJSON, version_manualCheckJSON


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

def check_toGenre(root_path,maimaiSongInfoJSON,genre_manualCheckJSON):
    checkPop, checkVocaloid, checkTouhou, checkGame, checkMaimai, checkOngeki, checkUtage, checkChinese, checkUnidentifiedGenre = [],[],[],[],[],[],[],[],[]
    for root, dirs, files in os.walk(root_path):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            maidata_path = os.path.join(folder_path, 'maidata.txt')
            
            if os.path.isfile(maidata_path):
                lv_7_value, title_value = parse_maidata(maidata_path)
                print(f"&title:\t\t{title_value}")

                if lv_7_value:
                    print(f"matched to in maimaiJSON: \tutage")
                    checkUtage.append(title_value)

                elif title_value in popAndAnime or folder in popAndAnime:
                    print(f"matched to maimaiJSON: \tpop and anime")
                    checkPop.append(title_value)

                elif title_value in niconicoAndVocaloid or folder in niconicoAndVocaloid:
                    print(f"matched to maimaiJSON: \tniconico and vocaloid")
                    checkVocaloid.append(title_value)

                elif title_value in touhouProject or folder in touhouProject:
                    print(f"matched to maimaiJSON: \ttouhou project")
                    checkTouhou.append(title_value)

                elif title_value in gameAndVariety or folder in gameAndVariety:
                    print(f"matched to maimaiJSON: \tgame and variety")
                    checkGame.append(title_value)

                elif title_value in maimai or folder in maimai:
                    print(f"matched to maimaiJSON: \tmaimai")
                    checkMaimai.append(title_value)
                
                elif title_value in ongekiAndChunithm or folder in ongekiAndChunithm:
                    print(f"matched to maimaiJSON: \tongeki and chunithm")
                    checkOngeki.append(title_value)
                
                else:
                    if title_value in genre_manualCheckJSON:
                        if genre_manualCheckJSON[title_value] == "POPS＆アニメ":
                            print(f"matched to genre_manualCheckJSON: \tpop and anime")
                            checkPop.append(title_value)

                        elif genre_manualCheckJSON[title_value] == "niconico＆ボーカロイド":
                            print(f"matched to genre_manualCheckJSON: \tniconico and vocaloid")
                            checkVocaloid.append(title_value)

                        elif genre_manualCheckJSON[title_value] == "東方Project":
                            print(f"matched to genre_manualCheckJSON: \ttouhou project")
                            checkTouhou.append(title_value)

                        elif genre_manualCheckJSON[title_value] == "ゲーム＆バラエティ":
                            print(f"matched to genre_manualCheckJSON: \tgame and variety")
                            checkGame.append(title_value)

                        elif genre_manualCheckJSON[title_value] == "maimai":
                            print(f"matched to genre_manualCheckJSON: \tmaimai")
                            checkMaimai.append(title_value)

                        elif genre_manualCheckJSON[title_value] == "オンゲキ＆CHUNITHM":
                            print(f"matched to genre_manualCheckJSON: \tongeki and chunithm")
                            checkOngeki.append(title_value)

                        elif genre_manualCheckJSON[title_value] == "中国流行乐":
                            print(f"matched to genre_manualCheckJSON: \tchinese pop")
                            checkChinese.append(title_value)

                        elif genre_manualCheckJSON[title_value] == "宴会場":
                            print(f"matched to genre_manualCheckJSON: \tutage")
                            checkUtage.append(title_value)

                        else:
                            print(f"{title_value} found in manual check, value empty, @venb304 please update manualCheck.json")
                            checkUnidentifiedGenre.append(title_value)
                    else:
                        if title_value:
                            print(title_value + " not match, Unidentified genre")
                            checkUnidentifiedGenre.append(title_value)
                            debugging.write(f"Unidentified genre: {title_value}\n lv 7 value: {lv_7_value}\n")
                        else:
                            print(f"No title found, Unidentified genre in {folder_path}")
                            checkUnidentifiedGenre.append(folder_path)
                
            else:
                print(f"{folder_path} is empty, moving on")

    checkLog = open("logging/checkingLog.txt","w", encoding="utf-8-sig")
    checkLog.write("Check only Log for genres, the following are the folders that are matched to the genre\n")
    checkLog.write("Pop and Anime:\n")
    for item in checkPop:
        checkLog.write(f"\t{item}\n")
    checkLog.write("Niconico and Vocaloid:\n")
    for item in checkVocaloid:
        checkLog.write(f"\t{item}\n")
    checkLog.write("Touhou Project:\n")
    for item in checkTouhou:
        checkLog.write(f"\t{item}\n")
    checkLog.write("Game and Variety:\n")
    for item in checkGame:
        checkLog.write(f"\t{item}\n")
    checkLog.write("Maimai:\n")
    for item in checkMaimai:
        checkLog.write(f"\t{item}\n")
    checkLog.write("Ongeki and Chunithm:\n")
    for item in checkOngeki:
        checkLog.write(f"\t{item}\n")
    checkLog.write("Utage:\n")
    for item in checkUtage:
        checkLog.write(f"\t{item}\n")
    checkLog.write("Chinese Pop:\n")
    for item in checkChinese:
        checkLog.write(f"\t{item}\n")
    checkLog.write("Unidentified:\n")
    for item in checkUnidentifiedGenre:
        checkLog.write(f"\t{item}\n")

    checkLog.write("If no charts falls under unidentified, then the collections are supported and is able to be reorganized properly and automatically.\n")
    checkLog.close()
    print("\nChecking to genre complete, See checkingLog.txt in logging folder for results\n")

def proces_toGenre(root_path, maimaiSongInfoJSON, genre_manualCheckJSON, catcode, operation):
    savedFolderPaths = [[],[],[],[],[],[],[],[],[]]

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
                    if title_value in genre_manualCheckJSON:
                        if genre_manualCheckJSON[title_value] == "POPS＆アニメ":
                            print(f"{title_value} matched to genre_manualCheckJSON: pop and anime")
                            savedFolderPaths[0].append(folder_path)

                        elif genre_manualCheckJSON[title_value] == "niconico＆ボーカロイド":
                            print(f"{title_value} matched to genre_manualCheckJSON: niconico and vocaloid")
                            savedFolderPaths[1].append(folder_path)

                        elif genre_manualCheckJSON[title_value] == "東方Project":
                            print(f"{title_value} matched to genre_manualCheckJSON: touhou project")
                            savedFolderPaths[2].append(folder_path)

                        elif genre_manualCheckJSON[title_value] == "ゲーム＆バラエティ":
                            print(f"{title_value} matched to genre_manualCheckJSON: game and variety")
                            savedFolderPaths[3].append(folder_path)

                        elif genre_manualCheckJSON[title_value] == "maimai":
                            print("title matched in manual check: maimai list")
                            savedFolderPaths[4].append(folder_path)

                        elif genre_manualCheckJSON[title_value] == "オンゲキ＆CHUNITHM":
                            print("title matched in manual check: ongeki and chunithm list")
                            savedFolderPaths[5].append(folder_path)

                        elif genre_manualCheckJSON[title_value] == "中国流行乐":
                            print("title matched in manual check: chinese pop list")
                            savedFolderPaths[7].append(folder_path)

                        elif genre_manualCheckJSON[title_value] == "宴会場":
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
        operationText = ["copy","move","copied","moved"]
        for savedPaths in category:
            if savedFolderPaths.index(category) == 8:
                unknownHandler(os.path.basename(savedPaths), savedPaths, catcode)
                continue
            else:
                os.makedirs(os.path.dirname(root_path) +"/" + os.path.basename(root_path) +" - Reorganized/" + catcode[savedFolderPaths.index(category)] + "/" + os.path.basename(savedPaths), exist_ok=True)
                try:
                    if operation == 0:
                        shutil.copytree(savedPaths, os.path.dirname(root_path) + "/" + os.path.basename(root_path)+ " - Reorganized/" + catcode[savedFolderPaths.index(category)] + "/" + os.path.basename(savedPaths), dirs_exist_ok=True)
                    elif operation == 1:
                        shutil.move(savedPaths, os.path.dirname(root_path) + "/" + os.path.basename(root_path)+ " - Reorganized/" + catcode[savedFolderPaths.index(category)] + "/" + os.path.basename(savedPaths))
                except:
                    print(f"Error: {operationText[operation]} failed: {savedPaths}")
                    debugging.write(f"Error: {operationText[operation]} failed: {savedPaths} to Reorganization Output folder\n")
                print(f"{operationText[operation+2]} to {catcode[savedFolderPaths.index(category)]}: {savedPaths}")

                # removed the creation of the levels folder and instead creates the genre folders in the root path
                # unfortunately, the original charts do still exist as this program just copies them to the genre folders
                # the original charts are not deleted
                # implement a way to first have program un-nest the folders first, 
                #   then create backup collection.json files to be used for reverting changes
                # either to generate it first using the function generate_manifest 
                #   or use the data.json from zetaraku's database of maimai songs to organize them as 
                #   necesseary by version again as a way to revert back after organizing by genre

    print("\nReorganization to genre grouping complete\n")

def check_toVersion(root_path, versionCode, zetaraku_maimai_songlist_JSON):
    print("Checking to Version")
    checkmaimai, checkmaimai_PLUS, checkGreeN, checkGreeN_PLUS, checkORaNGE, checkORaNGE_PLUS, checkPiNK, checkPiNK_PLUS, checkMURASAKi, checkMURASAKi_PLUS, checkMiLK, checkMiLK_PLUS, checkFiNALE, checkDeluxe, checkDeluxe_PLUS, checkSplash, checkSplash_PLUS, checkUNiVERSE, checkUNiVERSE_PLUS, checkFESTiVAL, checkFESTiVAL_PLUS, checkBUDDiES, checkBUDDiES_PLUS, checkUnidentifiedVersion = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
    for root, dirs, files in os.walk(root_path):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            maidata_path = os.path.join(folder_path, 'maidata.txt')
            if os.path.isfile(maidata_path):
                lv_7_value, title_value = parse_maidata(maidata_path)
                print(f"&title:\t\t{title_value}")
                if title_value.startswith("["):
                    title_value = title_value.replace("[","(").replace("]",")")
                    print(f"replaced title value: {title_value}")

                if title_value in maimai or folder in maimai:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: maimai")
                    checkmaimai.append(title_value)

                elif title_value in maimai_PLUS or folder in maimai_PLUS:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: maimai PLUS")
                    checkmaimai_PLUS.append(title_value)

                elif title_value in GreeN or folder in GreeN:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: GreeN")
                    checkGreeN.append(title_value)

                elif title_value in GreeN_PLUS or folder in GreeN_PLUS:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: GreeN PLUS")
                    checkGreeN_PLUS.append(title_value)

                elif title_value in ORaNGE or folder in ORaNGE:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: ORANGE")
                    checkORaNGE.append(title_value)

                elif title_value in ORaNGE_PLUS or folder in ORaNGE_PLUS:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: ORANGE PLUS")
                    checkORaNGE_PLUS.append(title_value)

                elif title_value in PiNK or folder in PiNK:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: PiNK")
                    checkPiNK.append(title_value)

                elif title_value in PiNK_PLUS or folder in PiNK_PLUS:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: PiNK PLUS")
                    checkPiNK_PLUS.append(title_value)

                elif title_value in MURASAKi or folder in MURASAKi:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: MURASAKi")
                    checkMURASAKi.append(title_value)

                elif title_value in MURASAKi_PLUS or folder in MURASAKi_PLUS:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: MURASAKi PLUS")
                    checkMURASAKi_PLUS.append(title_value)

                elif title_value in MiLK or folder in MiLK:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: MiLK")
                    checkMiLK.append(title_value)

                elif title_value in MiLK_PLUS or folder in MiLK_PLUS:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: MiLK PLUS")
                    checkMiLK_PLUS.append(title_value)

                elif title_value in FiNALE or folder in FiNALE:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: FiNALE")
                    checkFiNALE.append(title_value)

                elif title_value in Deluxe or folder in Deluxe:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: DX")
                    checkDeluxe.append(title_value)

                elif title_value in Deluxe_PLUS or folder in Deluxe_PLUS:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: DX PLUS")
                    checkDeluxe_PLUS.append(title_value)

                elif title_value in Splash or folder in Splash:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: Splash")
                    checkSplash.append(title_value)

                elif title_value in Splash_PLUS or folder in Splash_PLUS:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: Splash PLUS")
                    checkSplash_PLUS.append(title_value)

                elif title_value in UNiVERSE or folder in UNiVERSE:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: UNiVERSE")
                    checkUNiVERSE.append(title_value)

                elif title_value in UNiVERSE_PLUS or folder in UNiVERSE_PLUS:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: UNiVERSE PLUS")
                    checkUNiVERSE_PLUS.append(title_value)

                elif title_value in FESTiVAL or folder in FESTiVAL:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: FESTiVAL")
                    checkFESTiVAL.append(title_value)

                elif title_value in FESTiVAL_PLUS or folder in FESTiVAL_PLUS:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: FESTiVAL PLUS")
                    checkFESTiVAL_PLUS.append(title_value)

                elif title_value in BUDDiES or folder in BUDDiES:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: BUDDiES")
                    checkBUDDiES.append(title_value)

                elif title_value in BUDDiES_PLUS or folder in BUDDiES_PLUS:
                    print(f"matched to in zetaraku_maimai_songlist_JSON: BUDDiES PLUS")
                    checkBUDDiES_PLUS.append(title_value)

                else:
                    print(f"\nunable to determine version for {title_value} in {folder_path}")
                    checkUnidentifiedVersion.append(title_value)

    checkLog = open("logging/checkingLog.txt","w", encoding="utf-8-sig")
    checkLog.write("Check only Log for version, the following are the folders that are matched to the version\n")
    checkLog.write("maimai:\n")
    
    for item in checkmaimai:
        checkLog.write(f"\t{item}\n")
    checkLog.write("maimai PLUS:\n")
    for item in checkmaimai_PLUS:
        checkLog.write(f"\t{item}\n")
    checkLog.write("GreeN:\n")
    for item in checkGreeN:
        checkLog.write(f"\t{item}\n")
    checkLog.write("GreeN PLUS:\n")
    for item in checkGreeN_PLUS:
        checkLog.write(f"\t{item}\n")
    checkLog.write("ORANGE:\n")
    for item in checkORaNGE:
        checkLog.write(f"\t{item}\n")
    checkLog.write("ORANGE PLUS:\n")
    for item in checkORaNGE_PLUS:
        checkLog.write(f"\t{item}\n")
    checkLog.write("PiNK:\n")
    for item in checkPiNK:
        checkLog.write(f"\t{item}\n")
    checkLog.write("PiNK PLUS:\n")
    for item in checkPiNK_PLUS:
        checkLog.write(f"\t{item}\n")
    checkLog.write("MURASAKi:\n")
    for item in checkMURASAKi:
        checkLog.write(f"\t{item}\n")
    checkLog.write("MURASAKi PLUS:\n")
    for item in checkMURASAKi_PLUS:
        checkLog.write(f"\t{item}\n")
    checkLog.write("MiLK:\n")
    for item in checkMiLK:
        checkLog.write(f"\t{item}\n")
    checkLog.write("MiLK PLUS:\n")
    for item in checkMiLK_PLUS:
        checkLog.write(f"\t{item}\n")
    checkLog.write("FiNALE:\n")
    for item in checkFiNALE:
        checkLog.write(f"\t{item}\n")
    checkLog.write("DX:\n")
    for item in checkDeluxe:
        checkLog.write(f"\t{item}\n")
    checkLog.write("DX PLUS:\n")
    for item in checkDeluxe_PLUS:
        checkLog.write(f"\t{item}\n")
    checkLog.write("Splash:\n")
    for item in checkSplash:
        checkLog.write(f"\t{item}\n")
    checkLog.write("Splash PLUS:\n")
    for item in checkSplash_PLUS:
        checkLog.write(f"\t{item}\n")
    checkLog.write("UNiVERSE:\n")
    for item in checkUNiVERSE:
        checkLog.write(f"\t{item}\n")
    checkLog.write("UNiVERSE PLUS:\n")
    for item in checkUNiVERSE_PLUS:
        checkLog.write(f"\t{item}\n")
    checkLog.write("FESTiVAL:\n")
    for item in checkFESTiVAL:
        checkLog.write(f"\t{item}\n")
    checkLog.write("FESTiVAL PLUS:\n")
    for item in checkFESTiVAL_PLUS:
        checkLog.write(f"\t{item}\n")
    checkLog.write("BUDDiES:\n")
    for item in checkBUDDiES:
        checkLog.write(f"\t{item}\n")
    checkLog.write("BUDDiES PLUS:\n")
    for item in checkBUDDiES_PLUS:
        checkLog.write(f"\t{item}\n")
    checkLog.write("Unidentified:\n")
    for item in checkUnidentifiedVersion:
        checkLog.write(f"\t{item}\n")
    checkLog.write("If no charts falls under unidentified, then the collections are supported and is able to be reorganized properly and automatically.\n")
    checkLog.close()

    print("\nChecking to Version complete, See checkingLog.txt in logging folder for results\n")
                    
def proces_toVersion(root_path, versionCode):
    print("Processing to Version")



# Start of the program
os.makedirs("logging", exist_ok=True)
debugging = open("logging/debugging.txt","w", encoding="utf-8-sig")
unidentifiedChartsDebug = open("logging/unidentifiedCharts.txt","w", encoding="utf-8-sig")

popAndAnime = []
niconicoAndVocaloid = []
touhouProject = []
gameAndVariety = []
maimai = []
ongekiAndChunithm = []

maimai = []
maimai_PLUS = []
GreeN = []
GreeN_PLUS = []
ORaNGE = []
ORaNGE_PLUS = []
PiNK = []
PiNK_PLUS = []
MURASAKi = []
MURASAKi_PLUS = []
MiLK = []
MiLK_PLUS = []
FiNALE = []
Deluxe = []
Deluxe_PLUS = []
Splash = []
Splash_PLUS = []
UNiVERSE = []
UNiVERSE_PLUS = []
FESTiVAL = []
FESTiVAL_PLUS = []
BUDDiES = []
BUDDiES_PLUS = []


catcode = [["POPS＆アニメ", "niconico＆ボーカロイド", "東方Project", "ゲーム＆バラエティ", "maimai", "オンゲキ＆CHUNITHM", "宴会場", "中国流行乐","UNIDENTIFEIED"],["POPS ＆ ANIME", "niconico＆VOCALOID", "TOUHOU Project", "GAME ＆ VARIETY", "maimai", "ONGKEI ＆ CHUNITHM", "UTAGE", "CHINESE-POP","UNIDENTIFIED"]]
versionCode = ["01. maimai","02. maimai PLUS","02.5. 舞萌中国", "03. GreeN","04. Green PLUS","05. ORANGE", "06. ORANGE PLUS", "07. PiNK", "08. PiNK PLUS", "09. MURASAKi", "10. MURASAKi PLUS", "11. MiLK", "12. MiLK PLUS", "13. FiNALE", "14. DX", "15. DX PLUS", "16. Splash", "17. Splash PLUS", "18. UNiVERSE", "19. UNiVERSE PLUS", "20. FESTiVAL", "21. FESTiVAL PLUS", "22. BUDDiES", "23. BUDDiES PLUS"]
maimaiSongInfoJSON = []
genre_manualCheckJSON = []
zetaraku_maimai_songlist_JSON = []

genre_manualCheckURL = "https://raw.githubusercontent.com/VenB304/AstroDX-Collection-Reorganizer/main/data/genre_manualCheck.json"
version_manualCheckURL = "https://raw.githubusercontent.com/VenB304/AstroDX-Collection-Reorganizer/main/data/version_manualCheck.json"
zetaraku_maimai_songlist_URL = "https://raw.githubusercontent.com/VenB304/AstroDX-Collection-Reorganizer/main/data/zetaraku_maimai_songlist.json"
maimai_JP_songlist_URL = "https://maimai.sega.jp/data/maimai_songs.json"
maimai_JP_songlist_other_URL = "https://raw.githubusercontent.com/VenB304/AstroDX-Collection-Reorganizer/main/data/maimai_songs.json"

maimaiSongInfoJSON, zetaraku_maimai_songlist_JSON, genre_manualCheckJSON, version_manualCheckJSON = parse_JSON_Database()


running = True

while running:
    print("\nMenu\n")
    #CHecks
    print("[1] Check given path if compatible for GENRE GROUPING (folder structure is ignored, only checks for maidata.txt)")
    print("[2] Check given path if compatible for VERSION GROUPING (if you want to go back to version grouping from genre grouping)")
    #Restructure
    print("[3] Restructure into GENRE GROUPING (folder structure is ignored as it moved folders with maidata.txt to genre folders)")
    print("[4] Restructure into VERSION GROUPING (folder structure is ignored as it moved folders with maidata.txt to version folders)")
    #Compatibility
    print("[5] For Beta 2.0: Generate ADX Archives (use option[3] or [4] for this for easy importing to AstroDX)\n\t(Warning: Only use if the charts totals to 2gb or less, bigger sizes is not supported as of Beta 2 Patch 5)")
    print("[6] For Beta 2.0: With the give path, generates the manifest.json files and levels structure to be used for the newer beta 2.0 of AstroDX\n\t(Note: this is your best option to use for now, without zip64 support for astrodx, this is the only way to reorganize the collection)")
    print("[7] For Pre Beta: Restructure for pre beta (Note: options [2] and [4] is already structured for pre beta, if current structure is for beta 2.0, use this to revert back to import)")
    
    # list of what i wanna do now
    # 1. Perform CHeck: check folders only for genre grouping and displays the genre it belongs to
    # 2. Perform organize into Genre: checks and takes a list matched and unidentified folders, copies the content of matched folders to genre folders, and user can choose what to do with unidentified folders
    # 2.1 also implement to copy or to move the files to the genre folders and makes it so that the will be unnested
    # 3. Restructure Collection: generate collection.json files and unnests the folders from path to be used for newer beta 2.0 of AstroDX
    # 4. Restructure Collection for pre beta: reads collection.json files and restructures the folders to be nested for pre beta versions of AstroDX(ehem, apple devices hehe[this could become outdated as fumi might update for apple deviced any time now])
    # 5. backup: use generate_manifest to create a backup of the current collection and to be used to revert back to the original collections
    # 6. restore: use the backup collection.json files to revert back to the original collections

    print("[0] Exit")

    choice = str(input("Enter the number you wanna do: "))

    match choice:
        case "1":
            print("Sample path: C:/Users/username/Downloads/maisquared/")
            root_path = input("Enter the root directory path: ").strip()
            check_toGenre(root_path,maimaiSongInfoJSON,genre_manualCheckJSON)
        case "2":
            print("check only for Version grouping")
            print("path should have a the following:")
            print(" - collection folder: inside that more folder with each has manifest.json, ")
            print(" - levels folder: should be the charts/levels folders that each contain maidata.txt and the rest")
            root_path = input("Enter path: ")
            check_toVersion(root_path, versionCode, zetaraku_maimai_songlist_JSON)
        case "3":
            print("Sample path: C:/Users/username/Downloads/maisquared/")
            root_path = input("Enter the root directory path: ").strip()
            langChosen = False
            while not langChosen:
                print("\nJapanese or English Collection Name:")
                print("[0] Japanese Collection Name")
                print("[1] English Collection Name")
                catLang = str(input("Enter choice: ")).strip()
                if catLang in ["0","1"]:
                    langChosen = True
                else:
                    print("Invalid choice, please try again")
                    langChosen = False
                    continue

            operationChosen = False
            while not operationChosen:
                print("\nTo Copy, or to Move(Warning: Moving will move the files instead of keeping a copy)")
                print("[0] Copy")
                print("[1] Move")
                operation = str(input("Enter choice: ")).strip()
                if operation in ["0","1"]:
                    operation = int(operation)
                    operationChosen = True
                else:
                    print("Invalid choice, please try again")
                    operationChosen = False
                    continue
            proces_toGenre(root_path,maimaiSongInfoJSON,genre_manualCheckJSON,catcode[int(catLang)], operation)
        case "4":
            print("Version grouping")
            print("path should have a the following:")
            print(" - collection folder: inside that more folder with each has manifest.json, ")
            print(" - levels folder: should be the charts/levels folders that each contain maidata.txt and the rest")
            root_path = input("Enter path: ")
            proces_toVersion(root_path, versionCode)
            # need to implement
        case "5":
            print("Generating ADX Archives")
            print("zip64 to be implemented by fumiko, the dev of astrodx, to astrodx. to which CURRENTLY DOES NOT SUPPORT ADX ARCHIVES BIGGER THAN 2GB")
            print("idk maybe fumiko will, the current supported is the original zip format, zip64 is probably still similar")
            print("this will still generate zip64 files with the file extention renamed to .adx")

            toSave = False
            while not toSave:
                root_path = input("Enter the root directory path: ").strip()
                zip_name = input("Enter the name of the zip [exluding the file extention'.zip' or '.adx', it will be automatically added in]: ").strip()
                print(f"ADX Archives will be generated in {root_path}/{zip_name}.adx")
                decided = False
                while not decided:
                    choice = input("Do you want to save the adx archive here?? (y/n): ").strip()
                    if choice == "y":
                        toSave = True
                        decided = True
                    elif choice == "n":
                        toSave = False
                        decided = True
                    else:
                        print("Invalid choice, please try again")
                        decided = False
                        continue
            zip_folder(root_path, (zip_name + ".adx"))

        case "6":
            print("Generating collection.json files")
            print("this will generate collection.json files in the levels folder of a path")
            print("Sample root path: C:/Users/username/Downloads/maisquared/levels")
            print("inside the levels folder or any folder, there should be genre folders like pop and anime, niconico and vocaloid, etc.")
            
            # get a way to save and use the recent genre or version grouping to be used with this function
            root_path = input("Enter the root directory path: ").strip()
            replace_files = input("Move files in levels folder to output? this will move them instead of copy only(y/n): ").strip()
            append_guid = input("Append GUID to folder names? (y/n): ").strip()

            if replace_files == "y":
                replace_files = True
            else:
                replace_files = False

            if append_guid == "y":
                append_guid = True
            else:
                append_guid = False

            generate_manifest(root_path, replace_files, append_guid)

            print(f"collection.json files generated in {root_path}/output")
        

        case "7":
            print("Restructuring for pre beta")
            print("to be implemented")

        case "0":
            print("Exiting program")
            debugging.close()
            unidentifiedChartsDebug.close()

            running = False
        case _:
            print("Invalid choice, please try again")
            continue