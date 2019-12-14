from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from geopy.geocoders import Nominatim
geolocator = Nominatim()
from geopy.exc import GeocoderTimedOut
URL_INIT = 'https://twitter.com/'

#list_of_users --> From all scraped tweets, get a set of unique usernames and put them in this list. 

list_of_users = ['PresidentFBAN', 'Sikowitz17', 'DotunBorokinni']

#The located userlocations are appended to this list
list_of_found_userlocations = []


#The not located userlocations are appended to this list. 
#Maybe they contain some typo or something else like that. 
list_of_nonfound_userlocations = []

for user in list_of_users:
    try:
        url = parse_url(user)
        response = urlopen(url)
    except:
        continue
    html = response.read()
    soup = BeautifulSoup(html)
    location = False
    a = soup.find('a', {"data-place-id": True})
    if a: # Does the location info exist?
        location = a.string
    if location:
        if ',' in location:
            splitted_location = location.split(',')
        else:
            splitted_location = re.split('|;|-|/|°|#', location)
        try:
            if splitted_location:
                located_location = geolocator.geocode(splitted_location[0], timeout=100)
            else:
                located_location = geolocator.geocode(location, timeout=100)
            if located_location:
                user_plus_location = (user, located_location)
                list_of_found_userlocations.append(user_plus_location)
            else:
                user_plus_incorrect_location = (user, location)
                list_of_nonfound_userlocations.append(user_plus_incorrect_location)
        except GeocoderTimedOut as e:
            print("Error: geocode failed on input %s with message %s"%(location, e))






# def parse_url(tweet_user):
#     url = URL_INIT+ tweet_user.strip('@')
#     return url

# for user in list_of_users:
#     try:
#         url = parse_url(user)
#         response = urllib2.urlopen(url)
#     except:
        # continue
#     html = response.read()
#     soup = BeautifulSoup(html)
#     location = soup.find('span','ProfileHeaderCard-locationText').text.encode('utf8').strip('\n').strip()
#     if location:
#         if ',' in location:
#             splitted_location = location.split(',')
#         else:
#             splitted_location = re.split('|;|-|/|°|#', location)
#         try:
#             if splitted_location:
#                 located_location = geolocator.geocode(splitted_location[0], timeout=100)
#             else:
#                 located_location = geolocator.geocode(location, timeout=100)
#             if located_location:
#                 user_plus_location = (user, located_location)
#                 list_of_found_userlocations.append(user_plus_location)
#             else:
#                 user_plus_incorrect_location = (user, location)
#                 list_of_nonfound_userlocations.append(user_plus_incorrect_location)
#         except GeocoderTimedOut as e:
#             print("Error: geocode failed on input %s with message %s"%(location, e))

print(list_of_nonfound_userlocations)

print(list_of_found_userlocations)