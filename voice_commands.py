
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



import time
import datetime

import math




# Global Variables
voice_controlled_timer = None
voice_controlled_alarm = None


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



#Method to aid with voice responses

def respond(response):
    myobj = gTTS(text=response, lang='en', slow=False) 
    myobj.save('response.mp3')
    os.system("mpg321 response.mp3")

# Method to help with finding products in a string - takes words from end of command to end of string

def find_products(command, text):
    products_to_add = text[text.index(command) + len(command): len(text)]
    if ' and ' in products_to_add: 
        products_to_add = products_to_add.replace(' and ', ' ')
    
    products_to_add = products_to_add.split()
    return products_to_add


        


class AddItemToBuy(VoiceCommand):

    #'add' must be the first string in the text
    def passes_condition(self, text):
        return  'buy ' in text or 'purchase ' in text or ('add ' in text and 'to shopping list' in text)#text.index('add') == 0

    def voice_manipulation(self, text):

        if 'today' in text:
            text = text.replace('today', '')

        if 'buy ' in text:
            command = 'buy'

        if 'purchase ' in text:
            command = 'purchase'

        if 'add ' in text:
            command = 'add'
        if 'to shopping list' in text:
            text = text.replace('to shopping list', '')
        products_to_add = find_products(command, text)

        self.action(products_to_add)

        respond('Added ' + str(products_to_add) +' to shopping list')


    def action(self, products):

        for product in products: 

            payload = {'add': product}
            url = 'http://127.0.0.1:8000/myapp/receive_shopping_list_add/'
            r = requests.post(url, data= payload)
            print(r.status_code, r.reason)

class DeleteItemToBuy(VoiceCommand):

    #'delete' must be the first string in the text
    def passes_condition(self, text):
        return 'delete ' in text and 'from shopping list' in text or 'remove ' in text  #and text.index('delete') == 0

    def voice_manipulation(self, text):
        if 'delete ' in text:
            command = 'delete'

        if 'remove ' in text:
            command = 'remove'

        text = text.replace('from shopping list', '')
        products_to_delete = find_products(command, text)

        self.action(products_to_delete)

        respond('Deleted ' + str(products_to_delete))

        
    def action(self, products):
        
        for product in products:   

            payload = {'delete': product}
            url = 'http://127.0.0.1:8000/myapp/receive_shopping_list_delete/'
            r = requests.post(url, data = payload)
            print(r.status_code, r.reason)


class ClearBuyingList(VoiceCommand):

    #'clear' must be the first string in the text
    def passes_condition(self, text):
        return 'clear' in text and text.index('clear') == 0 and 'shopping list' in text

    def voice_manipulation(self, text):
        self.action()

        respond('Shopping List cleared')

        
    def action(self):
        payload = {}
        url = 'http://127.0.0.1:8000/myapp/receive_shopping_list_clear/'
        r = requests.post(url, data = payload)
        print(r.status_code, r.reason)


class ReadShoppingList(VoiceCommand):

    #'read shopping list' must be the first string in the text
    def passes_condition(self, text):
        return 'read shopping list' in text and text.index('read shopping list') == 0

    def voice_manipulation(self, text):
        string_of_items = self.action()

        mytext = 'Current shopping list is :' + str(string_of_items)
        respond(mytext)

    def action(self):
        url = 'http://127.0.0.1:8000/myapp/read_shopping_list/'
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
        respond(mytext)

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
        valid_timer = "alarm" in text and ('second' in text or 'minute' in text) and not 'cancel' in text
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
                respond('Invalid Input, Try again')
            
        except Exception as e:
            print(e)
            respond('Invalid Input, Try again')

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

        respond(timer_speech)

        # Starts the timer
        voice_controlled_timer = Timer(combined_time, self.start_timer_helper)
        voice_controlled_timer.start()

    def start_timer_helper(self):
        respond('timer timer timer timer timer timer timer timer timer timer timer')
    
class CancelTimer(VoiceCommand):

    def passes_condition(self, text):
        return 'cancel' in text and ('timer' in text)


    def voice_manipulation(self, text):
        self.action()

    def action(self):
        global voice_controlled_timer
        try:
            voice_controlled_timer.cancel()

            respond('Timer Canceled')

        except Exception as e:
            print(e)
            
            respond('There is no timer to cancel')


class GetTime(VoiceCommand):

    def passes_condition(self, text):
        return ' time'  in text 


    def voice_manipulation(self, text):
        self.action()

    def action(self):
        current_hour = time.strftime("%H")
        am_or_pm = ''
        if int(current_hour) > 12:
            am_or_pm = 'pm'

        else:
            am_or_pm = 'am'

        current_time = time.strftime("%I %M " + am_or_pm)

        respond('The current time is ' + current_time)

        

class GetDate(VoiceCommand):

    def passes_condition(self, text):
        return ' day' in text or ' date' in text


    def voice_manipulation(self, text):
        self.action()

    def action(self):
        currentDT = datetime.datetime.now()

        #From https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])
        ordinal_day = str(ordinal(int(currentDT.strftime("%d"))))

        day = currentDT.strftime("Today is %A, %B " + ordinal_day + ", %Y")
        respond(day)

        
class AddReminder(VoiceCommand):

    #'add' must be the first string in the text
    def passes_condition(self, text):
        return 'remind ' in text and 'to ' in text and not ('add ' in text or 'buy ' in text or 'purchase ' in text) or ('add ' in text and 'to reminders')#text.index('add') == 0


    def voice_manipulation(self, text):

        if 'remind ' in text:
            command = 'to '


        if 'to reminders' in text:
            text = text.replace('to reminders', '')
            command = 'add'

        if 'today' in text:
            text = text.replace('today', '')

        reminder_to_add = text[text.index(command) + len(command): len(text)]
        print (reminder_to_add)


        self.action(reminder_to_add)

        respond('Added ' + str(reminder_to_add) + ' to reminders')


    def action(self, reminder):

        payload = {'add': reminder}
        url = 'http://127.0.0.1:8000/myapp/receive_reminders_add/'
        r = requests.post(url, data= payload)
        print(r.status_code, r.reason)


