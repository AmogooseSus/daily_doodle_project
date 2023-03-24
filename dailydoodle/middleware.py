# This custom middleware allows us to query 
# and add a new prompt when there is a request made
# for the next day but no prompt exists in the database

# We ensure that no two users can add a prompt by 
# using a mutex


from dailydoodle.apis import get_random_prompt
from dailydoodle.models import Prompt
from datetime import date
from django.db import transaction


class PromptMiddleware:

    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):   
        response = self.get_response(request)
        return response
    
    def process_view(self,request,view_func,view_args,view_kwargs):
        expected_date = date.today()
        todays_prompt = Prompt.objects.filter(prompt_date=expected_date)
        if(not len(todays_prompt) == 0):
            return
        next_prompt = get_random_prompt()
        while(len(Prompt.objects.filter(prompt=next_prompt)) != 0 and next_prompt != None):
            next_prompt = get_random_prompt()
        # lock this critical section so no 2 users can activate this middleware at the same time and hence generating a new prompt
        print(next_prompt)
        with transaction.atomic():
            Prompt.objects.create(prompt=next_prompt,prompt_date=date.today())


       

