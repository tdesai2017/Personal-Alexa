
from voice_functions import VoiceRobot
import speech_recognition as sr
from gtts import gTTS 
import os 

# Takes all voice inputs and uses the Voice Robot accordingly

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


# For testing - keep in mind that anything before the last trigger word is ignored
# text = 'weather'

add_in_text = 'add' in text and text.index('add') == 0
delete_in_text = 'delete' in text and text.index('delete') == 0
clear_in_text = 'clear' in text and text.index('clear') == 0
multiadd_in_text = 'multi add' in text and text.index('multi add') == 0
multidelete_in_text = 'multi delete' in text and text.index('multi delete') == 0
read_shopping_list_in_text = 'read shopping list' in text and text.index('read shopping list') == 0
get_weather_in_text = 'weather' in text and not (read_shopping_list_in_text or multidelete_in_text or multiadd_in_text or clear_in_text or delete_in_text or add_in_text)
timer_and_seconds_in_text = 'timer' in text and ('second' in text or 'minute' in text) 


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

# Command read_shopping_list
elif read_shopping_list_in_text:
    list_of_items = text.split()[2:]
    voice_robot = VoiceRobot()
    string_of_items = voice_robot.read_shopping_list()
    mytext = 'Current list is:' + str(string_of_items)

####################################

# Command get_my_weather
elif get_weather_in_text:
    voice_robot = VoiceRobot()
    mytext = voice_robot.get_my_weather()

####################################

#Command start_timer - use word to num
elif timer_and_seconds_in_text:
        pass





####################################


# Invalid input  
else:
    mytext = 'Invalid Input, try again'
    


# Speech response
myobj = gTTS(text=mytext, lang='en', slow=False) 
myobj.save('response.mp3')
os.system("mpg321 response.mp3") 







