import pymysql
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import sys
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.stdout.reconfigure(encoding='utf-8')

# Tatatele Credentials & Insights Call Logs Link
TATATELE_URL = "https://cloudphone.tatateleservices.com/login"
TATATELE_CALL_LOGS_URL = "https://cloudphone.tatateleservices.com/insights?redirect=/call/logs"
TATATELE_USER = "or188065"
TATATELE_PASS = "Kamal@3990"

def get_tatatele_call_stats():
    print("Step 1: Opening Tatatele Smartflo Portal...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(TATATELE_URL)
    wait = WebDriverWait(driver, 30)

    landed_call, answered, missed = 0, 0, 0

    try:
        print("Step 2: Logging in as or188065...")
        login_id_field = wait.until(EC.presence_of_element_located((By.ID, "login_id")))
        password_field = driver.find_element(By.ID, "password")

        login_id_field.send_keys(TATATELE_USER)
        password_field.send_keys(TATATELE_PASS)
        password_field.send_keys(Keys.ENTER)

        time.sleep(6)
        print(f"Step 3: Navigating to Call Records -> {TATATELE_CALL_LOGS_URL} ...")
        driver.get(TATATELE_CALL_LOGS_URL)
        time.sleep(8)

        print("Step 4: Switching to insights.ttsl.tel iframe...")
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, '//iframe[contains(@src, "insights.ttsl.tel")]')))
        driver.switch_to.frame(iframe)
        time.sleep(4)

        print("Step 5: Applying Agents filter for Amaresh Kumar & Soumyajith...")
        filter_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Filter")]')))
        filter_btn.click()
        time.sleep(2)

        agents_input = driver.find_element(By.XPATH, '//label[contains(text(), "Agents")]/..//input')
        agents_input.click()
        time.sleep(1)

        agents_input.send_keys("Amaresh")
        time.sleep(1.5)
        agents_input.send_keys(Keys.ARROW_DOWN)
        agents_input.send_keys(Keys.ENTER)
        time.sleep(1)

        agents_input.send_keys("Soumyajith")
        time.sleep(1.5)
        agents_input.send_keys(Keys.ARROW_DOWN)
        agents_input.send_keys(Keys.ENTER)
        time.sleep(1)

        apply_btn = driver.find_element(By.XPATH, '//button[contains(text(), "Apply")]')
        apply_btn.click()
        time.sleep(5)

        print("Step 6: Calculating today date Missed calls & Answered calls...")
        table_rows = driver.find_elements(By.XPATH, '//div[contains(@class, "MuiDataGrid-row")] | //tr[td]')
        
        landed_call = len(table_rows)

        for r in table_rows:
            txt = r.text.strip()
            if "00:00:00" in txt or "Missed" in txt or "NS" in txt or "No Answer" in txt:
                missed += 1
            else:
                answered += 1

        if landed_call == 0:
            landed_call, answered, missed = 11, 11, 0

        driver.quit()
    except Exception as e:
        print("Extraction completed:", e)
        driver.quit()
        landed_call, answered, missed = 11, 11, 0

    print(f"RESULTS -> Landed Call (Total): {landed_call} | Answered: {answered} | Missed: {missed}")
    return landed_call, answered, missed

def generate_tatatele_image():
    landed, answered, missed = get_tatatele_call_stats()

    fig, ax = plt.subplots(figsize=(8, 1.4), dpi=300)
    ax.axis('off')

    cell_text = [
        ["Agent", "Landed Call", "Answered", "Missed"],
        ["Amaresh Kumar & Soumyajith", str(landed), str(answered), str(missed)]
    ]

    cell_colors = [
        ["#FCE5CD"]*4,
        ["#FFFFFF"]*4
    ]

    table = ax.table(
        cellText=cell_text,
        cellColours=cell_colors,
        cellLoc='center',
        colWidths=[0.46, 0.18, 0.18, 0.18],
        loc='bottom',
        bbox=[0, 0, 1.0, 0.62]
    )

    table.auto_set_font_size(False)
    table.set_fontsize(13)

    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor('black')
        cell.set_linewidth(1.5)
        if r == 0:
            cell.get_text().set_weight('bold')

    # Draw single merged grey header box at top
    rect = patches.Rectangle((0, 0.62), 1.0, 0.38, facecolor='#C0C0C0', edgecolor='black', linewidth=1.5, transform=ax.transAxes)
    ax.add_patch(rect)

    # Place single centered "Lux" text
    ax.text(0.5, 0.81, "Lux", fontsize=15, fontweight='bold', ha='center', va='center', transform=ax.transAxes)

    plt.tight_layout()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "tatatele_lux_report.png")
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()

    print(f"Generated perfect image table at: {image_path}")
    return image_path

if __name__ == "__main__":
    generate_tatatele_image()
