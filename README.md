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

# AstroDX Collection Genre Reorganizer

Sorts charts under a path into of the following genre categories:

1. pop and anime
2. niconico and vocaloid
3. touhou project
4. maimai
5. ongeki and chunithm
6. Utage
7. Chinese pop
8. Unknown (in cases where it cannot find a genre to where it matches)

Current status of the program is functional with the only 3 options it has.

is able to categorize all the available charts for AstroDX as of September 5, 2024

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

1. download main.py(this will most like be more updated than release executable) OR use a latest release executable

## Usage

To use the AstroDX Collection Genre Reorganizer, follow these steps:

1. execute main.py in your command line or the executable
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
 - In the event this program encounters unidentified charts, you can choose the option to paste them in the "Unidentified" Folder, manually choose a genre to paste it in, or Log the chart in "unidentifiedCharts.txt" and ignor.

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
