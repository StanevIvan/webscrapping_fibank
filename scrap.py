import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

FROM_EMAIL = os.getenv('FROM_EMAIL')
TO_EMAIL = os.getenv('TO_EMAIL')
APP_PASSWORD = os.getenv('APP_PASSWORD')

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome()
driver.get("https://my.fibank.bg/EBank/public/offices")

time.sleep(5)

data = []

offices = driver.find_elements(By.CLASS_NAME, "margin-16")
for office in offices:
    name_element = office.find_element(By.CSS_SELECTOR, 'p[bo-bind="item.name"]')
    address_element = office.find_element(By.CSS_SELECTOR, 'p.grey-txt.s2.ellipsis-txt')
    telephone_element = office.find_element(By.CSS_SELECTOR, 'p[bo-bind="item.phones[0].phone"]')
    working_hours_elements = office.find_elements(By.CLASS_NAME, 'sg-office-work-time')
    
    saturday_hours = None
    sunday_hours = None
    
    for el in working_hours_elements:
        lines = el.text.split('\n')
        for i, line in enumerate(lines):
            if 'събота' in line.lower() and i + 1 == 'Неделя':
                saturday_hours = lines[i + 3].strip() if i + 3 < len(lines) else None
            elif 'събота' in line.lower():
                saturday_hours = lines[i + 2].strip() if i + 2 < len(lines) else None
            if 'неделя' in line.lower():
                sunday_hours = lines[i + 3].strip() if i + 3 < len(lines) else None

    name = name_element.text.strip() if name_element else None
    address = address_element.text.strip() if address_element else None
    telephone = telephone_element.text.strip() if telephone_element else None
    
    if saturday_hours != None or sunday_hours != None:
        data.append({
            'Име на офис': name,
                'Адрес': address,
                'Телефон': telephone,
                'Раб.време събота': saturday_hours,
                'Раб.време неделя': sunday_hours
        })

driver.quit()

df = pd.DataFrame(data)
OUTER_DIR = 'C:\\PythonApp'

if not os.path.exists(OUTER_DIR):
    os.makedirs(OUTER_DIR)

OUTPUT_FILE = os.path.join(OUTER_DIR, 'fibank_offices.xlsx')
df.to_excel(OUTPUT_FILE, index=False)

print(df) # Uncomment to see the data in CLI

def send_email():
    '''
    Send email with the data in attachment.
    '''

    FROM_ADDR = FROM_EMAIL
    TO_ADDR = TO_EMAIL

    msg = MIMEMultipart()
    msg['From'] = FROM_ADDR
    msg['To'] = TO_ADDR
    msg['Subject'] = "Fibank Branches"

    body = "Fibank Branches Asignment - DONE, https://github.com/StanevIvan/webscrapping_fibank"
    msg.attach(MIMEText(body, 'plain'))

    FILENAME = 'fibank_offices.xlsx'
    attachment = open(OUTPUT_FILE, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % FILENAME)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(FROM_ADDR, APP_PASSWORD)
    text = msg.as_string()
    server.sendmail(FROM_ADDR, TO_ADDR, text)
    server.quit()

send_email()

