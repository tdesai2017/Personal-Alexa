import speech_recognition as sr
from voice_commands import *

from gtts import gTTS 
import os 


import time 





COMMAND_1 = AddItemToBuy()
COMMAND_2 = DeleteItemToBuy()
COMMAND_3 = ClearBuyingList()
# COMMAND_4 = MultiAddToBuyingList()
# COMMAND_5 = MultiDeleteFromBuyingList()
COMMAND_6 = ReadShoppingList()
COMMAND_7 = GetMyCurrentWeather()
COMMAND_8 = CancelTimer()
COMMAND_9 = StartTimer()
# COMMAND_10 = GetDate()
COMMAND_11 = GetTime()
COMMAND_12 = GetDate()
COMMAND_13 = AddReminder()
COMMAND_14 = ClearReminders()
COMMAND_15 = ReadReminders()
COMMAND_16 = CreateAlarm()


# In order of preference ( as soon as one returns true, all others are ignored)
list_of_commands = [
    COMMAND_1,
    COMMAND_2,
    COMMAND_3,
    # COMMAND_4,
    # COMMAND_5,
    COMMAND_6,
    COMMAND_7,
    COMMAND_8,
    COMMAND_9,
    # COMMAND_10,
    COMMAND_11,
    COMMAND_12,
    COMMAND_13,
    COMMAND_14,
    COMMAND_15,
    COMMAND_16]



# def start_listening():
#     r = sr.Recognizer()
#     text = ''
#     with sr.Microphone() as source:
#         r.adjust_for_ambient_noise(source)
#         print("Waiting for 'Hey Alexa' :")
#         audio = r.listen(source)
#         try:
#             text = r.recognize_google(audio).upper()
#             print(text)
#             if 'ALEXA' in text:
#                 respond('Hey Whatsup')
#                 return True
#             else:
#                 pass
#         except:
#             pass


# while True:

#     if start_listening():    
#         r = sr.Recognizer()
#         text = ''
#         with sr.Microphone() as source:
#             r.adjust_for_ambient_noise(source)
#             print("Speak your command :")
#             audio = r.listen(source)
#             try:
#                 text = r.recognize_google(audio)
#                 print(text)
#             except:
#                 print("Sorry could not recognize what you said")


#         # found_valid_command = False
#         count = 0
#         for command in list_of_commands:
#             if command.passes_condition(text):
#                 command.voice_manipulation(text)
#                 found_valid_command = True
#                 break

        # if not found_valid_command:
        #     myobj = gTTS(text='Invalid Input, Try again', lang='en', slow=False) 
        #     myobj.save('response.mp3')
        #     os.system("mpg321 response.mp3")



                        

                        

# this is called from the background thread
def callback(recognizer, audio):
    print("in callback")
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


is_listening = True
r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)

stop_listening(wait_for_stop=False)
respond ('hello there alexa how are you doing today')




stop_listening = r.listen_in_background(m, callback)
print('Speak something')



# `stop_listening` is now a function that, when called, stops background listening

# do some unrelated computations for 5 seconds
# for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things

# calling this function requests that the background listener stop listening
# stop_listening(wait_for_stop=False)

# do some more unrelated things
# while True: time.sleep(0.1)  # we're not listening anymore, even though the background thread might still be running f


while True:
    # if is_listening:
    #     print("is lisetning")
    # else:
    #     print("is not listening")
    time.sleep(1)


                                
                            
                            


                    










                




