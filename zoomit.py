# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin

# def crawl(start_url, max_depth, max_pages):
#     visited = set()
#     queue = [(start_url, 0)]
#     crawled_data = []

#     while queue and len(crawled_data) < max_pages:
#         url, depth = queue.pop(0)

#         if url not in visited and depth <= max_depth:
#             try:
#                 response = requests.get(url)
#                 html = response.text
#                 visited.add(url)
#                 soup = BeautifulSoup(html, 'html.parser')

#                 # Extracting title and text
#                 title = soup.title.text if soup.title else ""
#                 date = soup.find('span', class_="typography__StyledDynamicTypographyComponent-t787b7-0 gLcHWK fa")
#                 if date is not None:
#                     print(date.getText())
#                 else:
#                     print("Date not found")

#                 # text = soup.get_text(separator="\n").strip()
#                 print("this is the title")
#                 print(title)
#                 crawled_data.append({'url': url, 'title': title, 'published_date':date})
#                 print(f"Crawled: {url}")

#                 # Find and process all the links in the content
#                 if depth < max_depth:
#                     for link in soup.find_all('a', href=True):
#                         absolute_link = urljoin(url, link['href'])
#                         if absolute_link not in visited:
#                             queue.append((absolute_link, depth + 1))

#             except requests.RequestException as e:
#                 print(f"Failed to fetch {url}: {str(e)}")

#     return crawled_data

# # Start crawling from a given URL with a specified depth and maximum number of pages
# start_url = "https://zoomit.ir/"  # Replace with your desired starting URL
# max_depth = 2  # Replace with your desired depth
# max_pages = 10  # Replace with your desired maximum number of pages
# crawled_data = crawl(start_url, max_depth, max_pages)

# # Print the extracted titles and text
# # for data in crawled_data:
# #     print(f"URL: {data['url']}")
# #     print(f"Title: {data['title']}")
# #     print(f"Text:\n{data['text']}\n")

import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl(start_url, max_depth, max_pages):
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
                     # Find the div tag with the specified class
                div_tags = soup.findAll('p', class_='typography__StyledDynamicTypographyComponent-t787b7-0 lddBNw ParagraphElement__ParagraphBase-sc-1soo3i3-0 gOVZGU')

                if div_tags:
    # Initialize an empty list to store text content from each <p> tag
                    div_content_list = []

    # Iterate over each <p> tag and extract its text content
                    for div_tag in div_tags:
                        div_content_list.append(div_tag.get_text(separator='\n'))
    
    # Join the text content from all <p> tags into a single string
                        div_content = '\n'.join(div_content_list).strip()
                else:
                    div_content = "Content not found"

                crawled_data.append({'url': url, 'title': title, 'publishedDate_shoppingNum': published_date, 'description_content':description_content,'Content': div_content})
                print(f"Crawled: {url}")

                # Find and process all the links in the content
                if depth < max_depth:
                    for link in soup.find_all('a', href=True):
                        absolute_link = urljoin(url, link['href'])
                        if absolute_link not in visited:
                            queue.append((absolute_link, depth + 1))

            except requests.RequestException as e:
                print(f"Failed to fetch {url}: {str(e)}")

    return crawled_data

# Start crawling from a given URL with a specified depth and maximum number of pages
start_url = "https://zoomit.ir/"  # Replace with your desired starting URL
max_depth = 3  # Replace with your desired depth
max_pages = 100  # Replace with your desired maximum number of pages
crawled_data = crawl(start_url, max_depth, max_pages)

# Save crawled data to a JSON file
output_file = "crawled_data.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(crawled_data, f, ensure_ascii=False, indent=4)

print(f"Saved crawled data to {output_file}")


