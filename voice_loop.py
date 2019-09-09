import speech_recognition as sr
from voice_commands import *

# Voice requirments for timer
from gtts import gTTS 
import os 




COMMAND_1 = AddItemToBuy()
COMMAND_2 = DeleteItemToBuy()
COMMAND_3 = ClearBuyingList()
COMMAND_4 = MultiAddToBuyingList()
COMMAND_5 = MultiDeleteFromBuyingList()
COMMAND_6 = ReadShoppingList()
COMMAND_7 = GetMyCurrentWeather()
COMMAND_8 = CancelTimer()
COMMAND_9 = StartTimer()


# In order of preference
list_of_commands = [
    COMMAND_9,
    COMMAND_1,
    COMMAND_2,
    COMMAND_3,
    COMMAND_4,
    COMMAND_5,
    COMMAND_6,
    COMMAND_7,
    COMMAND_8,
    
]



while True:

    r = sr.Recognizer()
    text = ''
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Speak your command :")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(text)
        except:
            print("Sorry could not recognize what you said")


    found_valid_command = False
    for command in list_of_commands:
        if command.passes_condition(text):
            command.voice_manipulation(text)
            found_valid_command = True
            break

    if not found_valid_command:
        myobj = gTTS(text='Invalid Input, Try again', lang='en', slow=False) 
        myobj.save('response.mp3')
        os.system("mpg321 response.mp3")



        

        


                
                
                


        










        




