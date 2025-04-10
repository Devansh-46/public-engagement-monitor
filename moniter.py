import os
import csv
import time
import datetime
import pywhatkit
import schedule
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Setup headless browser
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Constants
NIU_WEBSITE_URL = 'https://niu.edu.in'
NIU_LINKEDIN_URL = 'https://www.linkedin.com/school/noida-international-university/'
NIU_INSTAGRAM_URL = 'https://www.instagram.com/niuniversity/'
WHATSAPP_NUMBER = '+91xxxxxxxxxx'  # Replace with your number

# Create directory for reports
os.makedirs("reports", exist_ok=True)

def fetch_niu_website_data():
    driver.get(NIU_WEBSITE_URL)
    time.sleep(5)
    title = driver.title
    return {"page_title": title, "url": NIU_WEBSITE_URL}

def fetch_linkedin_followers():
    # Simulation: Replace with actual scraping via API or tool if needed
    return {"followers": 20000}  # Placeholder

def fetch_instagram_followers():
    # Simulation: Replace with actual scraping via API or tool if needed
    return {"followers": 15000}  # Placeholder

def save_to_csv(data):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"reports/niu_public_engagement_{date_str}.csv"
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date", "NIU Title", "LinkedIn Followers", "Instagram Followers"])
        writer.writerow([date_str, data["website"]["page_title"], data["linkedin"]["followers"], data["instagram"]["followers"]])
    return filename

def generate_chart(data):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    labels = ['LinkedIn', 'Instagram']
    values = [data['linkedin']['followers'], data['instagram']['followers']]
    plt.bar(labels, values, color=['blue', 'purple'])
    plt.title(f"NIU Public Engagement on {date_str}")
    plt.ylabel("Followers")
    chart_path = f"reports/niu_engagement_chart_{date_str}.png"
    plt.savefig(chart_path)
    plt.close()
    return chart_path

def send_whatsapp_message(text):
    now = datetime.datetime.now()
    send_time = now + datetime.timedelta(minutes=2)
    pywhatkit.sendwhatmsg(WHATSAPP_NUMBER, text, send_time.hour, send_time.minute)

def job():
    data = {
        "website": fetch_niu_website_data(),
        "linkedin": fetch_linkedin_followers(),
        "instagram": fetch_instagram_followers()
    }
    csv_path = save_to_csv(data)
    chart_path = generate_chart(data)
    msg = f"NIU Daily Engagement Report\nWebsite: {data['website']['url']}\nLinkedIn Followers: {data['linkedin']['followers']}\nInstagram Followers: {data['instagram']['followers']}\nCSV: {csv_path}\nChart: {chart_path}"
    send_whatsapp_message(msg)

# Schedule the job daily
schedule.every().day.at("10:00").do(job)

print("Scheduler started. Waiting for 10:00 AM daily run...")

while True:
    schedule.run_pending()
    time.sleep(60)
