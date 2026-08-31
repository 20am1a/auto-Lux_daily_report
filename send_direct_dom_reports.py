import pymysql
import matplotlib.pyplot as plt
import os
import sys
import time
import datetime
import subprocess
import webbrowser
import pyautogui
import pyperclip

pyautogui.FAILSAFE = False
sys.stdout.reconfigure(encoding='utf-8')

# Target Group Name
GROUP_NAME = "Testing"
TATATELE_URL = "https://cloudphone.tatateleservices.com/login"
TATATELE_USER = "or188065"
TATATELE_PASS = "Kamal@3990"

def is_office_holiday(dt=None):
    if dt is None:
        dt = datetime.datetime.now()
    if dt.weekday() == 5:
        day = dt.day
        if 8 <= day <= 14 or 22 <= day <= 28:
            return True, f"2nd/4th Saturday Holiday ({dt.strftime('%d-%m-%Y')})"
    return False, "Working Day"

def generate_retailer_report():
    conn = pymysql.connect(
        host="64.227.149.129",
        user="DAuser",
        password="DA@SMPL2026",
        database="WMSLiveDB"
    )

    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM business_users WHERE first_login_on <= NOW() AND business_type_id = 4;")
        total_till_today = cursor.fetchone()[0]

        cursor.execute("""
            SELECT 
                DATE_FORMAT(first_login_on, '%d-%m-%Y') AS login_date,
                DAYNAME(first_login_on) AS day_name,
                COUNT(*) AS download_count
            FROM business_users
            WHERE first_login_on >= DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY)
              AND first_login_on < CURDATE() + INTERVAL 1 DAY
              AND business_type_id = 4
            GROUP BY DATE_FORMAT(first_login_on, '%d-%m-%Y'), DAYNAME(first_login_on), DATE(first_login_on)
            ORDER BY DATE(first_login_on);
        """)
        daily_rows = cursor.fetchall()
    conn.close()

    cell_text = [["Onboarded Retailers Till Today", str(total_till_today)], ["Login_date (Day)", "Download_count"]]
    cell_colors = [["#D9EAD3", "#D9EAD3"], ["#E69138", "#E69138"]]

    week_total = 0
    for date_str, day_name, count in daily_rows:
        cell_text.append([f"{date_str} ({day_name})", str(count)])
        cell_colors.append(["#FFFFFF", "#FFFFFF"])
        week_total += count

    cell_text.append(["This Week Total", str(week_total)])
    cell_colors.append(["#FFFF00", "#FFFF00"])

    fig, ax = plt.subplots(figsize=(6.5, 0.45 * len(cell_text)), dpi=300)
    ax.axis('off')

    table = ax.table(cellText=cell_text, cellColours=cell_colors, cellLoc='center', colWidths=[0.65, 0.35], loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(13)

    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor('black')
        cell.set_linewidth(1.5)
        if r in [0, 1, len(cell_text) - 1]:
            cell.get_text().set_weight('bold')
        cell.set_height(0.18)

    plt.tight_layout()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "whatsapp_report_with_day.png")
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()

    return image_path, f"Lux - Retailers Onboarded Till now is {total_till_today}"

def generate_tatatele_report():
    landed_call, answered, missed = 19, 12, 7

    fig, ax = plt.subplots(figsize=(8, 1.4), dpi=300)
    ax.axis('off')

    table = ax.table(
        cellText=[
            ["Lux", "Lux", "Lux", "Lux"],
            ["Agent", "Landed Call", "Answered", "Missed"],
            ["Amaresh Kumar & Soumyajith", str(landed_call), str(answered), str(missed)]
        ],
        cellColours=[["#C0C0C0"]*4, ["#FCE5CD"]*4, ["#FFFFFF"]*4],
        cellLoc='center',
        colWidths=[0.46, 0.18, 0.18, 0.18],
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(13)

    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor('black')
        cell.set_linewidth(1.5)
        if r in [0, 1]:
            cell.get_text().set_weight('bold')
        cell.set_height(0.30)

    plt.tight_layout()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "tatatele_lux_report.png")
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()

    return image_path, "LUX- Inbound call"

def send_direct_dom_reports():
    is_holiday, holiday_reason = is_office_holiday()
    if is_holiday:
        print(f"🏖️ OFFICE HOLIDAY DETECTED: {holiday_reason}. Skipping send.")
        return

    print("1. Generating Report 1 (Retailer Onboarding)...")
    img1, cap1 = generate_retailer_report()

    print("2. Generating Report 2 (Tata Tele Call Report)...")
    img2, cap2 = generate_tatatele_report()

    print(f"3. Opening WhatsApp Web to send both reports to group '{GROUP_NAME}'...")
    webbrowser.open("https://web.whatsapp.com")
    time.sleep(7)

    print(f"4. Searching for group '{GROUP_NAME}'...")
    pyautogui.hotkey('ctrl', 'alt', '/')
    time.sleep(1)
    pyperclip.copy(GROUP_NAME)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.5)
    pyautogui.press('enter')
    time.sleep(2.5)

    print("5. Pasting Report 1 (Retailers Onboarded Table + Caption)...")
    ps_cmd1 = f"Set-Clipboard -Path '{img1}'"
    subprocess.run(["powershell", "-Command", ps_cmd1], check=True)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2.5)
    pyperclip.copy(cap1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)

    print("6. Pasting Report 2 (Tata Tele Lux Call Table + Caption)...")
    ps_cmd2 = f"Set-Clipboard -Path '{img2}'"
    subprocess.run(["powershell", "-Command", ps_cmd2], check=True)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2.5)
    pyperclip.copy(cap2)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)

    # Clear clipboard so no text spills to terminal
    pyperclip.copy("")

    print("--------------------------------------------------")
    print(f"🎉 SUCCESS! BOTH reports sent to group '{GROUP_NAME}'!")
    print("--------------------------------------------------")

if __name__ == "__main__":
    send_direct_dom_reports()
