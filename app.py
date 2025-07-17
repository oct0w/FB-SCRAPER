import os
import json
import time
import random
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class FbScraperGUI:
    def __init__(self, root):
        self.root = root
        root.title("Facebook Group Members Scraper")
        root.geometry("700x500")

        tk.Label(root, text="Facebook Group Members URL:").pack(anchor="w", padx=10, pady=(10, 0))
        self.url_entry = tk.Entry(root, width=90)
        self.url_entry.pack(padx=10)

        tk.Label(root, text="Number of scrolls:").pack(anchor="w", padx=10, pady=(10, 0))
        self.scrolls_entry = tk.Entry(root, width=10)
        self.scrolls_entry.pack(padx=10)
        self.scrolls_entry.insert(0, "15")

        self.start_btn = tk.Button(root, text="Start Scraping", command=self.start_scraping)
        self.start_btn.pack(pady=10)

        self.status_label = tk.Label(root, text="Status: Idle")
        self.status_label.pack()
        self.timer_label = tk.Label(root, text="Elapsed time: 0s | Members scraped: 0")
        self.timer_label.pack()

        self.log_area = scrolledtext.ScrolledText(root, width=80, height=20, state='disabled')
        self.log_area.pack(padx=10, pady=10)

        self.members_count = 0
        self.start_time = None
        self.scraping_thread = None
        self.running = False

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def update_timer(self):
        if not self.running:
            return
        elapsed = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Elapsed time: {elapsed}s | Members scraped: {self.members_count}")
        self.root.after(1000, self.update_timer)

    def start_scraping(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Input Error", "Please enter a valid Facebook group members URL.")
            return
        try:
            scrolls = int(self.scrolls_entry.get())
            if scrolls < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Number of scrolls must be a positive integer.")
            return

        self.start_btn.config(state='disabled')
        self.log_area.config(state='normal')
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state='disabled')

        self.members_count = 0
        self.start_time = time.time()
        self.running = True
        self.status_label.config(text="Status: Running...")

        self.scraping_thread = threading.Thread(target=self.scrape_members, args=(url, scrolls))
        self.scraping_thread.start()
        self.update_timer()

    def scrape_members(self, group_url, scrolls):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        chrome_options.add_argument(
            "--user-data-dir=C:/Users/Asus/AppData/Local/Google/Chrome/SeleniumProfile"
        )

        service = Service("D:/Download/chromedriver-win64/chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=chrome_options)

        members = []
        seen_urls = set()

        try:
            driver.get(group_url)
            self.log("[✓] Opened group members page. Waiting for page load...")
            time.sleep(random.uniform(5, 8))

            for i in range(scrolls):
                if not self.running:
                    break
                self.log(f"[*] Scrolling {i+1}/{scrolls}...")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                wait_time = random.uniform(1, 4)
                self.log(f"[*] Waiting {wait_time:.1f} seconds before scraping members")
                time.sleep(wait_time)

                try:
                    elements = driver.find_elements(By.XPATH, "//a[@role='link' and contains(@href, '/user/')]")
                    new_found = 0
                    for el in elements:
                        name = el.text.strip()
                        href = el.get_attribute("href")
                        if name and href and href not in seen_urls:
                            members.append({"name": name, "profile_url": href})
                            seen_urls.add(href)
                            new_found += 1
                            self.members_count += 1
                            self.log(f"[+] Found member: {name} — {href}")

                    self.log(f"[*] Found {new_found} new members on this scroll.")
                except Exception as e:
                    self.log(f"[!] Error while extracting members: {e}")

            # Save results
            with open("members.json", "w", encoding="utf-8") as f:
                json.dump(members, f, ensure_ascii=False, indent=2)

            self.log(f"\n✅ Scraping complete. Total members found: {len(members)}")
            self.log(f"✅ Saved to members.json")

        except Exception as e:
            self.log(f"[!] Unexpected error: {e}")

        finally:
            driver.quit()
            self.running = False
            self.start_btn.config(state='normal')
            self.status_label.config(text="Status: Idle")
            self.log("[✓] Browser closed.")

def main():
    root = tk.Tk()
    app = FbScraperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
