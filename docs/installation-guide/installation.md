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

