"""Email utility library for EMIS."""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List
from pathlib import Path

from src.config import settings
from src.lib.logging import get_logger

logger = get_logger(__name__)


class EmailService:
    """Service for sending emails."""

    def __init__(self):
        self.smtp_host = getattr(settings, "SMTP_HOST", "localhost")
        self.smtp_port = getattr(settings, "SMTP_PORT", 587)
        self.smtp_user = getattr(settings, "SMTP_USER", "")
        self.smtp_password = getattr(settings, "SMTP_PASSWORD", "")
        self.from_email = getattr(settings, "FROM_EMAIL", "noreply@emis.edu")
        self.from_name = getattr(settings, "FROM_NAME", "EMIS System")

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        attachments: Optional[List[Path]] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
    ) -> bool:
        """Send an email."""
        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email
            
            if cc:
                msg["Cc"] = ", ".join(cc)
            if bcc:
                msg["Bcc"] = ", ".join(bcc)

            # Add body
            if body:
                msg.attach(MIMEText(body, "plain"))
            
            if html_body:
                msg.attach(MIMEText(html_body, "html"))

            # Add attachments
            if attachments:
                for file_path in attachments:
                    if file_path.exists():
                        with open(file_path, "rb") as f:
                            part = MIMEBase("application", "octet-stream")
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                "Content-Disposition",
                                f"attachment; filename= {file_path.name}",
                            )
                            msg.attach(part)

            # Send email
            recipients = [to_email]
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                if self.smtp_user and self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg, from_addr=self.from_email, to_addrs=recipients)

            logger.info(f"Email sent to {to_email}: {subject}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}", exc_info=True)
            return False

    def send_template_email(
        self,
        to_email: str,
        template_name: str,
        context: dict,
        attachments: Optional[List[Path]] = None,
    ) -> bool:
        """Send email using a template."""
        # TODO: Implement template rendering (Jinja2)
        # For now, just pass through
        subject = context.get("subject", "EMIS Notification")
        body = context.get("body", "")
        html_body = context.get("html_body")
        
        return self.send_email(
            to_email=to_email,
            subject=subject,
            body=body,
            html_body=html_body,
            attachments=attachments
        )

    def send_bulk_email(
        self,
        recipients: List[str],
        subject: str,
        body: str,
        html_body: Optional[str] = None,
    ) -> dict:
        """Send bulk emails."""
        results = {"success": 0, "failed": 0}
        
        for recipient in recipients:
            if self.send_email(recipient, subject, body, html_body):
                results["success"] += 1
            else:
                results["failed"] += 1
        
        logger.info(f"Bulk email sent: {results['success']} success, {results['failed']} failed")
        return results


# Global email service instance
email_service = EmailService()
