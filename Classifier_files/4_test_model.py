#Test classifier

import cv2
import mediapipe as mp
import pickle
import numpy as np

#Load the pickle file in the variable
model_dict = pickle.load(open('./model_for_training.p','rb'))

model = model_dict['model']


#Create the object to use the camera with cv2 library
cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


hands= mp_hands.Hands(static_image_mode = True, max_num_hands = 1, min_detection_confidence = 0.3)


#Create a dictionary to associate the hand with a letter
labels_dict = {0:'A',
               1:'B',
               2:'C',
               3:'D',
               4:'E',
               5:'F',
               6:'G',
               7:'H',
               8:'I',
               9:'J',
               10:'K',
               11:'L',
               12:'M',
               13:'N',
               14:'ñ',
               15:'O',
               16:'P',
               17:'Q',
               18:'R',
               19:'S',
               20:'T',
               21:'U',
               22:'V',
               23:'W',
               24:'X',
               25:'Y',
               26:'Z'               
               }

while True:
    #Create auxiliary variables
    data_aux = []
    
    #Take one frame from the webcam
    ret,frame = cap.read()
    #Flip the picture
    frame = cv2.flip(frame,1)
    #Change it to RGB (mp works only with rbg images)
    frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    #Process the images 
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
				frame, #Image to draw
				hand_landmarks, #Model output
				mp_hands.HAND_CONNECTIONS, #Hand connections
				mp_drawing_styles.get_default_hand_landmarks_style(),
				mp_drawing_styles.get_default_hand_connections_style()    
			)
        
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x)
                data_aux.append(y)
        
        #Create a list of the model we trained
        #The number in the list correspond with the value assigned for each letter
        prediction = model.predict([np.asarray(data_aux)])
        
        #Get a corresponding letter from the number given in the list
        predicted_character = labels_dict[int(prediction[0])]
        print(predicted_character)
        cv2.putText(frame, str(predicted_character), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,cv2.LINE_AA)
               
    
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
    
    

cap.release()
cv2.destroyAllWindows()