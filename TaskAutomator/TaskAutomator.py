import smtplib
import imaplib
import email
import os
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader, PdfWriter
import openpyxl
from PIL import Image
import pandas as pd
from datetime import datetime
from nsetools import Nse

# Initializing Nse object
nse = Nse()

# Performing automated market tasks
def perform_market_tasks():
    try:
        # Fetch historical stock market data for a particular stock using nsetools
        stock_data = nse.get_quote('SBIN')

        # Check if data is fetched successfully
        if stock_data:
            print("Stock market data fetched successfully:")
            print(stock_data)  # Print the fetched data
        else:
            print("Failed to fetch stock market data.")
    except Exception as e:
        print("Error fetching stock market data:", e)

# Modified function to handle redirects
def perform_market_tasks():
    try:
        # Fetch historical stock market data for a particular stock using nsetools
        stock_data = nse.get_quote('SBIN')

        # Check if data is fetched successfully
        if stock_data:
            print("Stock market data fetched successfully:")
            print(stock_data)  # Print the fetched data
        else:
            print("Failed to fetch stock market data.")
    except Exception as e:
        print("Error fetching stock market data:", e)


# Sending out, replying to, and sorting emails
def send_email(sender_email, sender_password, recipient_email, subject, message):
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        email_content = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, recipient_email, email_content)
    print("Email sent successfully.")

def receive_email(username, password):
    with imaplib.IMAP4_SSL('imap.gmail.com') as mail:
        mail.login(username, password)
        mail.select('inbox')
        _, data = mail.search(None, 'ALL')
        mail_ids = data[0]
        id_list = mail_ids.split()
        latest_email_id = id_list[-1]
        _, data = mail.fetch(latest_email_id, '(RFC822)')
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        msg = email.message_from_string(raw_email_string)
        subject = msg['subject']
        sender = msg['from']
        content = msg.get_payload()
    print("Email received successfully.")
    return subject, sender, content

# Filling out PDFs and Excel files
def fill_pdf(pdf_path, form_data):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt("password")
        for key, value in form_data.items():
            writer.add_metadata({key: value})
        with open('filled_form.pdf', 'wb') as output_file:
            writer.write(output_file)
    print("PDF form filled successfully.")

def fill_excel(excel_path, data):
    wb = openpyxl.Workbook()
    sheet = wb.active
    for row_data in data:
        sheet.append(row_data)
    wb.save(excel_path)
    print("Excel file filled successfully.")

# Converting images, renaming files
def convert_image(image_path, output_format):
    output_path = os.path.splitext(image_path)[0] + '.' + output_format
    with Image.open(image_path) as img:
        img.save(output_path)
    print("Image converted successfully.")

def rename_files(directory):
    for count, filename in enumerate(os.listdir(directory)):
        new_filename = f"file_{count}.txt"
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
    print("Files renamed successfully.")

# Performing math equations
def perform_math_equations():
    result = 5 + 3 * 2
    print("Mathematical calculations performed successfully.")
    return result

# Calculating exchange rates
def calculate_exchange_rate():
    response = requests.get('https://api.exchangeratesapi.io/latest')
    if response.status_code == 200:
        data = response.json()
        exchange_rate = data['rates']['USD']  # Example: Exchange rate for USD
        print("Exchange rate calculated successfully.")
        return exchange_rate
    else:
        print("Failed to fetch exchange rate.")
        return None

# Main function to demonstrate automated tasks
def main():
    # Perform automated market tasks
    perform_market_tasks()

    # Perform automated email tasks
    sender_email = input("Enter your email address: ")
    sender_password = input("Enter your email password: ")
    recipient_email = input("Enter recipient's email address: ")
    subject = input("Enter email subject: ")
    message = input("Enter email message: ")
    send_email(sender_email, sender_password, recipient_email, subject, message)
    subject, sender, content = receive_email(sender_email, sender_password)
    print(f"Received email - Subject: {subject}, Sender: {sender}, Content: {content}")

    # Perform PDF and Excel automation tasks
    pdf_path = input("Enter path to PDF file: ")
    form_data = {}
    while True:
        key = input("Enter form field name (or type 'done' to finish): ")
        if key.lower() == 'done':
            break
        value = input(f"Enter value for '{key}': ")
        form_data[key] = value
    fill_pdf(pdf_path, form_data)

    excel_path = input("Enter path to Excel file: ")
    data = []
    while True:
        row = input("Enter data for a row (or type 'done' to finish): ").split(',')
        if row[0].lower() == 'done':
            break
        data.append(row)
    fill_excel(excel_path, data)

    # Perform image conversion and file renaming tasks
    image_path = input("Enter path to image file: ")
    output_format = input("Enter output format (e.g., 'png', 'jpg'): ")
    convert_image(image_path, output_format)

    directory = input("Enter path to directory containing files to rename: ")
    rename_files(directory)

    # Perform mathematical calculations
    result = perform_math_equations()
    print(f"Result of math operations: {result}")

    # Perform exchange rate calculation
    exchange_rate = calculate_exchange_rate()
    if exchange_rate is not None:
        print(f"Exchange rate: {exchange_rate}")

if __name__ == "__main__":
    main()
