import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
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

    message = Mail(
        from_email='tripmatehackupc@gmail.com',
        to_emails=params.email,
        subject=params.subject,
        html_content=params.content)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
    
    print(params)

if __name__ == "__main__":
    load_dotenv()
    send_email(SendEmail(
        email="pol.de.los.santos@estudiantat.upc.edu",
        subject="Subject XSD",
        content="this is a test"
    ))