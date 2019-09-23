import speech_recognition as sr
from voice_commands import *

from gtts import gTTS 
import os 




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

# while True:

#     r = sr.Recognizer()
#     text = ''
#     with sr.Microphone() as source:
#         r.adjust_for_ambient_noise(source)
#         print("Speak your command :")
#         audio = r.listen(source)
#         try:
#             text = r.recognize_google(audio)
#             print(text)
#         except:
#             print("Sorry could not recognize what you said")


text = 'create alarm for 12:00 a.m.'

found_valid_command = False
count = 0
for command in list_of_commands:
    if command.passes_condition(text):
        command.voice_manipulation(text)
        found_valid_command = True
        break

if not found_valid_command:
    myobj = gTTS(text='Invalid Input, Try again', lang='en', slow=False) 
    myobj.save('response.mp3')
    os.system("mpg321 response.mp3")



                

                


                        
                    
                    


            










            




