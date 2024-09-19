import re
import json
import time
from tqdm import tqdm
from threading import Thread
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException  # Import the exception
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class TV(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.req_data = data
        self.value = None

    def run(self):
        # Linkextraction from json file:
        def tv_link_creator(data):

            # trudvsem.ru #UTF-8

            char_mapping_UTF_8 = {
                " ": "%20", "а": "%D0%B0", "б": "%D0%B1", "в": "%D0%B2", "г": "%D0%B3",
                            "д": "%D0%B4", "е": "%D0%B5", "ё": "%D1%91", "ж": "%D0%B6", "з": "%D0%B7",
                            "и": "%D0%B8", "й": "%D0%B9", "к": "%D0%BA", "л": "%D0%BB", "м": "%D0%BC",
                            "н": "%D0%BD", "о": "%D0%BE", "п": "%D0%BF", "р": "%D1%80", "с": "%D1%81",
                            "т": "%D1%82", "у": "%D1%83", "ф": "%D1%84", "х": "%D1%85", "ц": "%D1%86",
                            "ч": "%D1%87", "ш": "%D1%88", "щ": "%D1%89", "ъ": "%D1%8A", "ы": "%D1%8B",
                            "ь": "%D1%8C", "э": "%D1%8D", "ю": "%D1%8E", "я": "%D1%8F"
            }

            # Позиция поиска
            position = {
                "SerP1": "",  # "всему резюме"
                "SerP2": "titleType=CV_NAME",  # "должности"
                "SerP3": "&titleType=CV_DESCRIPTION",  # "образованию"
                "SerP4": "&titleType=CV_DESCRIPTION",  # "навыкам"
                "SerP5": "&titleType=CV_DESCRIPTION"  # "опыту работы"
            }

            # Города
            area = {
                "Везде": "",
                "Москва": "_regionIds=7700000000000",          # Москва
                "Санкт-Петербург": "_regionIds=7800000000000",          # Санкт-Петербург
                "Новосибирск": "_regionIds=5400000000000",          # Новосибирск
                "Нижний Новгород": "_regionIds=5200000000000",          # Нижний Новгород
                "Челябинск": "_regionIds=7400000000000",          # Челябинск
                "Красноярск": "_regionIds=2400000000000",          # Красноярск
                "Самара": "_regionIds=6300000000000",          # Самара
                "Ростов-на-Дону": "_regionIds=6100000000000",         # Ростов-на-Дону
                "Омск": "_regionIds=5500000000000",  # Омск
                "Краснодар": "_regionIds=2300000000000",  # Краснодар
                "Воронеж": "_regionIds=3600000000000",  # Воронеж
                "Пермь": "_regionIds=5900000000000",  # Пермь
                "Волгоград": "_regionIds=3400000000000",  # Волгоград
                "Казань": "_regionIds=1600000000000",  # Казань
            }

            # Mapping for in_service values
            in_service_mapping = {
                None: "",   # "Не имеет значения"
                0: "experience=EXP_0",  # "Без опыта"
                1: "experience=EXP_1",  # "От 1 года"
                2: "experience=EXP_2",  # "От 2 лет"
                3: "experience=EXP_2",  # "От 3 лет"
                4: "experience=EXP_3"   # "От 5 лет"
            }

            education = {
                "Учащийся": "",  # Учащийся
                "Среднее": "education=MIDDLE",  # Среднее
                "Среднее профессиональное": "education=MIDDLE_SPECIAL",  # Среднее профессиональное
                "Неоконченное высшее": "education=UNFINISHED_HIGH",  # Неоконченное высшее
                "Высшее": "education=HIGH",  # Высшее
                "Не имеет значения": "",  # Любое
            }

            # Пол
            sex = {
                "Любой": "",  # "Любой"
                "Мужской": "gender=MALE",  # "Мужской"
                "Женский": "gender=FEMALE",  # "Женский"
            }

            # занятость
            employment = {
                "Не имеет значения": "",  # Любой
                "Полная занятость": "busyType=FULL",  # Полная занятость
                "Частичная занятость": "busyType=PARTIAL",  # Частичная занятость
                "Временная": "busyType=PROJECT",  # Временная
                "Стажировка": "busyType=PROBATION",  # Стажировка
                "Сезонная": "busyType=SEASONAL",  # Сезонная
            }

            # График работы
            work_schedule = {
                "Не имеет значения": "",  # "Не имеет значения"
                "Полный день": "scheduleType=FULL",   # Полный день
                "Сменный график": "scheduleType=TURN",   # Сменный график
                "Гибкий график": "scheduleType=FLOAT",   # Гибкий график
                "Вахтовый метод": "scheduleType=WATCH",   # Вахтовый метод работы
                "даленная работа": "busyType=REMOTE"    # Удаленная работа
            }

            # Водительские права
            car_category = {
                "drl1": "driverLicense=A",  # A
                "drl2": "driverLicense=B",  # B
                "drl3": "driverLicense=C",  # C
                "drl4": "driverLicense=D",  # D
                "drl5": "driverLicense=E",  # E
            }

            # Иностранный язык
            language_dict = {
                "lan0": "",               # Не выбрано
                "lan1": "langsLevels=014",  # Английский
                "lan2": "langsLevels=135",  # Немецкий
                "lan3": "langsLevels=213",  # Французский
                "lan4": "langsLevels=069",  # Испанский
                # Итальянский (you didn't provide a new value for Italian)
                "lan5": "langsLevels=070",
                "lan6": "langsLevels=092",  # Китайский
                "lan7": "langsLevels=018",  # Арабский
                "lan8": "langsLevels=070"   # Хинди
            }

            # Уровень иностранного языка
            languages_lvl = {
                "llvl0": "__BASIC",                               # Не выбран
                "llvl1": "__BASIC",                               # A1
                "llvl2": "__BASIC",                               # A2
                "llvl3": "__READ_AND_WRITE_WITH_DICTIONARY",      # B1
                "llvl4": "__CAN_BE_INTERVIEWED",                  # B2
                "llvl5": "__FLUENT",                              # C1
                "llvl6": "__NATIVE"                               # C2
            }

            # Extract values from the JSON data
            key_words = data.get("key_words", "").lower()
            key_words_transformed = ''.join(
                [char_mapping_UTF_8.get(char, char) for char in key_words])
            position_value = position.get(data["pos"], None)
            area_value = area.get(data["region"], None)
            min_salary = data.get('min_salary', 1)
            max_salary = data.get('max_salary', 999999)
            in_service_min = in_service_mapping.get(
                data.get("in_service_min", None), None)
            in_service_max = data.get('in_service_max', None)
            education_value = education.get(data["education"], None)
            age_min = data.get('age_min', 18)
            age_max = data.get('age_max', 99)
            sex_value = sex.get(data["sex"], None)
            work_schedule_value = work_schedule.get(
                data["work_schedule"], None)
            employment_value = employment.get(data["employment"])
            car_category_value = car_category.get(data["car_category"], None)
            language_value = language_dict.get(data["languages"], None)
            if language_value is not None:
                languages_lvl_value = languages_lvl.get(
                    data["languages_lvl"], "llvl0")

            # Create a list of parameter strings
            parameters = []

            if key_words_transformed:
                parameters.append(f"title={key_words_transformed}")

            if position_value:
                parameters.append(position_value)

            if area_value:
                parameters.append(area_value)

            if min_salary:
                parameters.append(f'salary={min_salary}')

            if max_salary:
                parameters.append(f'salary={max_salary}')

            if in_service_min:
                parameters.append(in_service_min)

            if education_value:
                parameters.append(education_value)

            if age_min:
                parameters.append(f'age={age_min}')

            if age_max:
                parameters.append(f'age={age_max}')

            if sex_value:
                parameters.append(sex_value)

            if work_schedule_value:
                parameters.append(work_schedule_value)

            if employment:
                parameters.append(employment_value)

            if car_category_value:
                parameters.append(car_category_value)

            if language_value:
                parameters.append(f"{language_value}{languages_lvl_value}")

            # Construct the link by joining the parameter strings
            link = "https://trudvsem.ru/cv/search?" + \
                "&".join(parameters) + "&page=0&cvType=LONG"
            return link

        # Extract the link from the JSON file
        link = tv_link_creator(self.req_data)

        if link:
            print("Link extracted from JSON file:")
            print(link)
        else:
            print("No link found in JSON file.")

        #       A C T U A L   E X T R A C T I O N

        # Create Chrome options with headless mode
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')  

        # Create a Chrome webdriver instance with headless mode
        # driver = webdriver.Chrome(options=chrome_options)
        driver = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.CHROME, options=chrome_options)

        # Open the initial link
        driver.get(link)

        # You can perform additional actions on the initial tab if needed
        time.sleep(10)

        print("Activated the Fresh-ones first option ;) ")

        # Find the button element by its data-uid attribute
        button = driver.find_element(
            By.CSS_SELECTOR, 'button[data-uid="PUBLISH_DATE_DESC"]')
        # Execute JavaScript to click the button
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)

        print("Confirmed! Now The Freshones are on top!")

        # Load results
        for _ in range(8):
            try:
                time.sleep(2)
                # Use JavaScript to click the button
                driver.execute_script(
                    "arguments[0].click();",
                    driver.find_element(
                        By.CSS_SELECTOR, ".align_center .button_secondary"),
                )
                time.sleep(1)
            except NoSuchElementException:  # Handle the exception
                break
        print("Loaded 90 resumes!")

        # Find all the CV links on the page and store them in a list
        href_elements = driver.find_elements(
            By.CSS_SELECTOR,
            ".search-results-simple-card .search-results-simple-card__main-content a",
        )

        # Find all the CV links on the page and store them in a list
        href_elements = driver.find_elements(
            By.CSS_SELECTOR,
            ".search-results-simple-card .search-results-simple-card__main-content a",
        )

        # Create a list to store the scraped data
        data = []

        # Create a tqdm progress bar
        progress_bar = tqdm(total=len(href_elements), unit="TV - CVs")
        # Initialize a variable to keep track of the candidate number
        candidate_number = 1
        # Iterate through each CV link and other data fields
        for cv_href_element in href_elements:
            cv_href = cv_href_element.get_attribute("href")

            # Open the URL in a new tab using JavaScript
            driver.execute_script(f"window.open('{cv_href}', '_blank');")

            # Switch to the newly opened tab
            driver.switch_to.window(driver.window_handles[-1])

            # Wait for the content to load (you may need to adjust the wait time)
            time.sleep(2)

            # Get the page source with Selenium
            page_source = driver.page_source

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(page_source, "html.parser")

            # profession
            try:
                profession_element = driver.find_element(
                    By.CSS_SELECTOR, ".content__title")
                profession = profession_element.text.strip()
            except:
                profession = ""

            # salary
            try:
                salary_element = driver.find_element(
                    By.CSS_SELECTOR, ".vacancy-sidebar__price")
                salary = salary_element.text.strip()
            except:
                salary = ""

            # "actuality"
            try:
                actuality_element = driver.find_element(
                    By.CSS_SELECTOR, ".mb-2.mt-1")
                actuality_text = actuality_element.text.strip()
                actuality = actuality_text.replace('Обновлено: ', '').strip()

            except:
                actuality = ""

            # Schedule
            try:
                schedule_element = driver.find_element(
                    By.CSS_SELECTOR, ".definitions__item:nth-child(1)")
                schedule_text = schedule_element.text.strip()
                schedule = schedule_text.replace("График работы: ", "")
            except:
                schedule = ""

            # Employment
            try:
                # Find the <dt> element with the text "Занятость:"
                employment_dt_element = soup.find("dt", string="Занятость:")

                # Extract the employment information from the next <dd> element
                if employment_dt_element:
                    employment_dd_element = employment_dt_element.find_next(
                        "dd", class_="definitions__value")
                    employment = employment_dd_element.text.strip()
                else:
                    employment = ""
            except Exception as e:
                employment = ""

            # gender & age
            try:
                # Locate the element that contains the "age" and "gender" information
                extra_info_element = driver.find_element(
                    By.CSS_SELECTOR, '.row+ .content_muted')
                # Extract the text content from the element
                extra_info_text = extra_info_element.text.strip()
                # Split the text to extract
                extra_info_split = extra_info_text.split(', ')

                if len(extra_info_split) == 2:
                    gender = extra_info_split[0].strip()
                    age = extra_info_split[1].strip()
                else:
                    gender = ""
                    age = ""
            except:
                gender = ""
                age = ""

        # Area
            try:
                area_element = driver.find_element(
                    By.CSS_SELECTOR, ".mb-3 .content_muted:nth-child(3)")
                area = area_element.text.strip()
            except:
                area = ""
        # citizenship
            try:
                citizenship_element = driver.find_element(
                    By.CSS_SELECTOR, ".content_muted~ .content_muted+ .content_muted")
                citizenship_text = citizenship_element.text.strip()
                citizenship = citizenship_text.replace(
                    'Гражданство:', '').strip()
            except:
                citizenship = ""

        # Education
            try:
                # Find the parent element containing "Образование"
                education_element = soup.find("h3", string="Образование")

                # Extract the education information from the next <div> element
                if education_element:
                    education_info_element = education_element.find_next(
                        "div", class_="content_strong")
                    education = education_info_element.text.strip()
                else:
                    education = ""
            except Exception as e:
                education = ""

            # Car
            try:
                # Find the <div> element containing the car information
                car_div_element = soup.find("div", string=re.compile(
                    "Водительское удостоверение категории:"))

                # Extract the car information after the indicator text
                if car_div_element:
                    car = car_div_element.text.split(
                        "Водительское удостоверение категории:")[1].strip()
                else:
                    car = ""
            except Exception as e:
                car = ""

            language_section = soup.find("div", {'data-content': 'languages'})

            # Initialize a list to store the languages
            languages = []

            if language_section:
                # Find all the <div> elements containing language information
                language_divs = language_section.find_all("div")

                for div in language_divs:
                    # Extract and append the language information to the list
                    language = div.text.strip()
                    languages.append(language)

            # Join the languages list into a single string
            languages_str = ", ".join(languages)

            # Find the element containing work experience information
            work_experience_section = soup.find(
                "div", {'data-content': 'work-experience'})

            # Initialize variables for storing the information
            in_service = ""
            relevant_in_service = ""

            if work_experience_section:
                # Find the subtitle element
                subtitle_element = work_experience_section.find(
                    "h4", class_="content__section-subtitle")

                if subtitle_element:
                    # Extract text from the subtitle element
                    subtitle_text = subtitle_element.get_text(strip=True)

                    # Split the subtitle text by comma and trim spaces
                    parts = subtitle_text.split(',')
                    parts = [part.strip() for part in parts]

                    # Iterate through the parts and extract relevant information
                    for part in parts:
                        if part.startswith('Общий стаж -'):
                            in_service = part.replace(
                                'Общий стаж -', '').strip()
                        elif part.startswith('релевантный опыт -'):
                            relevant_in_service = part.replace(
                                'релевантный опыт -', '').strip()

            # Find the element containing work experience information
            work_experience_section = soup.find(
                "div", {'data-content': 'work-experience'})

            # Initialize a list to store job data
            jobs_data = []

            if work_experience_section:
                # Find all resume-data blocks
                resume_data_blocks = work_experience_section.find_all(
                    "div", class_="resume-data")

                for resume_data_block in resume_data_blocks:
                    job_data = {}

                    # Extract period of work
                    period_element = resume_data_block.find(
                        "div", class_="resume-data__period")
                    if period_element:
                        period_text = period_element.find(
                            "div").get_text(strip=True)
                        period_year_element = period_element.find(
                            "div", class_="resume-data__period-year")

                        if period_year_element:
                            period_year_text = period_year_element.get_text(
                                strip=True)
                            job_data["job_period"] = f"{period_text} ({period_year_text})"
                        else:
                            job_data["job_period"] = period_text

                    # Extract job title
                    title_element = resume_data_block.find(
                        "div", class_="content_strong")
                    if title_element:
                        job_data["position"] = title_element.get_text(
                            strip=True)

                    # Extract company name
                    company_element = resume_data_block.find(
                        "div", class_="resume-data__subtitle")
                    if company_element:
                        job_data["company"] = company_element.get_text(
                            strip=True)

                    # Extract duties
                    duties_elements = resume_data_block.find_all("p")
                    duties = [duty.get_text(strip=True)
                              for duty in duties_elements]
                    if duties:
                        job_data["duties"] = duties

                    jobs_data.append(job_data)

            # Extract skills
            skills_data = []

            skills_section = soup.find("div", {"data-content": "skills"})
            if skills_section:
                professional_skills = skills_section.find_next(
                    "div", class_="card mb-3")
                for skill in professional_skills:
                    # skill_name = skill.text.strip()
                    skill_level = skill.find_all_next(
                        "span", class_="badge__text")
                    for x in skill_level:
                        if x:
                            x = x.text.strip()
                        else:
                            x = ""

                        skills_data.append(x)

            skills_data = list(set(skills_data))

            data.append(
                {
                    "profession": profession,
                    "salary": salary,
                    "name": f"Кандидат № {candidate_number}(TrudVsem)",
                    "actuality": actuality,
                    "age": age,
                    "area": area,
                    "gender": gender,
                    "schedule": schedule,
                    "education": education,
                    "total_in_service": in_service,
                    "relevant_in_service": relevant_in_service,
                    "citizenship": citizenship,
                    "car": car,
                    "languages": languages_str,
                    "skills": skills_data,
                    "work_experience": jobs_data,
                    "cv_link": cv_href,
                }
            )
            # Increment the candidate number for the next CV
            candidate_number += 1
            # Close the CV tab
            driver.close()

            # Switch back to the original tab
            driver.switch_to.window(driver.window_handles[0])

            # Update the progress bar
            progress_bar.update(1)

        # Close the progress bar
        progress_bar.close()
        
        self.value = data

        driver.quit()
