# HandiTalkie 

#### Description

HandiTalkie is an innovative project that combines machine learning, Raspberry Pi, and embedded systems to create a sign language interpreter. Using a camera, the system captures hand gestures, predicts corresponding alphabet letters, and converts them into speech.


## Building process
To get started, you first need to create the machine learning model that will be used by the Raspberry Pi to predict hand gestures. This process is done on a computer (e.g., Windows).

### Dependencies
Install the following Python libraries before running any scripts:


```
pip install mediapipe opencv-python elevenlabs scikit-learn
```
- `mediapipe` : Hand gesture recognition.
- `opencv-python`: Computer vision tasks.
- `elevenlabs`: Text-to-speech conversion.
- `scikit-learn`: Model training.

The necessary scripts are in the `Classifier_files` folder.



### Steps to Create the Model
1. Collect Hand Gesture Images
Run `1_collect_imgs.py` script to capture images of hand gestures. It is recommended to collect at least 500 images per sign language letter for better accuracy.

*Optional:* Use a virtual environment to isolate dependencies:

```
python -m venv name_of_the_enviroment

#Example:
python -m venv venv

#Access the enviroment:
source venv/Scripts/activate
```

2. Extract Key Points

Use the `2_create_dataset.py` script to extract hand key points and generate the `data_for_training.pickle` file.

3. Train the Model

Train the model by running the `3_train_classifier.py` script. This outputs the `model_for_training.p` file, which is used for predictions.

4. Test the Model (Optional)

Test the trained model using `4_test_model.py`.

Example output:

![Random Forest model Test](/Media_files/image1.png)


## Audio HAT
To enhance the project, a custom multi-layer PCB was designed to create an embedded system. The PCB includes:

- Class A-B Audio amplifier ([LM386](https://www.ti.com/lit/ds/symlink/lm386.pdf)).

- LEDs and push buttons for additional functionalities.

- A 3.5mm audio jack and USB-C port for power input.

- Dedicated layers for power and signals


The schematic was created using [EasyEDA](https://easyeda.com/).


#### Schematic

![Schematic for the Audio HAT](/Media_files/image2.png)


#### PCB Layout


![PCB layout](/Media_files/image3.png)


![PCB animation](/Media_files/PCB.gif)



Once manufactured with [JLCPCB](https://jlcpcb.com/), the PCBs looked like this:

![PCB manufactured_top](/Media_files/image4.jpg) 

![PCB manufactured_bottom](/Media_files/image5.jpg)


### Required Accessories

- [USB to 3.5mm Audio Adapter](https://amzn.eu/d/fj7LUFb)
- [3.5mm Male-to-Male Audio Cable](https://amzn.eu/d/7yTrx6h)


## Setting Up the Hardware

This project uses:

- [Camera Module 3](https://www.raspberrypi.com/products/camera-module-3/)
- [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/)


After soldering the components and connecting the camera, the project looks like this



![HandiTalkie_Completed_1](/Media_files/image6.jpg)


![HandiTalkie_Completed_2](/Media_files/image7.jpg)


![HandiTalkie_Completed_3](/Media_files/image8.jpg)



## Programming the Raspberry
### Steps to prepare the Raspberry Pi


1. Create and Activate a Virtual Environment

```
#Create a virtual environment
python3 -m venv --system-site-packages new_env

#Activate the new environment
source new_env/bin/activate
```

2. Update and Install Dependencies

```
sudo apt-get update
pip install --upgrade pip
pip install mediapipe opencv-python elevenlabs scikit-learn
sudo apt-get install libasound2-dev
pip install pyalsaaudio
```

3. Configure Audio Output
- Connect the USB adapter to the Raspberry Pi.
- Identify the USB port:

```
aplay -l
```
- Edit the ALSA configuration file:
```
sudo nano /usr/share/alsa/alsa.conf
```

Look for the lines:

```
defaults.ctl.card 0
defaults.pcm.card 0
```

And replace "0" with your USB port number

- Add at the end of the file:

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
In case no adapter is connected!


- Save and Reboot:

After that, we exit the file `Ctrl+X`, then `Y`, and finaly press `Enter`

Then we proceed to reboot the raspberry:
```
sudo reboot
```

## Running the Program 
Run the main script `sign_language_RB.py`. You can specify resolution and voice settings using command-line arguments.

```
python sign_language_RB.py --resolution [value] --voice [value]
```

### Available Options

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


## Demo
<video width="50%" controls>
  <source src="https://drive.google.com/file/d/1ZsCAE8BdoFo-KcmjtEL_0qf92XkF0BYN/view?usp=sharing" type="video/mp4">
</video>


### Important things to remember:
- Create an account for [elevenlabs](https://elevenlabs.io/)