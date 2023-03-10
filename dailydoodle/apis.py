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
        print("TODAYS WORD ",response.json()["word"])
        return response.json()["word"]
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
                to_copy = open(f"{MEDIA_ROOT}/profile_images/fractal_1.png","rb")
                shutil.copyfileobj(to_copy,out_file)
        print("Error:", response.status_code, response.text)
        return f"/profile_images/{username}.jpg"
    
# helper function used to query unsplash api for pictures for a certain search query
def get_references(query,page=1,per_page=10,orientation="landscape"):
    key = env("UNSPLASH_ACCESS_KEY")
    end_point = f"https://api.unsplash.com/search/photos?client_id={key}&page={page}&per_page={per_page}&query={query}&orientation={orientation}"
    response = requests.get(end_point)
    if response.status_code == requests.codes.ok:
          # returnd data of form [link1,link2,....,link{perpage}]
          data = response.json()
          output = []
          for x in data["results"]:
               output.append({"thumb": x["urls"]["thumb"],"small": x["urls"]["small"]})
          return output
    else:
         print("Error:",response.status_code,response.text)

     
    
