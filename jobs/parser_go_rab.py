import json
import time
import random
from tqdm import tqdm
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class GoRab(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.req_data = data
        self.value = None

    def run(self):
        def rvr_link_creator(data):
            # Update the area dictionary to map regions to subdomains
            area = {
                "Везде": "https://russia.",      # Everywhere
                "Москва": "https://moskva.",     # Москва
                "Санкт-Петербург": "https://sankt-peterburg.",    # Санкт-Петербург
                "Новосибирск": "https://novosibirsk.",     # Новосибирск
                "Нижний Новгород": "https://nijni-novgorod.",     # Нижний Новгород
                "Казань": "https://kazan.",     # Казань
                "Челябинск": "https://chelyabinsk.",     # Челябинск
                "Красноярск": "https://krasnoyarsk.",     # Красноярск
                "Омск": "https://omsk.",     # Омск
                "Самара": "https://samara.",     # Самара
                "Уфа": "https://ufa.",     # Уфа
                "Ростов-на-Дону": "https://rostov-na-donu.",    # Ростов-на-Дону
                "Краснодар": "https://krasnodar.",    # Краснодар
                "Воронеж": "https://voronej.",    # Воронеж
                "Пермь": "https://perm.",    # Пермь
                "Волгоград": "https://volgograd."     # Волгоград
            }

            # Match the keys and values
            # Default to Russia if no match
            area_value = area.get(data["region"], "https://russia.")

            # Параметры поиска:
            char_mapping_UTF_8 = {
                " ": "%5C", "а": "%D0%B0", "б": "%D0%B1", "в": "%D0%B2", "г": "%D0%B3",
                            "д": "%D0%B4", "е": "%D0%B5", "ё": "%D1%91", "ж": "%D0%B6", "з": "%D0%B7",
                            "и": "%D0%B8", "й": "%D0%B9", "к": "%D0%BA", "л": "%D0%BB", "м": "%D0%BC",
                            "н": "%D0%BD", "о": "%D0%BE", "п": "%D0%BF", "р": "%D1%80", "с": "%D1%81",
                            "т": "%D1%82", "у": "%D1%83", "ф": "%D1%84", "х": "%D1%85", "ц": "%D1%86",
                            "ч": "%D1%87", "ш": "%D1%88", "щ": "%D1%89", "ъ": "%D1%8A", "ы": "%D1%8B",
                            "ь": "%D1%8C", "э": "%D1%8D", "ю": "%D1%8E", "я": "%D1%8F"
            }

            # Determine the experience parameter based on the provided "in_service_min" value
            # Default to None if key is not present
            in_service_min = data.get("in_service_min", None)

            if in_service_min is None:
                experience_param = ""  # No experience param provided
            else:
                # Convert the value to integer
                in_service_min = int(in_service_min)
                if in_service_min == 0:
                    experience_param = "exp=%D0%B1%D0%B5%D0%B7+%D0%BE%D0%BF%D1%8B%D1%82%D0%B0"  # без опыта
                elif 1 <= in_service_min < 3:
                    experience_param = "exp=1"  # 1-3 года
                elif 3 <= in_service_min < 6:
                    experience_param = "exp=3"  # 3-6 лет
                else:
                    experience_param = "exp=6"  # более 6 лет

            # For the second link based on the salary
            # Default to None if key is not present
            max_salary = data.get("max_salary", None)

            salary_param = ""  # Default value if max_salary is not provided or not a valid number

            if max_salary:
                try:
                    max_salary = int(max_salary)  # Try to cast to integer
                    if max_salary <= 10000:
                        salary_param = "&s=10000"
                    elif max_salary <= 20000:
                        salary_param = "&s=20000"
                    elif max_salary <= 40000:
                        salary_param = "&s=40000"
                    elif max_salary <= 100000:
                        salary_param = "&s=100000"
                    elif max_salary <= 200000:
                        salary_param = "&s=200000"
                    elif max_salary <= 500000:
                        salary_param = "&s=500000"
                except ValueError:
                    pass  # max_salary is not a valid number; leave salary_param as an empty string

            # Adding employment mapping
            employment_mapping = {
                "Не имеет значения": "",  # не важно
                "Полная занятость": "&jt=%D0%BF%D0%BE%D0%BB%D0%BD%D0%B0%D1%8F+%D0%B7%D0%B0%D0%BD%D1%8F%D1%82%D0%BE%D1%81%D1%82%D1%8C",  # полная занятость
                "Частичная занятость": "&jt=%D1%87%D0%B0%D1%81%D1%82%D0%B8%D1%87%D0%BD%D0%B0%D1%8F+%D0%B7%D0%B0%D0%BD%D1%8F%D1%82%D0%BE%D1%81%D1%82%D1%8C",  # частичная занятость
                "Временная": "&jt=%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F+%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0",  # временная работа
                "Стажировка": "&jt=%D1%81%D1%82%D0%B0%D0%B6%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B0",  # стажировка
                # "Удаленная работа": "&jt=%D1%83%D0%B4%D0%B0%D0%BB%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F+%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0",  # удаленная работа
            }

            # Extract and transform keywords
            key_words = data.get("key_words", "").lower()
            key_words_transformed = ''.join(
                [char_mapping_UTF_8.get(char, char) for char in key_words])
            # Extracting employment value from data and mapping to URL fragment
            employment_value = employment_mapping.get(
                data.get("employment"), "")

            parameters = []
            if key_words_transformed:
                parameters.append(f"q={key_words_transformed}")

            if employment_value:
                parameters.append(employment_value)

            if experience_param:
                parameters.append(experience_param)

            # Constructing the base link using the region and combined parameters
            base_link = area_value + \
                "gorodrabot.ru/resumes?" + "&".join(parameters)

            # For the first link (договорная)
            link1 = base_link + \
                "&s=%D0%B4%D0%BE%D0%B3%D0%BE%D0%B2%D0%BE%D1%80%D0%BD%D0%B0%D1%8F" + "&sort=date&p={}"

            # Check for the existence of max_salary in the data and if it has a valid value
            if "max_salary" in data and data["max_salary"]:
                link2 = base_link + salary_param + "&sort=date&p={}"
                return link1, link2
            else:
                base_link = base_link + "&p={}"
                return base_link,

        # Testing
        links = rvr_link_creator(self.req_data)
        print("GoRab link(s) are:")
        print(links)
        for link in links:
            #   MISSING !!!
            #                            "schedule" : schedule,
            #                            "employment": employment,
            #                            "car": car,

            BASE_URL = link
            print("GoRab-Bot is currently parsing:"+BASE_URL)

            def gather_links_from_page(driver):
                """Gathers all resume links from the current page."""
                resume_elements = driver.find_elements(
                    By.CSS_SELECTOR, "a.snippet__title-link.link")
                return [resume.get_attribute("href") for resume in resume_elements]

            def extract_work_experience(driver):
                work_experience = []

                # Identify all job entries
                job_entries = driver.find_elements(
                    By.CSS_SELECTOR, ".section:nth-child(2) ul.section__item.section__list.resume-view__list")

                for index, job_entry in enumerate(job_entries):
                    job_data = {}
                    # Add job number
                    job_data['Job Number'] = index + 1

                    # Extract period of work
                    period_elements = job_entry.find_elements(
                        By.CSS_SELECTOR, "li.section__list-item.resume-view__list-item")
                    for element in period_elements:
                        if "Период работы:" in element.text:
                            period = element.find_element(
                                By.CSS_SELECTOR, "span.resume-view__text").text.strip()
                            break
                    else:
                        period = ""  # Handle cases where "Период работы:" is not present
                    job_data['job_period'] = period

                    # Extract position or title
                    position = job_entry.find_element(
                        By.CSS_SELECTOR, "li.section__list-item span.resume-view__text").text.strip()
                    job_data['position'] = position

                    # Extract company name
                    company_name = job_entry.find_element(
                        By.CSS_SELECTOR, "h3.section__label-title").text.strip()
                    job_data['company'] = company_name

                    # Extract city
                    city = job_entry.find_element(
                        By.CSS_SELECTOR, "span.section__label-subtitle").text.strip()
                    job_data['city'] = city

                    # Extract industry or field
                    industry = job_entry.find_element(
                        By.CSS_SELECTOR, "span.resume-view__title").text.strip()
                    job_data['industry'] = industry

                    # Extract duties or achievements
                    duties_element = job_entry.find_element(
                        By.CSS_SELECTOR, "div.content-minimizer__body")
                    duties = [duty.strip() for duty in duties_element.get_attribute(
                        'innerHTML').split('<br>')]
                    job_data['duties'] = duties

                    work_experience.append(job_data)

                return work_experience

            def extract_skills_and_about(driver):
                skills_and_about_data = {}

                # Extract skills
                try:
                    skills_elements = driver.find_elements(
                        By.CSS_SELECTOR, ".section__list_without-mark .section__list-item.resume-view__tags-wrapper span.tags__tag.tag")
                    skills_list = [skill.text.strip()
                                   for skill in skills_elements]
                    skills_and_about_data['skills'] = skills_list
                except:
                    skills_and_about_data['skills'] = []

                # Extract about
                try:
                    about_element = driver.find_element(
                        By.CSS_SELECTOR, ".content-minimizer__body")
                    about_text = about_element.get_attribute(
                        'innerHTML').strip()
                    skills_and_about_data['about'] = about_text
                except:
                    skills_and_about_data['about'] = ''

                return skills_and_about_data

            def extract_area(driver):
                # Find all list items with the class 'resume-view__list-item'.
                list_items = driver.find_elements(
                    By.CSS_SELECTOR, "li.resume-view__list-item")

                # Iterate over each list item.
                for item in list_items:
                    # Check if the text "Город проживания:" exists in the current list item.
                    if "Город проживания:" in item.text:
                        # Extract and return the city.
                        city = item.find_element(
                            By.CSS_SELECTOR, "span.resume-view__text > strong").text.strip()
                        return city

                # If not found, return N/A.
                return "N/A"

            def extract_gender(driver):
                list_items = driver.find_elements(
                    By.CSS_SELECTOR, "li.resume-view__list-item")

                for item in list_items:
                    if "Пол:" in item.text:
                        gender = item.find_element(
                            By.CSS_SELECTOR, "span.resume-view__text > strong").text.strip()
                        return gender

                return "N/A"

            def extract_in_service(driver):
                try:
                    # Locate the element that contains the in_service data using the provided CSS selector
                    in_service_element = driver.find_element(
                        By.CSS_SELECTOR, ".section:nth-child(2) .section__subtitle")
                    # Extract the text from the located element
                    in_service = in_service_element.text.strip()
                except NoSuchElementException:
                    # In case the element is not found, set the in_service value to an empty string
                    in_service = ""
                return in_service

            def extract_citizenship(driver):
                list_items = driver.find_elements(
                    By.CSS_SELECTOR, "li.resume-view__list-item")

                for item in list_items:
                    if "Гражданство:" in item.text:
                        citizenship = item.find_element(
                            By.CSS_SELECTOR, "span.resume-view__text > strong").text.strip()
                        return citizenship

                return "N/A"

            def extract_education(driver):
                list_items = driver.find_elements(
                    By.CSS_SELECTOR, "div.section__content li.section__list-item.resume-view__list-item")

                for item in list_items:
                    if "Образование:" in item.text:
                        education = item.find_element(
                            By.CSS_SELECTOR, "span.resume-view__text > strong").text.strip()
                        return education

                return "N/A"

            def extract_data_from_cv_link(driver, cv_link):
                driver.get(cv_link)

                # Extract name
                try:
                    name_element = driver.find_element(
                        By.CSS_SELECTOR, "li.resume-view__list-item span.resume-view__text[title]")
                    name = name_element.get_attribute("title").strip()
                except:
                    name = "N/A"

                # Extracting age information
                try:
                    age_element = driver.find_element(
                        By.CSS_SELECTOR, "span.snippet__meta-value")
                    age = age_element.text.strip().split(" ")[0]
                except:
                    age = "N/A"

                # Extracting actuality information
                try:
                    actuality_element = driver.find_element(
                        By.CSS_SELECTOR, "div.label-info__date span")
                    actuality = actuality_element.text.strip()
                except:
                    actuality = "N/A"

                # Extract language proficiency
                try:
                    language_section = driver.find_element(
                        By.CSS_SELECTOR, ".resume-view__section:nth-child(4)")

                    language_elements = language_section.find_elements(
                        By.CSS_SELECTOR, "h3.section__label-title")

                    languages = []

                    for lang_element in language_elements:
                        lang_name = lang_element.find_element(
                            By.CSS_SELECTOR, "span:not(.resume-view__lang)").text.strip()
                        lang_proficiency = lang_element.find_element(
                            By.CSS_SELECTOR, ".resume-view__lang").text.strip()
                        languages.append(f"{lang_name} {lang_proficiency}")

                    if not languages:
                        languages_str = ""
                    else:
                        languages_str = ', '.join(languages)
                except:
                    languages_str = ""

                work_experience_data = extract_work_experience(driver)

                # Extract area (city of residence)
                area = extract_area(driver)

                # Extract gender
                gender = extract_gender(driver)

                # Extract citizenship
                citizenship = extract_citizenship(driver)

                # Extract education
                education = extract_education(driver)

                in_service = extract_in_service(driver)

                skills_list = extract_skills_and_about(driver)

                # Extracting profession (job title) information
                try:
                    job_title_element = driver.find_element(
                        By.CSS_SELECTOR, "h1.resume-view__name.content__title")
                    job_title = job_title_element.text.strip()
                except:
                    job_title = "N/A"

                # Extracting salary information
                try:
                    salary_element = driver.find_element(
                        By.CSS_SELECTOR, "div.resume-view__salary strong")
                    # Replace the non-breaking space with a regular space
                    salary = salary_element.text.strip().replace("\xa0", " ")
                    if not salary:  # If the extracted salary is empty
                        salary = "договорная"
                except Exception as e:
                    salary = "договорная"

                time.sleep(2)
                return {
                    "profession": job_title,
                    "salary": salary,
                    "name": name,
                    "actuality": actuality,
                    "age": age,
                    "area": area,
                    "gender": gender,
                    "work_experience": work_experience_data,
                    "skills_list": skills_list,

                    "education": education,
                    "citizenship": citizenship,
                    "in_service": in_service,
                    "languages": languages_str,
                    "cv_link": cv_link,
                }

            def get_random_delay():
                # Returns a random float between 5 to 15 seconds
                return random.uniform(3, 6)

            def main(BASE_URL):
                # Define your credentials here
                login_email = "theperfectfithr@gmail.com"
                password_key = "MyTebyaNaidem911"

                # Create Chrome options with headless mode
                chrome_options = Options()
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--window-size=1920,1080')
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--disable-dev-shm-usage')  

                # Create a Chrome webdriver instance with the options specified
                # driver = webdriver.Chrome(options=chrome_options)
                driver = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.CHROME, options=chrome_options)

                # Go to the login page
                driver.get("https://gorodrabot.ru/site/login")

                # Wait for the elements to become available, then input the login credentials and submit
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "email"))
                    ).send_keys(login_email)

                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "password"))
                    ).send_keys(password_key)

                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, "button[type='submit']"))
                    ).click()
                except Exception as e:
                    print(e)
                    driver.quit()
                    return []

                # Wait for the login to complete
                time.sleep(5)  # Adjust the sleep time as needed

                # Gather all resume links first
                all_links = []
                # Use a random delay between pages
                for page_num in tqdm(range(1, 7), desc="Gathering links", unit="page of GoRab"):
                    time.sleep(get_random_delay())
                    driver.get(BASE_URL.format(page_num))
                    all_links.extend(gather_links_from_page(driver))

                # Now extract individual data from each CV link
                all_data = []
                for cv_link in tqdm(all_links, desc="Processing CVs", unit="GoRab - CVs"):
                    time.sleep(get_random_delay())
                    cv_data = extract_data_from_cv_link(driver, cv_link)
                    all_data.append(cv_data)

                driver.quit()
                return all_data

        # if __name__ == "__main__":
            # Assume links are retrieved from the rvr_link_creator function
        links = rvr_link_creator(self.req_data)  # Make sure this function returns the correct links

        combined_data = []

        for link in links:
            extracted_data = main(link)

            if not extracted_data:  # If there's no data returned, break
                break

            combined_data.extend(extracted_data)

       
        self.value = combined_data
