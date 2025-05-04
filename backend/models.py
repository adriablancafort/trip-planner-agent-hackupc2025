from pydantic import BaseModel, Field

class SearchFlightRequest(BaseModel):
    """Parameters for flight search"""
    originIata: str = Field(..., description="Origin airport IATA code (e.g., 'BCN')")
    destinationIata: str = Field(..., description="Destination airport IATA code (e.g., 'JFK')")
    year: int = Field(..., description="Year of travel")
    month: int = Field(..., description="Month of travel")
    day: int = Field(..., description="Day of travel")
    market: str = Field(default="ES", description="Market country code")
    locale: str = Field(default="es-ES", description="Locale for results")
    currency: str = Field(default="EUR", description="Currency for prices")

class SearchHotelRequest(BaseModel):
    """Parameters for hotel search"""
    location: str = Field(..., description="Location for hotel search (e.g., 'Barcelona')")
    year: int = Field(..., description="Year of travel")
    month: int = Field(..., description="Month of travel")
    day: int = Field(..., description="Day of travel")

class SearchEventRequest(BaseModel):
    """Parameters for event search"""
    location: str = Field(..., description="Location for event search (e.g., 'Barcelona')")
    year: int = Field(..., description="Year of travel")
    month: int = Field(..., description="Month of travel")
    day: int = Field(..., description="Day of travel")

