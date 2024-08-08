
# fits2db installation guide
It is recommended to use a virtual environment when running this tool. Utilizing [`venv`](https://docs.python.org/3/library/venv.html) or [`conda`](https://www.anaconda.com/) ensures a clean and isolated environment, which is a best practice.

## Install from [`PYPI`](https://pypi.org/project/fits2db/)


!!! tip "You can just use pip to install this library "
    ```bash 
    pip install fits2db
    ```
    or for specific version use 
    ```bash 
    pip install fits2db==<your_version> 
    ```


## Install from source
Clone this repo to your local machine. Once cloned navigate to the `root` directory of this project and run in your python environment 
!!! tip "Build install with pip install"
    ```bash 
    pip install .
    ```
With this the `fits2db` lib should be installed. You can test if its properly installed by running the version command to check if you got the right version
```bash title="ssh terminal"
fits2db --version
>>> fits2db, version 0.0.1
```

**Happy coding :sparkles:**



# Copying a Pre-configured Image to an SD Card
For those who prefer a quick setup or are less familiar with Linux and Raspberry Pi configurations, using a pre-configured image is the recommended approach.
Requirements:

- A Raspberry Pi 5
- A microSD card (16GB or larger recommended)
- A microSD card reader
- The pre-configured HAlpha image file. You will find the latest release in the source repo.
- Imaging software (such as [Raspberry Pi Imager](https://www.raspberrypi.com/software/) or balenaEtcher)

### Steps
1. Download the Pre-configured Image: Obtain the latest version of the HAlpha pre-configured image from the [latest release page]().

2. Prepare the microSD Card: Insert the microSD card into your card reader and connect it to your computer.

3. Write the Image to the microSD Card:

    - Open your imaging software (Raspberry Pi Imager, balenaEtcher, or similar).
    - Select the downloaded HAlpha image file as the source.
    - Choose the connected microSD card as the target.
    - Start the writing process. This will overwrite all existing data on the microSD card.
    - Eject the microSD Card: Safely eject the microSD card from your computer once the imaging process is complete.

4. Insert the microSD Card into Your Raspberry Pi 5: Place the microSD card into the Raspberry Pi's card slot.

5. Power Up: Connect the Raspberry Pi to power. The system should boot up from the pre-configured image, and you'll be ready to proceed with the HAlpha setup.
!!! tip
    We used the default username and password you can change once connected!


    | Role  | Username | Password  |
    | ----- | -------- | --------- |
    | Admin | pi       | raspberry |

    to change just use the `passwd` comand

