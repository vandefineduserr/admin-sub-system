from flask import request, jsonify
import openai
import constants
import asyncio
import json
import os


class AiRequests:

    def __init__(self, app):
        self.app = app

        def format_candidate(candidate_data):
            formatted_candidate = f"Имя: {candidate_data['name']} | Общая информация: "

            formatted_candidate += f"Проживание: {candidate_data['area']} | Заработная плата: {candidate_data['salary']} | "
            formatted_candidate += f"График работы: {candidate_data['schedule']} | Образование: {candidate_data['education']} | "
            formatted_candidate += f"Опыт работы: {candidate_data['in_service']} | Гражданство: {candidate_data['citizenship']} | "
            formatted_candidate += f"Пол: {candidate_data['gender']} | Возраст: {candidate_data['age']} | "

            # Add work experience details
            formatted_candidate += "Опыт работы:\n"
            for experience in candidate_data['work_experience']:
                formatted_candidate += f"Период работы: {experience['job_period']} | Должность: {experience['position']} | "
                formatted_candidate += f"Компания: {experience['company']} | "
                formatted_candidate += f"Обязанности: {', '.join(experience['duties'])} | "

            # Add additional candidate information
            formatted_candidate += f"Дополнительная информация: Иностранные языки: {candidate_data['languages']} | "
            formatted_candidate += f"Права: {candidate_data['car']} | Образование  {candidate_data['education']} | "
            formatted_candidate += f"Навыки и умения: {candidate_data['skills']} | "
            formatted_candidate += f"ссылка на профиль: {candidate_data['cv_link']}"

            return formatted_candidate

        
        def send_request(message):
            if not message:
                return

            if isinstance(message, dict):
                message = json.dumps(message)

            messages = constants.MESSAGES

            messages.append({"role": "user", "content": message})
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k", messages=messages)
            reply = chat.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})

            return jsonify(reply),200
            
            
        @app.route('/ai/get_percent', methods=["POST"])
        def run_script():
            openai.api_key = constants.API_KEY

            candidates = []
            candidates.append(request.get_json())
            print(candidates)

            # Create the base list with the job_offer and Hr_Task
            requests = [constants.REQUEST +
                        "\n".join(constants.JOB_OFFER), (constants.DISCLAIMER + constants.PROMPT)]

            # Add up to 5 candidates to the list
            for i in range(min(5, len(candidates))):
                formatted_candidate = format_candidate(candidates[i])
                requests.append(formatted_candidate)
                

            asyncio.run(send_request(requests))
