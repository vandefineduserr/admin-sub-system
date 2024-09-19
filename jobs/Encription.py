#1. key_words
#2. logic - logic of search (by selector)
#3. pos - positon of search (by selector)
#4. region - selectable places (by selector)
#5. in_region - live in the specified region (by tickbox)
#6. min_salary - minimal salary (int)
#7. max_salary - maximal salary (int)
#8. in_service_min - minimal service (int)
#9. in_service_max - maximal service (int)
#10. education - type of ecducation (multiple tickbox)
#11. age_min – number(int)
#12. age_max – number(int)
#13. sex - selectable sex (by selector)
#14. employment - selectable type of  employment (by selector)
#15. work_schedule - selectable type of  work schedule (by selector)
#16. car_category - type of driverslicens (multiple tickbox)
#17. car - owns car (tickbox)
#18.  languages -  multiple selectors
#if a language is chosen:
#19. languages_lvl - multiple selectors levels 


#1. key_words => Ecryption UTF8/ANSI
char_mapping_UTF_8 = {
                " ": "%5C", "а": "%D0%B0", "б": "%D0%B1", "в": "%D0%B2", "г": "%D0%B3",
                "д": "%D0%B4", "е": "%D0%B5", "ё": "%D1%91", "ж": "%D0%B6", "з": "%D0%B7",
                "и": "%D0%B8", "й": "%D0%B9", "к": "%D0%BA", "л": "%D0%BB", "м": "%D0%BC",
                "н": "%D0%BD", "о": "%D0%BE", "п": "%D0%BF", "р": "%D1%80", "с": "%D1%81",
                "т": "%D1%82", "у": "%D1%83", "ф": "%D1%84", "х": "%D1%85", "ц": "%D1%86",
                "ч": "%D1%87", "ш": "%D1%88", "щ": "%D1%89", "ъ": "%D1%8A", "ы": "%D1%8B",
                "ь": "%D1%8C", "э": "%D1%8D", "ю": "%D1%8E", "я": "%D1%8F"
            } 
char_mapping_ANSI = {
                " ": "%5C", "а": "%E0", "б": "%E1", "в": "%E2", "г": "%E3",
                "д": "%E4", "е": "%E5", "ё": "%B8", "ж": "%E6", "з": "%E7",
                "и": "%E8", "й": "%E9", "к": "%EA", "л": "%EB", "м": "%EC",
                "н": "%ED", "о": "%EE", "п": "%EF", "р": "%F0", "с": "%F1",
                "т": "%F2", "у": "%F3", "ф": "%F4", "х": "%F5", "ц": "%F6",
                "ч": "%F7", "ш": "%F8", "щ": "%F9", "ъ": "%FA", "ы": "%FB",
                "ь": "%FC", "э": "%FD", "ю": "%FE", "я": "%FF"
            }

#logic of search (by selector)                  #тип поиска
logic = {
        "все слова":"SerL1",
        "любое из слов":"SerL2",
        "точная фраза":"SerL3",
        "Не встречаются":"SerL4"
        }

#positon of search (by selector)                #позиция поиска

positon = {
        "везде":"SerP1",
        "в название резюме":"SerP2",
        "в образовании":"SerP3",
        "в ключевых навыках":"SerP4",
        "в опыте работы":"SerP5"
        }

#4. region - selectable places (by selector)    #Регион 
regions = {"Везде":"Ar0",
          "Москва":"Ar1",
          "Санкт Питербург":"Ar2",
          "Новосибирск":"Ar3",
          "Екатеринбург":"Ar4",
          "Казань":"Ar5",
          "Нижний Новгород":"Ar6",
          "Челябинск":"Ar7",
          "Красноярск":"Ar8",
          "Самара":"Ar9",
          "Уфа":"Ar10",
          "Ростов-на-Дону":"Ar11",
          "Омск":"Ar12",
          "Краснодар":"Ar13",
          "Воронеж":"Ar14",
          "Пермь":"Ar15",
          "Волгоград":"Ar16"
          }

#5. in_region - live in the specified region (by tickbox)
        #in_region = true / false 

#6. min_salary - minimal salary (int)           #зарплата
#7. max_salary - maximal salary (int)           #зарплата
#8. in_service_min - minimal service (int)      #опыт работы
#9. in_service_max - maximal service (int)      #опыт работы

#10. education - type of ecducation (multiple tickbox) #Образование
education = {
        "Любое":"edu0",
        "Учащийся":"edu1",
        "Среднее":"edu2",
        "Среднее специальное":"edu3",
        "Неполное высшее":"edu4",
        "Высшее":"edu5",
    }

#11. age_min – number(int) #Возраст 
#12. age_max – number(int) #Возраст

#13. sex - selectable sex (by selector) #Пол
sex = {
    "Любой":"Sex0",
    "Мужской":"SexM",
    "Женский":"SexW",
}

#14. employment - selectable type of  employment (by selector) #Тип занятости
employment={
"Любой":"emp0",
"Полная занятость":"emp1",
"Частичная занятость":"emp2",
"Временная":"emp3",
"Стажировка":"emp4",
"Сезонная":"emp5",
}

#15. work_schedule - selectable type of  work schedule (by selector)    #график работы 
work_schedule = {
    "любой":"worsc0",
    "Полный день":"worsc1",
    "Сменный график":"worsc2",
    "Гибкий график":"worsc3",
    "Удаленная работа":"worsc4",
    "Вахтовый метод":"worsc5"
}

#16. car_category - type of driverslicens (multiple tickbox) #Категория прав
car_category ={
"Нет":"drl0",
"A":"drl1",
"B":"drl2",
"C":"drl3",
"D":"drl4",
"E":"drl5",
"BE":"drl6",
"CE":"drl7",
"DE":"drl8",
"TM":"drl9",
"TB":"drl10",
}

#17. car - owns car (tickbox) # Есть личный автомобиль
#car = true / false

#18.  languages -  multiple selectors     #Знание языков
languages ={
    "Не выбрано":"lan0",
    "Английский": "lan1",
    "Немецкий": "lan2",
    "Французский":"lan3",
    "Испанский":"lan4",
    "Итальянский":"lan5",
    "Китайский":"lan6",
    "Арабский":"lan7",
    "Хинди":"lan8"
}

#19. languages_lvl - multiple selectors levels #Уровень языков
languages_lvl ={
    "Не выбрано":"llvl0",
    "A1":"llvl1",
    "A2":"llvl2",
    "B1":"llvl3",
    "B2":"llvl4",
    "C1":"llvl5",
    "C2":"llvl6",
}