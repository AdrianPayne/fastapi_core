from fastapi import APIRouter, Query, Response
import joblib
import requests
import googlemaps

from config import settings
from .models import MobileSignal


router = APIRouter(
    prefix="/mobile_signal",
    tags=["mobile_signal"]
)


@router.get("/get_by_coords", response_model=MobileSignal)
async def predict_mobile_signal(
        longitude: float = Query(None, example=-8.515573),
        latitude: float = Query(None, example=51.881049),
):
    """
    Get predicted RSSI from coordinates
    """
    # Load the model from file and predict
    model = joblib.load('services/mobile_signal/data/rssi_model.pkl')
    predicted_rssi = model.predict([[longitude, latitude]])[0]

    # Google maps
    gmaps = googlemaps.Client(key=settings.google_api_key)
    reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))

    address = reverse_geocode_result
    number = address[0]['address_components'][0]['long_name']
    street = address[0]['address_components'][1]['long_name']
    neighborhood = address[0]['address_components'][2]['long_name']
    city = address[0]['address_components'][3]['long_name']
    country = address[0]['address_components'][5]['long_name']
    code = address[0]['address_components'][6]['long_name']

    address = f'{number}, {street}, {neighborhood}, {city}, {code}, {country}'

    # DB
    mobile_signal = MobileSignal(address=address, latitude=latitude, longitude=longitude, rssi=predicted_rssi).create()

    return mobile_signal


@router.get("/get_by_address", response_model=MobileSignal)
async def predict_mobile_signal(
        address: str = Query(None, example="9 Bishopscourt Rd, Bishopstown, Cork, T12 R86C, Ireland")
):
    """
    Get predicted RSSI from address
    """
    # Google maps
    gmaps = googlemaps.Client(key=settings.google_api_key)
    geocode_result = gmaps.geocode(address)
    latitude = geocode_result[0]['geometry']['location']['lat']
    longitude = geocode_result[0]['geometry']['location']['lng']

    # Load the model from file and predict
    model = joblib.load('services/mobile_signal/data/rssi_model.pkl')
    predicted_rssi = model.predict([[longitude, latitude]])[0]

    # DB
    mobile_signal = MobileSignal(address=address, latitude=latitude, longitude=longitude, rssi=predicted_rssi).create()

    return mobile_signal


@router.get("/get_petitions", response_model=list[MobileSignal])
async def get_petitions():
    """
    Get the list of previous petitions
    """
    return MobileSignal.get_all(MobileSignal)
