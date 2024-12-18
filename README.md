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
<img src="/Media_files/image1.png" width="48">



