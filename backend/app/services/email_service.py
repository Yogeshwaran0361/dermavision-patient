"""
DermaVision AI — Notification Helper Module
Email notifications are managed via EmailJS browser SDK (@emailjs/browser) directly from the client.
"""

def get_notification_status() -> dict:
    return {
        "engine": "EmailJS Browser SDK",
        "status": "ACTIVE"
    }
