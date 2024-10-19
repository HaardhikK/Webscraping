# Webscraping applications with Captcha
## Frameworks used: Selenium, Pytesseract OCR , NLP , Python.
Project 1: Specifically designed to bypass the CAPTCHA challenge, using Selenium the script navigates to the target webpage, captures the CAPTCHA image, and employs the pytesseract module for Optical Character Recognition (OCR) to extract the text from the image. After multiple attempts to solve the CAPTCHA, it attempts to extract relevant data from the page regardless of the CAPTCHA success, ensuring that valuable information is obtained even if the CAPTCHA is not bypassed. The overall approach showcases the integration of web scraping techniques with OCR to automate data retrieval from web applications that implement CAPTCHA security measures.

Project 2:
Scraped 155 websites in single go.
Displaying the URL of each website.
Skipping URLs that are not currently active (approximately 5 links are inactive).
Displaying the heading of each webpage.
Formatting and displaying subheadings appropriately.
Removing blank subheadings.
Displaying the text content of the website.
Summarizing the text using natural language processing (NLP) and cleaning by removing stopwords.
Retrieving and storing only safe links (starting from "https://") after cleaning any void links.
Storing image URLs.
