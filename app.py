import os
import logging
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__, static_folder='static', static_url_path='/static')

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term']
        results = {}
        for site in ['berlinstartupjobs', 'weworkremotely', 'web3career']:
            try:
                scraper_function = globals()[f"scrape_{site}"]
                results[site] = scraper_function(search_term)
                logger.info(f"Scraped {len(results[site])} jobs from {site}")
            except Exception as e:
                logger.error(f"Error scraping {site}: {str(e)}")
                results[site] = []
        return render_template('results.html',
                               results=results,
                               search_term=search_term)
    return render_template('index.html')


def scrape_berlinstartupjobs(search_term):
    url = f"https://berlinstartupjobs.com/skill-areas/{search_term}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = []

        job_list = soup.find('ul', class_='jobs-list-items')
        if job_list:
            job_items = job_list.find_all('li', class_='bjs-jlid')

            for job in job_items:
                wrapper = job.find('div', class_='bjs-jlid__wrapper')
                if wrapper:
                    header = wrapper.find('div', class_='bjs-jlid__header')
                    description_div = wrapper.find(
                        'div', class_='bjs-jlid__description')

                    if header and description_div:
                        title = header.find('h4')
                        link = header.find('a')
                        company = description_div.find('div')

                        description = description_div.find(
                            'p', class_='bjs-jlid__description')
                        description_text = description.text.strip(
                        ) if description else 'No description available'

                        if title and link and company:
                            jobs.append({
                                'title': title.text.strip(),
                                'company': company.text.strip(),
                                'link': link['href'],
                                'description': description_text
                            })

        logger.info(
            f"Scraped {len(jobs)} jobs from Berlin Startup Jobs for '{search_term}'"
        )
        return jobs
    except requests.RequestException as e:
        logger.error(f"Error fetching Berlin Startup Jobs: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in scrape_berlinstartupjobs: {str(e)}")
        return []


def scrape_weworkremotely(search_term):
    url = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={search_term}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = []

        job_sections = soup.find_all('section', class_='jobs')

        for section in job_sections:
            for job in section.select('li.feature'):
                job_link = job.select_one('a[href^="/remote-jobs/"]')

                if job_link:
                    title = job_link.select_one('span.title')
                    company = job_link.select_one('span.company')
                    job_type = job_link.select_one('span.company',
                                                   string='Full-Time')
                    location = job_link.select_one('span.region')

                    description = f"Job Type: {job_type.text.strip() if job_type else 'N/A'}, Location: {location.text.strip() if location else 'N/A'}"

                    if title and company:
                        jobs.append({
                            'title':
                            title.text.strip(),
                            'company':
                            company.text.strip(),
                            'link':
                            'https://weworkremotely.com' + job_link['href'],
                            'description':
                            description
                        })

        logger.info(
            f"Scraped {len(jobs)} jobs from We Work Remotely for '{search_term}'"
        )
        return jobs
    except requests.RequestException as e:
        logger.error(f"Error fetching We Work Remotely: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in scrape_weworkremotely: {str(e)}")
        return []


def scrape_web3career(search_term):
    url = f"https://web3.career/{search_term}-jobs"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = []

        job_table = soup.find('table', class_='table table-borderless')
        if job_table:
            for job_row in job_table.find_all('tr', class_='table_row'):
                job_id = job_row.get('data-jobid')
                if job_id:
                    title_elem = job_row.find(
                        'td',
                        style=lambda value: value and 'width: 500px' in value)
                    company_elem = job_row.find('td',
                                                class_='job-location-mobile')
                    link_elem = job_row.find('a', href=True)

                    location_elem = job_row.find('td',
                                                 class_='job-location-mobile')
                    salary_elem = job_row.find('td',
                                               style=lambda value: value and
                                               'text-align: end' in value)

                    if title_elem and company_elem and link_elem:
                        title = title_elem.text.strip()
                        company = company_elem.text.strip()
                        link = 'https://web3.career' + link_elem['href']
                        location = location_elem.text.strip(
                        ) if location_elem else 'N/A'
                        salary = salary_elem.text.strip(
                        ) if salary_elem else 'N/A'

                        description = f"Location: {location}, Salary: {salary}"

                        jobs.append({
                            'title': title,
                            'company': company,
                            'link': link,
                            'description': description
                        })

        logger.info(
            f"Scraped {len(jobs)} jobs from Web3 Career for '{search_term}'")
        return jobs
    except requests.RequestException as e:
        logger.error(f"Error fetching Web3 Career: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in scrape_web3career: {str(e)}")
        return []


if __name__ == '__main__':
    app.run(debug=True)
