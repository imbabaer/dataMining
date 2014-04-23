from googlemaps import GoogleMaps
gmaps = GoogleMaps(api_key = 'AIzaSyDjuqAztMNv_TgGdQMdpjMo68x9eNbEl-E')
address = 'Constitution Ave NW & 10th St NW, Washington, DC'
lat, lng = gmaps.address_to_latlng(address)
print lat, lng