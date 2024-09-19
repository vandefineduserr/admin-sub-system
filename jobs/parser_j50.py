import json
import re
from threading import Thread
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from tqdm import tqdm


class J50(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.req_data = data
        self.value = None

    def run(self):
        def j50_link_creator(data):

            char_mapping_ANSI = {
                " ": "%5C", "а": "%E0", "б": "%E1", "в": "%E2", "г": "%E3",
                            "д": "%E4", "е": "%E5", "ё": "%B8", "ж": "%E6", "з": "%E7",
                            "и": "%E8", "й": "%E9", "к": "%EA", "л": "%EB", "м": "%EC",
                            "н": "%ED", "о": "%EE", "п": "%EF", "р": "%F0", "с": "%F1",
                            "т": "%F2", "у": "%F3", "ф": "%F4", "х": "%F5", "ц": "%F6",
                            "ч": "%F7", "ш": "%F8", "щ": "%F9", "ъ": "%FA", "ы": "%FB",
                            "ь": "%FC", "э": "%FD", "ю": "%FE", "я": "%FF"
            }

            education = {
                "Не имеет значения": "sredu=%CB%FE%E1%EE%E5",  # Любое
                "Учащийся": "sredu=%D3%F7%E0%F9%E8%E9%F1%FF",  # Учащийся
                "Среднее": "sredu=%D1%F0%E5%E4%ED%E5%E5",  # Среднее
                # Среднее специальное
                "Среднее специальное": "sredu=%D1%F0%E5%E4%ED%E5%E5+%F1%EF%E5%F6%E8%E0%EB%FC%ED%EE%E5",
                "Неполное высшее": "sredu=%CD%E5%EF%EE%EB%ED%EE%E5+%E2%FB%F1%F8%E5%E5",  # Неполное высшее
                "Высшее": "sredu=%C2%FB%F1%F8%E5%E5",  # Высшее
            }

            # Пол
            sex = {
                "Любой": "srgender=%CB%FE%E1%EE%E9",  # "Любой"
                "Мужской": "srgender=%CC%F3%E6%F1%EA%EE%E9",  # "Мужской"
                "Женский": "srgender=%C6%E5%ED%F1%EA%E8%E9",  # "Женский"
            }

            # График работы
            work_schedule = {
                "Не имеет значения": "srgrafic=%CB%FE%E1%EE%E9",  # "Не имеет значения"
                "Полный день": "srgrafic=%CF%EE%EB%ED%FB%E9+%E4%E5%ED%FC",   # Полный рабочий день
                "Сменный график": "srgrafic=%D1%EC%E5%ED%ED%FB%E9",   # Сменный график
                "Гибкий график": "srgrafic=%D1%E2%EE%E1%EE%E4%ED%FB%E9",   # Гибкий график
                "Удаленная работа": "srgrafic=%C2%E0%F5%F2%EE%E2%FB%E9",   # Вахтовый метод работы
                "Вахтовый метод": "srgrafic=%CB%FE%E1%EE%E9"    # Удаленная работа
            }

            # занятость
            employment = {
                "Не имеет значения": "srzanatost=%CB%FE%E1%E0%FF",  # Любой
                "Полная занятость": "srzanatost=%CF%EE%EB%ED%E0%FF",  # Полная занятость
                "Частичная занятость": "srzanatost=%CF%EE+%F1%EE%E2%EC%E5%F1%F2%E8%F2%E5%EB%FC%F1%F2%E2%F3",
                "Временная": "srzanatost=%D0%E0%E7%EE%E2%E0%FF%2F%C2%F0%E5%EC%E5%ED%ED%E0%FF+%F0%E0%E1%EE%F2%E0",  # Временная
                "Стажировка": "busyType=PROBATION",  # Стажировка
                "Сезонная": "busyType=SEASONAL",  # Сезонная
            }

            # Extract values from the JSON data
            key_words = data.get("key_words", "").lower()
            key_words_transformed = ''.join(
                [char_mapping_ANSI.get(char, char) for char in key_words])
            max_salary = data.get('max_salary', None)
            education_value = education.get(data["education"], None)
            age_min = data.get('age_min', None)
            age_max = data.get('age_max', None)
            sex_value = sex.get(data["sex"], None)
            work_schedule_value = work_schedule.get(
                data["work_schedule"], None)
            employment_value = employment.get(data["employment"])

            parameters = []
            if key_words_transformed:
                parameters.append(f"srprofecy={key_words_transformed}")

            "city_id=999"

            if max_salary is not None:
                parameters.append(f'srzp={max_salary}')

            if education_value is not None:
                parameters.append(education_value)

            if age_min is not None:
                parameters.append(f'agemin={age_min}')

            if age_max is not None:
                parameters.append(f'agemax={age_max}')

            if sex_value:
                parameters.append(sex_value)

            if work_schedule_value is not None:
                parameters.append(work_schedule_value)

            if employment is not None:
                parameters.append(employment_value)

            # Construct the link by joining the parameter strings
            link = "https://job50.ru/search_r.php?" + \
                "&".join(parameters) + "&maxThread=50"
            print("Generated the Job50-link successfully:   " + link)

            return link

        def extract_links_from_page(soup):
            links = []
            for li in soup.select("ul.list > li"):
                title_element = li.find("a", target="_blank")

                gender_element = None
                desc_container = li.find("div", class_="i-desc")
                if desc_container:
                    for div in desc_container.find_all("div"):
                        if "Пол:" in div.text:
                            gender_element = div.find("span")
                            break

                href = title_element['href'] if title_element else None
                gender = gender_element.text.strip() if gender_element else None

                if href:
                    links.append({
                        'href': href,
                        'gender': gender
                    })
            return links

        link = j50_link_creator(self.req_data)

        if not link:
            print("No link found in JSON file.")
            exit()

        session = HTMLSession()

        # Extract links from the first page
        response = session.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        all_links = extract_links_from_page(soup)

        # We're setting the limit of pages to scrape as 4.
        total_pages = 4

        # Loop through the rest of the pages
        base_url = link
        if "page=" in base_url:
            base_url = base_url.rsplit("page=", 1)[0]
        for page in range(2, total_pages + 1):
            # Construct the URL for each page
            page_url = base_url + \
                ("&" if "?" in base_url else "?") + "page=" + str(page)
            response = session.get(page_url)
            soup = BeautifulSoup(response.text, "html.parser")
            all_links.extend(extract_links_from_page(soup))

        # Your main extraction code starts from here
        data = []
        candidate_number = 1

        # Iterate through each CV link with tqdm
        for link_info in tqdm(all_links, desc="Processing CVs", unit="J50 - CVs"):
            resume_link = link_info['href']
            gender = link_info['gender']
            response = session.get(resume_link)
            soup = BeautifulSoup(response.text, "html.parser")

            # Extracting various details as per the code I provided

            # Profession
            job_title = soup.find("h1", class_="header").get_text(strip=True)

            # Salary extraction logic
            salary_div = soup.find(
                "span", string=lambda text: "Зарплата:" in (text or ""))
            if salary_div:
                salary_p = salary_div.find_next("p", class_="nb")
                salary = salary_p.get_text(strip=True) if salary_p else None
            else:
                salary = None

            # Actuality
            actuality_div = soup.find(string=re.compile(
                r"Дата последнего обновления резюме"))
            if actuality_div:
                actuality = actuality_div.strip().split(":")[-1].strip()
            else:
                actuality = None

            # Find the div with class 'section personal'
            personal_section = soup.find("div", class_="section personal")
            # Look for the age element
            age_divs = personal_section.find_all("div", class_="cm")
            for age_div in age_divs:
                span_text = age_div.find(
                    "span").text.strip() if age_div.find("span") else ""
                if "Возраст:" in span_text:
                    age = age_div.find_next("p", class_="nb").text.strip()
                    break
            else:
                age = None

            # Area extraction
            area_span = soup.find(
                "span", string=lambda text: "Место жительства:" in (text or ""))
            if area_span:
                area_div = area_span.find_parent("div", class_="cm")
                if area_div:
                    area_p = area_div.find_next("p", class_="nb")
                    area = area_p.get_text(strip=True) if area_p else None
                else:
                    area = None
            else:
                area = None

            # Schedule extraction logic
            schedule_span = soup.find(
                "span", string=lambda text: "График работы:" in (text or ""))
            if schedule_span:
                schedule_div = schedule_span.find_parent("div", class_="cm")
                if schedule_div:
                    schedule_p = schedule_div.find_next("p", class_="nb")
                    schedule = schedule_p.get_text(
                        strip=True) if schedule_p else None
                else:
                    schedule = None
            else:
                schedule = None

            # Employment extraction logic
            employment_span = soup.find(
                "span", string=lambda text: "Занятость:" in (text or ""))
            if employment_span:
                employment_div = employment_span.find_parent(
                    "div", class_="cm")
                if employment_div:
                    employment_p = employment_div.find_next("p", class_="nb")
                    employment = employment_p.get_text(
                        strip=True) if employment_p else None
                else:
                    employment = None
            else:
                employment = None

            # Education extraction
            education_span = soup.find(
                "span", string=lambda text: "Образование:" in (text or ""))
            if education_span:
                education_div = education_span.find_parent("div", class_="cm")
                if education_div:
                    education_p = education_div.find_next("p")
                    education = education_p.get_text(
                        strip=True) if education_p else None
                else:
                    education = None
            else:
                education = None

            # Languages extraction logic
            languages_span = soup.find(
                "span", string=lambda text: "Иностранные языки:" in (text or ""))
            if languages_span:
                languages_div = languages_span.find_parent("div", class_="cm")
                if languages_div:
                    languages_p = languages_div.find_next("p")
                    if languages_p:
                        languages = [
                            str(child).strip() for child in languages_p.children if isinstance(child, str)]
                    else:
                        languages = None
                else:
                    languages = None
            else:
                languages = None
            # Citizenship extraction logic
            citizenship_span = soup.find(
                "span", string=lambda text: "Гражданство:" in (text or ""))
            if citizenship_span:
                citizenship_div = citizenship_span.find_parent(
                    "div", class_="cm")
                if citizenship_div:
                    citizenship_p = citizenship_div.find_next("p", class_="nb")
                    if citizenship_p:
                        citizenship = citizenship_p.text.strip()
                    else:
                        citizenship = None
                else:
                    citizenship = None
            else:
                citizenship = None
            # Skills extraction logic
            skills_span = soup.find(
                "span", string=lambda text: "Навыки и знания:" in (text or ""))
            if skills_span:
                skills_div = skills_span.find_parent("div", class_="cm")
                if skills_div:
                    skills_p = skills_div.find_next("p")
                    if skills_p:
                        skills = [
                            str(child).strip() for child in skills_p.children if isinstance(child, str)]
                    else:
                        skills = None
                else:
                    skills = None
            else:
                skills = None

            # Work Experience extraction logic
            experience_span = soup.find(
                "span", string=lambda text: "Опыт работы:" in (text or ""))
            if experience_span:
                experience_div = experience_span.find_parent(
                    "div", class_="cm")
                if experience_div:
                    experience_p = experience_div.find_next("p")
                    if experience_p:
                        # Split the <p> tag's content using <br> tags
                        experiences = [str(child).strip(
                        ) for child in experience_p.children if isinstance(child, str)]

                        # Now group the experiences. We'll use "Период работы" as a delimiter.
                        grouped_experiences = []
                        current_experience = []
                        for exp in experiences:
                            if "Период работы" in exp:
                                if current_experience:
                                    grouped_experiences.append(
                                        "\n".join(current_experience))
                                    current_experience = []
                            current_experience.append(exp)
                        if current_experience:
                            grouped_experiences.append(
                                "\n".join(current_experience))

                        work_experience = grouped_experiences
                    else:
                        work_experience = None
                else:
                    work_experience = None
            else:
                work_experience = None

            data.append({
                "profession": job_title,
                "salary": salary,
                "name": f"Кандидат Nø {candidate_number} (Job50)",
                "actuality": actuality,
                "age": age,
                "area": area,
                "gender": gender,
                "schedule": schedule,
                "employment": employment,
                "education": education,
                "citizenship": citizenship,
                "in_service": work_experience,
                "languages": languages,
                "skills": skills,

                "cv_link": resume_link
            })
            # Increment the candidate number for the next CV
            candidate_number += 1

        # Saving the extracted data
        self.value = data
