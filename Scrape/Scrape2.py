from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import json
import time
import urllib.parse

# Setup Firefox
options = Options()
# options.headless = True
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

base_url = "https://www.shl.com/solutions/products/product-catalog/"
driver.get(base_url)

visited_urls = set()
all_data = []

def scrape_detail_page(url):
    """Scrape description, job levels, and download links from the product detail page."""
    driver.get(url)
    time.sleep(2)  # Wait for content to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Description
    description_section = soup.find("h4", string="Description")
    description = ""
    if description_section:
        desc_p = description_section.find_next("p")
        if desc_p:
            description = desc_p.get_text(strip=True)

    # Job Levels
    job_levels_section = soup.find("h4", string="Job levels")
    job_levels = []
    if job_levels_section:
        job_text = job_levels_section.find_next("p")
        if job_text:
            job_levels = [j.strip() for j in job_text.get_text(strip=True).split(",") if j.strip()]
            
    #Assessment Length
    asslen = ""
    assessment_length_section = soup.find("h4", string="Assessment length")
    if assessment_length_section:
        asslen_text = assessment_length_section.find_next("p")
        if asslen_text:
            asslen = asslen_text.get_text(strip=True)

    # Downloads
    downloads = []
    download_section = soup.find("h2", string="Downloads")
    if download_section:
        links = download_section.find_all_next("a", href=True)
        for link in links:
            if "Sample Report" in link.text or "Development Report" in link.text:
                lang = link.find_next(string=lambda s: "English" in s)
                downloads.append({
                    "label": link.get_text(strip=True),
                    "url": urllib.parse.urljoin(url, link["href"]),
                    "language": lang.strip() if lang else None
                })
            if len(downloads) >= 4:  # Limit to avoid overflow
                break
            
    return description, job_levels, downloads, asslen

while True:
    time.sleep(2)
    current_url = driver.current_url
    print(f"Collecting data from: {current_url}")

    if current_url in visited_urls:
        print("Already visited or loop detected.")
        break
    visited_urls.add(current_url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table_wrappers = soup.find_all('div', class_='custom__table-wrapper')
    is_base_page = "start=" not in current_url

    if is_base_page and len(table_wrappers) > 1:
        target_wrapper = table_wrappers[1]
    elif table_wrappers:
        target_wrapper = table_wrappers[0]
    else:
        print("❌ No table wrapper found.")
        break

    table = target_wrapper.find('table')
    if not table:
        print("❌ Target table not found.")
        break

    rows = table.find_all('tr')

    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) < 4:
            continue

        title_link = cols[0].find('a')
        if title_link:
            title = title_link.text.strip()
            redirect_url = urllib.parse.urljoin(base_url, title_link['href'].strip())
        else:
            title = cols[0].text.strip()
            redirect_url = None

        remote = bool(cols[1].find('span', class_='-yes'))
        adaptive = bool(cols[2].find('span', class_='-yes'))
        test_types = [span.text.strip() for span in cols[3].find_all('span')]

        description, job_levels, downloads, asslen = ("", [], [], "")
        if redirect_url:
            try:
                description, job_levels, downloads, asslen = scrape_detail_page(redirect_url)
            except Exception as e:
                print(f"⚠️ Failed to scrape detail page: {e}")

        all_data.append({
            "title": title,
            "redirect_url": redirect_url,
            "remote_testing": remote,
            "adaptive_IRT": adaptive,
            "test_type": test_types,
            "description": description,
            "assessment length": asslen,
            "job_levels": job_levels,
            "downloads": downloads
        })
        
    driver.get(current_url)

    # Pagination
    try:
        next_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.pagination__item.-next a")))
        next_href = next_button.get_attribute("href")

        if next_href:
            parsed_url = urllib.parse.urlparse(next_href)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            query_params['type'] = ['1']
            new_query = urllib.parse.urlencode(query_params, doseq=True)
            updated_url = urllib.parse.urlunparse(parsed_url._replace(query=new_query))

            if updated_url not in visited_urls:
                driver.get(updated_url)
            else:
                print("✅ No more unique pages.")
                break
        else:
            print("✅ No more pages.")
            break
    except Exception as e:
        print("❌ Next button not found or end of pagination:", e)
        break

driver.quit()

# Save the output
with open("shl_full_data.json", "w") as f:
    json.dump(all_data, f, indent=4)

print("\n✅ Full data has been saved to 'shl_full_data.json'")
