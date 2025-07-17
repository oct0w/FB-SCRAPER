# 📘 Facebook Group Members Scraper GUI

A user-friendly Python GUI app for scraping member names and profile URLs from Facebook group pages. Built using `tkinter` for the interface and `selenium` for automated browsing, this tool is ideal for data collection in research, community analysis, or outreach tasks.

> ⚠️ **Note**: Scraping Facebook data may violate their terms of service. Use responsibly and ensure compliance with local laws and platform policies.

---

## 🚀 Features

- GUI-based URL input and scrape configuration
- Real-time member discovery logs
- Timer and scrape progress tracker
- Export scraped member data as `members.json`
- Handles dynamic scrolling and random delays to mimic natural interaction

---

## 🛠 Requirements

- Python 3.8+
- Google Chrome installed
- ChromeDriver (matching your Chrome version)
- Pre-configured Selenium Chrome profile for Facebook login

### 📦 Usage

Update the ChromeDriver path and user profile directory in the script:

- chrome_options.add_argument("--user-data-dir=...")  # Your Chrome user profile path
- service = Service(".../chromedriver.exe")           # Your ChromeDriver path
- run app.py

 ### 🔒 Before You Start
To ensure the scraper launches correctly with your Selenium Chrome profile:

- Close all running Chrome tabs and windows using the specified profile.

- Make sure Chrome isn’t running in the background (check Task Manager).

- Ensure your profile path and ChromeDriver are correctly set in the code.

Failure to close Chrome beforehand may lead to unexpected behavior or browser launch errors
