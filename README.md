# HandiTalkie 

#### Description

Amazing proyect that combines machine learning, Raspberry Pi, and more!!!. This project is A sign language interpreter that uses machine learning in a Raspberry Pi to capture hand gestures through a camera and convert them into speech.


## Building process
First it is necessary to create the model that the raspberry will use to predict any character from the alphabet. This task can be done on a normal windows computer.

### Dependencies
Before running any script to create the model, the dependencies needed are:

Some basic Git commands are:
```
pip install mediapipe
pip install opencv-python
pip install elevenlabs
pip install scikit-learn
```

`mediapipe` is for hand gesture recognition, `opencv-python` for computer vision tasks, `elevenlabs` for audio control (text-to-chat), and`scikit-learn` for training the hand gesture model. All the nessary scripts are located in the `Classifier_files` folder.

To make the model that predicts the sign languge, first the pictures of the hands need to be collected. The more pictures are analized the better. For this project, 500 pictures of each sing-language letter were taken from the hand. To do this, the run the script `1_collect_imgs.py`. As a suggestion, you can create a virtual environment for this part; just type on a terminal in your main folder:

```
python -m venv name_of_the_enviroment

Example:
python -m venv venv

Access the enviroment:
source venv/Scripts/activate
```

After the images are collected, the information extraction regarding key-points on the hand is the next target. The script `2_create_dataset.py`. That file will output a `data_for_training.pickle` file. 
Once the data has been extracted, the model is created with the script `3_train_classifier.py`. This script will output `model_for_training.p` file, which is the one that is going to be used to predict the words from the alphabet and make words!

#### Testing the model
As an extra, the recently created model can be tested with the file `4_test_model.py`

![Random Forest model Test](/Media_files/image1.png)


## Audio HAT

For this to be a more complete proyect, the main idea was to create a whole embedded system, that is why a PCB customized was design. The schematich used to was primarlay compound of an audio amplifier [LM386](https://www.ti.com/lit/ds/symlink/lm386.pdf) (5V Class A-B audio amplifier). Additionally, some LEDs and push bottons were allocated in the PCB to add extra functionalities, as well as an audio jack 3.5mm femal, and a USB type-C port for power input. The schematic was designed on the free CAD software, from the PCB manufacturer JLCPCB, [EasyEDA](https://easyeda.com/).


![Schematic for the Audio HAT](/Media_files/image2.png)


After routing and placing all the componentes, the final layout ended like this:


![PCB layout](/Media_files/image3.png)


![PCB animation](/Media_files/PCB.gif)


Once the schematic was finished, the design was sent to manufature with [JLCPCB](https://jlcpcb.com/) to have a more professional finish. Once the PCBs arrived, they looked like these:


![PCB manufactured_top](/Media_files/image4.jpg) 

![PCB manufactured_bottom](/Media_files/image5.jpg)


### Special elements

In order to connect the HAT with the raspberry, a [USB to 3.5mm Jack Audio Adapter](https://amzn.eu/d/fj7LUFb) and a [jack 3.5mm male-male](https://amzn.eu/d/7yTrx6h) were used to extract the audio.


## Setting the hardware

For this project, the [module 3 camera](https://www.raspberrypi.com/products/camera-module-3/) was used in the [raspberry pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/)

Once all the extra components, such as headers, were soldered, and the camera was installed, the project looked can look like this:



![HandiTalkie_Completed_1](/Media_files/image6.jpg)


![HandiTalkie_Completed_2](/Media_files/image7.jpg)


![HandiTalkie_Completed_3](/Media_files/image8.jpg)



## Programming the Raspberry

Once all the hardware is ready and the raspberry is powered and ready, the next actions are requiered:

1. In our main folder, we create a virtual environment. This is important because you can get compatibility issues with the camera and other functions. Following the commnads:

```
#Create a virtual environment
python3 -m venv --system-site-packages new_env
```

2. Activate your virtual enviroment

```
#Activate the new environment
source new_env/bin/activate
```

3. Updatethe raspberry

```
#Update pip
pip install --upgrade pip
#Updte the hardware
sudo apt-get update
```

4. Install all the necessary libraries

```
#Install mediapipe
pip install mediapipe

#Install OpenCV
pip install opencv-python

#Install ElevenLabs
pip install elevenlabs

#Install scikit-learn to use the model and open it with pickle
pip install scikit-learn

#Sound libreries
sudo apt-get install libasound2-dev
pip install pyalsaaudio
```

5. Now it is time to set the audio output from the Raspberry. This has to come out from the USB port in case it is connected!

The first thing to do is connect the USB adapter to the raspberry and then check the USB port we connected to. Once we have the port number, we modify the ALSA file (Responsable for the sound settings in the raspberry)

```
#Once the adapter connected, check the port connection number
aplay -l
```

```
#Edit ALSA file:
sudo nano /usr/share/alsa/alsa.conf
```

Then we look for the lines:

```
defaults.ctl.card 0
defaults.pcm.card 0
```

And replace "0" with our USB connection number

Once we changed that, we need to make sure that in case no USB device is connected, the audio can have the default value. To do so, in the same file, we add at the end:

```
pcm.!default {
    type plug
    slave.pcm {
        @func getenv
        vars [ ALSA_DEFAULT_PCM ]
        default {
            type hw
            card Audio
            device 0
        }
    }
}

ctl.!default {
    type plug
    slave.pcm {
        @func getenv
        vars [ ALSA_DEFAULT_CTL ]
        default {
            type hw
            card Audio
        }
    }
}
```

After that, we exit the file `Ctrl+X`, then `Y`, and finaly press `Enter`

Then we proceed to reboot the raspberry:
```
sudo reboot
```



## Start making some "Sign language" 

Now is time to play with the raspberry and our hands!!! Get into the virtual enviroment and run the script!!!


The main script (`sign_language_RB.py`) comes with different resolutions, and voice selection!, Don't forget to specify them in the terminal when executing, otherwise you'll get default values, such as the resolution at 1280x720 and "Janet" as a voice.

```
python sign_language_RB.py --resolution [value_for_resolution] --voice [value_for_voice]
```

### Posible values for voice and resolution
#### Voice

| Input | Voice | 
|-------|-------|
| `0`   | Adam  |
| `1`   | Phoebe|
| `2`   | Sarah |
| `3`   | Asarte|
| `4`   | Janet |


#### Resolution

| Input | Resolution | Type of resolution|
|-------|------------|-------------------|
| `0`   | 4056 x 3040| Highest resolution|
| `1`   | 1920 x 1080| Full-HD resolution|
| `2`   | 1280 x 720 |    HD resolution  |
| `3`   | 640 x 480  |   VGA resolution  |
| `4`   | 320 x 240  | Lowest resolution |


### Buttons function

When the buttons are pressed, here is what happens:

| Button        | Action |
|---------------|------------|
| `B1`          | Plays whatever words made|
| `B2`          | Delete the last character|
| `B3`          | "_" character. It will be replaced by white space in processing |
| `B4`          | Concatenate word  |
| `B3 and B4`   | End the script  | 




