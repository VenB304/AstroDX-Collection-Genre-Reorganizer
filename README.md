To do list maybe:
- ~~Complete and maintain mapping json~~
  - Maintain manualCheck.json for updates
- Collection manager with this json thingies for the game
  - a way to revert them into grouping by version or a custom made by the user if ever needed
- ~~unknown handler~~
  - what you wanna do, trash, keep to unknown folder or choose where(only able to copy to unknown folder for now)
- collection manager
  - move copy remove add charts to a collection 
- maybe learn how this shit works and maybe, just maybe I get better and stop relying on chatgpt

User usage to do list
1. Perform CHeck: check folders only for genre grouping and displays the genre it belongs to
2. Perform organize into Genre: checks and takes a list matched and unidentified folders, copies the content of matched folders to genre folders, and user can choose what to do with unidentified folders
   - also implement to copy or to move the files to the genre folders and makes it so that the will be unnested
3. Restructure Collection: generate collection.json files and unnests the folders from path to be used for newer beta 2.0 of AstroDX
4. Restructure Collection for pre beta: reads collection.json files and restructures the folders to be nested for pre beta versions of AstroDX(ehem, apple devices hehe[this could become outdated as fumi might update for apple deviced any time now])
5. backup: use generate_manifest to create a backup of the current collection and to be used to revert back to the original collections
6. restore: use the backup collection.json files to revert back to the original collections

# AstroDX Collection Genre Reorganizer

Sorts charts under a path into of the following genre categories:

1. pop and anime
2. niconico and vocaloid
3. touhou project
4. game and variety
5. maimai
6. ongeki and chunithm
7. Utage
8. Chinese pop
9. Unknown (in cases where it cannot find a genre to where it matches)

- able to categorize charts to genre as of September 5, 2024
- mostly able to categorize charts to version as of Semptember 8, 2024
  - could not account for 105, waiting for version_manualCheck.json to be filled up

## Description

This project automates the sorting and categorization of maimai song charts into their respective genres based on a JSON mapping file. The script parses folders and files, identifies genre categories from chart data, and organizes them into specific directories. Unidentified charts are either logged or manually categorized by the user.

## Features
- Generate Manifest Files
  - Automatically create manifest.json files for each directory, with optional GUID appending.
- Customizable Chart Sorting
  - Organizes song charts into genres based on provided data in a JSON file or manual input.
- Unidentified Handler
  - Allows users to decide how to process folders that don’t match known genres by either copying them to an unidentified folder, logging them, or assigning them manually.
- Support for Manual and Automated Classification
  - The script uses both automatic matching against JSON data and manual input for unidentified items.

more chatgpt bs, raahhhhh

## Prerequisuites

- install python at maybe atleast 3.x

## Installation

To install the AstroDX Collection Genre Reorganizer, follow these steps:

1. DOwnload whole project (Code > DOwnload Zip): this will most like be more updated than release executable 

## Usage

To use the AstroDX Collection Genre Reorganizer, follow these steps:

1. execute main.py in your command line
2. follow on console instructions

[1] Check folders only for GENRE grouping
 - Checks folders from the path you input for GENRE grouping, and verify if all the charts was successfully categorized, if not, the unidentified charts will be tagged as Unidentified Genere
 - this will not copy to levels folder
 - Sample path: C:/Users/username/Downloads/maisquared/"

[2] Check folders for GENRE grouping and copy to Output folder
 - CHecks folders for GENRE grouping and copies the identified folders and paste it in a new folder "levels"
 - this will copy to levels folder within the same root directory/path you input"
 - Sample path: C:/Users/username/Downloads/maisquared/"
 - inside the maisquared folder, there should be folders with maidata.txt files
 - after the program is finished, inside the levels folder there should be genre folders like pop and anime, niconico and vocaloid, etc.
 - In the event this program encounters unidentified charts, you can choose the option to paste them in the "Unidentified" Folder, manually choose a genre to paste it in, or Log the chart in "unidentifiedCharts.txt" and ignore.

[3] Generate collection.json files
 - generates the necessary collection.json files to be used for AstroDX
 - this will generate collection.json files and saves them to "output" folder
 - Sample root path: C:/Users/username/Downloads/maisquared/levels/
 - inside the levels folder or any folder, there should be genre folders like pop and anime, niconico and vocaloid, etc.
   - can also be used for normal grouping by version, or grouped according to user.

 (To maintainer of this project, update usage to allow users to better understand how to use the program)

## Attribution

This project has a file called "zetakaru_maimai_songlist.json", a copied json file from [arcade-songs](https://github.com/zetaraku/arcade-songs), created by [zetaraku](https://github.com/zetaraku). This component is used with permission, and credit is attributed to the original project as required.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.
6. ???
7. Profit

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
