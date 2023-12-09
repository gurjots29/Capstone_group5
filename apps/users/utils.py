
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


DISTANCE_THRESHOLD = 6  # 5 km
MAX_DISTANCE_SCORE = 10  # Puntuación máxima para la distancia

def calculate_distance_score(distance):
    if distance <= DISTANCE_THRESHOLD:
        # Escala inversa: a menor distancia, mayor puntuación
        return MAX_DISTANCE_SCORE * (1 - (distance / DISTANCE_THRESHOLD))
    return 0

# Puntaje adicional por cada interés coincidente
INTEREST_SCORE = 2  # Puntaje adicional por cada interés coincidente

def calculate_match(volunteer_encoded_data, organization_encoded_data, volunteer_coords, organization_coords):
    match_score = 0
    interest_match = False

    # Comparación de intereses
    for interest, has_interest in volunteer_encoded_data.items():
        if has_interest and organization_encoded_data.get(interest, False):
            match_score += INTEREST_SCORE  # Usar INTEREST_SCORE aquí
            interest_match = True

    # Comparación de ubicación solo si hay coincidencia de intereses
    if interest_match and volunteer_coords and organization_coords:
        distance = calculate_distance(volunteer_coords, organization_coords)
        match_score += calculate_distance_score(distance)

    return match_score