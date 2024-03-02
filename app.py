from flask import Flask, render_template,request
from geopy.distance import geodesic
import pandas as pd
import geocoder


app = Flask(__name__)


def find_nearest_hospital(my_lat, my_lon, hospital_data):
    nearest_hospital = None
    min_distance = float('inf')

    for index, hospital in hospital_data.iterrows():
        hospital_lat = hospital['latitude']
        hospital_lon = hospital['longitude']
        distance = geodesic((my_lat, my_lon), (hospital_lat, hospital_lon)).kilometers

        if distance < min_distance:
            min_distance = distance
            nearest_hospital = hospital

    return nearest_hospital

def get_current_location():
    location = geocoder.ip('me')
    latitude = location.latlng[0]
    longitude = location.latlng[1]
    return latitude, longitude

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        current_latitude, current_longitude = get_current_location()
        hospital_data = pd.read_excel('Hospital_Name.xlsx')
        nearest_hospital = find_nearest_hospital(current_latitude, current_longitude, hospital_data)
        return f"The nearest hospital is {nearest_hospital['Name']} located at latitude {nearest_hospital['latitude']} and longitude {nearest_hospital['longitude']}"
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
