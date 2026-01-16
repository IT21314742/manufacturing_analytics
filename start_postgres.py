# Desktop/start_postgres.py - SIMPLE VERSION
import os
import sys

print("=" * 50)
print("POSTGRESQL STARTUP TOOL")
print("=" * 50)

# Method 1: Try to start via services command
print("\n1️⃣  Trying to start PostgreSQL...")
os.system('net start postgresql-x64-18')

# Wait a moment
import time
time.sleep(3)

# Method 2: Check if it's running
print("\n2️⃣  Checking if PostgreSQL is running...")
result = os.system('netstat -an | find "5432"')

if result == 0:
    print("✅ SUCCESS! PostgreSQL is running on port 5432")
    print("\n📊 You can now:")
    print("1. Open Tableau/Power BI")
    print("2. Connect to PostgreSQL")
    print("3. Build your dashboard")
else:
    print("❌ PostgreSQL is NOT running")
    print("\n🔧 Try this instead:")
    print("1. Press WIN + R")
    print("2. Type: services.msc")
    print("3. Find 'postgresql-x64-18'")
    print("4. Right-click → Start")

print("\n" + "=" * 50)
input("Press Enter to close...")