import time
import pandas as pd
import nltk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Path to the ChromeDriver executable
path_of_chromedriver = "C:/Users/kunde/Downloads/Web scraping/selinium/chromedriver.exe"

# Initialize the Chrome WebDriver
s = Service(path_of_chromedriver)
driver = webdriver.Chrome(service=s)

# List of website URLs with their categories
websites = {
    "AI in Packaging Market": [
        "https://www.monolithai.com/blog/4-ways-ai-is-changing-the-packaging-industry",
        "https://mitsubishisolutions.com/the-role-of-artificial-intelligence-in-smart-packaging-lines/",
        "https://thedatascientist.com/how-artificial-intelligence-is-revolutionizing-the-packaging-industry/",
        "https://packagingeurope.com/comment/ai-and-the-future-of-packaging/9665.article",
        "https://www.sttark.com/blog/ai-powered-custom-packaging-a-creative-revolution",
        "https://dragonflyai.co/resources/blog/how-ai-and-iot-are-transforming-packaging-design",
        "https://sustainability-in-packaging.com/sustainability-in-packaging-europe/ai-and-sustainable-packaging",
        "https://becominghuman.ai/the-role-of-artificial-intelligence-in-the-packaging-industry-c08b58b2f475",
        "https://www.industrialpackaging.com/blog/ai-packaging-is-artificial-intelligence-the-future-of-packaging-design",
        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10418964/",
        "https://www.designerpeople.com/blog/ai-packaging-design/",
        "https://www.aiccbox.org/news/662305/Revolutionizing-the-Packaging-Industry-Through-AI-and-Innovation.htm",
        "https://www.springfieldsolutions.co.uk/insights/blog/ai-packaging",
        "https://interbrandspackaging.com/en/2023/05/26/artificial-intelligence-in-sustainable-packaging/",
        "https://www.whatpackaging.co.in/features/ai-in-packaging-industry-to-hit-usd-537528-mn-by-2032-57671",
        "https://www.packworld.com/trends/operational-excellence/article/22869386/ai-in-packaging-to-reach-6-billion-by-the-end-of-2033",
        "https://www.packaginginsights.com/news/ai-in-packaging-how-artificial-intelligence-is-driving-the-packaging-industry-forward.html",
        "https://www.packagingdigest.com/packaging-design/how-to-use-and-not-use-ai-for-package-design",
        "https://www.monolithai.com/blog/packaging-sustainability-eu-and-ai",
        "https://packagingguruji.com/ai-for-packaging-design/",
        "https://www.arka.com/pages/ai-packaging-design",
        "https://chaseandassoc.com/how-artificial-intelligence-ai-in-the-packaging-industry-is-making-advancements/",
        "https://pollthepeople.app/ai-for-packaging/",
        "https://robopacusa.com/how-ai-is-revolutionizing-the-packaging-industry/",
        "https://www.pickfu.com/blog/ai-packaging-design/",
        "https://www.globaltrademag.com/ai-in-the-packaging-market-to-hit-5375-28-mn-by-2032/"
    ],
    "Next Generation Packaging Market": [
        "https://www.dhl.com/global-en/home/insights-and-innovation/thought-leadership/trend-reports/next-generation-advanced-packaging.html#:~:text=With%20a%20current%20market%20size,49.3%20billion%20USD%20by%202032.",
        "https://www.parispackagingweek.com/en/2022/10/31/next-generation-packaging-technologies-enabling-circularity-future-market-insights/",
        "https://isig.ac.cd/alumni/blogs/20158/Next-Generation-Packaging-Market-Key-Trends-Shaping-the-Global-Industry",
        "https://lot.dhl.com/glossary/next-generation-packaging/",
        "https://www.thegpstime.com/next-generation-packaging-market/",
        "https://www.automation.com/en-us/articles/2016-2/next-generation-packaging-market-growth-is-led-by",
        "https://plantesetparfums.wordpress.com/2015/09/13/next-generation-packaging-market-trends/",
        "https://www.whatech.com/og/markets-research/materials-chemicals/786942-next-generation-packaging-market-worth-usd-77-08-million-by-2029-at-a-cagr-of-6-1-says-exactitude-consultancy",
        "https://whattheythink.com/news/102777-next-generation-packaging-market-surpass-us-44-million-2027/",
        "https://www.packagingtoday.co.uk/news/newsglobal-next-generation-packaging-market-to-surpass-us-44-million-by-2027-8187695",
        "https://www.supplychainbrain.com/blogs/1-think-tank/post/39400-next-generation-packaging-brings-reliability-and-visibility-to-supply-chains",
        "https://www.globalreporterjournal.com/article/686821428-next-generation-packaging-market-is-projected-to-surpass-us-44-803-billion-by-2029-at-a-cagr-of-6-85",
        "https://www.mckinsey.com/~/media/mckinsey/industries/paper%20and%20forest%20products/our%20insights/winning%20with%20new%20models%20in%20packaging/no-ordinary-disruption-winning-with-new-models-in-packaging-2030-vf.ashx",
        "https://www.brandsgroup.com.au/next-generation-packaging/",
        "https://techbullion.com/rising-demand-from-various-end-use-industries-to-bolster-growth-of-next-generation-packaging-market/",
        "https://go.gale.com/ps/i.do?id=GALE%7CA735150557&sid=sitemap&v=2.1&it=r&p=AONE&sw=w&userGroupName=anon%7E5068a346&aty=open-web-entry",
        "https://www.yolegroup.com/product/monitor/advanced-packaging-market-monitor/",
        "https://nofima.com/projects/nano-functional-packaging/",
        "https://www.taiwannews.com.tw/news/5012843",
        "https://www.ifco.com/5-trends-shaping-sustainable-packaging-in-2024/"
    ],
    "Lab Automation in Drugs Discovery Market": [
        "https://www.genengnews.com/topics/artificial-intelligence/laboratory-automation-reaches-every-stage-of-drug-development/",
        "https://www.azolifesciences.com/article/How-Important-is-Lab-Automation-to-Drug-Discovery.aspx",
        "https://www.ddw-online.com/advances-in-laboratory-automation-for-drug-discovery-649-200604/",
        "https://frontlinegenomics.com/automation-in-drug-discovery/",
        "https://www.pharmaadvancement.com/pharma-news/lab-automation-market-what-is-in-the-store-now-future/",
        "https://www.ddw-online.com/media/32/06.spr.advances-in-laboratory-automation-for-drug-discovery.pdf",
        "https://newsstand.joomag.com/en/research-report-global-lab-automation-in-drug-discovery-market/0993469001489486111",
        "https://lifesciences.danaher.com/us/en/library/lab-automation-drug-discovery.html",
        "https://www.biocompare.com/Editorial-Articles/612020-Automated-Drug-Discovery-2-0/",
        "https://kaloramainformation.com/product/lab-automation-markets-2nd-edition-systems-key-companies-forecasts-and-trends/",
        "https://healthcare-in-europe.com/en/news/21st-century-lab-automation.html",
        "https://www.europeanpharmaceuticalreview.com/article/1808/driving-lab-automation-forward/",
        "https://pharmaceuticalmanufacturer.media/pharmaceutical-industry-insights/how-lab-automation-is-helping-drug-research/",
        "https://www.labiotech.eu/interview/arctoris-automation-drug-discovery/",
        "https://www.news-medical.net/whitepaper/20230206/Automation-as-a-drug-discovery-accelerator-in-the-pharmaceutical-industry.aspx",
        "https://www.htworld.co.uk/news/research-news/harnessing-automation-will-unlock-the-full-potential-of-drug-discovery-labs-digi23/",
        "https://www.biospace.com/article/biotech-investing-big-on-lab-automation-study/",
        "https://pittcon.org/analysis-automation-technologies-pharmaceutical-research/",
        "https://www.pharma-iq.com/pre-clinical-discovery-and-development/whitepapers/how-to-automate-the-data-lifecycle-to-make-lab-work-more-efficient-2",
        "https://www.biocompare.com/Editorial-Articles/612020-Automated-Drug-Discovery-2-0/#:~:text=Automation%20in%20drug%20discovery%20and,benefits%20offered%20by%20laboratory%20automation.",
        "https://www.ddw-online.com/how-end-to-end-laboratory-automation-and-ai-are-accelerating-drug-discovery-17751-202207/",
        "https://www.nature.com/articles/nrd.2017.232",
        "https://automata.tech/blog/investigating-laboratory-automation-in-early-drug-discovery/",
        "https://paa-automation.com/application/drug-discovery/",
        "https://paa-automation.com/applications/",
        "https://www.technologynetworks.com/drug-discovery/articles/transforming-drug-discovery-using-ai-and-automation-338301",
        "https://www.mckinsey.com/industries/life-sciences/our-insights/from-bench-to-bedside-transforming-r-and-d-labs-through-automation",
        "https://www.astrazeneca.com/r-d/our-technologies/ilab.html"
    ],
    "3D Printed Packaging Market": [
        "https://www.designtechproducts.com/articles/3d-printing-packaging#:~:text=3D%20printing%2C%20with%20its%20inherent,environment%20friendly%20material%20in%20packaging.&text=3D%20packaging%20has%20opened%20up,important%20constraints%20is%20the%20cost.",
        "https://www.stratasys.co.in/industries-and-applications/3d-printing-applications/packaging/",
        "https://www.alexanderdanielsglobal.com/blog/3d-printing-in-the-packaging-industry/",
        "https://www.3dnatives.com/en/3d-printing-sustainable-packaging-corporate-goals-consumer-demands-211220214/",
        "https://zortrax.com/applications/packaging-design/",
        "https://www.prescouter.com/2017/02/3d-printing-disrupting-packaging/",
        "https://www.weareamnet.com/blog/impact-3d-printing-packaging-supply-chain/",
        "https://replique.io/2023/08/24/6-reasons-why-the-packaging-industry-should-shift-to-3d-printing/",
        "https://amfg.ai/2020/08/17/how-3d-printing-transforms-the-food-and-beverage-industry/",
        "https://www.packagingconnections.com/blog/3d-printing-packaging.htm-0",
        "https://www.divbyz.com/blog/3d-printed-packaging-solutions",
        "https://www.packcon.org/index.php/en/articles/118-2022/328-3d-printing-in-the-packaging-industry",
        "https://nexa3d.com/industries/packaging/",
        "https://lekac.com/production/3-ways-3d-printing-is-disrupting-the-packaging-industry",
        "https://www.javelin-tech.com/3d/process/packaging-design/",
        "https://www.cossma.com/production/article/3d-printed-packaging-36939.html",
        "https://textilevaluechain.in/news-insights/transforming-consumer-experience-3d-printed-packaging-industry-is-the-new-big-thing-in-the-market-and-will-it-cross-us-3-billion-by-2033",
        "https://www.objective3d.com.au/resource/blog/developing-sustainable-packaging-solutions-with-3d-printing-technology/",
        "https://medium.com/@sindiajohn0246/3d-printed-packaging-market-key-drivers-and-challenges-2023-2033-ba372b4d151e",
        "https://ieeexplore.ieee.org/document/7887895",
        "https://quickparts.com/3d-printing-for-the-packaging-industry/",
        "https://www.packagingstrategies.com/articles/104099-podcast-the-role-of-3d-printing-in-sustainable-packaging",
        "https://www.health-care-it.com/company/910976/news/3408203/shaping-the-future-3d-printed-packaging-market-set-to-double-to-us-2-560-million-by-2033-with-a-7-8-cagr",
        "https://ijaers.com/detail/applications-and-prospects-of-3d-printing-in-the-packaging-industry/",
        "https://www.packagingdevelopments.com/blog/3d-printing-within-the-packaging-process-a-hindrance-or-a-help/",
        "https://www.packagingdigest.com/digital-printing/3d-printing-s-future-in-packaging-is-promising",
        "https://theuniquegroup.com/impact-3d-printing-packing-industry/",
        "https://www.liquidpackagingsolution.com/news/3d-printing-the-future-of-packaging",
        "https://www.jabil.com/blog/3d-printing-trends-show-positive-outlook.html",
        "https://replique.io/2023/08/24/6-reasons-why-the-packaging-industry-should-shift-to-3d-printing/",
        "https://www.startus-insights.com/innovators-guide/top-10-packaging-industry-trends-innovations-in-2021/",
        "https://www.printweek.in/features/various-packaging-trends-for-industry-advancements-57740",
        "https://pakfactory.com/blog/future-of-packaging-technology-design-in-the-next-10-years-and-beyond/",
        "https://www.mdpi.com/2673-687X/3/1/6",
        "https://www.printweek.in/news/deconstructing-growth-in-3dprinted-packaging-market-42523",
        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9818434/",
        "https://www.beautypackaging.com/issues/2020-03-01/view_features/digital-3d-printing-inspire-new-designs/",
        "https://www.researchgate.net/publication/368978658_Analysis_of_the_Application_and_Exploration_of_3D_Printing_Technology_Used_in_the_Future_Takeaway_Packaging",
        "https://www.thecustomboxes.com/blog/3d-printing-technology-and-packaging-industry/",
        "https://siliconsemiconductor.net/article/118244/Breakthroughs_and_opportunities_in_3D_packaging",
        "https://www.food.gov.uk/research/introduction-3d-printing-technologies-in-the-food-system-for-food-production-and-packaging"
    ]
}

