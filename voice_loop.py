import speech_recognition as sr
from voice_commands import *

from gtts import gTTS 
import os 


import time 

from snowboy.examples.Python import snowboydecoder






COMMAND_1 = AddItemToBuy()
COMMAND_2 = DeleteItemToBuy()
COMMAND_3 = ClearShoppingList()
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
COMMAND_17 = CancelAlarm()
COMMAND_18 = ClearAlarms()
COMMAND_19 = ClearTimers()
COMMAND_20 = CurrentMarinoCapacity()


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
    COMMAND_16,
    COMMAND_17,
    COMMAND_18,
    COMMAND_19,
    COMMAND_20]



# def start_listening():
#     r = sr.Recognizer()
#     text = ''
#     with sr.Microphone() as source:
#         r.adjust_for_ambient_noise(source)
#         print ('Timers', voice_controlled_timer_dict)
#         print("Waiting for 'Hey Alexa' :")
#         audio = r.listen(source)
#         try:
#             text = r.recognize_google(audio).upper()
#             print(text)
#             if 'ALEXA' in text:
#                 # respond('Hey Whatsup')
#                 return True
#             else:
#                 pass
#         except:
#             pass



def start_listening_snowboy():
    print ('Alarms', voice_controlled_alarm_dict)
    print ('Timers', voice_controlled_timer_dict)
    print('Waiting for "Alexa"')
    detector = snowboydecoder.HotwordDetector("Alexa.pmdl", sensitivity=0.6, audio_gain=1,)
    detector.start(lambda *args: None)
    del detector
    return True


while True:

    if start_listening_snowboy():    
        r = sr.Recognizer()
        text = ''
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Speak your command :")
            #Will wait five seconds before timing out
            try:
                audio = r.listen(source, timeout = 5)
                text = r.recognize_google(audio)
                print(text)
            except:
                pass# print("Sorry could not recognize what you said")


        # found_valid_command = False
        for command in list_of_commands:
            if command.passes_condition(text):
                command.voice_manipulation(text)
                found_valid_command = True
                break

        # if not found_valid_command:
        #     myobj = gTTS(text='Invalid Input, Try again', lang='en', slow=False) 
        #     myobj.save('response.mp3')
        #     os.system("mpg321 response.mp3")



                        

                        


                                
                            
                            


                    


# from snowboy.examples.Python import snowboydecoder


# def detected_callback():
#     return True


# detector = snowboydecoder.HotwordDetector("Alexa.pmdl", sensitivity=0.5, audio_gain=1)
# detector.start(detected_callback)







                




