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

For this to be a more complete proyect, the main idea was to create a whole embedded system, that is why a PCB customized was design. The schematich used to was primarlay compound of an audio amplifier [LM386](https://www.ti.com/lit/ds/symlink/lm386.pdf) (Class A-B audio amplifier). Additionally, some LEDs and push bottons were allocated in the PCB to add extra functionalities, as well as an audio jack 3.5mm femal, and a USB type-C port for power input. The schematic was designed on the free CAD software, from the PCB manufacturer JLCPCB, [EasyEDA](https://easyeda.com/).


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


![HandiTalkie_completed_1](/Media_files/image6.jpg)








