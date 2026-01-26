import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Test Gmail SMTP connection
smtp_server = "smtp.gmail.com"
smtp_port = 587
username = "drsprojekat30@gmail.com"
password = "dszyvqfkoqqwfshq"

print(f"Testing SMTP connection...")
print(f"Server: {smtp_server}:{smtp_port}")
print(f"Username: {username}")
print(f"Password length: {len(password)} chars")
print(f"Password: {password}")
print()

try:
    # Create SMTP connection
    server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
    server.set_debuglevel(2)  # Enable debug output
    
    # Start TLS
    print("Starting TLS...")
    server.starttls()
    
    # Login
    print("Attempting login...")
    server.login(username, password)
    
    print("\n✅ SUCCESS! Login successful!")
    
    # Try to send a test email
    from_email = username
    to_email = "bolenemanja59@gmail.com"  # Test recipient
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Test Email - DRS Project"
    
    body = "This is a test email from the Flight Booking System."
    msg.attach(MIMEText(body, 'plain'))
    
    print(f"\nSending test email to {to_email}...")
    server.send_message(msg)
    print("✅ Email sent successfully!")
    
    server.quit()
    print("\nConnection closed.")
    
except smtplib.SMTPAuthenticationError as e:
    print(f"\n❌ AUTHENTICATION ERROR: {e}")
    print("\nPossible causes:")
    print("1. App Password is incorrect or revoked")
    print("2. 2-Step Verification is not enabled on Gmail account")
    print("3. App Password was deleted from Google Account")
    print("\nPlease check: https://myaccount.google.com/apppasswords")
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")
