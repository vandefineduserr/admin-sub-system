import json
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from requests_html import HTMLSession
from threading import Thread

class HH_RU(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.req_data = data
        self.value = None

    def run(self):
        def hh_ru_link_creator(data):
            char_mapping_UTF_8 = {
                            " ": "+", "а": "%D0%B0", "б": "%D0%B1", "в": "%D0%B2", "г": "%D0%B3",
                            "д": "%D0%B4", "е": "%D0%B5", "ё": "%D1%91", "ж": "%D0%B6", "з": "%D0%B7",
                            "и": "%D0%B8", "й": "%D0%B9", "к": "%D0%BA", "л": "%D0%BB", "м": "%D0%BC",
                            "н": "%D0%BD", "о": "%D0%BE", "п": "%D0%BF", "р": "%D1%80", "с": "%D1%81",
                            "т": "%D1%82", "у": "%D1%83", "ф": "%D1%84", "х": "%D1%85", "ц": "%D1%86",
                            "ч": "%D1%87", "ш": "%D1%88", "щ": "%D1%89", "ъ": "%D1%8A", "ы": "%D1%8B",
                            "ь": "%D1%8C", "э": "%D1%8D", "ю": "%D1%8E", "я": "%D1%8F"
                        } 

            #logic of search | тип поиска       
            logic = {
                "SerL1": "logic=normal",       #"все слова"
                "SerL2": "logic=any",       #"любое слово"
                "SerL3": "logic=phrase"        #"точная фраза"
            }

            # Позиция поиска
            position = {
                "SerP1": "pos=full_text",    # "везде"
                "SerP2": "pos=position",     # "в название резюме"
                "SerP3": "pos=education",    # "в образовании"
                "SerP4": "pos=keywords",     # "в ключевых навыках"
                "SerP5": "pos=workplaces"    # "в опыте работы"
            }

            # New values dictionary
            area = {
                "Везде": "",   
                "Москва": "area=1",  # Москва
                "Санкт-Петербург": "area=2",  # Санкт-Петербург
                "Новосибирск": "area=4",  # Новосибирск
                "Екатеринбург": "area=3",  # Екатеринбург
                "Казань": "area=88",  # Казань
                "Нижний Новгород": "area=66",  # Нижний Новгород
                "Челябинск": "area=104",  # Челябинск
                "Красноярск": "area=54",  # Красноярск
                "Самара": "area=78",  # Самара
                "Уфа": "area=99",  # Уфа
                "Ростов-на-Дону": "area=76",  # Ростов-на-Дону
                "Омск": "area=68",  # Омск
                "Краснодар": "area=53",  # Краснодар
                "Воронеж": "area=26",  # Воронеж
                "Пермь": "area=72",  # Пермь
                "Волгоград": "area=24"  # Волгоград
            }

            # Mapping for in_service values
            in_service_mapping = {
                None: "",   # "Не имеет значения"
                0: "&experience=noExperience",  # "Без опыта"
                1: "experience=between1And3",  # "От 1 года"
                2: "experience=between1And3",  # "От 2 лет"
                3: "experience=between3And6",  # "От 3 лет"
                4: "experience=moreThan6"   # "От 5 лет"
            }

            # Образование
            education = {
                "Не имеет значения": "",  # Любое
                "Учащийся": "education_level=secondary",  # Учащийся
                "Среднее": "education_level=secondary",  # Среднее
                "Среднее специальное": "education_level=special_secondary",  # Среднее специальное
                "Неполное высшее": "education_level=unfinished_higher",  # Неполное высшее
                "Высшее": "education_level=higher",  # Высшее
            }

            #Пол
            sex = {
                "Любой": "gender=unknown",
                "Мужской": "gender=male", 
                "Женский": "gender=female"
            }

            #занятость 
            employment = {
                "Не имеет значения": "employment=any",  # Любой
                "Полная занятость": "employment=full",  # Полная занятость
                "Частичная занятость": "employment=part",  # Частичная занятость
                "Временная": "employment=project",  # Временная
                "Стажировка": "employment=probation",  # Стажировка
                "Сезонная": "employment=seasonal"  # Сезонная
            }

            #График работы 
            work_schedule = {
                "Не имеет значения": "любой",
                "worsc1": "schedule=fullDay",    # "Полный день"
                "worsc2": "schedule=shift",      # "Сменный график"
                "worsc3": "schedule=flexible",  # "Гибкий график"
                "worsc5": "schedule=flyInFlyOut",  # "Вахтовый метод"
                "worsc4": "schedule=remote"      # "Удаленная работа"
            }

            # Водительские права
            car_category = {
                "drl1": "driver_license_types=A",  # A
                "drl2": "driver_license_types=B",  # B
                "drl3": "driver_license_types=C",  # C
                "drl4": "driver_license_types=D",  # D
                "drl5": "driver_license_types=E",  # E
                "drl6": "driver_license_types=BE",  # BE
                "drl7": "driver_license_types=CE",  # CE
                "drl8": "driver_license_types=DE",  # DE
                "drl9": "driver_license_types=TM",  # TM
                "drl10": "driver_license_types=TB"  # TB
            }


            # Иностранный язык
            language_dict = {
                "lan0": "",               # Не выбрано
                "lan1": "language=eng",  # Английский
                "lan2": "language=deu",  # Немецкий
                "lan3": "language=fra",  # Французский
                "lan4": "language=spa",  # Испанский
                "lan5": "language=ita",  # Итальянский (you didn't provide a new value for Italian)
                "lan6": "language=zho",  # Китайский
                "lan7": "language=ara",  # Арабский
                "lan8": "language=hin"   # Хинди
            }

            # Уровень иностранного языка
            languages_lvl = {
                "llvl0": "",                                 # Не выбран
                "llvl1": ".a1",                               # A1
                "llvl2": ".a2",                               # A2
                "llvl3": ".b1",                               # B1
                "llvl4": ".b2",                               # B2
                "llvl5": ".c1",                              # C1
                "llvl6": ".c2E"                              # C2
            }

            #&isDefaultArea=true


            # Extract values from the JSON data
            key_words = data.get("key_words", "").lower()
            key_words_transformed = ''.join([char_mapping_UTF_8.get(char, char) for char in key_words])
            logic_value = logic.get(data["logic"], None)
            position_value = position.get(data["pos"], None)
            area_value = area.get(data["region"], "area=113")
            in_region=data.get("in_region",True)
            min_salary = data.get('min_salary', None)
            max_salary = data.get('max_salary', None)
            in_service_min = data.get('in_service_min', None)
            in_service_max = data.get('in_service_max', None)
            education_value = education.get(data["education"], None)
            age_min = data.get('age_min', None)
            age_max = data.get('age_max', None)
            sex_value = sex.get(data["sex"], None)
            employment_value = employment.get(data["employment"])
            work_schedule_value = work_schedule.get(data["work_schedule"], None)
            car_category_value = car_category.get(data["car_category"], None)
            language_value = language_dict.get(data["languages"], None)
            languages_lvl_value = languages_lvl.get(data["languages_lvl"], None)

            # Create a list of parameter strings
            parameters = []

            if key_words_transformed:
                parameters.append(f"text={key_words_transformed}")

            if position_value:
                parameters.append(position_value)

            if logic_value:
                parameters.append(logic_value) 

            if area_value:
                parameters.append(f"{area_value}&isDefaultArea=true")
                
            if in_region:  # Check if in_region is True
                parameters.append("relocation=living_or_relocation")

            expper="exp_period=all_time"


            if min_salary is not None:
                parameters.append(f'salary_from={min_salary}')

            if max_salary is not None:
                parameters.append(f'salary_to={max_salary}')

            if in_service_min is not None:
                try:
                    in_service_min = int(in_service_min)  # Convert to int if it's not already
                except ValueError:
                    # Handle the case where in_service_min cannot be converted to an integer
                    # This might be a good place to set it to a default value or raise a more specific error
                    in_service_min = 0  # setting to default value of 0 for example purposes

                in_service_min = min(in_service_min, 4)
                
            # Convert in_service_min to a string using the in_service_mapping dictionary and append it to parameters
            if in_service_min is not None:
                in_service_min_string = in_service_mapping.get(in_service_min, "")  # Get the corresponding value from the mapping
                parameters.append(in_service_min_string)

            if education_value is not None:
                parameters.append(education_value)

            if age_min is not None:
                parameters.append(f'age_from={age_min}')

            if age_max is not None:
                parameters.append(f'age_to={age_max}')

            if sex_value:
                parameters.append(sex_value)

            if work_schedule_value is not None:
                parameters.append(work_schedule_value)

            if employment is not None:
                parameters.append(employment_value)

            if car_category_value is not None:
                parameters.append(car_category_value)

            if language_value is not None:
                parameters.append(f"{language_value}{languages_lvl_value}")

            # Construct the link by joining the parameter strings
            link = "https://hh.ru/search/resume?" + "&".join(parameters) + "&currency_code=RUR&order_by=publication_time&search_period=365&items_on_page=20&no_magic=true"
            # with open("2_link_HH_ru.json", "w", encoding="utf-8") as json_file:
            #     json.dump(link, json_file, ensure_ascii=False, indent=4)

            print("Link has been saved to 2_link_HH_ru.json")
            print(link)
            return link


        # Extract the link from the JSON file
        link = hh_ru_link_creator(self.req_data)
        if link:
            print("Link extracted from JSON file:")
            print(link)
        else:
            print("No link found in JSON file.")


        # Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')  

        # Initialize Selenium webdriver
        # driver = webdriver.Chrome(options=chrome_options)
        driver = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.CHROME, options=chrome_options)


        # Open the page
        driver.get(link)

        # Wait for the button to be available, then click it
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-qa='search-button']"))
            )
            button.click()

            # Waiting for potential URL change (adjust the wait time if needed)
            WebDriverWait(driver, 10).until(EC.url_changes(link))
        except Exception as e:
            print("An error occurred:", e)
            driver.quit()

        # Fetch the updated URL
        link = driver.current_url

        # Don't forget to close the driver when you're done
        driver.quit()


        # Initialize an HTML session
        session = HTMLSession()

        # Send a GET request to the link to get the initial page
        response = session.get(link)
        # Ensure the response is successful
        if response.status_code == 200:
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            # Extract the "actuality" information
            actuality_element = soup.find("span", class_="date--cHInIjOdiyfDqTabYRkp")
            actuality = actuality_element.text.strip() if actuality_element else "Not specified"

            # Find the total number of pages in the search results
            pagination = soup.find("span", class_="pager-item-not-in-short-range")
            total_pages = int(pagination.text) if pagination else 1

            # Create a list to store the scraped data
            data = []
            hh_progress_bar = tqdm(total=total_pages, unit=" WebBlocks - 20 candidates/block")

            # Initialize a variable to keep track of the candidate number
            candidate_number = 1

            # Loop through each page to scrape CVs
            for page in range(1, total_pages + 1):
                page_link = f"{link}&page={page}"
                response = session.get(page_link)
                if response.status_code == 200:
                    # Parse and extract CVs from the page as you did before
                    soup = BeautifulSoup(response.text, "html.parser")
                    cv_links = soup.find_all("a", class_="serp-item__title", href=True)
                    
                    # Create a list to store the scraped data for this page
                    page_data = []
                    
                    # Iterate through CV links on the page
                    for cv_link in cv_links:
                        cv_href = cv_link["href"]
                        full_cv_url = f"https://hh.ru{cv_href}"

                            # Send a GET request to the CV URL
                        cv_response = session.get(full_cv_url)

                            # Ensure the CV response is successful
                        if cv_response.status_code == 200:

                                # Parse the CV HTML content with BeautifulSoup
                                cv_soup = BeautifulSoup(cv_response.text, "html.parser")

                                # Extract the job title
                                job_title_element = cv_soup.find("h2", class_="bloko-header-2")
                                job_title = job_title_element.find("span", class_="resume-block__title-text").text.strip() if job_title_element else "Not specified"

                                # Extract the gender
                                gender_element = cv_soup.find("span", {"data-qa": "resume-personal-gender"})
                                gender = gender_element.text if gender_element else "Not specified"
                                
                                # Extract the "in_service" information
                                in_service_element = cv_soup.find("span", class_="resume-block__title-text_sub")
                                in_service = in_service_element.find("span").text.strip() if in_service_element and in_service_element.find("span") else "Not specified"

                                # Extract the age number
                                age_element = cv_soup.find("span", {"data-qa": "resume-personal-age"})
                                age = age_element.find("span").text if age_element else "Not specified"
                                
                                # Extract the area
                                area_element = cv_soup.find("span", {"data-qa": "resume-personal-address"})
                                area = area_element.text.strip() if area_element else "Not specified"
                                
                                # Extract the salary
                                salary_element = cv_soup.find("span", {"class": "resume-block__salary", "data-qa": "resume-block-salary"})
                                salary = salary_element.text.strip() if salary_element else "Not specified"

                                # Extract all text within <p> elements
                                p_elements = cv_soup.find_all("p")

                                # Initialize variables to store the extracted values
                                employment = "Not specified"
                                schedule = "Not specified"
                                citizenship = "Not specified"

                                # Iterate through <p> elements and filter for employment and schedule
                                for p_element in p_elements:
                                    text = p_element.text.lower()
                                    
                                    if "занятость:" in text:
                                        employment = text.split("занятость:")[1].strip()
                                    
                                    if "график работы:" in text:
                                        schedule = text.split("график работы:")[1].strip()
                                    
                                    if "гражданство:" in text:
                                        citizenship = text.split("гражданство:")[1].strip()

                                # Search for the <span> element with "Высшее образование" text
                                education_element = cv_soup.find("span", class_="resume-block__title-text", string="Высшее образование")

                                # Initialize the education variable
                                education = "Not specified"

                                # Check if the education_element is found
                                if education_element:
                                    # Extract the education text
                                    education = education_element.text.strip()

                                # Find the <div> element containing language information
                                languages_div = cv_soup.find("div", {"data-qa": "resume-block-languages"})

                                # Initialize a list to store language information
                                languages = []

                                # Check if the languages_div is found
                                if languages_div:
                                    # Find all <p> elements containing language information within the <div>
                                    language_elements = languages_div.find_all("p", {"data-qa": "resume-block-language-item"})
                                    
                                    # Extract and store each language in the languages list
                                    languages = [element.text.strip() for element in language_elements]


                                # Find the <div> element containing skills information
                                skills_div = cv_soup.find("div", {"data-qa": "skills-table"})

                                # Initialize a list to store skills information
                                skills = []

                                # Check if the skills_div is found
                                if skills_div:
                                    # Find all <span> elements containing skill information within the <div>
                                    skill_elements = skills_div.find_all("span", {"class": "bloko-tag__section_text"})
                                    
                                    # Extract and store each skill in the skills list
                                    skills = [element.text.strip() for element in skill_elements]

                                # Find the <div> element containing car information
                                car_div = cv_soup.find("div", {"data-qa": "resume-block-driver-experience"})

                                # Initialize a variable to store car information
                                car_info = ""
                                car_info1 = ""

                                # Check if the car_div is found
                                if car_div:
                                    # Extract and store the car information
                                    car_text = car_div.text.strip()
                                    if "Опыт вождения" in car_text:
                                        car_info_parts = car_text.split("Опыт вождения")
                                        car_info = car_info_parts[1].replace("\n", ", ").strip()
                                    else:
                                        car_info = "Not specified"

                                    # Check if "Имеется собственный автомобиль" exists and add newline if needed
                                    if "Имеется собственный автомобиль" in car_info:
                                        car_info1 = "Имеется собственный автомобиль"
                                        car_info = car_info.replace("Имеется собственный автомобильПрава", "Права").strip()

                                car = [car_info, car_info1]




                                # Find all the <div> elements with class "resume-block" that have the specified data-qa attribute
                                experience_sections = cv_soup.find_all("div", {"data-qa": "resume-block-experience"})

                                # Initialize a list to store work experience data
                                work_experience = []
                                job_number = 1

                                # Iterate through each experience section to extract work experience
                                for section in experience_sections:
                                    # Find all the <div> elements with class "resume-block-item-gap" within the current section
                                    experience_divs = section.find_all("div", class_="resume-block-item-gap")
                                    
                                    # Iterate through each <div> element to extract work experience within the current section
                                    for experience_div in experience_divs:
                                        
                                        # Extract period of work
                                        period_element = experience_div.find("div", class_="bloko-column")
                                        if period_element:
                                            period_text = period_element.get_text()
                                            period_year_element = period_element.find("div", class_="bloko-text bloko-text_tertiary")
                                            
                                            if period_year_element:
                                                period_year_text = period_year_element.get_text()
                                                
                                                # Remove the duplicate part from period_text
                                                period_text = period_text.replace(period_year_text, "").strip()
                                                
                                                job_period = f"{period_text} ({period_year_text})"
                                            else:
                                                job_period = period_text
                                        else:
                                            job_period = None

                                        # Check if the position element exists
                                        position_element = experience_div.find("div", {"data-qa": "resume-block-experience-position"})
                                        position = position_element.text.strip() if position_element else "N/A"

                                        company_element = experience_div.find("div", class_="bloko-text_strong")
                                        company = company_element.text.strip() if company_element else "N/A"

                                            # Extract duties by finding the <div> element with the specific data-qa attribute
                                        duties_element = experience_div.find("div", {"data-qa": "resume-block-experience-description"})
                                        duties = duties_element.text.strip() if duties_element else "N/A"

                                        # Create a dictionary for each job entry and add it to the work_experience list
                                        job_entry = {
                                            "job_number":job_number,
                                            "job_period": job_period,
                                            "position": position,
                                            "company": company,
                                            "duties": duties,
                                        }
                                        work_experience.append(job_entry)
                        
                                        # Create an empty list to store unique entries
                                        unique_work_experience = []

                                        # Iterate through each dictionary in work_experience
                                        for entry in work_experience:
                                            # Check if the current entry is not already in unique_work_experience
                                            if entry not in unique_work_experience:
                                                # If it's not a duplicate, add it to the unique_work_experience list
                                                unique_work_experience.append(entry)
                                        
                                        job_number += 1





                                data.append({
                                    "profession": job_title,
                                    "salary": salary,
                                    "name":f"Кандидат № {candidate_number}(HH.ru)",
                                    "actuality":actuality,                
                                    "age": age,
                                    "area": area,
                                    "gender": gender,
                                    "schedule" : schedule,
                                    "employment": employment,
                                    "education" : education,
                                    "citizenship":citizenship,
                                    "in_service": in_service,
                                    "languages":languages,
                                    "car": car,
                                    "skills": skills,
                                    "work_experience":unique_work_experience,
                                    "cv_link": full_cv_url
                                })
                            # Increment the candidate number for the next CV
                        candidate_number += 1
                # Update the progress bar
                hh_progress_bar.update(1) 

        # Close the progress bar
        hh_progress_bar.close()
        # Save the data to a JSON file
        with open("3_data_HH_ru.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        print(f"Scraped {len(data)} HH.ru - records")

        self.value = data
        # Close the HTML session
        session.close()
