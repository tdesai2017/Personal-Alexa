
from voice_functions import VoiceRobot
import speech_recognition as sr
from gtts import gTTS 
import os 

#Word to numbers
from word2number import w2n


voice_robot = VoiceRobot()

while True:
    # Takes all voice inputs, reprocesses it for voice robot, and uses the Voice Robot accordingly

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
    #Can't do this with while loop
    # text = 'one second timer '

    add_in_text = 'add' in text and text.index('add') == 0
    delete_in_text = 'delete' in text and text.index('delete') == 0
    clear_in_text = 'clear' in text and text.index('clear') == 0
    multiadd_in_text = 'multi add' in text and text.index('multi add') == 0
    multidelete_in_text = 'multi delete' in text and text.index('multi delete') == 0
    read_shopping_list_in_text = 'read shopping list' in text and text.index('read shopping list') == 0
    get_weather_in_text = 'weather' in text and not (read_shopping_list_in_text or multidelete_in_text or multiadd_in_text or clear_in_text or delete_in_text or add_in_text)

    cancel_timer_in_text = 'cancel' in text and ('alarm' in text or 'timer' in text)
    
    # Ensures that a given timer is valid (takes into account cancel_timer_in_text)
    valid_timer = ('timer' in text or "alarm" in text) and ('second' in text or 'minute' in text) and not cancel_timer_in_text
    if valid_timer and 'second' in text:
        valid_timer = text.index('second') != 0

    if valid_timer and 'minute' in text:
        valid_timer = text.index('minute') != 0

        

    # Some commands work better if the speech takes place in the conditional as opposed to in the end
    skip_ending_speech = False


    INVALID_INPUT_SPEECH = 'Invalid Input, Try again'


    # Command add
    if add_in_text:

        command = 'add'
        voice_input = text[text.index(command) + len(command): len(text)].strip() 
        voice_input = voice_input.capitalize()       
        voice_robot.add(voice_input)
        mytext = 'Added' + voice_input

    # Command delete
    elif delete_in_text:

        command = 'delete'
        voice_input = text[text.index(command) + len(command): len(text)].strip()
        voice_input = voice_input.capitalize()       
        voice_robot.delete(voice_input)
        mytext = 'Deleted' + voice_input
                
    #Command clear
    elif clear_in_text:
        voice_robot.clear()
        mytext = 'List cleared'

    # Command multiadd - will split words based on spaces
    elif multiadd_in_text:
        # First two will be "multi" and "add", so I must remove those
        list_of_items = text.split()[2:]
        list_of_items = [item.capitalize() for item in list_of_items]
        voice_robot.multiadd(list_of_items)
        mytext = text.replace('add', 'added') 

    # Command multidelete - will split words based on spaces
    elif multidelete_in_text:
        # First two will be "multi" and "delete", so I must remove those
        list_of_items = text.split()[2:]
        list_of_items = [item.capitalize() for item in list_of_items]
        voice_robot.multidelete(list_of_items)
        mytext = text.replace('delete', 'deleted') 

    # Command read_shopping_list
    elif read_shopping_list_in_text:
        list_of_items = text.split()[2:]
        string_of_items = voice_robot.read_shopping_list()
        mytext = 'Current list is:' + str(string_of_items)

    ####################################

    # Command get_my_weather
    elif get_weather_in_text:
        mytext = voice_robot.get_my_weather()

    ####################################

    #Command start_timer - use word to num - only works with whole number inputs "one second timer, one minute timer, etc"
    elif valid_timer:
        text_list = text.split()

        second_value = 0
        minute_value = 0
        second_str = 'seconds'
        minute_str = 'minutes'
        


        try:
            if 'second' in text:
                if 'seconds' in text:
                    second_value_str = text_list[text_list.index('seconds') - 1]
                else:
                    second_value_str = text_list[text_list.index('second') - 1]
                
                second_value = w2n.word_to_num(second_value_str)


            if 'minute' in text:
                if 'minutes' in text:
                    minute_value_str = text_list[text_list.index('minutes') - 1]
                else: 
                    minute_value_str = text_list[text_list.index('minute') - 1]

                minute_value = w2n.word_to_num(minute_value_str)

                
            # Timer cannot contain negative amounts
            if second_value >= 0 and minute_value >= 0 and not (second_value == 0 and minute_value == 0):
                

                voice_robot.start_timer(second_value, minute_value)
                skip_ending_speech = True
            else:
                mytext = INVALID_INPUT_SPEECH
            


        except:
            mytext = INVALID_INPUT_SPEECH


    elif cancel_timer_in_text:
        skip_ending_speech = True
        voice_robot.cancel_timer()
        


    ####################################


    # Invalid input  
    else:
        mytext = INVALID_INPUT_SPEECH
        


    # Speech response

    if not skip_ending_speech:
        myobj = gTTS(text=mytext, lang='en', slow=False) 
        myobj.save('response.mp3')
        os.system("mpg321 response.mp3") 







