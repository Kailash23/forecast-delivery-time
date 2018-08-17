import numpy as np
import random
import googlemaps
from tqdm import tqdm
import pickle

gmaps1 = googlemaps.Client(key='AIzaSyDy3LNlFeCmPoJfGjxG4GhXewyhHHw3Ux8')
gmaps2 = googlemaps.Client(key='AIzaSyC4dICfe5c823PPYcjeCefHV7C6uxsntpQ')

weather_idx_to_label = {0: 'normal', 1: 'mild', 2: 'dangerous'}
weather = [0, 1, 2]
weather_probs = [14, 5, 1]
weather_delay = [0.0, 0.3, 1.0]

transport_mode_idx_to_label = {0: 'truck', 1: 'train', 2: 'flight'}
transport_mode = [0, 1, 2]
transport_mode_probs = [10, 7, 3]
transport_mode_delay = [0.0, 0.3, 0.7]

delay_time = [2, 6, 10, 14, 20, 24, 30, 36, 42, 48]
delay_time_probs = [2, 4, 6, 4, 2, 3, 2, 2, 1, 1]

shipping_centres = ['Mumbai', 'Banglore', 'Hyderabad', 'Chennai', 'Ahmedabad', 'Jaipur', 'Gurgaon', 'Pune', 'Delhi', 'Kolkata', 'Allahabad']
delivery_centres = ['Nagpur', 'Jabalpur', 'Pune', 'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 
                    'Thane', 'Bhopal', 'Visakhapatnam', 'Patna', 'Vadodara', 'Ghaziabad', 
                    'Ludhiana', 'Agra', 'Nashik', 'Faridabad', 'Meerut', 'Rajkot', 'Varanasi', 
                    'Srinagar', 'Aurangabad', 'Dhanbad', 'Amritsar', 'Allahabad', 'Ranchi', 
                    'Haora', 'Coimbatore', 'Jabalpur', 'Gwalior', 'Vijayawada', 'Jodhpur', 
                    'Madurai', 'Raipur', 'Kota', 'Guwahati', 'Chandigarh', 'Solapur', 'Bareilly', 
                    'Mysore', 'Gurgaon', 'Amritsar', 'Jalandhar']

multiset = lambda values, probs: [values[j] for j in range(len(probs)) for i in range(probs[j])]

weather_ditro = multiset(weather, weather_probs)
transport_mode_distro = multiset(transport_mode, transport_mode_probs)
delay_time_distro = multiset(delay_time, delay_time_probs)
random.shuffle(weather_ditro)
random.shuffle(transport_mode_distro)
random.shuffle(delay_time_distro)

def make_city_matrix():
    city_matrix = {}

    for sh_city in shipping_centres:
        for de_city in delivery_centres:
            city_matrix[sh_city] = {}

    i = 0
    for sh_city in shipping_centres:
        print(sh_city)
        for de_city in delivery_centres:
            try:
                if i % 2 == 0:
                    response = gmaps1.distance_matrix(sh_city, de_city)
                else: 
                    response = gmaps2.distance_matrix(sh_city, de_city)
                response = response['rows'][0]['elements'][0]
                dist_kms = response['distance']['value'] / 1000
                time_hrs = response['duration']['value'] / 3600
                city_matrix[sh_city][de_city] = [dist_kms, time_hrs]
                i += 1
            except Exception as e:
                print(e)
                print([sh_city, de_city])
    return city_matrix

def make_dataset(num_examples, city_matrix):
    
    X = []
    y = []
    
    for i in tqdm(range(num_examples), total=num_examples, desc='Examples'):
        try:
            weather_val = random.choice(weather_ditro)
            transport_mode_val = random.choice(transport_mode_distro)
            delay_time_val = random.choice(delay_time_distro)

            shipping_centre = random.choice(shipping_centres)
            delivery_centre = random.choice(delivery_centres)

            dist_kms, time_hrs = city_matrix[shipping_centre][delivery_centre]

            time_hrs += time_hrs * weather_delay[weather_val]
            time_hrs -= time_hrs * transport_mode_delay[transport_mode_val]
            time_hrs += delay_time_val

            X.append([weather_val, transport_mode_val, delay_time_val, dist_kms])
            y.append(time_hrs)
        except Exception as e:
            print(str(e))
            print(shipping_centre)
            print(delivery_centre)
            
    return X, y