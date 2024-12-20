#Importar librerias
import cv2
import mediapipe as mp
import numpy as np
import pickle
import sys
import warnings
import argparse
from picamera2 import Picamera2
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings, play
from gpiozero import Button
from time import sleep
from multiprocessing import Process, Manager


#Getting rid of warning
warnings.filterwarnings("ignore", category=UserWarning, module='google.protobuf')

#Camera resolutions
RESOLUTIONS = {
    0:(4056,3040),#Highest definition
    1:(1920,1080), #Full HD
    2:(1280,720), #HD
    3:(640,480), # VGA resolution
    4:(320,240) # really low resolution
    }

#Words configurations
word_configuration = {
#Index: [size, position (x,y), tickness, second word position (x,y)] 
    0:[8, (10,200), 20,(10,400)],
    1:[3, (10,70), 10,(10,160)],
    2:[2,(10,50),5,(10,110)],
    3:[1.5,(10,35),3,(10,80)],
    4:[1,(10,35),3,(10,70)]
    }


#Voices options
VOICES = {
    0:"pNInz6obpgDQGcFmaJgB",# Adam ID
    1:"rzfmYX98xnepumq7VkeQ",# Phoebe ID
    2:"EXAVITQu4vr4xnSDxMaL",# Sarah ID
    3:"vOmFQ6x26mxAgHTbjk8r",# Asarte ID
    4:"v2UHGPYqDd312FnKtFOE",# Janet ID
}

#Create a dictionary to associate the hand with a letter
LABELS_DICT = {
        0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H',
        8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'Ñ', 15: 'O',
        16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V', 23: 'W',
        24: 'X', 25: 'Y', 26: 'Z'              
               }

#Define button pins
BUTTONS_GPIO = {
    'B1': 17,
    'B2': 27,
    'B3': 22,
    'B4': 5
    }


#Resolution help

resolution_help = """\n
Options:
0 -> 4056 x 3040 -> Highest resolution
1 -> 1920 x 1080 -> Full-HD resolution
2 -> 1280 x 720 -> HD resolution
3 -> 640 x 480 -> VGA resolution
4 -> 320 x 240 -> Lowest resolution\n
"""

voice_help = """\n
Options:
0 -> Adam
1 -> Phoebe
2 -> Sarah
3 -> Asarte
4 -> Janet\n
"""

#Initialize buttons
buttons = {name:Button(pin, pull_up=False, bounce_time=0.1)for name,pin, in BUTTONS_GPIO.items()}



#Importar llave de API para voz
client = ElevenLabs(
  api_key= "Your key" 
)

#Load the pickle file in the variable
model_dict = pickle.load(open('./model_for_training.p','rb'))
model = model_dict['model']



#Create the object with the camera
picam2 = Picamera2()


def configure_camera(resolution_key):
    #Configure the camera with an specific resolution
    picam2.configure(picam2.create_video_configuration(queue=False,main={"format": 'XRGB8888', "size": RESOLUTIONS[resolution_key]}))
    picam2.start()


def voice_out(voice_key, words,end_audio,play_audio):
    final_text = ''
    play_audio.value = False
    end_audio.value = False
    try:
        while True:
            final_text = words.value.replace("_",", ").strip().capitalize()
            if play_audio.value:
                sleep(0.1)
                text_to_chat = client.generate(
                        text = "a                "+final_text,
                        voice=Voice(
                    voice_id=VOICES[voice_key],
                    settings=VoiceSettings(
                        stability=0.5,
                        similarity_boost=0.5,
                        speaking_rate=0.25))                        
                        )
                print(f"message: {final_text}")
                play(text_to_chat)
                play_audio.value = False
            if end_audio.value:
                break
    except KeyboardInterrupt:
        print("\nVoice function deactivated")


