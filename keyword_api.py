import requests
from my_project.Secret import api_key
from my_project.Secret import service_id

def keyword_api(text_data):
    result_list = []
    for data in text_data:
        json_data = {
            "key": api_key,
            "serviceId": service_id,
            "argument": {
                "question": data['title']
            }
        }

        response = requests.post(url='http://svc.saltlux.ai:31781', json=json_data)
        result_list.append(response.text)

    return result_list
