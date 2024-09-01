import json
import urllib.request
import os
import shutil

# Define genre lists
popAndAnime = []
niconicoAndVocaloid = []
touhouProject = []
gameAndVariety = []
maimai = []
ongekiAndChunithm = []
Utage = []

def load_mapping_file(mapping_url):
    mappings = {}
    try:
        response = urllib.request.urlopen(mapping_url)
        if response.status == 200:
            # Load the JSON content directly
            mappings = json.loads(response.read().decode('utf-8'))
        else:
            print(f"Failed to fetch mapping file, status code: {response.status}")
    except Exception as e:
        print(f"Error fetching or parsing mapping file: {e}")
    return mappings

def update_mapping_file(mapping_file, folder, genre):
    # This function can be used to handle updates if needed
    pass

def create_genre_folders(base_directory, names_lists, mapping_url):
    parent_directory = os.path.dirname(base_directory)
    base_directory_name = os.path.basename(base_directory)
    new_directory = os.path.join(parent_directory, f"{base_directory_name} Grouped as Genre")
    os.makedirs(new_directory, exist_ok=True)

    # Create the "Unknown" folder
    unknown_folder = os.path.join(new_directory, "Unknown")
    os.makedirs(unknown_folder, exist_ok=True)

    # Load folder mappings from the online JSON file
    folder_mappings = load_mapping_file(mapping_url)

    # Walk through all subdirectories and files
    for root, dirs, files in os.walk(base_directory):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            has_bg_or_track = any(f.lower().startswith(("bg", "track")) for f in os.listdir(folder_path))
            
            if has_bg_or_track:
                matched = False
                if folder in folder_mappings:
                    # Use the genre from the mapping file
                    genre = folder_mappings[folder]
                    genre_folder = os.path.join(new_directory, genre)
                    os.makedirs(genre_folder, exist_ok=True)
                    destination = os.path.join(genre_folder, folder)
                    try:
                        shutil.copytree(folder_path, destination, dirs_exist_ok=True)
                        matched = True
                    except Exception as e:
                        print(f"Error copying folder {folder_path} to {destination}: {e}")
                else:
                    for list_name, name_list in names_lists.items():
                        if folder in name_list:
                            genre_folder = os.path.join(new_directory, list_name)
                            os.makedirs(genre_folder, exist_ok=True)
                            destination = os.path.join(genre_folder, folder)
                            try:
                                shutil.copytree(folder_path, destination, dirs_exist_ok=True)
                                matched = True
                                break
                            except Exception as e:
                                print(f"Error copying folder {folder_path} to {destination}: {e}")
                                matched = False
                                break

                if not matched:
                    # Move unmatched folders to the "Unknown" folder
                    destination = os.path.join(unknown_folder, folder)
                    try:
                        shutil.copytree(folder_path, destination, dirs_exist_ok=True)
                        # Prompt user to manually map the folder later
                        print(f"Folder '{folder}' was not matched. Please update the mapping file with the correct genre.")
                    except Exception as e:
                        print(f"Error copying folder {folder_path} to {destination}: {e}")

directory = input("Enter the base directory path: ").strip()
mapping_url = "https://raw.githubusercontent.com/VenB304/AstroDX-Collection-Genre-Reorganizer/711fb494c77bed825e030339f0d46382a040b379/folder_mapping.json"

# Example URL and JSON parsing
maimaiSongListURL = "https://maimai.sega.jp/data/maimai_songs.json"
try:
    response = urllib.request.urlopen(maimaiSongListURL)
    if response.status == 200:
        maimaiSongList = json.loads(response.read())
    else:
        print(f"Failed to fetch data, status code: {response.status}")
        maimaiSongList = []
except Exception as e:
    print(f"Error fetching or parsing JSON: {e}")
    maimaiSongList = []

for item in maimaiSongList:
    if item.get('catcode') == 'maimai':
        maimai.append(item.get('title'))
        maimai.append(item.get('title_kana'))
    elif item.get('catcode') == 'POPS＆アニメ':
        popAndAnime.append(item.get('title'))
        popAndAnime.append(item.get('title_kana'))
    elif item.get('catcode') == 'ゲーム＆バラエティ':
        gameAndVariety.append(item.get('title'))
        gameAndVariety.append(item.get('title_kana'))
    elif item.get('catcode') == '宴会場':
        Utage.append(item.get('title'))
        Utage.append(item.get('title_kana'))
    elif item.get('catcode') == '東方Project':
        touhouProject.append(item.get('title'))
        touhouProject.append(item.get('title_kana'))
    elif item.get('catcode') == 'niconico＆ボーカロイド':
        niconicoAndVocaloid.append(item.get('title'))
        niconicoAndVocaloid.append(item.get('title_kana'))
    elif item.get('catcode') == 'オンゲキ＆CHUNITHM':
        ongekiAndChunithm.append(item.get('title'))
        ongekiAndChunithm.append(item.get('title_kana'))

testObject = {
    "POPS＆アニメ": popAndAnime,
    "niconico＆ボーカロイド": niconicoAndVocaloid,
    "東方Project": touhouProject,
    "ゲーム＆バラエティ": gameAndVariety,
    "maimai": maimai,
    "オンゲキ＆CHUNITHM": ongekiAndChunithm,
    "宴会場": Utage
}

create_genre_folders(directory, testObject, mapping_url)
