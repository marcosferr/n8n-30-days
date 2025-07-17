# Recordatorios de Vencimientos - Python Version

## Overview

This Python script automates expiration reminders for an accounting firm's clients. It monitors client expiration dates from Google Sheets and sends personalized WhatsApp messages when IVA (VAT) deadlines are due today.

**Business Use Case**: Proactive client communication for tax deadline management
**Input**: Google Sheets with client data (Name, Last Name, Phone, Expiration Date)
**Output**: Personalized WhatsApp messages sent to clients with expiration dates today
**Execution**: Daily at 8:00 AM or on-demand

## Requirements

### Python Dependencies

```bash
pip install -r requirements.txt
```

### Required Dependencies:

- `gspread==5.12.0` - Google Sheets API client
- `oauth2client==4.1.3` - OAuth2 authentication for Google APIs
- `requests==2.31.0` - HTTP requests for WhatsApp API
- `schedule==1.2.0` - Task scheduling
- `python-dateutil==2.8.2` - Date manipulation utilities

### System Requirements

- Python 3.7+
- Google Sheets API credentials
- WhatsApp API service running
- Internet connection

## Setup Instructions

### 1. Google Sheets Setup

1. **Create Google Sheets Document**:

   - Create a new Google Sheet with your client data
   - Columns must be: `Nombre`, `Apellido`, `Numero`, `Vencimiento`
   - Date format for `Vencimiento` must be YYYY-MM-DD

2. **Enable Google Sheets API**:

   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Google Sheets API
   - Create service account credentials
   - Download the JSON credentials file

3. **Share Sheet with Service Account**:
   - Copy the `client_email` from your credentials JSON
   - Share your Google Sheet with this email address
   - Give "Editor" permissions

### 2. WhatsApp API Setup

Ensure you have a WhatsApp API service running that accepts POST requests with:

- Endpoint: `http://172.17.0.1:3000/send-message/`
- Parameters: `to` (phone number), `message` (text)

### 3. Configuration Setup

1. **Run Initial Setup**:

   ```bash
   python recordatorios_vencimientos.py
   ```

   This will create a default `config.json` file.

2. **Update Configuration**:
   Edit `config.json` with your actual values:

   ```json
   {
     "google_sheets": {
       "credentials_file": "path/to/your/google_sheets_credentials.json",
       "sheet_id": "your_google_sheets_document_id"
     },
     "whatsapp_api": {
       "endpoint": "http://172.17.0.1:3000/send-message/",
       "timeout": 30,
       "delay_between_messages": 2
     },
     "message_template": "Muy buenos días {{ Nombre }}. Se le recuerda que hoy vence su IVA por si tiene algunos comprobantes que entregar esperamos atentamente",
     "schedule": {
       "time": "08:00",
       "timezone": "UTC"
     }
   }
   ```

3. **Place Credentials File**:
   - Download your Google Sheets service account JSON file
   - Place it in the same directory as the script
   - Update the `credentials_file` path in config.json

## Usage

### One-time Execution

```bash
python recordatorios_vencimientos.py
```

### Scheduled Execution

```bash
python recordatorios_vencimientos.py --schedule
```

This will run the script continuously, checking for expiration dates daily at the configured time.

### Service/Daemon Mode

For production deployment, consider using:

- **systemd** (Linux)
- **Windows Service** (Windows)
- **Docker container** with restart policy
- **cron job** for simple scheduling

## Configuration Options

### Google Sheets Configuration

- `credentials_file`: Path to service account JSON file
- `sheet_id`: Google Sheets document ID (from the URL)

### WhatsApp API Configuration

- `endpoint`: WhatsApp API endpoint URL
- `timeout`: Request timeout in seconds
- `delay_between_messages`: Delay between messages to avoid rate limiting
- `api_key`: Optional API key for authentication

### Message Configuration

- `message_template`: Message template with `{{ Nombre }}` placeholder
- Custom templates can be created for different types of reminders

### Schedule Configuration

- `time`: Daily execution time in HH:MM format
- `timezone`: Timezone for scheduling (consider using local timezone)

