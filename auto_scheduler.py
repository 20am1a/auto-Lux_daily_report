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

sys.stdout.reconfigure(encoding='utf-8')

# Configuration
SEND_TIME = "18:30"  # 6:30 PM Daily
GROUP_NAME = "Simpel.AI_DA_Group"
CAPTION_TEXT = "Lux - Retailers Onboarded"

# Tracks last date sent to prevent duplicate sends
last_sent_date = None

def is_office_holiday(dt=None):
    """
    Checks if today is a 2nd or 4th Saturday Office Holiday.
    - 2nd Saturday: Days 8 to 14 of the month
    - 4th Saturday: Days 22 to 28 of the month
    """
    if dt is None:
        dt = datetime.datetime.now()
    
    # Weekday 5 = Saturday
    if dt.weekday() == 5:
        day = dt.day
        if 8 <= day <= 14:
            return True, f"2nd Saturday Holiday ({dt.strftime('%d-%m-%Y')})"
        elif 22 <= day <= 28:
            return True, f"4th Saturday Holiday ({dt.strftime('%d-%m-%Y')})"
            
    return False, "Working Day"

def generate_table_image():
    conn = pymysql.connect(
        host="64.227.149.129",
        user="DAuser",
        password="DA@SMPL2026",
        database="WMSLiveDB"
    )

    with conn.cursor() as cursor:
        # Total Till Today
        cursor.execute("SELECT COUNT(*) FROM business_users WHERE first_login_on <= NOW() AND business_type_id = 4;")
        total_till_today = cursor.fetchone()[0]

        # Current Week Breakdown (Monday to Today) with DAYNAME
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

    cell_text = []
    cell_colors = []

    cell_text.append(["Onboarded Retailers Till Today", str(total_till_today)])
    cell_colors.append(["#D9EAD3", "#D9EAD3"])

    cell_text.append(["Login_date (Day)", "Download_count"])
    cell_colors.append(["#E69138", "#E69138"])

    week_total = 0
    for date_str, day_name, count in daily_rows:
        date_with_day = f"{date_str} ({day_name})"
        cell_text.append([date_with_day, str(count)])
        cell_colors.append(["#FFFFFF", "#FFFFFF"])
        week_total += count

    cell_text.append(["This Week Total", str(week_total)])
    cell_colors.append(["#FFFF00", "#FFFF00"])

    fig, ax = plt.subplots(figsize=(6.5, 0.45 * len(cell_text)), dpi=300)
    ax.axis('off')

    table = ax.table(
        cellText=cell_text,
        cellColours=cell_colors,
        cellLoc='center',
        colWidths=[0.65, 0.35],
        loc='center'
    )

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

    return image_path

def send_report_now():
    global last_sent_date
    today_str = datetime.date.today().strftime("%Y-%m-%d")

    # Holiday check
    is_holiday, reason = is_office_holiday()
    if is_holiday:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🏖️ Holiday Detected: {reason}. Skipping send.")
        last_sent_date = today_str
        return

    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🚀 Running daily report automation...")
    image_path = generate_table_image()

    webbrowser.open("https://web.whatsapp.com")
    time.sleep(7)

    pyautogui.hotkey('ctrl', 'alt', '/')
    time.sleep(1)
    pyperclip.copy(GROUP_NAME)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.5)
    pyautogui.press('enter')
    time.sleep(2.5)

    ps_cmd = f"Set-Clipboard -Path '{image_path}'"
    subprocess.run(["powershell", "-Command", ps_cmd], check=True)
    time.sleep(1)

    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2.5)

    pyperclip.copy(CAPTION_TEXT)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)

    pyautogui.press('enter')
    time.sleep(2)

    last_sent_date = today_str
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🎉 SUCCESS! Daily report sent to '{GROUP_NAME}'.")

def start_scheduler():
    global last_sent_date
    print("==================================================")
    print("🤖 Auto Lux Daily Report Scheduler Started")
    print(f"⏰ Scheduled Time: {SEND_TIME} daily")
    print(f"👥 Target Group: {GROUP_NAME}")
    print("==================================================")

    while True:
        now = datetime.datetime.now()
        today_str = now.date().strftime("%Y-%m-%d")

        target_hour, target_min = map(int, SEND_TIME.split(":"))
        target_datetime = now.replace(hour=target_hour, minute=target_min, second=0, microsecond=0)

        # Send if target time reached OR if missed today's send because laptop was turned off earlier
        if last_sent_date != today_str:
            if now >= target_datetime:
                send_report_now()

        time.sleep(30) # Check every 30 seconds

if __name__ == "__main__":
    start_scheduler()
