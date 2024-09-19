import json
from parser_j50 import J50
from parser_hh_ru import HH_RU
from parser_jl import JobLab
from parser_go_rab import GoRab
from parser_rvr import RVR
from parser_tv import TV

class Parser:

    def parse(self, req_data, mongo_client, task_id):
        def generate_json():
            print('start generating')
            # Get values from the form
            keywords = req_data.get('keywords')
            logic_value = req_data.get('logic', 'SerL1')
            position_value = req_data.get('position', 'SerP1')
            region_value = req_data.get('region', 'Ar0')
            in_region = req_data.get('in_region', False)
            min_salary = req_data.get('min_salary', None)
            max_salary = req_data.get('max_salary', None)
            min_service = req_data.get('min_service', None)
            max_service = req_data.get('max_service', None)
            education_value = req_data.get('education', 'edu0')
            age_min = req_data.get('age_min', None)
            age_max = req_data.get('age_max', None)
            sex_value = req_data.get('sex', 'Sex0')
            employment_value = req_data.get('employment', 'emp0')
            work_schedule_value = req_data.get('work_schedule', 'worsc0')
            car_category_value = req_data.get('car_category', 'drl0')
            owns_car = req_data.get('car', False)
            languages_value = req_data.get('languages', 'lan0')
            languages_lvl_value = req_data.get('languages_lvl', 'llvl0')

            # Create a dictionary with the values
            data = {
                "key_words": keywords,
                "logic": logic_value,
                "pos": position_value,
                "region": region_value,
                "in_region": in_region,
                "min_salary": min_salary,
                "max_salary": max_salary,
                "in_service_min": min_service,
                "in_service_max": max_service,
                "education": education_value,
                "age_min": age_min,
                "age_max": age_max,
                "sex": sex_value,
                "employment": employment_value,
                "work_schedule": work_schedule_value,
                "car_category": car_category_value,
                "owns_car": owns_car,
                "languages": languages_value,
                "languages_lvl": languages_lvl_value,
            }

            # Remove empty fields
            data = {k: v for k, v in data.items() if v or v == 0 or v == False}
            return data

        data = generate_json()

        # threads = [ HH_RU(data), JobLab(data), GoRab(data), RVR(data), TV(data) ]
        threads = [ HH_RU(data), JobLab(data) ]
        # if data.get("region") in ["Везде", "Москва"]:
        #     threads.append(J50(data))

        result = []

        for index, thread in enumerate(threads, start=0):   # default is zero
            print(index)
            thread.start()
            thread.join()
            if thread.value is not None:
                print(thread.value)
                result = result + thread.value



        # print(result)
        # mongo_client
        # with open("result.json", "w", encoding="utf-8") as file:
        #     json.dump(result, file, ensure_ascii=False, indent=4)

        mongo_client["tasks"].update_one({"id": task_id},
                                         {'$set': {"status": "completed",
                                                   "result": result}})