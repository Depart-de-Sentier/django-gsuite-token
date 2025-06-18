from email.message import EmailMessage
from pathlib import Path
import base64
import os

from django.core.mail.message import sanitize_address
from django.core.mail.backends.base import BaseEmailBackend
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

__version__ = "0.1"


class GSuiteEmailBackend(BaseEmailBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.creds = self.get_creds()

    def get_creds(self):
        try:
            token = Path(os.environ['GOOGLE_TOKEN_FILEPATH'])
            assert token.is_file()

        except (KeyError, AssertionError):
            return

        SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
        return Credentials.from_authorized_user_file(token, SCOPES)

    def refresh_creds(self):
        if not self.creds.valid:
            self.creds.refresh(Request())

    def send_messages(self, email_messages):
        if not self.creds:
            return

        self.refresh_creds()
        service = build("gmail", "v1", credentials=self.creds)

        for message in email_messages:
            for recipient in message.to:
                email_message = EmailMessage()
                email_message.set_content(message.body)
                email_message["To"] = sanitize_address(recipient, "utf-8")
                email_message["From"] = sanitize_address(message.from_email, "utf-8")
                email_message["Subject"] = message.subject

                encoded_message = base64.urlsafe_b64encode(email_message.as_bytes()).decode()
                service.users().messages().send(userId="me", body={"raw": encoded_message}).execute()
