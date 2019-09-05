import requests

#For open weather
import pyowm 

# Returns latitude and longitude of my current location
import geocoder

#Timer
from threading import Timer

#Word to numbers
from word2number import w2n



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
        weather = weather[weather.find('status=') + len('status=') : weather.find(',', weather.find('status'))]


        temperature_info = w.get_temperature('fahrenheit')
        current_temp = str(int(temperature_info['temp']))
        max_temp = str(int(temperature_info['temp_max']))
        min_temp = str(int(temperature_info['temp_min']))
        weather_output = 'The current temperature in ' + current_loc_str + ' is ' + current_temp + " degrees fahrenheit, and today's weather calls for " + weather + ' and temperatures ranging from ' + min_temp + ' to ' + max_temp + ' degrees fahrenheit'
        return weather_output



    #minutes and seconds will come as strings
    def start_timer(self, seconds=0, minutes=0):
        
        try:
            if not (seconds or minutes):
                return 'Invalid'

            if minutes:
                minutes = w2n.word_to_num(minutes)
                
            if seconds:
                seconds = w2n.word_to_num(minutes)

            combined_time = seconds + (minutes * 60)

            self.t = Timer(combined_time, lambda : print('Timer finished'))
            self.t.start()
        except:
            return 'Invalid'

    def cancel_timer(self):
        
        try:
            self.t.cancel()
            print('Timer Ended')
        except:
            return 'There is not timer to cancel'

    

    






    



