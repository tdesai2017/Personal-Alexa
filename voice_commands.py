
from abc import ABC,abstractmethod

#Makes post requests to UI
import requests

#For open weather
import pyowm 

# Returns latitude and longitude of my current location
import geocoder

#Timer
from threading import Timer

# Voice requirments for timer
from gtts import gTTS 
import os 

import speech_recognition as sr

#Word to numbers
from word2number import w2n



# Global Variables
voice_controlled_timer = None


class VoiceCommand(ABC):


    @abstractmethod
    def passes_condition(self, text):
        pass

# Responsible for the simple string manipulation aspect of the voice input
    @abstractmethod
    def voice_manipulation(self, text):
        pass


#Responsible for taking action on the command
    # @abstractmethod
    # def action(self):
    #     pass
        


class AddItemToBuy(VoiceCommand):

    #'add' must be the first string in the text
    def passes_condition(self, text):
        return 'add' in text and text.index('add') == 0

    def voice_manipulation(self, text):
        command = 'add'
        voice_input = text[text.index(command) + len(command): len(text)].strip() 
        voice_input = voice_input.capitalize()       
        self.action(voice_input)

        myobj = gTTS(text='Added ' + voice_input, lang='en', slow=False) 
        myobj.save('response.mp3')
        os.system("mpg321 response.mp3")


    def action(self, item):
        payload = {'add': item}
        url = 'http://127.0.0.1:8000/home/receive_add/'
        r = requests.post(url, data= payload)
        print(r.status_code, r.reason)

class DeleteItemToBuy(VoiceCommand):

    #'delete' must be the first string in the text
    def passes_condition(self, text):
        return 'delete' in text and text.index('delete') == 0

    def voice_manipulation(self, text):
        command = 'delete'
        voice_input = text[text.index(command) + len(command): len(text)].strip()
        voice_input = voice_input.capitalize()       
        self.action(voice_input)

        myobj = gTTS(text='Deleted ' + voice_input, lang='en', slow=False) 
        myobj.save('response.mp3')
        os.system("mpg321 response.mp3")

        
    def action(self, item):
        payload = {'delete': item}
        url = 'http://127.0.0.1:8000/home/receive_delete/'
        r = requests.post(url, data = payload)
        print(r.status_code, r.reason)


class ClearBuyingList(VoiceCommand):

    #'clear' must be the first string in the text
    def passes_condition(self, text):
        return 'clear' in text and text.index('clear') == 0

    def voice_manipulation(self, text):
        self.action()

        myobj = gTTS(text='List cleared', lang='en', slow=False) 
        myobj.save('response.mp3')
        os.system("mpg321 response.mp3")

        
    def action(self):
        payload = {}
        url = 'http://127.0.0.1:8000/home/receive_clear/'
        r = requests.post(url, data = payload)
        print(r.status_code, r.reason)


class MultiAddToBuyingList(VoiceCommand):

    #'multi add' must be the first string in the text
    def passes_condition(self, text):
       return 'multi add' in text and text.index('multi add') == 0

    def voice_manipulation(self, text):
        list_of_items = text.split()[2:]
        list_of_items = [item.capitalize() for item in list_of_items]
        self.action(list_of_items)

        myobj = gTTS(text=text.replace('add', 'added'), lang='en', slow=False) 
        myobj.save('response.mp3')
        os.system("mpg321 response.mp3") 

    def action(self, list_of_items):
        add_command = AddItemToBuy()
        for item in list_of_items:
            add_command.action(item)


class MultiDeleteFromBuyingList(VoiceCommand):

    #'multi delete' must be the first string in the text
    def passes_condition(self, text):
       return 'multi delete' in text and text.index('multi delete') == 0

    def voice_manipulation(self, text):
        list_of_items = text.split()[2:]
        list_of_items = [item.capitalize() for item in list_of_items]
        self.action(list_of_items)

        myobj = gTTS(text=text.replace('delete', 'deleted'), lang='en', slow=False) 
        myobj.save('response.mp3')
        os.system("mpg321 response.mp3") 

    def action(self, list_of_items):
        delete_command = DeleteItemToBuy()
        for item in list_of_items:
            delete_command.action(item)

class ReadShoppingList(VoiceCommand):

    #'read shopping list' must be the first string in the text
    def passes_condition(self, text):
        return 'read shopping list' in text and text.index('read shopping list') == 0

    def voice_manipulation(self, text):
        string_of_items = self.action()

        mytext = 'Current list is :' + str(string_of_items)
        myobj = gTTS(text=mytext, lang='en', slow=False) 
        myobj.save('response.mp3')
        os.system("mpg321 response.mp3") 

    def action(self):
        url = 'http://127.0.0.1:8000/home/read_shopping_list/'
        r = requests.get(url)
        items = r.json()
        items_list = []
        for item in items:
            items_list.append(item['name'])

        return items_list


