import os
import requests
from models import SendEmail

def send_email(params: SendEmail):
    """
    Send email.
    """

    print("Sending email:", params)

    # Set the URL for the SendGrid API
    url = "https://api.sendgrid.com/v3/mail/send"

    # Create the headers
    headers = {
        "Authorization": f"Bearer {os.getenv("SENDGRID_API_KEY")}",
        "Content-Type": "application/json"
    }

    # Define the data payload for the email
    data = {
        "personalizations": [
            {
                "to": [{"email": params.email}],
            }
        ],
        "from": {"email": "tripmatehackupc@gmail.com"},
        "subject": params.subject,
        "content": [
            {
                "type": "text/plain",
                "value": params.content
            }
        ]
    }

    # Send the POST request
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return str(response.status_code)

