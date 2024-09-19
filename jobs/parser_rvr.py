import re
import json
from threading import Thread
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from tqdm import tqdm


#Missing!!
#        "car":car,
#        "languages":languages_str,
#        "employment": employment,

class RVR(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.req_data = data
        self.value = None

    def run(self):
        def rvr_link_creator(data):
            #Параметры поиска:
            char_mapping_UTF_8 = {
                            " ": "%5C", "а": "%D0%B0", "б": "%D0%B1", "в": "%D0%B2", "г": "%D0%B3",
                            "д": "%D0%B4", "е": "%D0%B5", "ё": "%D1%91", "ж": "%D0%B6", "з": "%D0%B7",
                            "и": "%D0%B8", "й": "%D0%B9", "к": "%D0%BA", "л": "%D0%BB", "м": "%D0%BC",
                            "н": "%D0%BD", "о": "%D0%BE", "п": "%D0%BF", "р": "%D1%80", "с": "%D1%81",
                            "т": "%D1%82", "у": "%D1%83", "ф": "%D1%84", "х": "%D1%85", "ц": "%D1%86",
                            "ч": "%D1%87", "ш": "%D1%88", "щ": "%D1%89", "ъ": "%D1%8A", "ы": "%D1%8B",
                            "ь": "%D1%8C", "э": "%D1%8D", "ю": "%D1%8E", "я": "%D1%8F"
                        } 
            # New values dictionary
            area = {
                "Везде": "",  # везде
                "Москва": "f[]=field_city:%D0%BC%D0%BE%D1%81%D0%BA%D0%B2%D0%B0",  # Москва
                "Санкт-Петербург": "f[]=field_city:%D1%81%D0%B0%D0%BD%D0%BA%D1%82-%D0%BF%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3",  # Санкт-Петербург
                "Новосибирск": "f[]=field_city:%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA",  # Новосибирск
                "Екатеринбург": "f[]=field_city:%D0%B5%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3",  # Екатеринбург
                "Казань": "f[]=field_city:%D0%BA%D0%B0%D0%B7%D0%B0%D0%BD%D1%8C",  # Казань
                "Нижний Новгород": "f[]=field_city:%D0%BD%D0%B8%D0%B6%D0%BD%D0%B8%D0%B9%20%D0%BD%D0%BE%D0%B2%D0%B3%D0%BE%D1%80%D0%BE%D0%B4",  # Нижний Новгород
                "Челябинск": "f[]=field_city:%D1%87%D0%B5%D0%BB%D1%8F%D0%B1%D0%B8%D0%BD%D1%81%D0%BA",  # Челябинск
                "Красноярск": "f[]=field_city:%D0%BA%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D1%8F%D1%80%D1%81%D0%BA",  # Красноярск
                "Самара": "f[]=field_city:%D1%81%D0%B0%D0%BC%D0%B0%D1%80%D0%B0",  # Самара
                "Уфа": "f[]=field_city:%D1%83%D1%84%D0%B0",  # Уфа
                "Ростов-на-Дону": "f[]=field_city:%D1%80%D0%BE%D1%81%D1%82%D0%BE%D0%B2%20%D0%BD%D0%B0%20%D0%B4%D0%BE%D0%BD%D1%83",  # Ростов-на-Дону
                "Омск": "f[]=field_city:%D0%BE%D0%BC%D1%81%D0%BA",  # Омск
                "Краснодар": "f[]=field_city:%D0%BA%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B4%D0%B0%D1%80",  # Краснодар
                "Воронеж": "f[]=field_city:%D0%B2%D0%BE%D1%80%D0%BE%D0%BD%D0%B5%D0%B6",  # Воронеж
                "Пермь": "f[]=field_city:%D0%BF%D0%B5%D1%80%D0%BC%D1%8C",  # Пермь
                "Волгоград": "f[]=field_city:%D0%B2%D0%BE%D0%BB%D0%B3%D0%BE%D0%B3%D1%80%D0%B0%D0%B4"  # Волгоград
            }



            # Fetch the "in_service_min" value
            in_service_min_str = data.get("min_service", "")

            # Check if the string is empty
            if not in_service_min_str:
                experience_param = ""
            else:
                try:
                    in_service_min = int(in_service_min_str)
                except ValueError:
                    in_service_min = 0  # Default to 0 if conversion fails

                # Determine the experience parameter based on the "in_service_min" value
                if in_service_min == 0:
                    experience_param = "f[]=field_experience:experience_no&f[]=field_experience:experience_yes&"  # без опыта
                elif 1 <= in_service_min < 3:
                    experience_param = "f[]=field_experience:experience_yes1"  # 1-3 года
                elif 3 <= in_service_min < 5:
                    experience_param = "f[]=field_experience:experience_yes2"  # 3-6 лет
                else:
                    experience_param = "f[]=field_experience:experience_yes3"  # более 6 лет






            #График работы 
            work_schedule_mapping = {
                "Не имеет значения": "",
                "Полный день": "f[]=field_graphic:0",    # "Полный день"
                "Сменный график": "f[]=field_graphic:1",      # "Сменный график"
                "Гибкий график": "f[]=field_graphic:2",  # "Гибкий график"
                "Вахтовый метод": "f[]=field_graphic:3",  # "Вахтовый метод"
                "Удаленная работа": "f[]=field_graphic:5"      # "Удаленная работа"
            }



            # Extract and transform keywords
            key_words = data.get("key_words", "").lower()
            key_words_transformed = ''.join([char_mapping_UTF_8.get(char, char) for char in key_words])
            # Extracting employment value from data and mapping to URL fragment
            work_schedule_value = work_schedule_mapping.get(data.get("work_schedule"), "") 
            area_value = area.get(data["region"], None)
            min_salary = data.get('min_salary', 10000)
            max_salary = data.get('max_salary', 400000)

            parameters = []
            if key_words_transformed:
                parameters.append(f"{key_words_transformed}?")

            if area_value:
                parameters.append(area_value)
            if work_schedule_value:
                parameters.append(work_schedule_value)

            if experience_param:
                parameters.append(experience_param)

            # If both min_salary and max_salary are present, format the value
            if min_salary and max_salary:
                salary_value = f"f[]=field_salary:%5B{min_salary}%20TO%20{max_salary}%5D"
                parameters.append(salary_value)



            # Constructing the base link using the region and combined parameters
            base_link = "https://xn----7sbabacj4car8afxyh.xn--p1ai/resumes/" + "&".join(parameters) + "&items_per_page=60"
            return base_link


        # Extract the link from the JSON file
        BASE_URL = rvr_link_creator(self.req_data)

        if BASE_URL:
            print("Link extracted from JSON file:")
            print(BASE_URL)
        else:
            print("No link found in JSON file.")

        RESUME_LISTING_URLS = [
            BASE_URL,
            BASE_URL + "&page=1"
        ]


        # Initialize an HTML session
        session = HTMLSession()

        # Function to fetch and parse a given URL
        def fetch_and_parse(url):
            response = session.get(url)
            return BeautifulSoup(response.text, "html.parser")

        all_resume_links = []
        all_actualities = []

        # Fetch and extract resume links and actuality from listing pages
        for url in RESUME_LISTING_URLS:
            soup = fetch_and_parse(url)
            
            # Using the 'views-row' approach
            rows = soup.select('.views-row')
            for row in rows:
                # Fetch the CV link for this row
                link_element = row.select_one('div.field-name-title a')
                if link_element:
                    all_resume_links.append("https://xn----7sbabacj4car8afxyh.xn--p1ai/" + link_element['href'])
                    
                    # Fetch the actuality for this row
                    actuality_element = row.select_one('div.field-name-changed-date .field-item.even')
                    if actuality_element:
                        all_actualities.append(actuality_element.get_text(strip=True))
                    else:
                        all_actualities.append(None)

            # Cross-check with the direct selector approach
            direct_cv_actuality_elements = soup.select('div.field-name-changed-date div.field-item')
            direct_cv_actualities = [elem.text.strip() for elem in direct_cv_actuality_elements]
            
            # For each entry in all_actualities that is None, replace it with the direct method's result
            for i, actuality in enumerate(all_actualities):
                if actuality is None and i < len(direct_cv_actualities):
                    all_actualities[i] = direct_cv_actualities[i]


        # As in the provided code, this will hold the final data
        data = []

        # Iterate through each CV link with tqdm to show the progress bar
        for index, resume_link in enumerate(tqdm(all_resume_links, desc="Processing CVs", unit="RVR - CVs")):
            soup = fetch_and_parse(resume_link)

            # Extracting the job title or profession
            job_title_element = soup.select_one('div.field-name-title div.field-item.even h1')
            job_title = job_title_element.text.strip() if job_title_element else None

            # Extracting work schedule from the provided structure
            work_schedule_container = soup.select_one('.field-name-field-graphic .field-item')
            work_schedule_value = work_schedule_container.text.strip() if work_schedule_container else None
            # Extracting the salary
            salary_element = soup.select_one('div.field-name-field-salary div.field-item.even')
            salary = salary_element.text.strip() if salary_element else "договорная"

            # Assuming soup has been correctly initialized with the HTML content

            # Function to safely get text from a BeautifulSoup object, returning an empty string if the element is not found
            def safe_get_text(soup, selector):
                element = soup.select_one(selector)
                return element.get_text(strip=True) if element else ""

            # Update the CSS selectors to match the HTML structure
            surname = safe_get_text(soup, 'div.field-name-field-surname div.field-item')
            name = safe_get_text(soup, 'div.field-name-field-name div.field-item')
            middlename = safe_get_text(soup, 'div.field-name-field-middlename div.field-item')

            # Construct the full name
            full_name = f"{surname} {name} {middlename}".strip()

            # Now you can proceed with full_name which will be a string, either the name constructed or empty if elements were not found


            if middlename:
                if middlename[-1].lower() == "а":
                    gender = "женский"
                elif middlename[-1].lower() in ["ч"]:  # Some common male-ending patterns
                    gender = "мужской"
                else:
                    gender = "не указано"  # Neutral gender if the pattern is uncommon
            else:
                gender = "не указано"  # Neutral gender if there's no middle name provided
            
            # Extracting age and area
            age_city_element = soup.select_one('div.field-name-age-city span')
            if age_city_element:
                age_city_text = age_city_element.text.strip().split(', ')
                age = age_city_text[0].split()[0]  # Splitting '39 лет' to get '39'
                area = age_city_text[1] if len(age_city_text) > 1 else None
            else:
                age, area = None, None

            # Extracting citizenship
            citizenship_element = soup.select_one('div.field-name-field-nationality div.field-item.even')
            citizenship = citizenship_element.text.strip() if citizenship_element else None
            # Extract total years of service
            in_service_container = soup.find("div", class_="field-name-exp-header-title")
            if in_service_container:
                # Search for the h2 element, then get its next_sibling (the text node)
                in_service_text = in_service_container.find("h2").next_sibling
                if in_service_text:
                    # Assuming the text is "1 год общего стажа работы.", split by space and get the first element
                    in_service = in_service_text.split()[0]  # Get the first word which should be the years
                else:
                    in_service = None
            else:
                in_service = None

            # Extract work experience details
            work_experience = []

            # Find the main container for all jobs
            all_jobs_container = soup.find("div", class_="field-name-field-experience-all")
            if all_jobs_container:
                jobs = all_jobs_container.find_all("div", class_="field-collection-view")
                
                for idx, job in enumerate(jobs):
                    job_details = {"Job Number": idx + 1}

                    # Extract job period and clean it up using regex
                    period_container = job.find("div", class_="field-name-fc-dates-exp")
                    if period_container:
                        period_span = period_container.find("span")
                        if period_span:
                            raw_period = period_span.get_text(strip=True)
                            # Use regex to capture the start and end dates
                            match = re.search(r"(\w+ \d+ - \w+ \d+)", raw_period)
                            if match:
                                job_details["job_period"] = match.group(1)
                            else:
                                job_details["job_period"] = None
                        else:
                            job_details["job_period"] = None
                    else:
                        job_details["job_period"] = None


                    # Extract position
                    position_container = job.find("div", class_="field-name-field-position")
                    if position_container:
                        position = position_container.get_text(strip=True)
                        job_details["position"] = position
                    else:
                        job_details["position"] = None

                    # Extract duties
                    duties_container = job.find("div", class_="field-name-field-responsibilities")
                    if duties_container:
                        duties = duties_container.get_text(strip=True).replace("Обязанности на рабочем месте:&nbsp;", "").split(", ")
                        job_details["duties"] = duties
                    else:
                        job_details["duties"] = []

                work_experience.append(job_details)

            # Find the container that contains the 'about me' section
            about_me_container = soup.find("div", class_="field-name-field-about-me")

            if about_me_container:
                # Find the <p> tag inside the 'about me' container
                p_tag = about_me_container.find("p")
                
                if p_tag:
                    skills = p_tag.get_text(strip=True)
                else:
                    skills = None
            else:
                skills = None




            # Extract education details
            education = []

            # Find the main container for all education records
            all_education_container = soup.find("div", class_="field-name-field-edu-all")
            if all_education_container:
                edu_records = all_education_container.find_all("div", class_="field-collection-view")
                
                for idx, record in enumerate(edu_records):
                    edu_details = {"Education Number": idx + 1}

                    # Extract year of graduation
                    year_container = record.find("div", class_="field-name-field-year-of-grad")
                    if year_container:
                        year = year_container.get_text(strip=True).replace("Год выпуска\t:", "")
                        edu_details["Year of Graduation"] = "Год выпуска\t:" + year
                    else:
                        edu_details["Year of Graduation"] = None 

                    # Extract year of graduation
                    year_container = record.find("div", class_="field-name-field-year-of-grad")
                    if year_container:
                        year = year_container.find("span", class_="date-display-single").get_text(strip=True)
                        edu_details["Year of Graduation"] = year
                    else:
                        edu_details["Year of Graduation"] = None 

                    # Extract university
                    univer_container = record.find("div", class_="field-name-field-univer")
                    if univer_container:
                        university = univer_container.get_text(strip=True)
                        edu_details["University"] = university
                    else:
                        edu_details["University"] = None

                    # Extract faculty
                    faculty_container = record.find("div", class_="field-name-field-fac")
                    if faculty_container:
                        faculty = faculty_container.get_text(strip=True).replace("Факультет:&nbsp;", "")
                        edu_details["Faculty"] = faculty
                    else:
                        edu_details["Faculty"] = None

                    # Extract specialty
                    spec_container = record.find("div", class_="field-name-field-spec")
                    if spec_container:
                        specialty = spec_container.get_text(strip=True).replace("Специальность:&nbsp;", "")
                        edu_details["Specialty"] = specialty
                    else:
                        edu_details["Specialty"] = None

                    education.append(edu_details)



            data.append({
                "profession": job_title,
                "salary": salary,
                "name": full_name,
                "actuality": all_actualities[index] if index < len(all_actualities) else None,  # Ensure we don't go out of bounds
                "age": age,
                "area": area,
                "gender": gender,
                "schedule": work_schedule_value,
                "education" : education,
                "in_service": in_service,
                "citizenship": citizenship,
                "skills": skills,
                "work_experience": work_experience,
                "cv_link": resume_link,
            })


        # Saving the extracted data
        self.value = data