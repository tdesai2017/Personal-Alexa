
from voice_functions import VoiceRobot
import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    # r.adjust_for_ambient_noise(source)
    print("Speak your command :")
    audio = r.listen(source)
    text = ''
    try:
        text = r.recognize_google(audio)
        print(text)
    except:
        print("Sorry could not recognize what you said")

    add_in_text = 'add' in text
    delete_in_text = 'delete' in text


# xor evaluation
    if add_in_text != delete_in_text:

        command = ''

        if 'add' in text:
            command = 'add'
            voice_input = text[text.index('')]

        if 'delete' in text:
            command = 'delete'

        voice_input = text[text.index(command) + len(command) + 1: len(text)]        

        voice_robot = VoiceRobot()


        if command == 'add':
            voice_robot.add(voice_input)
    
        elif command == 'delete':
            voice_robot.delete(voice_input)
            
        else:
            print('exited')
             


    else:
        print ('Sorry, this was an invalid input')

