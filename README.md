# gpac_autocompletion
This repository contains a Python-based autocompletion script for `gpac` commands. The project is structured to include the main autocompletion logic and unit tests to ensure the functionality.

For more information about `gpac`, visit the [gpac repository](https://github.com/gpac/gpac).

## Project Structure

### Directories and Files

- **autocomplete/**: Contains the main autocompletion scripts.
  - `gpac_autocomplete.py`: The primary script for `gpac` autocompletion.
- **unittests/**: Contains unit tests for the autocompletion scripts.
- **bash_gpac_autocomplete.sh**: Shell script to enable `gpac` autocompletion.
- **README.md**: This file, providing an overview of the project.

## Installation

1. Clone the repository:
```sh
git clone https://github.com/touatily/gpac_autocompletion.git
cd gpac_autocompletion
```

2. Install:
To install the script for the current user, run:
```sh
./install.sh
```

Alternatively, to install it system-wide for all users, use:
```sh
sudo ./install.sh
```

## Running Tests
To run the unit tests, use the following command:

```sh
./run_unittests.sh
```

## Contributing
- Fork the repository.
- Create a new branch (`git checkout -b feature-branch`).
- Make your changes.
- Run the unit tests (`./run_unittests.sh`) to ensure everything works.
- Commit your changes (`git commit -am 'Add new feature'`).
- Push to the branch (`git push origin feature-branch`).
- Create a new Pull Request.