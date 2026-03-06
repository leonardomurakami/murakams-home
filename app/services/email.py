import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from ..config import settings


class EmailService:
    """Service for sending emails"""
    
    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.smtp_from = settings.smtp_from
        self.contact_email = settings.contact_email
    
    @property
    def _requires_auth(self) -> bool:
        return bool(self.smtp_username and self.smtp_password)

    def _create_smtp_connection(self) -> smtplib.SMTP:
        server = smtplib.SMTP(self.smtp_host, self.smtp_port)
        if self._requires_auth:
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
        return server
    
    async def send_contact_email(self, name: str, email: str, message: str) -> bool:
        """Send contact form email"""
        if not self.contact_email:
            print("Contact email not configured")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_from
            msg['To'] = self.contact_email
            msg['Subject'] = f"Portfolio Contact Form: Message from {name}"
            
            # Email body
            body = f"""
            New contact form submission:
            
            Name: {name}
            Email: {email}
            
            Message:
            {message}
            
            ---
            Sent from your portfolio website
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email with appropriate configuration
            server = self._create_smtp_connection()
            text = msg.as_string()
            server.sendmail(self.smtp_from, self.contact_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    async def send_notification_email(self, subject: str, content: str) -> bool:
        """Send general notification email"""
        if not self.contact_email:
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_from
            msg['To'] = self.contact_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(content, 'plain'))
            
            # Send email with appropriate configuration
            server = self._create_smtp_connection()
            text = msg.as_string()
            server.sendmail(self.smtp_from, self.contact_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Error sending notification email: {e}")
            return False
