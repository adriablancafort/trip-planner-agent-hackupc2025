from models import SearchFlightRequest
import requests
import os
import re

def search_flights(params: SearchFlightRequest):
    """
    Search for flights using the Skyscanner API.
    """
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
        return format_flight_results(response.json())

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


def format_flight_results(results):
    """
    Format flight search results for better LLM understanding
    """
    if not results or "content" not in results or "results" not in results["content"]:
        return "No flight results available."
    
    quotes = results["content"]["results"].get("quotes", {})
    if not quotes:
        return "No flight quotes available."
    
    lines = []
    
    lines.append("## Flight Options")
    lines.append("| Flight ID | Price | Direct | Date |")
    lines.append("|-----------|-------|--------|------|")
    
    for identifier, quote in quotes.items():
        price = quote.get("minPrice", {}).get("amount", "N/A")
        is_direct = "Yes" if quote.get("isDirect", False) else "No"
        
        departure = quote.get("outboundLeg", {}).get("departureDateTime", {})
        year = departure.get("year", "N/A")
        month = departure.get("month", "N/A")
        day = departure.get("day", "N/A")
        
        date = f"{year}-{month:02d}-{day:02d}" if isinstance(year, int) else "N/A"
        
        airline_match = re.search(r'\*([a-z]+)\*([A-Z]{2,})', identifier)
        if airline_match:
            airline_name = airline_match.group(1)  # e.g., 'leve', 'skyp', 'iber'
            airline_code = airline_match.group(2)  # e.g., 'LL', 'IB', 'FR'
            airline_info = f"{airline_name}-{airline_code}"
        else:
            airline_info = identifier
        
        lines.append(f"| {airline_info} | {price} | {is_direct} | {date} |")
    
    return "\n".join(lines)
