import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia as wiki
import webbrowser
import pywhatkit
import os
import sys
import cv2
import numpy as np

# Load the pre-trained face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load a sample image for face authentication (replace 'sample_image.jpg' with the actual image file)
known_image = cv2.imread('ref.jpg', cv2.IMREAD_GRAYSCALE)

# Check if the image is loaded successfully
if known_image is None:
    print("Error: Could not load the sample image.")
    exit()

# Initialize webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capture each frame from the webcam
    ret, frame = video_capture.read()

    # Convert the frame to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    is_match = False

    for (x, y, w, h) in faces:
        # Extract the face region from the frame
        face_region = gray_frame[y:y+h, x:x+w]

        # Resize the face region to match the size of the known image
        face_region_resized = cv2.resize(face_region, (known_image.shape[1], known_image.shape[0]))

        # Simple comparison: Check if pixel-wise absolute difference is below a threshold
        threshold = 50
        diff = cv2.absdiff(face_region_resized, known_image)

        if np.mean(diff) < threshold:
            is_match = True

        # Draw rectangle around the face and display the result
        color = (0, 255, 0) if is_match else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Print match status
    if is_match:
        print("Face matched!")
        success='yes'
        
    else:
        print("Face not matched!")
        success='no'

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
video_capture.release()
cv2.destroyAllWindows()

if success == 'yes':
    engine=pyttsx3.init('sapi5')
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[0].id)

    def say(audio):
        engine.say(audio)
        engine.runAndWait()

    def wishMe():
        hour=int(datetime.datetime.now().hour) #returns value b/w 0-24
        if hour>=0 and hour<12:
            say("Good Morning")
        elif hour>=12 and hour<16:
            say("Good Afternoon")
        else :
            say("Good Evening")

        say("i am zoro, may i know the password please")

    def takecommand():
            listner = sr.Recognizer()
            print("listening...")
            with sr.Microphone() as source:
                listner.adjust_for_ambient_noise(source)
                audio = listner.listen(source,phrase_time_limit=4)
            try:
                print("Recognizing...")
                query = listner.recognize_google(audio, language='en-in')
                print(f"user said: {query}\n")

            except Exception as e: 
                print(e)
                print("say that again please...")
                return "some error occurred"
            return query

    if __name__=="__main__":
        wishMe()
        query=takecommand().lower()
        if(query =='minor project'):
            say("Welcome Back, how may i help you")
        else:
            sys.exit()
        while True:
            query=takecommand().lower()
            if 'send message to' in query:
                d1 = {"mummy": "+91 9911735527", "papa": "+91 9891273597", "rishika": "+91 8546063336"}
                name=query.replace("send message to ","")
                say('whats the message')
                message=takecommand()
                pywhatkit.sendwhatmsg_instantly(str(d1.get(name)),message)
            elif 'play' in query:
                song=query.replace('play','')
                say(f"playing {song}")
                pywhatkit.playonyt(song)
            elif 'what is your name' in query:
                say("I am zoro, nice to meet you")
            elif 'wikipedia' in query:
                word = query
                info=wiki.summary(word,sentences=2)
                say(info)
            elif 'the time' in query:
                current_time=datetime.datetime.now().strftime("%H:%M:%S")
                say(f"the time is {current_time}")
            elif 'open made easy prime' in query:
                say("sure opening Made Easy Prime")
                target = "C:\\Program Files\\MadeEasyPrime\\MadeEasyPrime.exe"
                os.startfile(target)
            elif 'open whatsapp' in query:
                say("sure opening whatsapp")
                webbrowser.open("https://web.whatsapp.com/")
            elif 'open facebook' in query:
                say("sure opening facebook")
                webbrowser.open("https://www.facebook.com/")
            elif 'open youtube' in query:
                say("sure opening youtube")
                webbrowser.open("https://www.youtube.com/")
            elif 'open google' in query:
                say("sure opening google")
                webbrowser.open("https://www.google.com/")
            elif 'open classroom' in query:
                say("sure opening classroom")
                webbrowser.open("https://classroom.google.com/u/1/h")
            elif 'shut down computer' in query:
                say("sure shutting down the computer")
                os.system("shutdown /s /t 1")
            elif 'thank you' in query:
                say("pleasure helping you have a great day ahead")
                sys.exit()
            else:
                say("do you need some more help?")