class ClearReminders(VoiceCommand):

    #'clear' must be the first string in the text
    def passes_condition(self, text):
        return 'clear' in text and text.index('clear') == 0 and 'reminders' in text

    def voice_manipulation(self, text):
        self.action()

        respond('Reminders cleared')

        
    def action(self):
        payload = {}
        url = 'http://127.0.0.1:8000/myapp/receive_reminders_clear/'
        r = requests.post(url, data = payload)
        print(r.status_code, r.reason)


class ReadReminders(VoiceCommand):

    #'read reminders' must be the first string in the text
    def passes_condition(self, text):
        return 'read reminders' in text and text.index('read reminders') == 0

    def voice_manipulation(self, text):
        string_of_items = self.action()

        mytext = 'Current reminders are :' + str(string_of_items)
        respond(mytext)

    def action(self):
        url = 'http://127.0.0.1:8000/myapp/read_reminders/'
        r = requests.get(url)
        items = r.json()
        items_list = []
        for item in items:
            items_list.append(item['text'] ) 

        return items_list


class CreateAlarm(VoiceCommand):
    def passes_condition(self, text):
        is_valid = 'alarm' in text and ('a.m.' in text or 'p.m.' in text)
        print('I am here in creating alarms')

        if is_valid:
            if 'a.m.' in text:
                is_valid = text.find('a.m.') != 0
            if 'p.m.' in text:
                is_valid = text.find('p.m.') != 0

        return is_valid


    
    def voice_manipulation(self, text):

        print ('I am kinda deep')

        command = ''
        #Hours are requred, but I want to give minutes a default value
        minute = 0


        if 'a.m.' in text:
            command = 'a.m.'

        if 'p.m.' in text:
            command = 'p.m.'

        split_text = text.split()
        if ':' not in text:
            hour = int(split_text[split_text.index(command) - 1])
            print(hour, command)

        if ':' in text:
            split_text = text.split()
            time = split_text[split_text.index(command) - 1]
            hour = int(time[0:time.find(':')])
            minute = int(time[time.find(':') + 1: len(time)])


        try:
            if hour >= 1 and hour <= 12:
                if command == 'p.m.' and hour != 12:
                    hour += 12

                if command == 'a.m.' and hour == 12:
                    hour = 0
                    
                self.action(command, alarm_hours = hour, alarm_minutes = minute)
            else:
                respond('Ivalid Input, Try Again')

        except Exception as e:
            print(e)
            respond('Invalid Input, Try Again')
        
       
    def action(self, am_or_pm, alarm_hours = 0, alarm_minutes = 0):
        global voice_controlled_alarm

        print('I am deep now')


        current_time = datetime.datetime.now() 
        alarm_time = datetime.datetime.now()
        alarm_time = alarm_time.replace(second = 0, microsecond = 0)

        print('TIMES:')
        print(int(current_time.hour))
        print(alarm_hours)

        # If alarm_hours have already passed current hours, add a day
        if current_time.hour != alarm_hours and current_time.hour > alarm_hours:
            alarm_time = alarm_time + datetime.timedelta(days=1)

        # If alarm_mintues have already passed current minutes, add a day
        if current_time.hour == alarm_hours:
            if current_time.minute >= alarm_minutes:
                alarm_time = alarm_time + datetime.timedelta(days=1)


        alarm_time = alarm_time.replace(hour = alarm_hours, minute = alarm_minutes)

        seconds_difference = (alarm_time-current_time).total_seconds()

        print(alarm_time)
        print(current_time)
        print(seconds_difference)

        #  I don't want minutes mentioned when minutes == 0
        alarm_minutes_str = int(alarm_minutes)
        if alarm_minutes == 0:
            alarm_minutes_str = ''
        else:
            alarm_minutes_str = str(alarm_minutes)


        #Different ways of responding to am or pm inputs

        if am_or_pm == 'a.m.' and alarm_hours != 0:
            am_or_pm = am_or_pm.replace('.', "  ")
            respond('Alarm for' + str(alarm_hours) + ' ' + alarm_minutes_str + ' ' + am_or_pm  + ' starts now')

        if (am_or_pm == 'a.m.' and alarm_hours == 0) or (am_or_pm == 'p.m.' and alarm_hours == 12):
            am_or_pm = am_or_pm.replace('.', "  ")
            respond('Alarm for 12' + ' ' + alarm_minutes_str + ' ' + am_or_pm  + ' starts now')

        if am_or_pm == 'p.m.' and alarm_hours != 12:
            am_or_pm = am_or_pm.replace('.', "  ")
            respond('Alarm for' + str(alarm_hours-12) + ' ' + alarm_minutes_str + ' ' + am_or_pm  + ' starts now')



        print('Alarm for' + str(alarm_hours) + ' ' + str(alarm_minutes) + ' ' + am_or_pm  + ' starts now')
        voice_controlled_alarm = Timer(seconds_difference, self.start_alarm_helper)
        voice_controlled_alarm.start()
        print(voice_controlled_alarm)

    def start_alarm_helper(self):
        respond('alarm alarm alarm alarm alarm alarm alarm alarm alarm alarm alarm alarm alarm alarm alarm ')










        

            


        

            

        

            










