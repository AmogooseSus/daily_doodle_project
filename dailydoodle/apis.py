# helper functions to use apis
from daily_doodle_project.settings import env,MEDIA_ROOT
import requests
import json
import shutil
import random

# helper function used to get a random prompt daily
def get_random_prompt():
    # use requests api with api key to get a word
    api_url = 'https://api.api-ninjas.com/v1/randomword?type=verb'
    response = requests.get(api_url, headers={'X-Api-Key': env("NINJAS_KEY")})
    #verify response 
    if response.status_code == requests.codes.ok:
        print("TODAYS WORD ",response.json()["word"])
        return response.json()["word"]
    else:
        print("Error:", response.status_code, response.text, "BASCIALLY THE PROMPT API DIED SO WE USE A RANDOM WORD IN OUR LONG LIST")
    return random.choice(word_list)
    

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
                to_copy = open(f"{MEDIA_ROOT}/profile_images/cat.png","rb")
                shutil.copyfileobj(to_copy,out_file)
        print("Random Image API Error:", response.status_code, response.text)
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

     
    

word_list = ['abandoned', 'able', 'absolute', 'adorable', 'adventurous', 'academic', 'acceptable', 'acclaimed', 'accomplished', 'accurate', 'aching', 'acidic', 'acrobatic', 'active', 'actual', 'adept', 'admirable', 'admired', 'adolescent', 'adorable', 'adored', 'advanced', 'afraid', 'affectionate', 'aged', 'aggravating', 'aggressive', 'agile', 'agitated', 'agonizing', 'agreeable', 'ajar', 'alarmed', 'alarming', 'alert', 'alienated', 'alive', 'all', 'altruistic', 'amazing', 'ambitious', 'ample', 'amused', 'amusing', 'anchored', 'ancient', 'angelic', 'angry', 'anguished', 'animated', 'annual', 'another', 'antique', 'anxious', 'any', 'apprehensive', 'appropriate', 'apt', 'arctic', 'arid', 'aromatic', 'artistic', 'ashamed', 'assured', 'astonishing', 'athletic', 'attached', 'attentive', 'attractive', 'austere', 'authentic', 'authorized', 'automatic', 'avaricious', 'average', 'aware', 'awesome', 'awful', 'awkward', 'babyish', 'bad', 'back', 'baggy', 'bare', 'barren', 'basic', 'beautiful', 'belated', 'beloved', 'beneficial', 'better', 'best', 'bewitched', 'big', 'big-hearted', 'biodegradable', 'bite-sized', 'bitter', 'black', 'black-and-white', 'bland', 'blank', 'blaring', 'bleak', 'blind', 'blissful', 'blond', 'blue', 'blushing', 'bogus', 'boiling', 'bold', 'bony', 'boring', 'bossy', 'both', 'bouncy', 'bountiful', 'bowed', 'brave', 'breakable', 'brief', 'bright', 'brilliant', 'brisk', 'broken', 'bronze', 'brown', 'bruised', 'bubbly', 'bulky', 'bumpy', 'buoyant', 'burdensome', 'burly', 'bustling', 'busy', 'buttery', 'buzzing', 'calculating', 'calm', 'candid', 'canine', 'capital', 'carefree', 'careful', 'careless', 'caring', 'cautious', 'cavernous', 'celebrated', 'charming', 'cheap', 'cheerful', 'cheery', 'chief', 'chilly', 'chubby', 'circular', 'classic', 'clean', 'clear', 'clear-cut', 'clever', 'close', 'closed', 'cloudy', 'clueless', 'clumsy', 'cluttered', 'coarse', 'cold', 'colorful', 'colorless', 'colossal', 'comfortable', 'common', 'compassionate', 'competent', 'complete', 'complex', 'complicated', 'composed', 'concerned', 'concrete', 'confused', 'conscious', 'considerate', 'constant', 'content', 'conventional', 'cooked', 'cool', 'cooperative', 'coordinated',]
