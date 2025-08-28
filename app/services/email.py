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
        self.contact_email = settings.contact_email
    
    def _is_mailhog(self) -> bool:
        """Check if we're using MailHog (local development SMTP)"""
        return self.smtp_host.lower() in ['mailhog', 'localhost'] and self.smtp_port == 1025
    
    def _create_smtp_connection(self) -> smtplib.SMTP:
        """Create SMTP connection with appropriate configuration"""
        server = smtplib.SMTP(self.smtp_host, self.smtp_port)
        
        # MailHog doesn't support STARTTLS or authentication
        if not self._is_mailhog():
            server.starttls()
            if self.smtp_username and self.smtp_password:
                server.login(self.smtp_username, self.smtp_password)
        
        return server
    
    async def send_contact_email(self, name: str, email: str, message: str) -> bool:
        """Send contact form email"""
        # For MailHog, we don't need authentication
        if not self._is_mailhog() and not all([self.smtp_username, self.smtp_password, self.contact_email]):
            print("Email configuration incomplete")
            return False
        
        # For MailHog, just need contact_email
        if not self.contact_email:
            print("Contact email not configured")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username or 'noreply@localhost'
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
            from_addr = self.smtp_username or 'noreply@localhost'
            server.sendmail(from_addr, self.contact_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    async def send_notification_email(self, subject: str, content: str) -> bool:
        """Send general notification email"""
        # For MailHog, we don't need authentication
        if not self._is_mailhog() and not all([self.smtp_username, self.smtp_password, self.contact_email]):
            return False
        
        # For MailHog, just need contact_email
        if not self.contact_email:
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username or 'noreply@localhost'
            msg['To'] = self.contact_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(content, 'plain'))
            
            # Send email with appropriate configuration
            server = self._create_smtp_connection()
            text = msg.as_string()
            from_addr = self.smtp_username or 'noreply@localhost'
            server.sendmail(from_addr, self.contact_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Error sending notification email: {e}")
            return False
