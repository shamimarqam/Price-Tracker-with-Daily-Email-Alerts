# Price-Tracker-with-Daily-Email-Alerts
Track product prices from Amazon, Flipkart, and Myntra without login, store price history, and send daily email alerts when prices drop or deals appear.
# **Price Tracker with Daily Email Alerts**

A production-ready project that tracks product prices from major Indian e-commerce websites and sends automated daily email reports with price-drop alerts.

## **Features**

* Scrapes product prices from **Amazon**, **Flipkart**, **Myntra** (no login required)
* Stores and updates price history in **price_history.csv**
* Detects **price drops** using historical data
* Sends **daily HTML email** with:
  * Summary of all tracked prices
  * Highlighted price-drop alerts
* Can be scheduled with **cron (Linux/macOS)** or **Task Scheduler (Windows)**
* Clean modular codebase for real-world freelance work

---

## **Tech Stack**

* **Python**
  * requests
  * beautifulsoup4
  * pandas
  * smtplib
* **Scheduling**
  * Cron / Windows Task Scheduler

---

## **Project Structure**

```
price-tracker/
│
├── price_history.csv
│
└── src/
    ├── scraper.py      # Scrapes prices from Amazon/Flipkart/Myntra
    ├── tracker.py      # Updates CSV, detects price drops
    ├── emailer.py      # Sends HTML email summary
    ├── utils.py        # Helper functions (hashing URL → product ID)
    ├── config.py       # URLs, email settings, file paths
    └── main.py         # Main orchestrator (scrape → update → email)
```

---

## **Setup Instructions**

### **1. Clone the repository**

```
git clone https://github.com/yourusername/price-tracker.git
cd price-tracker
```

### **2. Install dependencies**

```
pip install -r requirements.txt
```


### **3. Configure product URLs & email credentials**

**Edit **src/config.py**:**

```
PRODUCT_URLS = [
    "https://www.amazon.in/dp/xxxxxxxx",
    "https://www.flipkart.com/p/xxxxxx",
]

EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # Gmail App Password
EMAIL_RECEIVER = "your_email@gmail.com"
```

For Gmail:

Create an App Password:

Account → Security → App Passwords → Generate → Paste in config.

---

## **Run Once (manual test)**

```
python3 src/main.py
```

You should receive an email with today’s prices.

---

## **Scheduling (Automation)**

### **Linux/macOS (cron)**

Edit cron:

```
crontab -e
```

Add job for daily 9 AM run:

```
0 9 * * * /usr/bin/python3 /absolute/path/price-tracker/src/main.py >> /absolute/path/price-tracker/log.txt 2>&1
```

### **Windows (Task Scheduler)**

Use “Create Basic Task” → choose time → run:

```
python.exe C:\path\to\price-tracker\src\main.py
```

---

## **How It Works**

### **Scraper**

* Uses **requests** + BeautifulSoup
* Extracts product title and price
* Supports fallback parsing if DOM changes
* Normalizes prices (₹1,999 → 1999)

### **Tracker**

* Writes daily price to **price_history.csv**
* Reads last known price
* Detects price drops and returns alert list

### **Emailer**

* Generates HTML tables for summary & alerts
* Sends via SMTP with TLS encryption
* Works with Gmail, Outlook, Zoho
