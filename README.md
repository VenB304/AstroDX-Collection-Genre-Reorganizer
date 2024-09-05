To do list maybe:
1. ~~Complete and maintain mapping json~~
 - Maintain manualCheck.json for updates
2. Collection manager with this json thingies for the game
- a way to revert them into grouping by version or a custom made by the user if ever needed
3. ~~unknown handler~~
- what you wanna do, trash, keep to unknown folder or choose where(only able to copy to unknown folder for now)
4. collection manager
- move copy remove add charts to a collection 
5. maybe learn how this shit works and maybe, just maybe I get better and stop relying on chatgpt

# AstroDX Collection Genre Reorganizer

Sorts charts under a path into genre categories into one of the following:

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

AstroDX Collection Genre Reorganizer is a tool designed to sort and organize charts into specified genre categories. This can help to maintain a well-structured collection of music charts, making it easier to navigate and find specific genres. Chatgpt rawr

## Prerequisuites

- install python at maybe atleast 3.x

## Installation

To install the AstroDX Collection Genre Reorganizer, follow these steps:

1. download main.py or use a latest release to be executable

## Usage

To use the AstroDX Collection Genre Reorganizer, follow these steps:

1. execute main.py in your compiler or the executable
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
 - this will generate collection.json files in the levels folder of a path
 - Sample root path: C:/Users/username/Downloads/maisquared/levels/
 - inside the levels folder or any folder, there should be genre folders like pop and anime, niconico and vocaloid, etc.

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
