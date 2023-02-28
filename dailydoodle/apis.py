# helper functions to use apis
from daily_doodle_project.settings import env,MEDIA_ROOT
import requests
import json
import shutil

# helper function used to get a random prompt daily
def get_random_prompt():
    # use requests api with api key to get a word
    api_url = 'https://api.api-ninjas.com/v1/randomword?type=noun'
    response = requests.get(api_url, headers={'X-Api-Key': env("NINJAS_KEY")})
    #verify response 
    if response.status_code == requests.codes.ok:
        print(response.text)
        return json.loads(response.text)["word"]
    else:
        print("Error:", response.status_code, response.text)
        return None
    

# helper function used to get a random profile picture for users
def get_random_profile_picture(username):
    category = 'nature'
    api_url = 'https://api.api-ninjas.com/v1/randomimage?category={}'.format(category)
    response = requests.get(api_url, headers={'X-Api-Key': env("NINJAS_KEY"), 'Accept': 'image/jpg'}, stream=True)
    if response.status_code == requests.codes.ok:
        with open(f"{MEDIA_ROOT}/profile_images/{username}.jpg", 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
            return f"/profile_images/{username}.jpg"
    else:
        with open(f"{MEDIA_ROOT}/profile_images/{username}.jpg","wb") as out_file:
                to_copy = open(f"{MEDIA_ROOT}/profile_images/fractal_1.jpg","rb")
                shutil.copyfileobj(to_copy,out_file)
        print("Error:", response.status_code, response.text)
        return f"/profile_images/fractal_1.jpg"
    
