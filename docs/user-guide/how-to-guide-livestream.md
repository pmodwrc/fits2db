# How-to set up a livestream 

This is a step-by-step guide for setting up a livestream of the images from the solar telescope and the CMOS camera. 

It is called a livestream but in reality it shoots and reloads the image approximatly every 10 seconds. This is due to the limited computing capacity of the raspberrypi and the very computationally intensive image processing. 

### Step by step guide
- **Step 1:** First off all you need to make sure that the focus of the camera is set properly and you tested it with different exposure times. To set up the focus you can follow this [How-to-guide](https://pmodwrc.github.io/halpha/how-to-guides/how-to-guide-set-focus/). 

- **Step 2:** After that you can start the `livestream.py` script with the following command:
    ```
    python livestream.py
    ```
!!! Important
    In general it is important to make sure that you are running the python scripts in the virtual environement `venv`. Otherwise there will be several errors with the libraries.

### Code description
The script which makes the livestream is structured into four main parts. Fisrstly you need to take the pictures with the [CameraControl](https://pmodwrc.github.io/halpha/reference/cameracontrol/) module. But before you can use this module you have to inialize the camera and set the `exposure time`,`gain`, `offset` and the number of images for the camera

```python
cam_id = b"QHY5III200M-c8764d41ba464ec75"
path = os.path.join(os.path.dirname(__file__), 'qhyccd.dll')
cam_control = CameraControl(cam_id=cam_id, dll_path=path)

#success = cam_control.cam.so.InitQHYCCDResource()
n = 10
exposure_time = np.linspace(50, 220, n)
gain = 20
offset = 6
```

- **Offset & gain:** Both can be set to integer values (offset ∈ [0 − 255] and gain ∈ [0, 1258]). An offset of 6 was found to be ideal to get the best dynamical range. A gain of 20 was found to be ideal to get the best out of every image

- **Exposure time & number of images:** The exposure time can be set from  15 µs − 900 s. The exposure time is given in µs. Exposure times in the range from 400 - 2500µs where found to be ideal to make solar images. The higher you go with the exposure time, the more overexposed images there are. To get the most visible structures with this images it was found that it isn't neccessary to take more than 10 images. It is best to take between 6 and 10 images.

This images are aligned with the following Python [script](https://github.com/pmodwrc/halpha/blob/main/sun_catching/alignment.py) to make sure that there is no blur in the later image processing steps. With the image processing [script](https://github.com/pmodwrc/halpha/blob/main/sun_catching/image_processing.py) the single images get stacked and colored in Halpha.


Afterwards the image is saved with the function `imwrite` from `cv2` and uploaded to the website of the PMOD/WRC Davos with the [run_smbclient()](https://pmodwrc.github.io/halpha/reference/upload/) function. 

!!!Important
    It is important to save the image in the same directory as the `run_smbclient()`is running. Otherwise the function won't be able to upload the image. 

### Python script
The Python script belonging to this can be found [here](https://github.com/pmodwrc/halpha/blob/main/sun_catching/livestream.py).






