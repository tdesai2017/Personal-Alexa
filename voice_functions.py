import requests

# URL = "http://127.0.0.1:8000/home/receive_delete/"

class VoiceRobot:

    def __init__(self):
        pass

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















