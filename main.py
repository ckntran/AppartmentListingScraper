import Kleinanzeigen

import time
import smtplib
import gspread # pip install gspread
from oauth2client.service_account import ServiceAccountCredentials # pip install oauth2client
# pip install PyOpenSSL

my_email = ""
receiver_email = ""
password = ""

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = ServiceAccountCredentials.from_json_keyfile_name('data/credentials.json', scopes=scopes)

gsfile = gspread.authorize(creds)
workbook = gsfile.open("Immobilienscraper")
sheet = workbook.worksheet("List")

# clear sheet
sheet.clear()

# add header
sheet.update(values =[
    ['Type', 'Last_Updated', 'Description', 'District', 'Price', 'Rooms', 'Website', 'Link']
], range_name='A1:H1')
sheet.format('A1:H1', {'textFormat': {'bold': True}})

final_list = Kleinanzeigen.kleinanzeigen()
sorted_list = sorted(final_list, key=lambda x: x[4])

# add values
counter = 2
for post in sorted_list:
    sheet.update(values = [post], range_name=f'A{counter}:H{counter}')
    counter += 1
    if counter % 60 == 0:
        time.sleep(60) # google sheets API quota per minute per user per project: 60

with smtplib.SMTP("smtp.gmail.com") as connection:
   connection.starttls() # encrypts intercepted message
   connection.login(user=my_email, password=password)
   connection.sendmail(
   from_addr = my_email
   , to_addrs = receiver_email
   , msg="Subject:New Apartment Listings\n\nHere are the latest apartment listings: https://docs.google.com/spreadsheets/d/126HzXJRcB4u2G3A3PdfDmNtVh6hCoqlCKgHjPiqMHVk"
   )
   connection.close()

