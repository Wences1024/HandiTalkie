import os
import cv2
import mediapipe as mp


DATA_DIR = './data_for_training'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 1
dataset_size = 500

#Variables para manejo de mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

#hands = mp_hands.Hands(static_image_mode = True, min_detection_confidence=0.3)
expected_landmarks = 21*2

hands = mp_hands.Hands(static_image_mode=True, max_num_hands = 1, min_detection_confidence=0.3)

cap = cv2.VideoCapture(0)


for j in range(number_of_classes):
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

    print('Collecting data for class {}'.format(j))

    done = False
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        cv2.putText(frame, 'Ready? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == ord('q'):
            for i in range(1,100):
                ret, frame = cap.read()
                frame = cv2.flip(frame,1)
                if i < 20:
                    cv2.putText(frame, "1", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,cv2.LINE_AA)
                if i > 20 and i < 40:
                    cv2.putText(frame, "2", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,cv2.LINE_AA)
                if i > 40 and i < 60:
                    cv2.putText(frame, "3", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,cv2.LINE_AA)
                if i > 60 and i < 80:
                    cv2.putText(frame, "4", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,cv2.LINE_AA)
                if i > 80:
                    cv2.putText(frame, "5", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,cv2.LINE_AA)        
                cv2.imshow('frame', frame)
                cv2.waitKey(1)
                #time.sleep(1)
            break

    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        cv2.putText(frame, str(counter), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,cv2.LINE_AA)
        #Analize the data to have the same size:
        data_aux = []
        img_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x)
                    data_aux.append(y)
            print(f"Landmarks value obtained = {len(data_aux)} vs the expected {expected_landmarks}")
            if len(data_aux) == expected_landmarks:
                cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame)
                print(f"Image saved. {counter} out of {dataset_size}")
                counter += 1
        
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
                

cap.release()
cv2.destroyAllWindows()
