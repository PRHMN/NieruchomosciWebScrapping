from geopy.geocoders import Nominatim
from math import sin, cos, sqrt, atan2, radians

geolocator = Nominatim(user_agent="specify_your_app_name_here")
location1 = geolocator.geocode("Brwinów, mazowieckie")
location2 = geolocator.geocode("Dworcowa 9, Piaseczno, mazowieckie")
x1 = location1.latitude
y1 = location1.longitude

x2 = location2.latitude
y2 = location2.longitude
print((x1, y1))
print((x2, y2))

R = 6373.0

lat1 = radians(x1)
lon1 = radians(y1)
lat2 = radians(x2)
lon2 = radians(y2)

dlon = lon2 - lon1
dlat = lat2 - lat1

a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
c = 2 * atan2(sqrt(a), sqrt(1 - a))

distance = R * c

print("Result:", distance)

#print(location.raw)