# Initialize an empty list to store the data
all_data = []

# Function to get text from elements with retry logic
def get_text_from_elements(elements):
    max_retries = 5
    for i in range(max_retries):
        try:
            return ' '.join([element.text for element in elements])
        except StaleElementReferenceException:
            time.sleep(1)
            continue
    return ''

# Function to summarize text using NLTK
def summarize_text(text):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    freq_table = dict()
    for word in words:
        word = word.lower()
        if word in stop_words:
            continue
        if word in freq_table:
            freq_table[word] += 1
        else:
            freq_table[word] = 1

    sentences = sent_tokenize(text)
    sentence_value = dict()
    
    for sentence in sentences:
        for word, freq in freq_table.items():
            if word in sentence.lower():
                if sentence in sentence_value:
                    sentence_value[sentence] += freq
                else:
                    sentence_value[sentence] = freq

    # If there are no sentences to process, return an empty summary
    if not sentence_value:
        return ""
    
    sum_values = 0
    for sentence in sentence_value:
        sum_values += sentence_value[sentence]
    
    average = int(sum_values / len(sentence_value))
    
    summary = ''
    for sentence in sentences:
        if (sentence in sentence_value) and (sentence_value[sentence] > (1.2 * average)):
            summary += " " + sentence
    
    return summary

