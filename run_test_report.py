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

# Target Group Name (Test Group)
GROUP_NAME = "Testing"

def is_office_holiday(dt=None):
    if dt is None:
        dt = datetime.datetime.now()
    if dt.weekday() == 5:
        day = dt.day
        if 8 <= day <= 14 or 22 <= day <= 28:
            return True, f"2nd/4th Saturday Holiday ({dt.strftime('%d-%m-%Y')})"
    return False, "Working Day"

def generate_table_image():
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

    caption_text = f"Lux - Retailers Onboarded Till now is {total_till_today}"
    return image_path, caption_text

def send_retailer_report():
    is_holiday, holiday_reason = is_office_holiday()
    if is_holiday:
        print(f"🏖️ OFFICE HOLIDAY DETECTED: {holiday_reason}. Skipping send.")
        return

    print("1. Generating live retailer onboarding report image...")
    image_path, caption_text = generate_table_image()

    print("2. Opening WhatsApp Web in Chrome...")
    webbrowser.open("https://web.whatsapp.com")
    time.sleep(7)

    print(f"3. Searching for group '{GROUP_NAME}'...")
    pyautogui.hotkey('ctrl', 'alt', '/')
    time.sleep(1)
    pyperclip.copy(GROUP_NAME)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.5)
    pyautogui.press('enter')
    time.sleep(2.5)

    print("4. Copying report image to Windows Clipboard...")
    ps_cmd = f"Set-Clipboard -Path '{image_path}'"
    subprocess.run(["powershell", "-Command", ps_cmd], check=True)
    time.sleep(1)

    print("5. Pasting table image into chat...")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2.5)

    print(f"6. Pasting caption '{caption_text}'...")
    pyperclip.copy(caption_text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)

    print("7. Sending report 1...")
    pyautogui.press('enter')
    time.sleep(3)

    print("--------------------------------------------------")
    print(f"🎉 SUCCESS! Retailer Report sent to group '{GROUP_NAME}' with caption: '{caption_text}'")
    print("--------------------------------------------------")

if __name__ == "__main__":
    send_retailer_report()
