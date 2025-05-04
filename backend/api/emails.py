import os
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field


class SendEmail(BaseModel):
    """Parameters for sending email"""
    email: str = Field(..., description="Email address to send the information")
    subject: str = Field(..., description="Subject of the email")
    content: str = Field(..., description="Content of the email")


def send_email(params: SendEmail):
    """
    Send email.
    """
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
    return str(response.status_code)



if __name__ == "__main__":
    load_dotenv()
    send_email(SendEmail(
        email="pol.de.los.santos@estudiantat.upc.edu",
        subject="Subject XSD",
        content="this is a test"
    ))