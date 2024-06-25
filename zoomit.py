import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from elasticsearch import Elasticsearch, RequestsHttpConnection

es = Elasticsearch(
    ['http://localhost:9200'],
    http_auth=('elastic', '_11+Wl9KHD+bUtuB3j35'),
    connection_class=RequestsHttpConnection
)

def crawl_and_label(start_url, label, max_depth, max_pages):
    visited = set()
    queue = [(start_url, 0)]
    crawled_data = []

    while queue and len(crawled_data) < max_pages:
        url, depth = queue.pop(0)

        if url not in visited and depth <= max_depth:
            try:
                response = requests.get(url)
                html = response.text
                visited.add(url)
                soup = BeautifulSoup(html, 'html.parser')

                # Extracting title and text
                title = soup.title.text if soup.title else ""
                data = soup.find('span', class_="typography__StyledDynamicTypographyComponent-t787b7-0 gLcHWK fa")
                published_date = data.getText() if data else "Date not found"
                meta_description = soup.find('meta', attrs={'name': 'description'})

                if meta_description:
                    description_content = meta_description.get('content')
                else:
                    description_content = "Description not found"

                # Extract keywords and tags
                meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
                keywords = meta_keywords.get('content').split(',') if meta_keywords else []
                tags = [tag.get_text() for tag in soup.find_all('a', class_='tag')]  # Assuming tags have 'tag' class

                # Find the div tag with the specified class
                div_tags = soup.findAll('p', class_='typography__StyledDynamicTypographyComponent-t787b7-0 lddBNw ParagraphElement__ParagraphBase-sc-1soo3i3-0 gOVZGU')

                if div_tags:
                    div_content_list = []

                    for div_tag in div_tags:
                        div_content_list.append(div_tag.get_text(separator='\n'))

                    div_content = '\n'.join(div_content_list).strip()
                else:
                    div_content = "Content not found"

                document = {
                    'url': url,
                    'title': title,
                    'published_date': published_date,
                    'description_content': description_content,
                    'content': div_content,
                    'tags': tags,
                    'keywords': keywords,
                    'label': label, 
                    'crawled_date': datetime.utcnow().isoformat()
                }

                crawled_data.append(document)
                index_document(es, document)
                print(f"Crawled: {url}")

                if depth < max_depth:
                    for link in soup.find_all('a', href=True):
                        absolute_link = urljoin(url, link['href'])
                        if absolute_link not in visited:
                            queue.append((absolute_link, depth + 1))

            except requests.RequestException as e:
                print(f"Failed to fetch {url}: {str(e)}")

    return crawled_data


def parse_persian_date(date_string):
    persian_months = {
        'فروردین': '01', 'اردیبهشت': '02', 'خرداد': '03', 'تیر': '04',
        'مرداد': '05', 'شهریور': '06', 'مهر': '07', 'آبان': '08',
        'آذر': '09', 'دی': '10', 'بهمن': '11', 'اسفند': '12'
    }
    
    persian_to_english = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
    date_string = date_string.translate(persian_to_english)
    
    patterns = [
        (r'(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})', '%Y-%m-%d %H:%M:%S'),
        (r'(\d{4})-(\d{2})-(\d{2})', '%Y-%m-%d'),
        (r'(\d{1,2})\s+(\w+)\s+(\d{4})\s*-\s*(\d{2}):(\d{2})', 
         lambda m: f"{m.group(3)}-{persian_months.get(m.group(2), '01')}-{int(m.group(1)):02d} {m.group(4)}:{m.group(5)}:00")
    ]
    
    for pattern, format_or_func in patterns:
        match = re.search(pattern, date_string)
        if match:
            if callable(format_or_func):
                return format_or_func(match)
            else:
                return datetime.strptime(match.group(), format_or_func).strftime('%Y-%m-%d %H:%M:%S')
    
    return None

def index_document(es, document):
    try:
        if document['published_date'] != "Date not found":
            parsed_date = parse_persian_date(document['published_date'])
            if parsed_date:
                document['published_date'] = parsed_date
            else:
                document['published_date'] = document['crawled_date']
        else:
            document['published_date'] = document['crawled_date']

        # Remove any fields that are causing issues
        document.pop('description_content', None)

        es.index(index="search-engine", body=document)
        print(f"Document indexed: {document['url']}")
    except Exception as e:
        print(f"Failed to index document: {str(e)}")
        print(f"Problematic document: {document}")

if __name__ == "__main__":
    sections = [
        {"url": "https://zoomit.ir/computer-learning/", "label": "computer-learning"},
        {"url": "https://zoomit.ir/mobile/", "label": "mobile"},
        {"url": "https://zoomit.ir/laptop/", "label": "laptop"}
    ]

    max_depth = 3  
    max_pages_per_section = 25  
    for section in sections:
        start_url = section["url"]
        label = section["label"]
        crawl_and_label(start_url, label, max_depth, max_pages_per_section)
