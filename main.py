#!/usr/bin/env python3
import os
import sys
import yaml
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # CHANGED FROM EDGE TO CHROME
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

# Import from modules folder
from modules.logger import *
from modules.Usernames import GenerateUsername
# Password generation (if you have it in modules)
try:
    from modules.password import GeneratePassword
except:
    # If password module doesn't exist, use simple generation
    import random
    import string
    def GeneratePassword():
        chars = string.ascii_letters + string.digits + "!@#$%"
        password = ''.join(random.choices(chars, k=12))
        return 'Aa1!' + password[4:]  # Ensure it meets requirements

# Load configuration
with open('config.yml', 'r') as file:
    Core = yaml.safe_load(file)

# Override config with environment variables for Railway
if os.getenv('RAILWAY_ENVIRONMENT'):
    Info("🚂 Railway environment detected")
    Core['Headless'] = True  # Force headless on Railway
    
# Environment variable overrides
if os.getenv('ACCOUNTS_TO_CREATE'):
    Core['Accounts_To_Create'] = int(os.getenv('ACCOUNTS_TO_CREATE'))
if os.getenv('USE_NOPECHA'):
    Core['Use_Nopecha'] = os.getenv('USE_NOPECHA').lower() == 'true'
if os.getenv('NOPECHA_KEY'):
    Core['NOPECHA_KEY'] = os.getenv('NOPECHA_KEY')
if os.getenv('RANDOM_PASSWORD'):
    Core['Random_Password'] = os.getenv('RANDOM_PASSWORD').lower() == 'true'
if os.getenv('HAS_COOKIES_PROMPT'):
    Core['Has_Cookies_Prompt'] = os.getenv('HAS_COOKIES_PROMPT').lower() == 'true'
if os.getenv('USE_PROXY'):
    Core['Use_Proxy'] = os.getenv('USE_PROXY').lower() == 'true'
if os.getenv('PROXY'):
    Core['Proxy'] = os.getenv('PROXY')
if os.getenv('HEADLESS'):
    Core['Headless'] = os.getenv('HEADLESS').lower() == 'true'

BrowserClient = None

def SetupDriver():
    """Setup Chrome driver with Railway compatibility"""
    global BrowserClient
    
    # Chrome options - CHANGED FROM EDGE
    chrome_options = Options()
    
    # CRITICAL: Railway/Docker requires these flags
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    
    # Headless mode
    if Core['Headless']:
        chrome_options.add_argument('--headless')
        Info("Running in headless mode")
    
    # Window size
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Anti-detection
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # User agent
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Proxy support
    if Core.get('Use_Proxy') and Core.get('Proxy'):
        chrome_options.add_argument(f'--proxy-server={Core["Proxy"]}')
        Info(f"Using proxy: {Core['Proxy']}")
    
    # Nopecha extension support
    if Core.get('Use_Nopecha'):
        Info("Nopecha CAPTCHA solver enabled")
        if os.path.exists('extra/nopecha'):
            chrome_options.add_argument(f'--load-extension=extra/nopecha')
    
    try:
        # CHANGED FROM EDGE TO CHROME
        BrowserClient = webdriver.Chrome(options=chrome_options)
        Success("✅ Chrome driver initialized successfully")
        return BrowserClient
    except Exception as e:
        Error(f"Failed to initialize Chrome driver: {e}")
        sys.exit(1)

def CheckDriver(driver):
    """Check if driver is still alive, restart if needed"""
    try:
        driver.current_url
        return driver
    except:
        Warning("Driver closed, restarting...")
        return SetupDriver()

