
from voice_functions import VoiceRobot
import speech_recognition as sr
from gtts import gTTS 
import os 



r = sr.Recognizer()
text = ''
with sr.Microphone() as source:
    # r.adjust_for_ambient_noise(source)
    print("Speak your command :")
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(text)
    except:
        print("Sorry could not recognize what you said")


# For testing - keep in mind that anything before the last trigger word is ignored
# text = ''

add_in_text = 'add' in text
delete_in_text = 'delete' in text
clear_in_text = 'clear all' in text

# Command add
if add_in_text and not (clear_in_text or delete_in_text):

    command = 'add'
    voice_input = text[text.index(command) + len(command): len(text)].strip() 
    voice_input = voice_input.capitalize()       
    voice_robot = VoiceRobot()
    voice_robot.add(voice_input)
    mytext = 'Added' + voice_input

# Command delete
elif delete_in_text and not (add_in_text or clear_in_text):

    command = 'delete'
    voice_input = text[text.index(command) + len(command): len(text)].strip()
    voice_input = voice_input.capitalize()       
    voice_robot = VoiceRobot()
    voice_robot.delete(voice_input)
    mytext = 'Deleted' + voice_input
            
#Command clear
elif clear_in_text and not (add_in_text or delete_in_text):
    voice_robot = VoiceRobot()
    voice_robot.clear()
    mytext = 'List cleared'

# Invalid input  
else:
    mytext = 'Invalid Input, try again'
    


# Speech response
myobj = gTTS(text=mytext, lang='en', slow=False) 
myobj.save('response.mp3')
os.system("mpg321 response.mp3") 







