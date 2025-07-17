# Recordatorios de Vencimientos - Estudio Contable

## Overview

This workflow automates expiration reminders for an accounting firm's clients. It monitors client expiration dates and sends personalized WhatsApp messages when IVA (VAT) deadlines are due today.

**Business Use Case**: Proactive client communication for tax deadline management
**Input**: Google Sheets with client data (Name, Last Name, Phone, Expiration Date)
**Output**: Personalized WhatsApp messages sent to clients with expiration dates today
**Execution**: Daily at 8:00 AM

## Node Documentation

### 1. Cron Trigger

- **Purpose**: Schedules daily execution at 8:00 AM
- **Configuration**: Runs every day at 8:00 AM
- **Trigger Type**: Time-based scheduler

### 2. Read Clients Sheet

- **Purpose**: Fetches client data from Google Sheets
- **Data Source**: Google Sheets containing client information
- **Expected Columns**:
  - Column A: `Nombre` (First Name)
  - Column B: `Apellido` (Last Name)
  - Column C: `Numero` (Phone Number)
  - Column D: `Vencimiento` (Expiration Date in YYYY-MM-DD format)
- **Range**: A:D (reads all rows with data)

### 3. Filter Expiration Today

- **Purpose**: Filters clients whose expiration date matches today's date
- **Logic**:
  - Gets current date in YYYY-MM-DD format
  - Compares with `Vencimiento` column
  - Returns only matching records
- **Output**: Array of clients with expiration today or empty array

### 4. Create Personalized Messages

- **Purpose**: Generates personalized WhatsApp messages for each client
- **Template**: "Muy buenos días {{ Nombre }}. Se le recuerda que hoy vence su IVA por si tiene algunos comprobantes que entregar esperamos atentamente"
- **Data Transformation**: Creates structured output with phone number and message

### 5. Send WhatsApp Reminder

- **Purpose**: Sends WhatsApp messages via HTTP API
- **Method**: POST request to WhatsApp API
- **Endpoint**: `http://172.17.0.1:3000/send-message/`
- **Parameters**:
  - `message`: Personalized reminder message
  - `to`: Client's phone number

## Implementation Guide

### Prerequisites

1. **Google Sheets Setup**:

   - Create a Google Sheet with client data
   - Ensure columns are: Nombre, Apellido, Numero, Vencimiento
   - Date format must be YYYY-MM-DD (e.g., 2025-01-15)

2. **WhatsApp API Setup**:

   - Configure WhatsApp Web API service
   - Ensure the API endpoint is accessible at `http://172.17.0.1:3000/send-message/`

3. **n8n Configuration**:
   - Set up Google Sheets OAuth2 credentials
   - Configure timezone in workflow settings

### Required Configuration

1. **Google Sheets Node**:

   - Replace `REPLACE_WITH_YOUR_SHEET_ID` with your actual Google Sheets ID
   - Replace `REPLACE_WITH_YOUR_CREDENTIALS_ID` with your Google Sheets credentials ID

2. **WhatsApp API Node**:
   - Verify the API endpoint URL
   - Ensure the API accepts `message` and `to` parameters

### Environment Variables

- **Timezone**: Set to your local timezone in workflow settings
- **API Endpoint**: Configure WhatsApp API base URL if different

### Deployment Considerations

- **Execution Time**: Set to run at 8:00 AM local time
- **Error Handling**: Workflow continues even if some messages fail
- **Logging**: Enabled for debugging and monitoring

## Troubleshooting

### Common Issues

1. **No Messages Sent**:

   - Check if there are clients with expiration date matching today
   - Verify date format in Google Sheets (YYYY-MM-DD)
   - Ensure Google Sheets credentials are valid

2. **WhatsApp API Errors**:

   - Verify API endpoint is accessible
   - Check if WhatsApp Web API service is running
   - Validate phone number format

3. **Date Filtering Issues**:
   - Ensure dates in Google Sheets are in YYYY-MM-DD format
   - Check timezone settings in workflow
   - Verify the date column contains valid dates

### Performance Optimization

- **Batch Size**: Handles up to 100 clients per execution
- **Rate Limiting**: Consider adding delays between messages if needed
- **Memory Usage**: Optimized for small to medium client lists

### Monitoring and Alerting

- **Execution Logs**: Monitor daily execution success/failure
- **Error Tracking**: Review failed message attempts
- **Performance**: Track message delivery rates

## Data Flow

1. **Daily Trigger** → Runs at 8:00 AM
2. **Fetch Data** → Reads client data from Google Sheets
3. **Filter Today** → Identifies clients with expiration today
4. **Personalize** → Creates custom messages for each client
5. **Send Messages** → Delivers WhatsApp reminders

## Security Considerations

- Google Sheets credentials stored securely in n8n
- WhatsApp API endpoint should be secured
- Client data is processed in memory only
- No sensitive data is logged or stored permanently
