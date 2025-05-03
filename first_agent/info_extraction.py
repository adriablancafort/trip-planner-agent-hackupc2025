import openaiç
from dotenv import load_dotenv
load_dotenv()

def extract_place_info(description):
    prompt = f"""
    Given the following description of a place, extract:
    1. The safety level of the country, a number from 1 to 10, where 10 means very safe and 1 very unsafe
    2. The cost of traveling there (e.g. cheap, moderate, expensive)
    3. All phrases or sentences that describe the qualities of the country

    Description:
    """
    prompt += description + "\n\nPlease return the results in the following JSON format:\n\n"
    prompt += """
    {
        "safety_level": "",
        "travel_cost": "",
        "beauty_description": []
    }
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts structured data from travel descriptions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response['choices'][0]['message']['content']

# Example usage
description = """
Nestled in the heart of the Alps, Switzerland offers breathtaking mountain landscapes and pristine lakes that reflect the sky like a mirror. It's one of the safest countries in the world, with extremely low crime rates. However, it's also known for being quite expensive for travelers, especially in cities like Zurich or Geneva.
"""

result = extract_place_info(description)
print(result)