def GenerateAccount():
    """Generate a single Roblox account"""
    global BrowserClient
    
    try:
        # Generate credentials
        username = GenerateUsername()
        
        if Core.get('Random_Password', True):
            password = GeneratePassword()
        else:
            password = Core.get('Fixed_Password', 'TestPass123!')
        
        Info(f"🔄 Creating account: {username}")
        
        # Navigate to Roblox
        BrowserClient.get("https://www.roblox.com/")
        time.sleep(3)
        
        # Handle cookie consent (EU)
        if Core.get('Has_Cookies_Prompt', False):
            try:
                cookie_btn = WebDriverWait(BrowserClient, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'OK')]"))
                )
                cookie_btn.click()
                time.sleep(1)
            except:
                pass
        
        # Fill birthday
        wait = WebDriverWait(BrowserClient, 10)
        
        # Month
        import random
        month_dropdown = wait.until(EC.presence_of_element_located((By.ID, "MonthDropdown")))
        month_dropdown.click()
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month = random.choice(months)
        month_option = BrowserClient.find_element(By.XPATH, f"//select[@id='MonthDropdown']/option[@value='{month}']")
        month_option.click()
        
        # Day
        day_dropdown = BrowserClient.find_element(By.ID, "DayDropdown")
        day_dropdown.click()
        day = random.randint(1, 28)
        day_option = BrowserClient.find_element(By.XPATH, f"//select[@id='DayDropdown']/option[@value='{day}']")
        day_option.click()
        
        # Year (18+ account)
        year = random.randint(1990, 2005)
        year_dropdown = BrowserClient.find_element(By.ID, "YearDropdown")
        year_dropdown.click()
        year_option = BrowserClient.find_element(By.XPATH, f"//select[@id='YearDropdown']/option[@value='{year}']")
        year_option.click()
        
        time.sleep(2)
        
        # Fill username
        username_input = BrowserClient.find_element(By.ID, "signup-username")
        username_input.clear()
        username_input.send_keys(username)
        time.sleep(1)
        
        # Fill password
        password_input = BrowserClient.find_element(By.ID, "signup-password")
        password_input.clear()
        password_input.send_keys(password)
        time.sleep(1)
        
        # Click signup
        signup_btn = BrowserClient.find_element(By.ID, "signup-button")
        signup_btn.click()
        
        Info("⏳ Waiting for CAPTCHA/verification...")
        
        # Wait for CAPTCHA or completion
        timeout = Core.get('Capture_Timeout_Minutes', 5) * 60
        time.sleep(timeout)
        
        # Check if successful
        current_url = BrowserClient.current_url.lower()
        if "home" in current_url or "games" in current_url:
            Success(f"✅ Account created: {username}")
            
            # Save credentials
            accounts_file = Core.get('Accounts_File', 'accounts.txt')
            with open(accounts_file, 'a') as f:
                f.write(f"{username}:{password}\n")
            Info(f"💾 Saved to {accounts_file}")
            
            # Save cookies if needed
            cookies_file = Core.get('Cookies_File')
            if cookies_file:
                try:
                    cookies = BrowserClient.get_cookies()
                    with open(cookies_file, 'a') as f:
                        f.write(f"{username}:{cookies}\n")
                except:
                    pass
            
            return True
        else:
            Warning(f"⚠️ Account creation may have failed: {username}")
            Warning(f"Current URL: {BrowserClient.current_url}")
            return False
            
    except Exception as e:
        Error(f"Error creating account: {e}")
        import traceback
        traceback.print_exc()
        
        # Try to save screenshot for debugging
        try:
            BrowserClient.save_screenshot('error.png')
            Info("📸 Error screenshot saved")
        except:
            pass
        
        return False

def Generation():
    """Main generation loop"""
    global BrowserClient
    
    # Setup driver
    BrowserClient = SetupDriver()
    
    Create_Count = Core.get("Accounts_To_Create", 1)
    Info(f"📊 Will create {Create_Count} account(s)")
    
    created = 0
    # Creation loop
    for i in range(1, Create_Count + 1):
        Info(f"\n{'='*50}")
        Info(f"Account {i}/{Create_Count}")
        Info('='*50)
        
        try:
            BrowserClient = CheckDriver(BrowserClient)
            if GenerateAccount():
                created += 1
        except WebDriverException:
            Info("Window closed! Now exiting...")
            break
        except Exception as e:
            BrowserClient = None
            Error(str(e))
        
        # Delay between accounts
        if i < Create_Count:
            time.sleep(5)
    
    Success(f"✨ Job finished! Created {created}/{Create_Count} accounts")
    
    if BrowserClient:
        BrowserClient.quit()

if __name__ == "__main__":
    Banner()
    
    try:
        Generation()
    except KeyboardInterrupt:
        Info("\n⚠️ Interrupted by user")
        sys.exit(0)
    except Exception as e:
        Error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Don't wait for input on Railway
    if not os.getenv('RAILWAY_ENVIRONMENT'):
        print("\nPress enter to exit...")
        input()
