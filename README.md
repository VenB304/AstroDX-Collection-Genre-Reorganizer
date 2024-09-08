# AstroDX Collection Genre Reorganizer

groups charts under a path into of the following genre categories:

1. pop and anime
2. niconico and vocaloid
3. touhou project
4. game and variety
5. maimai
6. ongeki and chunithm
7. Utage
8. Chinese pop
9. Unknown (in cases where it cannot find a genre to where it matches)

Groups charts under a path into the following version categories
 - up to Buddies plus

Status
 - able to categorize charts to genre as of September 5, 2024
 - able to categorize charts to version as of Semptember 8, 2024

## Description

This project automates the sorting and categorization of maimai song charts into their respective genres based on a JSON mapping file. The script parses folders and files, identifies genre categories from chart data, and organizes them into specific directories. Unidentified charts are either logged or manually categorized by the user.

## Features
- Automatic Grouping check
  - Checks the folders if there are able to be grouped by GENRE or by VERSION
- Structure Reorganization and Automatic Grouping
  - Organizes song charts into genres or version from a given path.
    - Uses Pre Beta Structure
- Generate ADX Archives (For Beta 2.0)
  - Currently has partial support from the game, only able to be used if total size of the archive is less than 2gb
  - Hoping Fumiko supports zip64 soon
- Generate Manifest.json files and unnests charts
  - Automatically creates manifest.json files for each directory, with optional GUID appending, and operation to copy or move.
  - To be used along side the automatic restructuring or path has pre beta folder structure
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

[1] Check given path if compatible for GENRE GROUPING (folder structure is ignored, only checks for maidata.txt)
 - Checks folders from the path you input for GENRE grouping, and verify if all the charts was successfully categorized, if not, the unidentified charts will be tagged as Unidentified and logged in checkLog.txt
 - 
[2] Check given path if compatible for VERSION GROUPING (if you want to go back to version grouping from genre grouping)
 - Checks folders from the path you input for VERSION grouping, and verify if all the charts was successfully categorized, if not, the unidentified charts will be tagged as Unidentified and logged in checkLog.txt
 - 
[3] Restructure into GENRE GROUPING (folder structure is ignored as it moved folders with maidata.txt to genre folders)
 - CHecks folders for GENRE grouping and saves folder path
 - this will copy or move the charts if users decides
 - Sample path: C:/Users/username/Downloads/maisquared/"
 - after the program is finished, inside the given path, there should be genre folders like pop and anime, niconico and vocaloid, etc.
 - In the event this program encounters unidentified charts, you can choose the option to paste them in the "Unidentified" Folder, manually choose a genre to paste it in, or Log the chart in "unidentifiedCharts.txt" and ignore.

[4] Restructure into VERSION GROUPING (folder structure is ignored as it moved folders with maidata.txt to version folders)
 - To be implemented

[5] For Beta 2.0: Generate ADX Archives (use option[3] or [4] for this for easy importing to AstroDX)\n\t(Warning: Only use if the charts totals to 2gb or less, bigger sizes is not supported as of Beta 2 Patch 5)
- given path should have GENRE or VERSION folders.
- creates an ADX Archive to be used for AstroDX
- ADX archives bigger than 2gb are current not support as the game is coded for the original zip format, zip64 soon maybe, fumi pls T_T

[6] For Beta 2.0: With the give path, generates the manifest.json files and levels structure to be used for the newer beta 2.0 of AstroDX\n\t(Note: this is your best option to use for now, without zip64 support for astrodx, this is the only way to reorganize the collection)
 - for each GENRE or VERSION(can also be called collection) it records the charts within that collection and uses that to generate collection.manifest files to be used for Beta 2.0 AstroDX
 - Also restructure/unnests the folders, within the given path, you should see a collection folder, and levels folder. The content of each are to be pasted in the respective folders within AstroDX
 - You can choose to add a GUID(random letters and numbers) at the end of each folder names of the charts
 - You can choose to copy or move them.

[7] For Pre Beta: Restructure for pre beta (Note: options [2] and [4] is already structured for pre beta, if current structure is for beta 2.0, use this to revert back to import)
 - Converts Beta 2.0 compatible folder structures into the older pre beta folder structure
 - to be Implemented

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
