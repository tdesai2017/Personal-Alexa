# import speech_recognition as sr

# r = sr.Recognizer()
# with sr.Microphone() as source:
#     print("Speak Anything :")
#     audio = r.listen(source)
#     try:
#         text = r.recognize_google(audio)
#         print("You said : {}".format(text))
#     except:
#         print("Sorry could not recognize what you said")




# while True: 

#     command = input('Please give a command: \n')

#     if command == 'clear':
#         with open('/mnt/c/Users/icett/OneDrive/Documents/all_things_code/projects/voice_recognition/input.txt', 'w') as f:
#             f.write('')

#     elif command == 'append':
#         write_command = input('What do you want to write?:\n')
#         with open('/mnt/c/Users/icett/OneDrive/Documents/all_things_code/projects/voice_recognition/input.txt', 'a') as f:
#             f.write(write_command)
#             f.write("\n")

#     elif command == 'read':
#         with open('/mnt/c/Users/icett/OneDrive/Documents/all_things_code/projects/voice_recognition/input.txt', 'r') as f:
#             f_contents = f.read()
#             print('XXXXXXXX\n' + f_contents + '\nXXXXXXXX')

#     else:
#         print('exited')
#         break

