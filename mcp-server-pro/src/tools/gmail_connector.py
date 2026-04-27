"""
gmail_connector.py - MCP tools for reading and sending Gmail messages.

Required environment variables:
    GMAIL_CLIENT_ID       - OAuth2 client ID from Google Cloud Console.
    GMAIL_CLIENT_SECRET   - OAuth2 client secret.
    GMAIL_REDIRECT_URI    - Must match the one registered (http://localhost).
    GMAIL_CREDENTIALS_PATH - Path to the credentials.json file.

On first run, the user will be prompted to authorize access via browser.
A token.json file will be saved next to credentials.json for future runs.
"""
import base64
import html as _html_module
import json
import os
import re as _re
from email.mime.text import MIMEText
from pathlib import Path

from src.utils.logging_config import logger

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]


def _get_gmail_service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    credentials_path = Path(os.getenv("GMAIL_CREDENTIALS_PATH", "credentials.json"))
    token_path = credentials_path.parent / "token.json"

    creds = None

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)

        token_path.write_text(creds.to_json())
        logger.info("Gmail token saved to %s", token_path)

    return build("gmail", "v1", credentials=creds)


def _clean_html(html: str) -> str:
    html = _re.sub(r"<style[^>]*>.*?</style>", " ", html, flags=_re.DOTALL | _re.IGNORECASE)
    html = _re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=_re.DOTALL | _re.IGNORECASE)
    html = _re.sub(r"<[^>]+>", " ", html)
    html = _html_module.unescape(html)
    html = _re.sub(r"\s+", " ", html).strip()
    return html


def _parse_message(msg: dict) -> dict:
    headers = {h["name"]: h["value"] for h in msg["payload"].get("headers", [])}

    body = ""
    payload = msg["payload"]

    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data", "")
                body = base64.urlsafe_b64decode(data + "==").decode("utf-8", errors="ignore")
                break
        if not body:
            for part in payload["parts"]:
                if part["mimeType"] == "text/html":
                    data = part["body"].get("data", "")
                    html = base64.urlsafe_b64decode(data + "==").decode("utf-8", errors="ignore")
                    body = _clean_html(html)
                    break
    elif "body" in payload:
        data = payload["body"].get("data", "")
        raw = base64.urlsafe_b64decode(data + "==").decode("utf-8", errors="ignore")
        body = _clean_html(raw) if "<html" in raw.lower() else raw

    return {
        "id": msg["id"],
        "from": headers.get("From", ""),
        "subject": headers.get("Subject", "(no subject)"),
        "date": headers.get("Date", ""),
        "snippet": msg.get("snippet", ""),
        "body": body[:1000],
    }


def register(mcp):

    @mcp.tool()
    def read_emails(max_results: int = 10, query: str = "is:unread") -> str:
        """
        Fetch emails from Gmail matching a query.

        Args:
            max_results: Maximum number of emails to return. Defaults to 10.
            query:       Gmail search query. Defaults to unread emails.
                         Examples: "is:unread", "is:important", "from:boss@company.com".

        Returns:
            JSON string with a list of emails, each containing id, from,
            subject, date, snippet, and body preview.
        """
        try:
            service = _get_gmail_service()

            result = service.users().messages().list(
                userId="me",
                q=query,
                maxResults=max_results,
            ).execute()

            messages = result.get("messages", [])
            if not messages:
                return "No emails found matching the query."

            emails = []
            for m in messages:
                full = service.users().messages().get(
                    userId="me",
                    id=m["id"],
                    format="full",
                ).execute()
                emails.append(_parse_message(full))

            logger.info("Fetched %d emails with query '%s'.", len(emails), query)
            return json.dumps(emails, indent=2, ensure_ascii=False)

        except Exception as exc:
            logger.error("Error reading emails: %s", exc)
            return f"Error reading emails: {exc}"

    @mcp.tool()
    def get_email(email_id: str) -> str:
        """
        Fetch the full content of a single email by ID.

        Args:
            email_id: The Gmail message ID (returned by read_emails).

        Returns:
            JSON string with the full email content.
        """
        try:
            service = _get_gmail_service()
            full = service.users().messages().get(
                userId="me",
                id=email_id,
                format="full",
            ).execute()
            email = _parse_message(full)
            logger.info("Fetched email id=%s subject='%s'.", email_id, email["subject"])
            return json.dumps(email, indent=2, ensure_ascii=False)

        except Exception as exc:
            logger.error("Error fetching email %s: %s", email_id, exc)
            return f"Error fetching email: {exc}"

    @mcp.tool()
    def send_email(to: str, subject: str, body: str) -> str:
        """
        Send an email via Gmail.

        Args:
            to:      Recipient email address.
            subject: Email subject line.
            body:    Plain text email body.

        Returns:
            Confirmation string with the sent message ID.
        """
        try:
            service = _get_gmail_service()

            message = MIMEText(body)
            message["to"] = to
            message["subject"] = subject

            encoded = base64.urlsafe_b64encode(message.as_bytes()).decode()
            result = service.users().messages().send(
                userId="me",
                body={"raw": encoded},
            ).execute()

            logger.info("Email sent to %s, message id=%s.", to, result["id"])
            return f"Email sent successfully. Message ID: {result['id']}"

        except Exception as exc:
            logger.error("Error sending email to %s: %s", to, exc)
            return f"Error sending email: {exc}"

    @mcp.tool()
    def suggest_reply(email_id: str, tone: str = "professional") -> str:
        """
        Fetch an email and return a structured prompt for the agent to draft a reply.

        Args:
            email_id: The Gmail message ID to reply to.
            tone:     Desired tone of the reply (professional, friendly, brief).

        Returns:
            A string containing the original email context and instructions
            for the agent to generate a reply.
        """
        try:
            service = _get_gmail_service()
            full = service.users().messages().get(
                userId="me",
                id=email_id,
                format="full",
            ).execute()
            email = _parse_message(full)

            prompt = (
                f"Draft a {tone} reply to the following email.\n\n"
                f"From: {email['from']}\n"
                f"Subject: {email['subject']}\n"
                f"Date: {email['date']}\n\n"
                f"Original message:\n{email['body']}\n\n"
                f"Write only the reply body, no subject line needed."
            )

            logger.info("Suggest reply prompt generated for email id=%s.", email_id)
            return prompt

        except Exception as exc:
            logger.error("Error generating reply suggestion for %s: %s", email_id, exc)
            return f"Error: {exc}"