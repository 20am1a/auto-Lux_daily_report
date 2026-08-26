import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# Import functions from both report scripts
from run_test_report import send_retailer_report
from run_tatatele_report import send_tatatele_report

def main():
    print("==================================================")
    print("🚀 Running BOTH Lux Daily Reports (Testing Group)...")
    print("==================================================")

    print("\n--- [1/2] Sending Retailers Onboarded Report ---")
    send_retailer_report()

    print("\n--- [2/2] Sending Tata Tele Inbound Call Report ---")
    send_tatatele_report()

    print("\n==================================================")
    print("🎉 SUCCESS! BOTH reports sent to group 'Testing'!")
    print("==================================================")

if __name__ == "__main__":
    main()