## Error Handling

### Common Issues and Solutions

1. **Google Sheets Authentication Error**:

   ```
   Error: Failed to setup Google Sheets client
   ```

   - Verify credentials file path and permissions
   - Ensure Google Sheets API is enabled
   - Check if sheet is shared with service account email

2. **WhatsApp API Connection Error**:

   ```
   Error: Network error sending message
   ```

   - Verify WhatsApp API service is running
   - Check endpoint URL and network connectivity
   - Ensure API accepts the expected parameters

3. **Date Format Issues**:

   ```
   Error: No clients with expiration today
   ```

   - Verify date format in Google Sheets (YYYY-MM-DD)
   - Check timezone settings
   - Ensure date column contains valid dates

4. **Configuration Errors**:
   ```
   Error: Configuration file not found
   ```
   - Run script once to generate default config
   - Verify config.json exists and has correct format
   - Check all required fields are populated

## Logging

The script provides comprehensive logging:

- **Console Output**: Real-time execution status
- **Log File**: `recordatorios_vencimientos.log` with detailed information
- **Log Levels**: INFO, WARNING, ERROR

### Log Analysis

```bash
# View recent logs
tail -f recordatorios_vencimientos.log

# Search for errors
grep ERROR recordatorios_vencimientos.log

# Count successful sends
grep "Message sent successfully" recordatorios_vencimientos.log | wc -l
```

## Performance Considerations

### Optimization Tips

- **Batch Processing**: Handles multiple clients efficiently
- **Rate Limiting**: Configurable delay between messages
- **Connection Pooling**: Reuses HTTP connections
- **Memory Management**: Processes data in chunks

### Monitoring

- Monitor log files for errors and performance
- Track message delivery success rates
- Monitor API response times
- Set up alerts for failed executions

## Security Best Practices

1. **Credentials Management**:

   - Keep Google Sheets credentials secure
   - Use environment variables for sensitive data
   - Regularly rotate service account keys

2. **API Security**:

   - Secure WhatsApp API endpoint
   - Use HTTPS when possible
   - Implement API key authentication

3. **Data Protection**:
   - Client data is processed in memory only
   - No sensitive data stored in logs
   - Secure configuration files

## Deployment Options

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "recordatorios_vencimientos.py", "--schedule"]
```

### Systemd Service (Linux)

```ini
[Unit]
Description=Recordatorios de Vencimientos Service
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/script
ExecStart=/usr/bin/python3 recordatorios_vencimientos.py --schedule
Restart=always

[Install]
WantedBy=multi-user.target
```

### Windows Service

Use `nssm` or `python-windows-service` to run as Windows service.

## Testing

### Unit Testing

```bash
# Test Google Sheets connection
python -c "from recordatorios_vencimientos import ExpirationReminderService; s = ExpirationReminderService(); print(s.get_clients_data())"

# Test message formatting
python -c "from recordatorios_vencimientos import ExpirationReminderService; s = ExpirationReminderService(); print(s.create_personalized_message({'Nombre': 'Juan'}))"
```

### Integration Testing

1. Create test Google Sheet with sample data
2. Set up test WhatsApp API endpoint
3. Run script with test configuration
4. Verify messages are sent correctly

## Troubleshooting Guide

### Debug Mode

Enable debug logging by modifying the logging level:

```python
logging.basicConfig(level=logging.DEBUG)
```

### Common Solutions

1. **Check Dependencies**: Ensure all required packages are installed
2. **Verify Credentials**: Test Google Sheets access manually
3. **Test API**: Use curl to test WhatsApp API endpoint
4. **Check Dates**: Verify date format and timezone settings
5. **Review Logs**: Check log files for detailed error information

## Support and Maintenance

### Regular Maintenance

- Monitor log files for errors
- Update dependencies regularly
- Rotate Google Sheets credentials
- Backup configuration files

### Scaling Considerations

- For large client lists, consider batch processing
- Implement database storage for better performance
- Use message queues for high-volume scenarios
- Consider multiple WhatsApp API instances for redundancy
