import os
import json
import urllib.request
import shutil

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

def process_folders(root_path):
    for root, dirs, files in os.walk(root_path):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            maidata_path = os.path.join(folder_path, 'maidata.txt')
            
            if os.path.isfile(maidata_path):
                lv_7_value, title_value = parse_maidata(maidata_path)
                print(f"Folder: {folder}")
                print(f"&lv_7: {lv_7_value}")
                print(f"&title: {title_value}")
                
                if lv_7_value:
                    print("utage found")
                    savedFolderPaths[6].append(folder_path)
                    #move or copy to utage folder

                elif title_value in popAndAnime or folder in popAndAnime:
                    #move or copy to pop and anime folder
                    print("title value matched in pop and anime list")
                    savedFolderPaths[0].append(folder_path)

                elif title_value in niconicoAndVocaloid or folder in niconicoAndVocaloid:
                    #move or copy to niconico and vocaloid folder
                    print("title value matched in niconico and vocaloid list")
                    savedFolderPaths[1].append(folder_path)

                elif title_value in touhouProject or folder in touhouProject:
                    #move or copy to touhou project folder
                    print("title value matched in touhou project list")
                    savedFolderPaths[2].append(folder_path)

                elif title_value in gameAndVariety or folder in gameAndVariety:
                    #move or copy to game and variety folder
                    print("title value matched in game and variety list")
                    savedFolderPaths[3].append(folder_path)

                elif title_value in maimai or folder in maimai:
                    #move or copy to maimai folder
                    print("title value matched in maimai list")
                    savedFolderPaths[4].append(folder_path)
                
                elif title_value in ongekiAndChunithm or folder in ongekiAndChunithm:
                    #move or copy to ongeki and chunithm folder
                    print("title value mathed in ongeki and chunithm list")
                    savedFolderPaths[5].append(folder_path)
                
                else:
                    if title_value in manualCheckJSON:
                        if manualCheckJSON[title_value] == "POPS＆アニメ":
                            print("title matched in manual check: pop and anime list")
                            savedFolderPaths[0].append(folder_path)

                        elif manualCheckJSON[title_value] == "niconico＆ボーカロイド":
                            print("title matched in manual check: niconico and vocaloid list")
                            savedFolderPaths[1].append(folder_path)

                        elif manualCheckJSON[title_value] == "東方Project":
                            print("title matched in manual check: touhou project list")
                            savedFolderPaths[2].append(folder_path)

                        elif manualCheckJSON[title_value] == "ゲーム＆バラエティ":
                            print("title matched in manual check: game and variety list")
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
                            unidentifiedChartsDebug.write(title_value + " found in manual check, value empty, @venb304 please update manualCheck.json" + folder_path + "\n")
                            # move or copy to unidentified folder
                    else:
                        if title_value:
                            print(title_value + " not match, Unidentified genre")
                            unidentifiedChartsDebug.write(title_value + " not matched, Unidentified genre\n")
                        else:
                            print("No title found, Unidentified genre")
                            unidentifiedChartsDebug.write("No title found, Unidentified genre in " + folder_path + "\n")  
                        
                        savedFolderPaths[8].append(folder_path)
                
                print("-" * 30)
            else:
                print("Current folder empty, moving on...\n\n")

debugging = open("debugging.txt","w", encoding="utf-8-sig")

manualCheckURL = "https://raw.githubusercontent.com/VenB304/AstroDX-Collection-Genre-Reorganizer/main/manualCheck.json"
maimai_JP_songlist_URL = "https://maimai.sega.jp/data/maimai_songs.json"
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

popAndAnime = []
niconicoAndVocaloid = []
touhouProject = []
gameAndVariety = []
maimai = []
ongekiAndChunithm = []
Utage = []

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

savedFolderPaths = [[],[],[],[],[],[],[],[],[]]
catcode = ["POPS＆アニメ", "niconico＆ボーカロイド", "東方Project", "ゲーム＆バラエティ", "maimai", "オンゲキ＆CHUNITHM", "宴会場", "中国流行乐","Unidentified"]
# 0 = pop and anime
# 1 = niconico and vocaloid
# 2 = touhou project
# 3 = game and variety
# 4 = maimai
# 5 = ongeki and chunithm
# 6 = utage
# 7 = chinese pop
# 8 = unidentified

unidentifiedChartsDebug = open("unidentifiedCharts.txt","a", encoding="utf-8-sig")

root_path = input("Enter the root directory path: ").strip()
process_folders(root_path)



for category in savedFolderPaths:
    match savedFolderPaths.index(category):
        case 0:
            print("current category: pop and anime\n\n")
        case 1:
            print("current category: niconico and vocaloid\n\n")
        case 2:
            print("current category: touhou project\n\n")
        case 3:
            print("current category: game and variety\n\n")
        case 4:
            print("current category: maimai\n\n")
        case 5:
            print("current category: ongeki and chunithm\n\n")
        case 6:
            print("current category: utage\n\n")
        case 7:
            print("current category: chinese pop\n\n")
        case 8:
            print("current category: unidentified\n\n")
        case _:
            print("current category: how? there should not be another category, how did this return to 8\n\n")
    
    for savedPaths in category:
        print(f"current folder: {savedPaths}\n")
        os.makedirs(root_path+"/levels/" + catcode[savedFolderPaths.index(category)] + "/" + os.path.basename(savedPaths), exist_ok=True)
        try:
            shutil.copytree(savedPaths, root_path + "/levels/" + catcode[savedFolderPaths.index(category)] + "/" + os.path.basename(savedPaths), dirs_exist_ok=True)
        except:
            print(f"Error copying {savedPaths} to Output folder")
            debugging.write(f"Copy Error: {savedPaths} to Output folder\n")
        print(f"{savedPaths} moved to Output folder")


