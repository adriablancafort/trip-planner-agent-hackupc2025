from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from dataclasses import dataclass


class FlightSearchParams(BaseModel):
    """Parameters for flight search"""
    origin: str = Field(..., description="Origin airport IATA code (e.g., 'BCN')")
    destination: str = Field(..., description="Destination airport IATA code (e.g., 'JFK')")
    departure_date: Optional[str] = Field(None, description="Departure date in YYYY-MM-DD format")
    market: str = Field("ES", description="Market country code")
    locale: str = Field("en-GB", description="Locale code")
    currency: str = Field("EUR", description="Currency code")
    anytime: bool = Field(False, description="Search for flights anytime")


class CarHireSearchParams(BaseModel):
    """Parameters for car hire search"""
    location_id: str = Field(..., description="Location ID for car pickup/dropoff")
    pickup_year: int = Field(..., description="Year of pickup date")
    pickup_month: int = Field(..., description="Month of pickup date")
    pickup_day: int = Field(..., description="Day of pickup date")
    dropoff_year: int = Field(..., description="Year of dropoff date")
    dropoff_month: int = Field(..., description="Month of dropoff date")
    dropoff_day: int = Field(..., description="Day of dropoff date")
    market: str = Field("ES", description="Market country code")
    locale: str = Field("en-GB", description="Locale code")
    currency: str = Field("EUR", description="Currency code")


class TripRequest(BaseModel):
    """Trip planning request from user"""
    origin: str
    destination: Optional[str] = None
    dates: Optional[str] = None
    budget: Optional[float] = None
    preferences: Optional[str] = None
    travelers: Optional[int] = None
    need_car: Optional[bool] = False
    car_preferences: Optional[str] = None


class TripPlan(BaseModel):
    """Trip plan response"""
    destination: str
    start_date: str
    end_date: str
    flights: Optional[List[Dict]] = None
    car_hire: Optional[List[Dict]] = None
    recommendations: Optional[List[str]] = None
    estimated_budget: Optional[float] = None


@dataclass
class FlightSearchParams:
    """Parameters for flight search requests."""
    origin: str
    destination: str
    departure_date: Optional[str] = None
    market: str = "US"
    locale: str = "en-US"
    currency: str = "USD"