# Function to extract all links from the page
def extract_links():
    links = driver.find_elements(By.TAG_NAME, 'a')
    hrefs = [link.get_attribute('href') for link in links if link.get_attribute('href')]
    return hrefs

# Function to extract all image URLs from the page
def extract_images():
    images = driver.find_elements(By.TAG_NAME, 'img')
    srcs = [image.get_attribute('src') for image in images if image.get_attribute('src')]
    return srcs

# Iterate over each category and its corresponding URLs
for category, urls in websites.items():
    for url in urls:
        data = {'URL': url, 'Headings': '', 'Subheadings': '', 'Text': '', 'Summary': '', 'Links': '', 'Images': ''}
        try:
            driver.get(url)
        except WebDriverException as e:
            print(f"Error occurred while accessing {url}: {e}. Skipping...")
            continue
        try:
            # Wait for the page to load
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))
        except TimeoutException:
            print(f"Timeout occurred while loading {url}. Skipping...")
            continue
        
        
        # Extract headings
        headings = driver.find_elements(By.TAG_NAME, 'h1')
        data['Headings'] = ' '.join([heading.text for heading in headings])
        
        # Extract subheadings and filter out empty ones
        subheadings = driver.find_elements(By.TAG_NAME, 'h3')
        non_empty_subheadings = [subheading.text for subheading in subheadings if subheading.text.strip()]
        formatted_subheadings = '\n'.join([f"{i+1}) {subheading}" for i, subheading in enumerate(non_empty_subheadings)])
        data['Subheadings'] = formatted_subheadings
        
        # Extract text content with retry logic
        paragraphs = driver.find_elements(By.TAG_NAME, 'p')
        text_content = get_text_from_elements(paragraphs)
        data['Text'] = text_content
        
        # Summarize the text
        summary = summarize_text(text_content)
        data['Summary'] = summary
        
        # Extract links
        links = extract_links()
        data['Links'] = '\n'.join(links)
        
        # Extract image URLs
        images = extract_images()
        data['Images'] = '\n'.join(images)
        
        all_data.append(data)

# Close the WebDriver
driver.quit()

# Create a Pandas DataFrame from the data
df = pd.DataFrame(all_data)

# Save DataFrame to an Excel file
df.to_excel('website_data0.xlsx', index=False)

print("Data has been written to website_data_with_summary_and_links_and_images.xlsx")

