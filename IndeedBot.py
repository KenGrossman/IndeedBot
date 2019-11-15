from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


def generate_wordcloud(words):
    stop_words = ['Quality Assurance', 'Developer', 'Software', 'Engineer', 'Engineering',
                  'Quality', 'QA', 'Testing', 'Welcomed', 'will', 'provide',
                  'business', 'hire', 'program', 'understanding', 'ring',
                  'high', 'end', 'team', 'start'] + list(STOPWORDS)
    word_cloud = WordCloud(width=1024, height=1024, background_color='white', stopwords=stop_words).generate(words)
    plt.figure(figsize=(10, 8), facecolor='white', edgecolor='blue')
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()

def mainloop(search_keyword):
    driver_path = Path('./Drivers/chromedriver')

    # Setup Driver and navigate to webpage
    driver = webdriver.Chrome(driver_path)
    driver.get('http://indeed.com')

    # Execute search
    what_search_field = driver.find_element_by_id('text-input-what')
    what_search_field.send_keys(search_keyword)
    what_search_field.send_keys(Keys.ENTER)

    current_page = 1
    max_page = 10

    jobs = []

    # Start loop that will continue until a specific page or until end of results
    while current_page < max_page:
        current_page = int(driver.find_element_by_id('searchCountPages').get_property('innerText').strip('Page ').split(" ")[0])
        print('current page is {0}'.format(current_page))

        # Identify all search results on this page
        page_results = driver.find_elements_by_class_name('result')

        # Click on each result to make more details appear
        for result in page_results:
            try:
                result.click()
            except:
                # Close popover if it appears
                driver.find_element_by_class_name('popover-close-link').click()
                result.click()

            # result.click()
            time.sleep(.5)

            job_title = driver.find_element_by_id('vjs-jobtitle').get_property("innerText")
            job_company = driver.find_element_by_id('vjs-cn').get_property("innerText")

            # If clause to skip promotional results with no description
            if job_company != 'Seen by Indeed':
                job_description = driver.find_element_by_id('vjs-desc').get_property("innerText")

                job = {'title': job_title, 'company': job_company, 'description': job_description}
                jobs.append(job)

                print(job)

        # Click next
        # For some reason both previous and next page use this class so im grabbing the last instance
        next_page = driver.find_elements_by_class_name('np')[-1]
        next_page.click()
        time.sleep(1)

    words = ''
    # Join all Descriptions into a single string
    for job in jobs:
        words = job['title'] + " " + words

    generate_wordcloud(words)



if __name__ == "__main__":
    search_term = "QA Engineer"
    mainloop(search_term)
