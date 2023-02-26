# helper functions to use apis
from daily_doodle_project.settings import env
import requests
import json


def get_random_prompt():
    api_url = 'https://api.api-ninjas.com/v1/randomword?type=noun'
    response = requests.get(api_url, headers={'X-Api-Key': env("NINJAS_KEY")})
    if response.status_code == requests.codes.ok:
        print(response.text)
        return json.loads(response.text)["word"]
    else:
        print("Error:", response.status_code, response.text)
        return None
