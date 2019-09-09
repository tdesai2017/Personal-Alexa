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



# All features of robot

class VoiceRobot:

    def __init__(self):
        pass

# Shopping list voice commands
    # Add a single item
    def add (self, item):
        payload = {'add': item}
        url = 'http://127.0.0.1:8000/home/receive_add/'
        r = requests.post(url, data= payload)
        print(r.status_code, r.reason)
        # print(r.text[:300] + '...')

    # Delete a single itme
    def delete (self, item):
        payload = {'delete': item}
        url = 'http://127.0.0.1:8000/home/receive_delete/'
        r = requests.post(url, data = payload)
        print(r.status_code, r.reason)
        # print(r.text[:300] + '...')

    #Clear all items
    def clear (self):
        payload = {}
        url = 'http://127.0.0.1:8000/home/receive_clear/'
        r = requests.post(url, data = payload)
        print(r.status_code, r.reason)
        # print(r.text[:300] + '...')

    #Add multiple items (is sending many post requests the most efficient means though)
    def multiadd(self, list_of_items):
        for item in list_of_items:
            print(item)
            self.add(item)

    #Deletes multiple items (is sending many post requests the most efficient means though)
    def multidelete(self, list_of_items):
        for item in list_of_items:
            print(item)
            self.delete(item)


    def read_shopping_list(self):
        url = 'http://127.0.0.1:8000/home/read_shopping_list/'
        r = requests.get(url)
        items = r.json()
        items_list = []
        for item in items:
            items_list.append(item['name'])

        return items_list



#Weather information - open - only 60 requests allowed per minute

    def get_my_weather(self):
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


    def start_timer_helper(self):
        text = ''

        for num in range (20):
            text += 'alarm'


        myobj = gTTS(text=text, lang='en', slow=False) 
        myobj.save('response.mp3')
        os.system("mpg321 response.mp3")

    #minutes and seconds will come as strings
    def start_timer(self, seconds=0, minutes=0):
        
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

        self.t = Timer(combined_time, self.start_timer_helper)
        self.t.start()


    def cancel_timer(self):

        try:
            self.t.cancel()
            
            myobj = gTTS(text='Timer canceled', lang='en', slow=False) 
            myobj.save('response.mp3')
            os.system("mpg321 response.mp3")

        except Exception as e:
            print(e)
            myobj = gTTS(text='There is no timer to cancel', lang='en', slow=False) 
            myobj.save('response.mp3')
            os.system("mpg321 response.mp3")


    


    


    

    






    



