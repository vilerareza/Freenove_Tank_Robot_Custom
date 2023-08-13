import speech_recognition as sr
from ctypes import *
 
# Initialize the recognizer
r = sr.Recognizer()
r.energy_threshold = 20

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    # Print nothing
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)


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
             
    except Exception as e:
        print("Could not request results; {0}".format(e))