from flask import Flask, render_template, request
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

app = Flask(__name__)

# Initializing Nse object
nse = Nse()


# Define routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Perform automated market tasks
    perform_market_tasks()

    # Perform automated email tasks
    sender_email = request.form['sender_email']
    sender_password = request.form['sender_password']
    recipient_email = request.form['recipient_email']
    subject = request.form['subject']
    message = request.form['message']
    send_email(sender_email, sender_password, recipient_email, subject, message)
    subject, sender, content = receive_email(sender_email, sender_password)

    # Perform PDF and Excel automation tasks
    pdf_path = request.form['pdf_path']
    form_data = {}
    excel_path = request.form['excel_path']
    data = []

    # Perform image conversion and file renaming tasks
    image_path = request.form['image_path']
    output_format = request.form['output_format']
    convert_image(image_path, output_format)
    directory = request.form['directory']
    rename_files(directory)

    # Perform mathematical calculations
    result = perform_math_equations()

    # Perform exchange rate calculation
    exchange_rate = calculate_exchange_rate()

    return render_template('result.html', subject=subject, sender=sender, content=content,
                           result=result, exchange_rate=exchange_rate)


# Performing automated market tasks
def perform_market_tasks():
    try:
        # Fetch historical stock market data for a particular stock using nsepy
        stock_data = nse.get_quote('SBIN')

        # Check if data is fetched successfully
        if stock_data:
            print("Stock market data fetched successfully:")
            print(stock_data)  # Print the fetched data
        else:
            print("Failed to fetch stock market data.")
    except Exception as e:
        print("Error fetching stock market data:", e)


# Automated Email Tasks
def send_email(sender_email, sender_password, recipient_email, subject, message):
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        email_content = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, recipient_email, email_content)
    print("Email sent successfully.")


def receive_email(username, password):
    try:
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
    except Exception as e:
        print("Error receiving email:", e)
        return None, None, None


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


if __name__ == "__main__":
    app.run(debug=True)
