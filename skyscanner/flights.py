from models import SearchFlightRequest
import requests
import os

def search_flights(params: SearchFlightRequest):
    api_key = os.getenv("SKYSCANNER_API_KEY")

    market = "ES"
    locale = "es-ES"
    currency = "EUR"

    url = "https://partners.api.skyscanner.net/apiservices/v3/flights/indicative/search"

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "query": {
            "market": market,
            "locale": locale,
            "currency": currency,
            "queryLegs": [
                {
                    "originPlace": {
                        "queryPlace": {
                            "iata": params.originIata
                        }
                    },
                    "destinationPlace": {
                        "queryPlace": {
                            "iata": params.destinationIata
                        }
                    },
                    "dateRange": {
                        "startDate": {
                            "year": params.year,
                            "month": params.month
                        },
                        "endDate": {
                            "year": params.year,
                            "month": params.month
                        }
                    }
                }
            ],
            "dateTimeGroupingType": "DATE_TIME_GROUPING_TYPE_BY_DATE"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {response.text if 'response' in locals() else 'No response'}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")

    return None
