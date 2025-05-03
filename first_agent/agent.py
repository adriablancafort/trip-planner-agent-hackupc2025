import openai
import os
import json
from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def asker(sentence: str):
    coses = input(sentence)
    return coses

def first_extraction(description):
    prompt = f"""
    Given the following description of a place, extract:
    1. The safety level of the country, a number from 1 to 10, where 10 means very safe and 1 very unsafe
    2. The cost of traveling there (e.g. cheap, moderate, expensive)
    3. All phrases or sentences that describe the qualities of the country

    Description:
    {description}
    If you are not able to find some of the entries you MUST put null instead of ""
    Please return the results in the following JSON format (only one of each entry), strat the response with the opening bracket and end it with the closing one
    DON'T start with '''json, start directly with bracket and end with it, nothing more:

    {{
        "safety_level": "",
        "travel_cost": "",
        "beauty_description": []
    }}

    """

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts structured data from travel descriptions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    response_text = response.choices[0].message.content

    try:
        result_dict = json.loads(response_text)
        return result_dict
    except json.JSONDecodeError:
        print("❌ Error: Could not parse the response as JSON")
        print("Raw response:")
        print(response_text)
        return None



def completer(result:dict):
    counter = 0
    while(counter != len(result.keys())):
        for key in result.keys():
            if result[key] is None:
                description = asker(f"To continue with the process please insert the following information:{key} of the destination")
                prompt: str = f"""Return the {key} that you think they are describing in the following text: 
                {description} 

                Remember that, only search for the answer to : {key}  
                1. The safety level of the country, a number from 1 to 10, where 10 means very safe and 1 very unsafe
                2. The cost of traveling there (e.g. cheap, moderate, expensive)
                3. All phrases or sentences that describe the qualities of the country, in the form of a list of strings
                Just give the "thing" corresponding to the information I need, nothing more.
                """
                response = client.chat.completions.create(
                    model="gpt-4-1106-preview",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that extracts structured data from travel descriptions."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2
                )
                result[key]  = response.choices[0].message.content
            if result[key] is not None:
                counter += 1
    return result


def summary(description: str):
    return completer(first_extraction(description))
desc1 = """
I want to travel to a place that is very beautiful where you can see incredible views to the mountains but you can also visit museums. The country must
have a very interesting culture and a rich history. I am a working class member of Spain with a relatively low salary and I don't like to spend money. I want a really really safe place
"""
desc2 = """
I want to travel to a place that is very beautiful where you can see the ocean, I want a sunny hot place with some interesting museums. 
I like to spend a lot of money. I don't like dangerous places so I would like a safe place but it does not have to be super safe.
"""

desc_list: list[str] = [desc1, desc2]
info_list: list[dict] = []

for desc in desc_list:
    info: dict = summary(desc)
    info_list.append(info)


#FINS AQUÍ TENS LA LLISTA DE INFORMACIÓ (falta triar country)
print(info_list)

#triem country
def format_preferences(info_list):
    formatted = []
    for idx, pref in enumerate(info_list):
        entry = f"Traveler {idx + 1}:\n"
        if pref.get("safety_level"):
            entry += f" - Prefers safety level: {pref['safety_level']}\n"
        if pref.get("travel_cost"):
            entry += f" - Budget: {pref['travel_cost']}\n"
        if pref.get("beauty_description"):
            beauty = ", ".join(pref["beauty_description"])
            entry += f" - Likes: {beauty}\n"
        formatted.append(entry)
    return "\n".join(formatted)

def get_car_preferences():
    car_desc = asker("What are your car preferences for the trip?")
    prompt: str = f"""
        Say wheather the given text wants a car for the trip or not, if they want a car you have 
        to extract the preferences of how the car should be. The text is:
        {car_desc}
        write an answer in the following format starting with the bracket and ending with the bracket, only write one entry of each:
        {{
            "want_car": ,
            "car_description": ""
        }}
        where the value of want_car is True or False and the car_description is the preferences that
        the user gave. If the user does not want a car, put "does not want a car".
        """
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are an information extracter from text and a JSON creator"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    response_text = response.choices[0].message.content
    try:
        result_dict = json.loads(response_text)
        return result_dict["want_car"],result_dict["car_description"]
    except json.JSONDecodeError:
        print("❌ Error: Could not parse the response as JSON")
        print("Raw response:")
        print(response_text)
        return None

def suggest_country(info_list,date,origin): #date origin
    num_travelers: int = len(info_list)
    need_car, car_preferences = get_car_preferences()
    prompt = (
        f"""You are a travel assistant. Based on the following preferences from multiple travelers, 
        suggest a list of 1 country that would satisfy all of them in some way:\n\n
        {format_preferences(info_list)}\n\n
        answer the question in the following format, don't repeat the entries:
        {{
            "destination": "",
            "budget": "",
            "preferences": ""
        }}
        
        where destination is the name of the country you are traveling to, budget is an integer
        number that should be chosen accordingly to the place and individual budgets, it is the amount 
        of money that they will spend in the trip, and preferences 
        is a string that describes the place that you are going and also describes the requirements of
        the users
        """

    )

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts structured data from travel descriptions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    response_text = response.choices[0].message.content
    print(response_text)
    try:
        result_dict = json.loads(response_text)
        result_dict["travelers"] = num_travelers
        result_dict["origin"] = origin
        result_dict["need_car"] = need_car
        result_dict["car_preferences"] = car_preferences
        result_dict["dates"] = date
        return result_dict
    except json.JSONDecodeError:
        print("❌ Error: Could not parse the response as JSON")
        print("Raw response:")
        print(response_text)
        return None

date = "May 2025"
origin = "Barcelona"
final_thing = suggest_country(info_list, date, origin)
print(final_thing)