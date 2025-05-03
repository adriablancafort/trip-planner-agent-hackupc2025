from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class FlightSearchParams(BaseModel):
    """Parameters for flight search"""
    origin: str = Field(..., description="Origin airport IATA code (e.g., 'BCN')")
    destination: str = Field(..., description="Destination airport IATA code (e.g., 'JFK')")
    departure_date: Optional[str] = Field(None, description="Departure date in YYYY-MM-DD format")
    market: str = Field("ES", description="Market country code")
    locale: str = Field("en-GB", description="Locale code")
    currency: str = Field("EUR", description="Currency code")
    anytime: bool = Field(False, description="Search for flights anytime")


class TripRequest(BaseModel):
    """Trip planning request from user"""
    origin: str
    destination: Optional[str] = None
    dates: Optional[str] = None
    budget: Optional[float] = None
    preferences: Optional[str] = None


class TripPlan(BaseModel):
    """Trip plan response"""
    destination: str
    start_date: str
    end_date: str
    flights: Optional[List[Dict]] = None
    recommendations: Optional[List[str]] = None
    estimated_budget: Optional[float] = None
