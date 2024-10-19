import time
import os
import pytesseract
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the save path
SAVE_PATH = r"C:\Users\kunde\Downloads\Web scraping"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
path_of_chromedriver = "C:/Users/kunde/Downloads/Web scraping/selinium/chromedriver.exe"

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    s = Service(path_of_chromedriver)
    driver = webdriver.Chrome(service=s, options=options)
    return driver

def capture_captcha_section(driver):
    # Wait for captcha to be present and visible
    captcha_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="captcha"]'))
    )
    
    # Scroll element into view with offset
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", captcha_element)
    time.sleep(2)  # Increased wait time after scroll
    
    # Get the device pixel ratio
    pixel_ratio = driver.execute_script("return window.devicePixelRatio;")
    
    # Get element location and size
    location = captcha_element.location_once_scrolled_into_view
    size = captcha_element.size
    
    # Define file paths with new save location
    full_screenshot_path = os.path.join(SAVE_PATH, "full_screenshot.png")
    captcha_path = os.path.join(SAVE_PATH, "captcha_image.png")
    
    # Take screenshot
    driver.save_screenshot(full_screenshot_path)
    
    # Calculate coordinates with pixel ratio adjustment and small padding
    padding = 5  # Add padding to ensure we capture the full captcha
    left = int(location['x'] * pixel_ratio) - padding
    top = int(location['y'] * pixel_ratio) - padding
    right = int((location['x'] + size['width']) * pixel_ratio) + padding
    bottom = int((location['y'] + size['height']) * pixel_ratio) + padding
    
    # Crop and save captcha
    image = Image.open(full_screenshot_path)
    captcha_image = image.crop((left, top, right, bottom))
    
    # Resize if needed
    if captcha_image.size[0] < 100:
        new_width = 200
        ratio = new_width / captcha_image.size[0]
        new_height = int(captcha_image.size[1] * ratio)
        captcha_image = captcha_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    captcha_image.save(captcha_path)
    return captcha_image

def solve_captcha():
    captcha_path = os.path.join(SAVE_PATH, "captcha_image.png")
    image = Image.open(captcha_path)
    image = image.convert('L')  # Convert to grayscale
    captcha_text = pytesseract.image_to_string(image, config='--psm 7 --oem 3')
    captcha_text = ''.join(filter(str.isalnum, captcha_text))[:6]
    print("Extracted CAPTCHA text:", captcha_text)
    return captcha_text

def handle_captcha_submission(driver):
    max_attempts = 3
    attempt = 0
    
    while attempt < max_attempts:
        try:
            print(f"\nAttempt {attempt + 1} of {max_attempts}")
            
            # Capture and solve captcha
            captcha_image = capture_captcha_section(driver)
            captcha_text = solve_captcha()
            
            # Clear existing captcha input if any
            captcha_input = driver.find_element(By.XPATH, '//*[@id="txt_Captcha"]')
            captcha_input.clear()
            
            # Enter new captcha text
            captcha_input.send_keys(captcha_text)
            
            # Click submit button
            submit_button = driver.find_element(By.XPATH, "//button[text()='View IEC']")
            submit_button.click()
            
            # Wait for page load
            time.sleep(5)
            
            # Check if new window opened
            if len(driver.window_handles) > 1:
                print("New window detected - Captcha successful!")
                return True
            
            # Check if page content changed significantly
            if "View IEC Details" not in driver.page_source:
                print("Page content changed - Captcha successful!")
                return True
                
        except Exception as e:
            print(f"Attempt {attempt + 1} error: {str(e)}")
        
        attempt += 1
        time.sleep(1)
    
    # After maximum attempts, try to extract text regardless of CAPTCHA success
    print("\nCAPTCHA submission failed after multiple attempts, extracting text from the current page...")
    if extract_and_save_text(driver):
        print("Data extracted and saved successfully despite CAPTCHA failure.")
    else:
        print("Failed to extract or save data after CAPTCHA failure.")
    
    return False  # Return false indicating CAPTCHA was not solved successfully


def extract_and_save_text(driver):
    try:
        # Switch to new window if one exists
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
        
        # Wait for the content to load
        time.sleep(3)
        
        extracted_text = []
        
        # Try multiple methods to get text
        try:
            # Try getting text from tables first
            tables = driver.find_elements(By.TAG_NAME, "table")
            for table in tables:
                text = table.text.strip()
                if text:
                    extracted_text.append(text)
        except:
            pass

        try:
            # Try getting text from specific div elements
            content_divs = driver.find_elements(By.CSS_SELECTOR, "div.content, div.details, div.main-content")
            for div in content_divs:
                text = div.text.strip()
                if text:
                    extracted_text.append(text)
        except:
            pass
        
        # If no text found from specific elements, get all body text
        if not extracted_text:
            body_text = driver.find_element(By.TAG_NAME, 'body').text
            extracted_text.append(body_text)
        
        # Combine all text
        full_text = "\n\n".join(extracted_text)
        
        # Save to file with fixed name
        filepath = os.path.join(SAVE_PATH, "iec2.txt")
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        print(f"Data saved successfully to: {filepath}")
        return True
        
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        return False

try:
    driver = create_driver()
    
    # Visit website
    driver.get("https://dgft.gov.in/CP/?opt=view-any-ice")
    
    # Click view any IEC
    view_any_iec_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[9]/div[3]/div/div[2]/div[1]/div/a"))
    )
    view_any_iec_button.click()
    time.sleep(2)
    
    # Enter data
    iec_code = "2194000127"
    name = "tata"
    driver.find_element(By.XPATH, '//*[@id="iecNo"]').send_keys(iec_code)
    driver.find_element(By.XPATH, '//*[@id="entity"]').send_keys(name)
    
    # Handle captcha and extract data
    success = handle_captcha_submission(driver)
    
    if success:
        print("\nCaptcha submitted successfully! Extracting data...")
        if extract_and_save_text(driver):
            print("Process completed successfully!")
        else:
            print("Failed to extract or save data.")
    else:
        print("\nFailed to submit captcha after multiple attempts")
    
    time.sleep(5)

except Exception as e:
    print(f"\nAn error occurred: {str(e)}")
finally:
    driver.quit()