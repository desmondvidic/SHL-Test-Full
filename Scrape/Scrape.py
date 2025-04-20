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

# Setup Firefox options
options = Options()
# options.headless = True  # Uncomment to run headless
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

# Start URL
base_url = "https://www.shl.com/solutions/products/product-catalog/"
driver.get(base_url)

visited_urls = set()
all_data = []


def get_description(url):
    """Extract description from the detail page."""
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    description = ""
    description_section = soup.find("h4", string="Description")
    if description_section:
        desc_p = description_section.find_next("p")
        if desc_p:
            description = desc_p.get_text(strip=True)
    return description


while True:
    time.sleep(2)
    current_url = driver.current_url
    print(f"Collecting data from: {current_url}")

    if current_url in visited_urls:
        print("Already visited or loop detected.")
        break
    visited_urls.add(current_url)

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Select correct table wrapper, always skipping the first on base page
    table_wrappers = soup.find_all('div', class_='custom__table-wrapper')
    is_base_page = "start=" not in current_url

    if is_base_page and len(table_wrappers) > 1:
        target_wrapper = table_wrappers[1]  # Use second wrapper on base page, ignoring first
    elif table_wrappers:
        target_wrapper = table_wrappers[0]  # Use first wrapper on subsequent pages
    else:
        print("❌ No table wrapper found.")
        break

    table = target_wrapper.find('table')
    if not table:
        print("❌ Target table not found.")
        break

    rows = table.find_all('tr')

    for row in rows[1:]:  # Skip header
        cols = row.find_all('td')
        if len(cols) < 4:
            continue

        title_link = cols[0].find('a')
            
        if title_link:
            title = title_link.text.strip()
            redirect_url = urllib.parse.urljoin(base_url, title_link['href'].strip())
            try:
                description = get_description(redirect_url)
            except Exception as e:
                print(f"Error fetching description: {e}")
                description = ""
            
            
        remote = bool(cols[1].find('span', class_='-yes'))
        adaptive = bool(cols[2].find('span', class_='-yes'))
        test_types = [span.text.strip() for span in cols[3].find_all('span')]

        all_data.append({
            "title": title,
            "redirect_url": redirect_url,
            "description": description,
            "remote_testing": remote,
            "adaptive_IRT": adaptive,
            "test_type": test_types
        })


    driver.get(current_url)
    
    # Try to find the next page button
    try:
        next_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.pagination__item.-next a")))
        next_href = next_button.get_attribute("href")
        from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

        if next_href:
            parsed_url = urlparse(next_href)
            query_params = parse_qs(parsed_url.query)
            query_params['type'] = ['1']  # Force type=1
            new_query = urlencode(query_params, doseq=True)
            updated_url = urlunparse(parsed_url._replace(query=new_query))

            if updated_url not in visited_urls:
                driver.get(updated_url)
            else:
                print("✅ No more unique pages with type=1.")
                break
        else:
            print("✅ No more pages.")
            break
    except Exception as e:
        print("❌ Next button not found:", e)
        break

# Close driver
driver.quit()

# Save to JSON
with open("shl_huehue.json", "w") as f:
    json.dump(all_data, f, indent=4)

print("\n✅ Data has been extracted and saved to 'shl_solutions.json'")