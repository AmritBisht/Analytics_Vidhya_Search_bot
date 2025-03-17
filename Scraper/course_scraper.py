import requests
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
from urllib.parse import urljoin

# Constants
BASE_URL = 'https://courses.analyticsvidhya.com/collections/'
COURSE_LISTING_URL = f'{BASE_URL}courses'
CSV_FILE = 'detailed_courses.csv'

# Function to fetch and parse HTML content
def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")

# Function to scrape course listing pages
def scrape_course_listings():
    courses = []  # Initialize empty list to store all courses
    page_num = 1
    max_pages = 9

    while page_num <= max_pages:
        print(f"\nProcessing page {page_num}")
        page_url = f"{COURSE_LISTING_URL}?page={page_num}"
        soup = fetch_html(page_url)

        if not soup:
            print(f"Failed to fetch or parse page {page_num}")
            break

        course_container = soup.find('div', class_='collections__product-cards collections__product-cards___0b9ab')
        if not course_container:
            print(f"No course container found on page {page_num}")
            break

        course_cards = course_container.find_all('li', class_='products__list-item')

        courses_on_this_page = 0  # Counter for courses added from current page

        for card in course_cards:
            price = card.find('span', class_='course-card__price')
            if price and price.text.strip() == 'Free':
                link = card.find('a')
                title = card.find('h3')

                if link and title:
                    full_link = urljoin(BASE_URL, link['href'])
                    courses.append({
                        'Title': title.text.strip(),
                        'Link': full_link,
                        'Page': page_num  # Adding page number for verification
                    })
                    courses_on_this_page += 1


        page_num += 1
        time.sleep(1)

    return courses

#Function to scrape detailed course information
def scrape_course_details(courses):
    for course in courses:
        soup = fetch_html(course['Link'])
        if not soup:
            continue

        try:
            # Brief
            h2_elements = soup.find_all('h2')
            course['Brief'] = h2_elements[0].text if h2_elements else 'No brief available'

            # Duration, Rating, Level
            h4_elements = soup.find_all('h4', class_=None)
            if len(h4_elements) >= 3:
                course['Duration'] = h4_elements[0].text
                course['Rating'] = h4_elements[1].text
                course['Level'] = h4_elements[2].text
            else:
                course['Duration'] = 'No duration available'
                course['Rating'] = 'No rating available'
                course['Level'] = 'No level available'

            # Trainer information
            trainer = []
            inst = soup.find_all('h4', class_=lambda x: x and x.startswith("section__subheading"))
            trainer.extend(i.text for i in inst)

            tf = soup.find_all('div', class_='section__body')
            if tf and tf[0].get_text(strip=True).startswith("Unlock a lifetime-valid"):
                tf = tf[1:]

            trainer_dict = {}
            for i in range(len(trainer)):
                if i < len(tf):
                    trainer_dict[trainer[i]] = tf[i].get_text(strip=True)
            course['Trainer'] = trainer_dict if trainer_dict else 'No trainer available'

            # Description
            description_elements = soup.find_all('div', class_='custom-theme')
            course['Description'] = description_elements[0].text if description_elements else 'No description available'

            # Curriculum
            spans = soup.find_all('span', class_='course-curriculum__chapter-lesson')
            curriculum = [span.get_text(strip=True) for span in spans]
            course['Curriculum'] = curriculum if curriculum else 'No curriculum available'

            # What should enroll & takeaway
            wse_ta = soup.find_all('li', class_='checklist__list-item')
            wa = [i.get_text(strip=True) for i in wse_ta]
            course['What should enroll & takeaway'] = wa if wa else 'No what should enroll & takeaway available'

            # FAQ
            faq_list_items = soup.find_all('li', class_='faq__list-item')
            faq_data = []
            for item in faq_list_items:
                question = item.find('strong')
                answer = item.find('p')
                if question and answer:
                    faq_data.append({
                        'Question': question.text,
                        'Answer': answer.text
                    })
            course['FAQ'] = faq_data if faq_data else 'No FAQ available'

        except Exception as e:
            print(f"Error processing {course['Title']}: {str(e)}")
            continue

        time.sleep(1)  # Respectful delay between requests

    return courses

# Example usage:
courses = scrape_course_listings()  # Get the initial courses
detailed_courses = scrape_course_details(courses)  # Add details to each course


# Function to save data to CSV
def save_to_csv(courses):
    df = pd.DataFrame(courses)
    df.to_csv(CSV_FILE, index=False)
    print(f"Data saved to {CSV_FILE}")


course_list = scrape_course_listings()
cr = scrape_course_details(course_list)
save_to_csv(cr)

