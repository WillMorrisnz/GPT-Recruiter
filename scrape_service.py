from concurrent.futures import ThreadPoolExecutor, as_completed
from scrapingbee import ScrapingBeeClient
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import re


load_dotenv()
API_KEY = os.getenv('SCRAPING_BEE_API_KEY')


# -------------------------


def extract_text_by_data_automation(html_content, attribute_value, element_type):
    soup = BeautifulSoup(html_content, 'lxml')
    element = soup.find(element_type, attrs={'data-automation': attribute_value})
    return element.get_text(strip=True) if element else None


# -------------------------


def parallel_proxy_scrape_with_retries(urls):
    client = ScrapingBeeClient(api_key=API_KEY)
    html_data = []
    MAX_RETRIES = 3

    print(f"{len(urls)} URLS TO SCRAPE")

    def scrape(url):
        for attempt in range(MAX_RETRIES):
            response = client.get(url, params={'render_js': False})
            if response.ok:
                return (url, response.content)
            else:
                print(f"Attempt {attempt + 1} failed : Status {response.status_code}")
        return None

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(scrape, url): url for url in urls}
        for future in as_completed(future_to_url):
            print(f"{len(html_data) + 1} / {len(urls)}")
            result = future.result()
            if result is not None:
                html_data.append(result)

    return html_data


# -------------------------


def construct_seek_search_link(search_term, job_category='information-communication-technology', search_distance='10'):
    return f'https://www.seek.co.nz/{search_term}-jobs-in-{job_category}/in-Abbotsford-VIC-3067-AU?distance={search_distance}'


# -------------------------


def scrape_job_page_links_from_seek(seek_search_link, num_pages=1):
    urls = []
    for page in range(0, num_pages):
        urls.append(f"{seek_search_link}&page={page}") 
    job_listings = parallel_proxy_scrape_with_retries(urls)
    
    job_urls = set() 
    for job in job_listings:
        job_url = extract_job_urls(job[1]) 
        job_urls.update(job_url) 

    return list(job_urls)


# -------------------------


def extract_job_urls(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    a_tags = soup.find_all('a', href=True)
    
    # Extract URLs that contain '/job/'
    job_urls = [a['href'] for a in a_tags if '/job/' in a['href']]
    
    base_url = "https://www.seek.co.nz"
    full_urls = [base_url + url for url in job_urls]
    
    return full_urls


# -------------------------


def extract_job_id_from_url(url):
    match = re.search(r'/job/(\d+)', url)
    if match:
        return match.group(1)
    else:
        return None


# -------------------------


def scrape_job_descriptions(job_page_links, num_jobs):
    job_listing_data = dict()
    job_page_links = job_page_links[:min(len(job_page_links), num_jobs)]
    html_content = parallel_proxy_scrape_with_retries(job_page_links)
    for scrape_content in html_content:
        url = scrape_content[0]
        page = scrape_content[1]

        job_id = extract_job_id_from_url(url)
        job_description = extract_text_by_data_automation(page, 'jobAdDetails', 'div')
        job_title = extract_text_by_data_automation(page, 'job-detail-title', 'h1')
        job_advertiser = extract_text_by_data_automation(page, 'advertiser-name', 'span')
        job_work_type = extract_text_by_data_automation(page, 'job-detail-work-type', 'span')

        # Storing the scraped data in the dictionary
        job_listing_data[job_id] = {
            'description': job_description,
            'title': job_title,
            'advertiser': job_advertiser,
            'work_type': job_work_type,
            'url': url
        }

    return job_listing_data


# -------------------------

 # TODO: There is a bug in this with the number of jobs / pages
def scrape_seek_job_data(search_term='Engineer', num_jobs=22):
    seek_search_link = construct_seek_search_link(search_term)
    job_page_links = scrape_job_page_links_from_seek(seek_search_link, num_jobs // 22 + 1)
    job_data_dict = scrape_job_descriptions(job_page_links, num_jobs)
    return job_data_dict

