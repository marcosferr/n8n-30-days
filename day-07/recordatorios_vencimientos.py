#!/usr/bin/env python3
"""
Recordatorios de Vencimientos - Python Version
Automated expiration reminders for accounting firm clients
"""

import os
import sys
import json
import logging
import requests
from datetime import datetime, date
from typing import List, Dict, Optional
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import schedule
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("recordatorios_vencimientos.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class ExpirationReminderService:
    """Service to handle expiration reminders for accounting clients"""

    def __init__(self, config_path: str = "config.json"):
        """Initialize the service with configuration"""
        self.config = self._load_config(config_path)
        self.sheets_client = self._setup_google_sheets()

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file {config_path} not found")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in configuration file {config_path}")
            raise

    def _setup_google_sheets(self) -> gspread.Client:
        """Setup Google Sheets client with OAuth2 credentials"""
        try:
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive",
            ]

            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                self.config["google_sheets"]["credentials_file"], scope
            )

            return gspread.authorize(credentials)
        except Exception as e:
            logger.error(f"Failed to setup Google Sheets client: {str(e)}")
            raise

    def get_clients_data(self) -> List[Dict]:
        """Fetch client data from Google Sheets"""
        try:
            # Open the worksheet
            sheet = self.sheets_client.open_by_key(
                self.config["google_sheets"]["sheet_id"]
            ).sheet1

            # Get all records
            records = sheet.get_all_records()

            logger.info(f"Retrieved {len(records)} client records from Google Sheets")
            return records

        except Exception as e:
            logger.error(f"Failed to fetch client data: {str(e)}")
            raise

    def filter_expiration_today(self, clients: List[Dict]) -> List[Dict]:
        """Filter clients with expiration day matching today's day"""
        today = date.today()
        today_day = today.day

        filtered_clients = []

        for client in clients:
            expiration_day = client.get("Vencimiento", "")

            # Handle both numeric and string inputs
            if isinstance(expiration_day, str):
                try:
                    day_number = int(expiration_day)
                except ValueError:
                    logger.warning(
                        f"Invalid day format for client {client.get('Nombre')}: {expiration_day}"
                    )
                    continue
            else:
                day_number = expiration_day

            if day_number == today_day:
                filtered_clients.append(client)
                logger.info(
                    f"Client {client.get('Nombre')} {client.get('Apellido')} has expiration day {day_number} (today)"
                )

        logger.info(
            f"Found {len(filtered_clients)} clients with expiration day {today_day}"
        )
        return filtered_clients

    def create_personalized_message(self, client: Dict) -> str:
        """Create personalized reminder message for client"""
        template = self.config["message_template"]

        # Replace placeholder with client name
        message = template.replace("{{ Nombre }}", client.get("Nombre", ""))

        return message

    def send_whatsapp_message(self, phone_number: str, message: str) -> bool:
        """Send WhatsApp message via API"""
        try:
            url = self.config["whatsapp_api"]["endpoint"]

            payload = {"to": phone_number, "message": message}

            headers = {"Content-Type": "application/json"}

            # Add API key if configured
            if "api_key" in self.config["whatsapp_api"]:
                headers["Authorization"] = (
                    f"Bearer {self.config['whatsapp_api']['api_key']}"
                )

            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=self.config["whatsapp_api"].get("timeout", 30),
            )

            if response.status_code == 200:
                logger.info(f"Message sent successfully to {phone_number}")
                return True
            else:
                logger.error(
                    f"Failed to send message to {phone_number}: {response.status_code} - {response.text}"
                )
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error sending message to {phone_number}: {str(e)}")
            return False
        except Exception as e:
            logger.error(
                f"Unexpected error sending message to {phone_number}: {str(e)}"
            )
            return False

    def process_reminders(self):
        """Main process to handle expiration reminders"""
        try:
            logger.info("Starting expiration reminder process")

            # Get all clients data
            clients = self.get_clients_data()

            # Filter clients with expiration day today
            clients_with_expiration = self.filter_expiration_today(clients)

            if not clients_with_expiration:
                logger.info("No clients with expiration day today")
                return

            # Send reminders to each client
            successful_sends = 0
            failed_sends = 0

            for client in clients_with_expiration:
                # Create personalized message
                message = self.create_personalized_message(client)

                # Send WhatsApp message
                phone_number = client.get("Numero", "")

                if not phone_number:
                    logger.warning(
                        f"No phone number for client {client.get('Nombre')} {client.get('Apellido')}"
                    )
                    failed_sends += 1
                    continue

                success = self.send_whatsapp_message(phone_number, message)

                if success:
                    successful_sends += 1
                else:
                    failed_sends += 1

                # Add delay between messages to avoid rate limiting
                time.sleep(self.config["whatsapp_api"].get("delay_between_messages", 2))

            logger.info(
                f"Reminder process completed: {successful_sends} successful, {failed_sends} failed"
            )

        except Exception as e:
            logger.error(f"Error in reminder process: {str(e)}")
            raise


def create_default_config():
    """Create a default configuration file"""
    config = {
        "google_sheets": {
            "credentials_file": "google_sheets_credentials.json",
            "sheet_id": "YOUR_GOOGLE_SHEETS_ID_HERE",
        },
        "whatsapp_api": {
            "endpoint": "http://172.17.0.1:3000/send-message/",
            "timeout": 30,
            "delay_between_messages": 2,
        },
        "message_template": "Muy buenos días {{ Nombre }}. Se le recuerda que hoy vence su IVA por si tiene algunos comprobantes que entregar esperamos atentamente",
        "schedule": {"time": "08:00", "timezone": "UTC"},
    }

    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print("Default configuration created in config.json")
    print("Please update the configuration with your actual values")


def main():
    """Main function to run the service"""
    # Check if configuration exists
    if not os.path.exists("config.json"):
        print("Configuration file not found. Creating default configuration...")
        create_default_config()
        return

    try:
        # Initialize service
        service = ExpirationReminderService()

        # Check if running in scheduled mode
        if len(sys.argv) > 1 and sys.argv[1] == "--schedule":
            # Schedule daily execution
            schedule.every().day.at(service.config["schedule"]["time"]).do(
                service.process_reminders
            )

            logger.info(
                f"Scheduled daily execution at {service.config['schedule']['time']}"
            )

            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        else:
            # Run once
            service.process_reminders()

    except KeyboardInterrupt:
        logger.info("Service stopped by user")
    except Exception as e:
        logger.error(f"Service error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
