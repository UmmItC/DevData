# DevData

DevData is a Python script that fetches user repository data from the Codeberg API.

## Features

- Fetches repository data of a specified Codeberg user.
- Displays repository details such as name, description, language, stars count, forks count, creation date, and last update date.
- Provides a loading animation while fetching data.

## Usage

1. Clone the repository:

```bash
git clone https://codeberg.org/UmmIt/DevData.git
cd DevData
```

2. Run the script:

```bash
python main.py --user <username>
```

Replace `<username>` with the Codeberg username of the user whose repositories you want to fetch.

### help

you can use the --help option to view the available command-line options:

```shell
❯ python main.py --help
usage: main.py [-h] [--user USER]

Fetch user data from Codeberg API

options:
  -h, --help   show this help message and exit
  --user USER  Codeberg username
```

## Screenshots

![./screenshots/2024-05-23-195556_hyprshot.png]

## License

This project is licensed under the MIT License, see the [LICENSE](./LICENSE.md) file for details.
