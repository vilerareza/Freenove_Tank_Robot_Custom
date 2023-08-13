import speech_recognition as sr
 
# Initialize the recognizer
r = sr.Recognizer()

while True:   

    try:
         
        # use the microphone as source for input.
        with sr.Microphone() as source_:
             
            r.adjust_for_ambient_noise(source_, duration=0.2)
             
            #listens for the user's input
            audio2 = r.listen(source_)
             
            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
 
            print("Did you say ",MyText)

             
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
         
    except sr.UnknownValueError:
        print("unknown error occurred")