class GetMyCurrentWeather(VoiceCommand):

    def passes_condition(self, text):
        return 'weather' in text
        
    def voice_manipulation(self, text):
        mytext = self.action()
        myobj = gTTS(text=mytext, lang='en', slow=False) 
        myobj.save('response.mp3')
        os.system("mpg321 response.mp3") 

    def action(self):
        current_loc = geocoder.ip('me')
        current_latlong = current_loc.latlng
        current_loc_str = str(current_loc)

        #Ex. Boston, Massachusetts
        current_loc_str = current_loc_str[current_loc_str.rindex('[') + 1: current_loc_str.index(',')]

        #Securely accesses key
        f = open ('/Users/tushardesai/Documents/all_things_code/projects/Voice-Recognition/open_weather_key.txt', 'r')
        key = f.read()
        owm = pyowm.OWM(key)
        observation = owm.weather_at_coords(current_latlong[0],current_latlong[1])

        #w = observation details used by pyowm
        w = observation.get_weather()

        #Ex. Rain, Snow, etc.
        weather =  (str(w))
        weather = weather[weather.find('status=') + len('status=') : weather.find(',', weather.find('status'))].lower()

        status_mappings = {
            'thunderstorm': 'thunderstorms',
            'drizzle': 'drizzles',
            'rain': 'rain',
            'snow': 'snow',
            'mist': 'misty skies',
            'smoke': 'smokey skies',
            'haze': 'haze',
            'fog': 'fog',
            'sand': 'sandy skies',
            'dust': 'dusty skies',
            'ash':  'ashy skies',
            'squall': 'a squall',
            'tornado': 'a tornado',
            'clear': 'clear skies',
            'clouds': 'cloudy skies'
        }

        if weather in status_mappings.keys():
            weather = status_mappings[weather]


        temperature_info = w.get_temperature('fahrenheit')
        current_temp = str(int(temperature_info['temp']))
        max_temp = str(int(temperature_info['temp_max']))
        min_temp = str(int(temperature_info['temp_min']))
        weather_output = 'The current temperature in ' + current_loc_str + ' is ' + current_temp + " degrees fahrenheit, and today's weather calls for " + weather + ' and temperatures ranging from ' + min_temp + ' to ' + max_temp + ' degrees fahrenheit'
        return weather_output


class StartTimer(VoiceCommand):

    def passes_condition(self, text):
        valid_timer = ('timer' in text or "alarm" in text) and ('second' in text or 'minute' in text) and not 'cancel' in text
        if valid_timer and 'second' in text:
            # The timer will only be valid if there is a value for time before the units
            valid_timer = text.index('second') != 0

        if valid_timer and 'minute' in text:
            valid_timer = text.index('minute') != 0

        return valid_timer

    def voice_manipulation(self, text):
        text_list = text.split()
        second_value = 0
        minute_value = 0

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
                

                self.action(second_value, minute_value)

            else:
                myobj = gTTS(text='Invalid Input, Try again', lang='en', slow=False) 
                myobj.save('response.mp3')
                os.system("mpg321 response.mp3") 
            
        except Exception as e:
            print(e)
            myobj = gTTS(text='Invalid Input, Try again', lang='en', slow=False) 
            myobj.save('response.mp3')
            os.system("mpg321 response.mp3") 

    def action(self, seconds=0, minutes=0):
        global voice_controlled_timer
        combined_time = seconds + (minutes * 60)

        second_str = ' seconds '
        minute_str = ' minutes '
        timer_speech = ''

        if seconds == 1:
            second_str = ' second '

        if minutes == 1:
            minute_str = ' minute '


        if seconds >= 1 and minutes >=1:
            timer_speech = 'Timer for ' + str(minutes) + minute_str + ' and ' + str(seconds) + second_str + ' starts now:'

        if seconds == 0 and minutes >= 1:
            timer_speech = 'Timer for ' + str(minutes) + minute_str + ' starts now:'

        if minutes == 0 and seconds >= 1:
            timer_speech = 'Timer for ' + str(seconds) + second_str + ' starts now:'

        myobj = gTTS(text=timer_speech, lang='en', slow=False) 
        myobj.save('response.mp3')
        os.system("mpg321 response.mp3")

        # Starts the timer
        voice_controlled_timer = Timer(combined_time, self.start_timer_helper)
        voice_controlled_timer.start()

    def start_timer_helper(self):
        text = ''

        for num in range (20):
            text += 'alarm'


        myobj = gTTS(text=text, lang='en', slow=False) 
        myobj.save('response.mp3')
        os.system("mpg321 response.mp3")
    
class CancelTimer(VoiceCommand):

    def passes_condition(self, text):
        return 'cancel' in text and ('alarm' in text or 'timer' in text)


    def voice_manipulation(self, text):
        self.action()

    def action(self):
        global voice_controlled_timer
        try:
            voice_controlled_timer.cancel()
            
            myobj = gTTS(text='Timer canceled', lang='en', slow=False) 
            myobj.save('response.mp3')
            os.system("mpg321 response.mp3")

        except Exception as e:
            print(e)
            myobj = gTTS(text='There is no timer to cancel', lang='en', slow=False) 
            myobj.save('response.mp3')
            os.system("mpg321 response.mp3")


