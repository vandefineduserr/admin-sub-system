import json
import time
from tqdm import tqdm
from threading import Thread
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class JobLab(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.req_data = data
        self.value = None

    def run(self):
        def jl_linl_creator(data):
            # Параметры поиска:
            char_mapping_ANSI = {
                " ": "%5C", "а": "%E0", "б": "%E1", "в": "%E2", "г": "%E3",
                            "д": "%E4", "е": "%E5", "ё": "%B8", "ж": "%E6", "з": "%E7",
                            "и": "%E8", "й": "%E9", "к": "%EA", "л": "%EB", "м": "%EC",
                            "н": "%ED", "о": "%EE", "п": "%EF", "р": "%F0", "с": "%F1",
                            "т": "%F2", "у": "%F3", "ф": "%F4", "х": "%F5", "ц": "%F6",
                            "ч": "%F7", "ш": "%F8", "щ": "%F9", "ъ": "%FA", "ы": "%FB",
                            "ь": "%FC", "э": "%FD", "ю": "%FE", "я": "%FF"
            }

            logic = {
                "SerL1": "kw_w1=1",  # "все слова"
                "SerL2": "kw_w1=2",  # "любое слово"
                "SerL3": "kw_w1=3"  # "точная фраза"
            }

            # Позиция поиска
            position = {
                "SerP1": "kw_w2=2",  # "всему резюме"
                "SerP2": "kw_w2=1",  # "должности"
                "SerP3": "kw_w2=4",  # "образованию"
                "SerP4": "kw_w2=5",  # "навыкам"
                "SerP5": "kw_w2=3"  # "опыту работы"
            }

            # Города
            area = {
                "Ar0": "&srregion=100&srcity=",      # везде
                "Ar1": "&srregion=50&srcity=77",     # Москва
                "Ar2": "&srregion=47&srcity=178",    # Санкт-Петербург
                "Ar3": "srregion=54&srcity=289",     # Новосибирск
                "Ar4": "srregion=52&srcity=288",     # Нижний Новгород
                "Ar5": "srregion=16&srcity=269",     # Казань
                "Ar6": "srregion=74&srcity=317",     # Челябинск
                "Ar7": "srregion=24&srcity=276",     # Красноярск
                "Ar8": "srregion=55&srcity=290",     # Омск
                "Ar9": "srregion=63&srcity=301",     # Самара
                # Уфа (assuming there's an entry for Уфа)
                "Ar10": "srregion=2&srcity=312",
                "Ar11": "srregion=61&srcity=298",    # Ростов-на-Дону
                "Ar12": "srregion=23&srcity=275",    # Краснодар
                "Ar13": "srregion=36&srcity=256",    # Воронеж
                "Ar14": "srregion=59&srcity=294",    # Пермь
                "Ar15": "srregion=34&srcity=260",    # Волгоград
            }

            # Mapping for in_service values
            in_service_mapping = {
                None: "",   # "Не имеет значения"
                0: "0",  # "Без опыта"
                1: "1",  # "От 1 года"
                2: "2",  # "От 2 лет"
                3: "3",  # "От 3 лет"
                4: "4"   # "От 5 лет"
            }

            # Образование
            education = {
                "Не имеет значения": "",  # Любое
                "Учащийся": "sredu%5B%5D=5",  # Учащийся
                "Среднее": "sredu%5B%5D=4",  # Среднее
                "Среднее специальное": "sredu%5B%5D=3",  # Среднее специальное
                "Неполное высшее": "sredu%5B%5D=2",  # Неполное высшее
                "Высшее": "sredu%5B%5D=1",  # Высшее
            }

            # Пол
            sex = {
                "Любой": "srgender=",  # "Любой"
                "Мужской": "srgender=m",  # "Мужской"
                "Женский": "srgender=f",  # "Женский"
            }

            # Опыт работы
            work_schedule = {
                "Не имеет значения": "",
                "Полный день": "gr%5B%5D=1",
                "Сменный график": "gr%5B%5D=2",
                "Гибкий график": "gr%5B%5D=3",
                "Вахтовый метод": "gr%5B%5D=4",
                "Удаленная работа": "gr%5B%5D=6"
            }

            # Водительские права
            car_category = {
                "A": "&dr_a=1",
                "B": "&dr_b=1",
                "C": "&dr_c=1",
                "D": "&dr_d=1",
                "E": "&dr_e=1",
            }
            default_value = None
            # Add a default value for keys not found in second_dict
            paired_dict = {key: car_category.get(
                value, default_value) for key, value in car_category.items()}

            # Иностранный язык
            language_dict = {
                "lan0": "",        # Не выбрано
                "lan1": "lng=3",   # Английский
                "lan2": "lng=31",  # Немецкий
                "lan3": "lng=52",  # Французский
                "lan4": "lng=19",  # Испанский
                "lan5": "lng=39",  # Итальянский
                "lan6": "lng=23",  # Китайский
                "lan7": "lng=4",   # Арабский
                "lan8": "lng=53"   # Хинди
            }
            # Уровень иностранного языка
            languages_lvl = {
                "llvl0": "",
                "llvl1": "lng_level=1",  # A1
                "llvl2": "lng_level=1",  # A2
                "llvl3": "lng_level=2",  # B1
                "llvl4": "lng_level=2",  # B2
                "llvl5": "lng_level=3",  # C1
                "llvl6": "lng_level=4",  # C2
            }

            # Extract values from the JSON data
            key_words = data.get("key_words", "").lower()
            key_words_transformed = ''.join(
                [char_mapping_ANSI.get(char, char) for char in key_words])
            logic_value = logic.get(data.get("logic", ""), None)
            position_value = position.get(data.get("pos", ""), None)
            area_value = area.get(data.get("region", ""), None)
            min_salary = data.get('min_salary', None)
            max_salary = data.get('max_salary', None)
            in_service_min = data.get('in_service_min', None)
            in_service_max = data.get('in_service_max', None)
            education_value = education.get(data.get("education", ""), None)
            age_min = data.get('age_min', None)
            age_max = data.get('age_max', None)
            sex_value = sex.get(data.get("sex", ""), None)
            work_schedule_value = work_schedule.get(
                data.get("work_schedule", ""), None)
            car_category_value = car_category.get(
                data.get("car_category", ""), None)
            language_value = language_dict.get(data.get("languages", ""), None)
            languages_lvl_value = languages_lvl.get(
                data.get("languages_lvl", ""), None)

            # Create a list of parameter strings
            parameters = []

            if key_words_transformed:
                parameters.append(f"srprofecy={key_words_transformed}")

            if logic_value:
                parameters.append(logic_value)

            if position_value:
                parameters.append(position_value)

            if area_value:
                parameters.append(area_value)

            if min_salary:
                parameters.append(f'srzpmin={min_salary}')

            if max_salary:
                parameters.append(f'srzpmax={max_salary}')

            if in_service_min:
                parameters.append(
                    f"srexpir={in_service_mapping.get(in_service_min, '')}")

            if education_value:
                parameters.append(education_value)

            if age_min:
                parameters.append(f'sragemin={age_min}')

            if age_max:
                parameters.append(f'sragemax={age_max}')

            if sex_value:
                parameters.append(sex_value)

            if work_schedule_value:
                parameters.append(work_schedule_value)

            if car_category_value:
                parameters.append(car_category_value)

            if language_value:
                parameters.append(language_value)

            if languages_lvl_value:
                parameters.append(languages_lvl_value)

            # Construct the link by joining the parameter strings
            link = "https://joblab.ru/search.php?" + \
                "&".join(parameters) + "&r=res&submit=1"
            return link

        link = jl_linl_creator(self.req_data)

        if link:
            print("Link extracted from JSON file:")
            print(link)
        else:
            print("No link found in JSON file.")

        #       A C T U A L   E X T R A C T I O N

        # Data decryption:    # Define a dictionary to map month names to their numeric representation

        def month_name_to_number(month_name):
            # Define a dictionary to map month names to their numeric representation
            month_dict = {
                "января": "01",
                "февраля": "02",
                "марта": "03",
                "апреля": "04",
                "мая": "05",
                "июня": "06",
                "июля": "07",
                "августа": "08",
                "сентября": "09",
                "октября": "10",
                "ноября": "11",
                "декабря": "12"
            }
            # Use the dictionary to convert the month name to its numeric representation
            return month_dict.get(month_name, "")

        # Function to extract responsibilities for a job
        def extract_responsibilities(experience_start_element):
            responsibilities = []

            # Find the next "Обязанности" element
            responsibilities_element = experience_start_element.find_next(
                "p", string="Обязанности")

            if responsibilities_element:
                # Get all the text content after the "Обязанности" element
                responsibilities_text = responsibilities_element.find_next(
                    "td").text.strip()
                responsibilities.append(responsibilities_text)

            return responsibilities

        # Function to extract the period of work
        def extract_work_period(experience_start_element):
            # Find the parent <tr> element
            tr_element = experience_start_element.find_parent("tr")

            # Find the <td> element containing "Период работы"
            period_td_element = tr_element.find("td", string="Период работы")

            # Find the following <td> element containing the period text
            period_text_td_element = period_td_element.find_next("td")

            # Extract the text from the period <td> element
            period_text = period_text_td_element.get_text(strip=True)

            return period_text

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
        driver.get(link)
        page_source = driver.page_source

        print(driver.title)
        time.sleep(3)

        # 90 resumees button press:
        driver.find_element(By.CSS_SELECTOR, 'span:nth-child(2) a+ a').click()
        time.sleep(1)

        # only one year:
        driver.find_element(By.CSS_SELECTOR, 'a:nth-child(5)').click()
        time.sleep(18)

        # Find all the CV links on the page and store them in a list
        cv_links = driver.find_elements(
            By.XPATH, "//a[contains(@href, '/res') and not(contains(@href, 'javascript'))]")
        cv_hrefs = [cv_link.get_attribute("href") for cv_link in cv_links]

        professions = driver.find_elements(By.CSS_SELECTOR, '.prof a')
        salaries = driver.find_elements(
            By.CSS_SELECTOR, '.hhide680 .font18, tr:nth-child(27) b')

        # Create a list to store the scraped data
        data = []

        # Create a tqdm progress bar
        JL_progress_bar = tqdm(total=len(cv_hrefs), unit="JobLab - CVs")

        # Iterate through each CV link and other data fields
        for cv_href, profession, salary in zip(cv_hrefs, professions, salaries):

            # Open the CV link in a new tab
            driver.execute_script(f"window.open('{cv_href}', '_blank');")
            # Adjust the sleep time as needed for the page to load
            time.sleep(2)

            # Switch to the newly opened tab
            driver.switch_to.window(driver.window_handles[-1])
            # Get the page source with Selenium
            page_source = driver.page_source

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(page_source, "html.parser")

            # Extract gender information for each CV
            try:
                gender_element = driver.find_element(
                    By.CSS_SELECTOR, 'tr:nth-child(11) td+ td p')
                gender = gender_element.text.strip()
            except:
                gender = ""
            # Extract name

            try:
                name_element = driver.find_element(
                    By.CSS_SELECTOR, '.table-to-div tr:nth-child(1) b')
                name = name_element.text.strip()
            except:
                name = ""

            # Extract age information for each CV
            try:
                age_element = driver.find_element(
                    By.CSS_SELECTOR, 'tr:nth-child(12) td+ td p')
                age = age_element.text.strip()
            except:
                age = ""

                # Extract area
            try:
                area_element = driver.find_element(
                    By.CSS_SELECTOR, 'tr:nth-child(4) td+ td p')
                area = area_element.text.strip()
            except:
                area = ""

            # Extract Workschedule
            try:
                schedule_element = driver.find_element(
                    By.CSS_SELECTOR, 'tr:nth-child(6) td+ td p')
                schedule = schedule_element.text.strip()
            except:
                schedule = ""

            # Education
            try:
                education_element = driver.find_element(
                    By.CSS_SELECTOR, 'tr:nth-child(8) td+ td p')
                education = education_element.text.strip()
            except:
                education = ""

            # Work experience
            try:
                in_service_element = driver.find_element(
                    By.CSS_SELECTOR, 'tr:nth-child(9) td+ td p')
                in_service = in_service_element.text.strip()
            except:
                in_service = ""

            # citizenship
            try:
                citizenship_element = driver.find_element(
                    By.CSS_SELECTOR, 'tr:nth-child(10) td+ td p')
                citizenship = citizenship_element.text.strip()
            except:
                citizenship = ""

            # actuality
            try:
                actuality_element = driver.find_element(
                    By.CSS_SELECTOR, '.small')
                actuality = actuality_element.text.strip()
            except:
                citizenship = ""

            # Car
            try:
                # Find the parent element containing "Водительские права"
                cars_element = soup.find("p", string="Водительские права")

                # Extract the language information from the next <p> element
                if cars_element:
                    car_element = cars_element.find_next("p")
                    car = car_element.text.strip()
                else:
                    car = ""
            except Exception as e:
                car = ""

            # Languages
            try:
                # Find the parent element containing "Иностранные языки"
                foreign_languages_element = soup.find(
                    "p", string="Иностранные языки")

                # Extract the language information from the next <p> element
                if foreign_languages_element:
                    language_info_element = foreign_languages_element.find_next(
                        "p")
                    languages = language_info_element.text.strip()
                else:
                    languages = ""
            except Exception as e:
                languages = ""

            # Skills
            try:
                # Find the parent element containing "Навыки и умения"
                skills_element = soup.find("p", string="Навыки и умения")

                # Extract the language information from the next <p> element
                if skills_element:
                    skills_element = skills_element.find_next("p")
                    skills = skills_element.text.strip()
                else:
                    skills = ""
            except Exception as e:
                skills = ""

            # Extract work experience
            jobs_data = []
            experience_start_element = soup.find("p", string="Период работы")

            job_number = 1
            while experience_start_element:
                job_data = {"Job Number": job_number}
                aspects_to_extract = ["Период работы", "Должность", "Компания"]
                for aspect in aspects_to_extract:
                    aspect_element = experience_start_element.find_next(
                        "p", string=aspect)

                    if aspect_element:
                        aspect_value_element = aspect_element.find_next("p")
                        aspect_value = aspect_value_element.text.strip()
                    # Map Russian keys to English keys
                        english_key = {
                            "Период работы": "job_period",
                            "Должность": "position",
                            "Компания": "company"
                        }.get(aspect, aspect)
                        job_data[english_key] = aspect_value
                    else:
                        job_data[aspect] = ""

                # Extract the period of work
                job_data["job_period"] = extract_work_period(
                    experience_start_element)

                # Extract responsibilities for the current job
                responsibilities = extract_responsibilities(
                    experience_start_element)
                if responsibilities:
                    job_data["duties"] = responsibilities

                # Filter out Cyrillic keys
                job_data = {key: value for key, value in job_data.items(
                ) if not any(ord(char) > 127 for char in key)}

                jobs_data.append(job_data)

                experience_start_element = experience_start_element.find_next(
                    "p", string="Период работы")
                job_number += 1

            # Close the CV tab
            driver.close()

            # Update the progress bar
            JL_progress_bar.update(1)

            # Switch back to the original tab
            driver.switch_to.window(driver.window_handles[0])

            parts = actuality.split("  ·  ")
            date_part = parts[1]  # Extract the date part

            # Split the date part into day, month name, and year
            date_parts = date_part.split(" ")
            day = date_parts[0]
            month_name = date_parts[1]
            year = date_parts[2]

            # Convert month name to numeric
            month = month_name_to_number(month_name)
            formatted_date = f"{day}.{month}.{year}".replace(',', '')

            data.append({
                'profession': profession.text.strip(),
                'salary': salary.text.strip(),
                'name': name,
                'actuality': formatted_date,
                'age': age,
                'area': area,
                'gender': gender,
                'schedule': schedule,
                'education': education,
                'in_service': in_service,
                'citizenship': citizenship,
                'languages': languages,
                'car': car,
                'skills': skills,
                "work_experience": jobs_data,
                'cv_link': cv_href,  # Variable for cv links
            })

        # Save the data as JSON
        self.value = data

        driver.quit()
