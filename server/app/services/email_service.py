"""
Email service for sending notifications.
"""
from flask import current_app, render_template_string
from flask_mail import Message
from app import mail


class EmailService:
    """Service for sending email notifications."""
    
    @staticmethod
    def send_email(subject, recipients, body_html, body_text=None):
        """
        Send email.
        
        Args:
            subject: Email subject
            recipients: List of recipient emails or single email
            body_html: HTML body content
            body_text: Plain text body content (optional)
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Convert single recipient to list
            if isinstance(recipients, str):
                recipients = [recipients]
            
            msg = Message(
                subject=subject,
                recipients=recipients,
                html=body_html,
                body=body_text
            )
            
            mail.send(msg)
            current_app.logger.info(f"Email sent to {recipients}: {subject}")
            return True
        
        except Exception as e:
            current_app.logger.error(f"Failed to send email: {str(e)}")
            return False
    
    @staticmethod
    def send_role_change_email(user, old_role, new_role):
        """
        Send email notification when user role is changed.
        
        Args:
            user: User object
            old_role: Previous role
            new_role: New role
        """
        subject = "Your role has been updated - Flight Booking System"
        
        body_html = f"""
        <html>
            <body>
                <h2>Role Update Notification</h2>
                <p>Hello {user.first_name} {user.last_name},</p>
                <p>Your role in the Flight Booking System has been updated.</p>
                <p><strong>Previous Role:</strong> {old_role}</p>
                <p><strong>New Role:</strong> {new_role}</p>
                <p>You now have access to additional features based on your new role.</p>
                <br>
                <p>Best regards,<br>Flight Booking System Team</p>
            </body>
        </html>
        """
        
        body_text = f"""
        Role Update Notification
        
        Hello {user.first_name} {user.last_name},
        
        Your role in the Flight Booking System has been updated.
        
        Previous Role: {old_role}
        New Role: {new_role}
        
        You now have access to additional features based on your new role.
        
        Best regards,
        Flight Booking System Team
        """
        
        return EmailService.send_email(subject, user.email, body_html, body_text)
    
    @staticmethod
    def send_flight_cancelled_email(user, flight):
        """
        Send email notification when flight is cancelled.
        
        Args:
            user: User object
            flight: Flight object (dict with flight details)
        """
        subject = "Flight Cancelled - Flight Booking System"
        
        body_html = f"""
        <html>
            <body>
                <h2>Flight Cancellation Notice</h2>
                <p>Dear {user.first_name} {user.last_name},</p>
                <p>We regret to inform you that your booked flight has been cancelled.</p>
                <h3>Flight Details:</h3>
                <ul>
                    <li><strong>Flight:</strong> {flight.get('name')}</li>
                    <li><strong>From:</strong> {flight.get('departure_airport')}</li>
                    <li><strong>To:</strong> {flight.get('arrival_airport')}</li>
                    <li><strong>Departure Time:</strong> {flight.get('departure_time')}</li>
                </ul>
                <p>Your ticket cost has been refunded to your account balance.</p>
                <p>We apologize for any inconvenience this may cause.</p>
                <br>
                <p>Best regards,<br>Flight Booking System Team</p>
            </body>
        </html>
        """
        
        body_text = f"""
        Flight Cancellation Notice
        
        Dear {user.first_name} {user.last_name},
        
        We regret to inform you that your booked flight has been cancelled.
        
        Flight Details:
        - Flight: {flight.get('name')}
        - From: {flight.get('departure_airport')}
        - To: {flight.get('arrival_airport')}
        - Departure Time: {flight.get('departure_time')}
        
        Your ticket cost has been refunded to your account balance.
        
        We apologize for any inconvenience this may cause.
        
        Best regards,
        Flight Booking System Team
        """
        
        return EmailService.send_email(subject, user.email, body_html, body_text)
    
    @staticmethod
    def send_pdf_report_email(user, report_type, pdf_path):
        """
        Send PDF report via email.
        
        Args:
            user: User object (admin)
            report_type: Type of report (e.g., "upcoming", "ongoing", "completed")
            pdf_path: Path to generated PDF file
        """
        subject = f"Flight Report - {report_type.capitalize()} - Flight Booking System"
        
        body_html = f"""
        <html>
            <body>
                <h2>Flight Report Generated</h2>
                <p>Hello {user.first_name} {user.last_name},</p>
                <p>Your requested flight report for <strong>{report_type}</strong> flights has been generated.</p>
                <p>Please find the PDF report attached to this email.</p>
                <br>
                <p>Best regards,<br>Flight Booking System Team</p>
            </body>
        </html>
        """
        
        body_text = f"""
        Flight Report Generated
        
        Hello {user.first_name} {user.last_name},
        
        Your requested flight report for {report_type} flights has been generated.
        
        Please find the PDF report attached to this email.
        
        Best regards,
        Flight Booking System Team
        """
        
        try:
            msg = Message(
                subject=subject,
                recipients=[user.email],
                html=body_html,
                body=body_text
            )
            
            # Attach PDF
            with current_app.open_resource(pdf_path) as fp:
                msg.attach(
                    filename=f"flight_report_{report_type}.pdf",
                    content_type="application/pdf",
                    data=fp.read()
                )
            
            mail.send(msg)
            current_app.logger.info(f"PDF report sent to {user.email}")
            return True
        
        except Exception as e:
            current_app.logger.error(f"Failed to send PDF report: {str(e)}")
            return False