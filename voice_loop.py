
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
# text = 'multi delete oranges'

add_in_text = 'add' in text and text.index('add') == 0
delete_in_text = 'delete' in text and text.index('delete') == 0
clear_in_text = 'clear' in text and text.index('clear') == 0
multiadd_in_text = 'multi add' in text and text.index('multi add') == 0
multidelete_in_text = 'multi delete' in text and text.index('multi delete') == 0


# Command add
if add_in_text:

    command = 'add'
    voice_input = text[text.index(command) + len(command): len(text)].strip() 
    voice_input = voice_input.capitalize()       
    voice_robot = VoiceRobot()
    voice_robot.add(voice_input)
    mytext = 'Added' + voice_input

# Command delete
elif delete_in_text:

    command = 'delete'
    voice_input = text[text.index(command) + len(command): len(text)].strip()
    voice_input = voice_input.capitalize()       
    voice_robot = VoiceRobot()
    voice_robot.delete(voice_input)
    mytext = 'Deleted' + voice_input
            
#Command clear
elif clear_in_text:
    voice_robot = VoiceRobot()
    voice_robot.clear()
    mytext = 'List cleared'

# Command multiadd - will split words based on spaces
elif multiadd_in_text:
    # First two will be "multi" and "add", so I must remove those
    list_of_items = text.split()[2:]
    list_of_items = [item.capitalize() for item in list_of_items]
    voice_robot = VoiceRobot()
    voice_robot.multiadd(list_of_items)
    mytext = text.replace('add', 'added') 

# Command multidelete - will split words based on spaces
elif multidelete_in_text:
    # First two will be "multi" and "delete", so I must remove those
    list_of_items = text.split()[2:]
    list_of_items = [item.capitalize() for item in list_of_items]
    voice_robot = VoiceRobot()
    voice_robot.multidelete(list_of_items)
    mytext = text.replace('delete', 'deleted') 


# Invalid input  
else:
    mytext = 'Invalid Input, try again'
    


# Speech response
myobj = gTTS(text=mytext, lang='en', slow=False) 
myobj.save('response.mp3')
os.system("mpg321 response.mp3") 







