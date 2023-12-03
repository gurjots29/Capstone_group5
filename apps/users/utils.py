
from geopy.distance import geodesic
import requests


GOOGLE_API_KEY ="AIzaSyC8Ln8eq5J8InDkZBlbht_6ePNN0aOBeBc"

def get_coordinates(direccion):
    api_key = GOOGLE_API_KEY
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={direccion}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            location = data['results'][0]['geometry']['location']
            lat, lng = location.get('lat'), location.get('lng')
            print("Coordenadas obtenidas para", direccion, ":", lat, lng)
            return (lat, lng)
        else:
            print("No se encontraron coordenadas para", url)
            return None, None
    else:
        print("Error en la respuesta de la API para", url)
        return None, None


def calculate_distance(coord1, coord2):
    if not coord1 or not coord2:
        return None
    return geodesic(coord1, coord2).kilometers

def apply_one_hot_encoding(interests):
    encoded_data = {interest: True for interest in interests}
    return encoded_data


DISTANCE_THRESHOLD = 5  # 5 km

def calculate_match(volunteer_encoded_data, organization_encoded_data, volunteer_coords, organization_coords):
    match_score = 0

    # Comparación de intereses
    for interest, has_interest in volunteer_encoded_data.items():
        if has_interest and organization_encoded_data.get(interest, False):
            match_score += 1

    # Comparación de ubicación con mayor peso
    if volunteer_coords and organization_coords:
        distance = calculate_distance(volunteer_coords, organization_coords)
        if distance <= DISTANCE_THRESHOLD:
            match_score += 3  # Incrementa el puntaje en mayor medida si las ubicaciones están cerca

    return match_score