#Main function
def main(resolution_key,voice_key):
    #Variable to store the predicted character on the hand
    predicted_character = ""
    
    #Configure the camera
    configure_camera(resolution_key)
    
    #Create the objects of the mediapipe
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    hands = mp_hands.Hands(static_image_mode = False, max_num_hands = 1, min_detection_confidence = 0.5,min_tracking_confidence=0.5)
    
    #Object to create parallel variables
    manager = Manager()
    #Parallel variable to store the words
    words = manager.Value(str,"")
    #Parallel variable to stop the audio
    end_audio = manager.Value(bool,False)
    #Parallel variable to play the audio
    play_audio = manager.Value(bool,False)
    #Create the object of the multiprocessing to perform
    voice_process = Process(target=voice_out, args=(voice_key,words,end_audio,play_audio))
    #Start the multiprocessing function
    voice_process.start()
    
        
    try:
        while True:
            #Create auxiliary variables
            data_aux = []
            #Take one frame from the webcam
            im = picam2.capture_array()
            #Change the frame from BGR to RGB
            im_rgb = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
            #Flip the picture
            im_rgb = cv2.flip(im_rgb,1)
            #Process the images
            results = hands.process(im_rgb)
            #print the text-to-speach in the frame
            cv2.putText(im_rgb,#Image where the word is going to be placed
                        str(words.value), #String to write on the image
                        word_configuration[resolution_key][3], #Position of the word
                        cv2.FONT_HERSHEY_SIMPLEX, #Font type
                        word_configuration[resolution_key][0], #Size of the font
                        (0,255,0), #Color in BGR
                        word_configuration[resolution_key][2], #Tickness of the font
                        cv2.LINE_AA) #Type of line. AA = antialiased line
           
            #If a hand is detected
            if results.multi_hand_landmarks:        
                #Process to extract the coordenates of each point in the hand
                for hand_landmarks in results.multi_hand_landmarks:
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x)
                        data_aux.append(y)
               
                #Create a list of the model used
                #The number in the list correspond to the value assigned for each letter
                prediction = model.predict([np.asarray(data_aux)])
               
                #Get a corresponding letter from the number given in the list
                predicted_character = LABELS_DICT[int(prediction[0])]
                #Write the letter in the video captured
                cv2.putText(im_rgb, #Image where the word is going to be placed
                            str(predicted_character), #String to write on the image
                            word_configuration[resolution_key][1], #Position of the word
                            cv2.FONT_HERSHEY_SIMPLEX, #Font type
                            word_configuration[resolution_key][0], #Size of the font
                            (0,255,0), #Color in BGR
                            word_configuration[resolution_key][2], #Tickness of the font
                            cv2.LINE_AA) #Type of line. AA = antialiased line
               
            #Display the image
            #First change the frame to BGR
            im_bgr = cv2.cvtColor(im_rgb,cv2.COLOR_RGB2BGR)
            
            # Name of the window to display de image
            cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
            #Make the windows the full size
            cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            
            #Display the image
            cv2.imshow("Frame", im_bgr)
            #Wait 1ms
            cv2.waitKey(1)
            if not buttons['B3'].is_pressed and not buttons['B4'].is_pressed:
                sleep(0.2)
                break
            
            if not buttons['B4'].is_pressed:
                words.value += predicted_character
                sleep(0.2)
         
            if not buttons['B3'].is_pressed:
                words.value += '_'
                sleep(0.2)
         
            if not buttons['B2'].is_pressed:
                words.value= words.value[:-1]
                sleep(0.2)
                
            if not buttons['B1'].is_pressed:
                play_audio.value= True
                sleep(0.2)
            
            

    except (ValueError, KeyboardInterrupt):
        print("\nA ValueError or KeyboardInterrupt has occured\n")
        pass
    
    finally:
        #Stop the audio function
        end_audio.value = True
        #Stop the multiprocessing function
        voice_process.join()
        #Stop the camera
        picam2.stop()
        #Destroy all the windows
        cv2.destroyAllWindows()
        #Print a message
        print("\nThank you for using this system :)")
        #Play goodbay message
        text_to_chat = client.generate(
                    text = "a Thank you for using this system",
                    voice = VOICES[4]
                    )
        play(text_to_chat)
        sys.exit()
        

#Run the program only if you are in the main script
if __name__ == "__main__":
    #Create the opject
    parser = argparse.ArgumentParser(
        description = "HandiTalkie. Hand Gesture Recognition with Raspberry Pi Camera",
        formatter_class=argparse.RawTextHelpFormatter
        )
    #Create the resolution argument
    parser.add_argument('--resolution', type=int,choices=range(len(RESOLUTIONS)),default=2,help="Set the resolution of the camera" + resolution_help)
    #Create the voice selection argument
    parser.add_argument('--voice',type=int,choices=range(len(VOICES)),default=4,help="Set the voice for the text-to-speech"+voice_help)
    #Pase those arguments to the variable args
    args = parser.parse_args()
    #Send the options to the main() function
    main(args.resolution,args.voice)