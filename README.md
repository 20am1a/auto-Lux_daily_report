# Auto Lux Daily Report

Automated daily WhatsApp report system that connects to MySQL database (`WMSLiveDB`), calculates live onboarding statistics for the current week (Monday to Sunday), generates a high-resolution styled table image, and sends it to WhatsApp.

---

## 📁 Files Included

- **`run_report.py`**: Production script configured for group `Simpel.AI_DA_Group`.
- **`run_test_report.py`**: Test script configured for group `Testing`.
- **`run_daily_report.bat`**: Double-click batch file to run `run_report.py` instantly.
- **`whatsapp_report_with_day.png`**: Auto-generated report image.

---

## 🚀 How to Run Manually

### Option A: Double Click `run_daily_report.bat`
Simply double-click `run_daily_report.bat` in this folder!

### Option B: Command Prompt
Open Command Prompt (`cmd`) and run:
```cmd
python "C:\Users\chandu\Desktop\auto-Lux_daily_report\run_report.py"
```

---

## ⏰ How to Automate Daily at 6:30 PM (100% Free)

1. Press `Win + R`, type **`taskschd.msc`**, and press Enter (**Task Scheduler**).
2. Click **Create Basic Task** on the right.
3. Name: `Auto Lux Daily Report`.
4. Trigger: **Daily** at **6:30 PM**.
5. Action: **Start a program**
   - Program/script: `python`
   - Add arguments: `"C:\Users\chandu\Desktop\auto-Lux_daily_report\run_report.py"`
6. Click **Finish**.

---

## 📊 Database Logic (MySQL)
- **Monday Reset**: `DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY)` dynamically finds Monday of the current week.
- **Week Progress**: Shows Monday through today, auto-accumulating counts.
- **Auto-Reset**: On Monday, it automatically resets to start fresh for the new week!
