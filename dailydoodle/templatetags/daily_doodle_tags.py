from django import template
from dailydoodle.models import UserProfile
from daily_doodle_project.settings import MEDIA_URL

register = template.Library()

@register.inclusion_tag("dailydoodle/nav.html")
def get_nav(current_link=None,user=None):
    # links of format { name: [link,svg_location]}
    user_profile_picture = None
    svgs = {"Homepage": """<svg width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M6.49996 7C7.96131 5.53865 9.5935 4.41899 10.6975 3.74088C11.5021 3.24665 12.4978 3.24665 13.3024 3.74088C14.4064 4.41899 16.0386 5.53865 17.5 7C20.6683 10.1684 20.5 12 20.5 15C20.5 16.4098 20.3895 17.5988 20.2725 18.4632C20.1493 19.3726 19.3561 20 18.4384 20H17C15.8954 20 15 19.1046 15 18V16C15 15.2043 14.6839 14.4413 14.1213 13.8787C13.5587 13.3161 12.7956 13 12 13C11.2043 13 10.4413 13.3161 9.87864 13.8787C9.31603 14.4413 8.99996 15.2043 8.99996 16V18C8.99996 19.1046 8.10453 20 6.99996 20H5.56152C4.64378 20 3.85061 19.3726 3.72745 18.4631C3.61039 17.5988 3.49997 16.4098 3.49997 15C3.49997 12 3.33157 10.1684 6.49996 7Z" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""","Collections": """<svg width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M22 11V17C22 21 21 22 17 22H7C3 22 2 21 2 17V7C2 3 3 2 7 2H8.5C10 2 10.33 2.44 10.9 3.2L12.4 5.2C12.78 5.7 13 6 14 6H17C21 6 22 7 22 11Z" stroke="#C0D0E7" stroke-width="2.5" stroke-miterlimit="10"/>
<path opacity="0.4" d="M8 2H17C19 2 20 3 20 5V6.38" stroke="#C0D0E7" stroke-width="2.5" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""", "Profile": """<svg width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M17.5 21.0001H6.5C5.11929 21.0001 4 19.8808 4 18.5001C4 14.4194 10 14.5001 12 14.5001C14 14.5001 20 14.4194 20 18.5001C20 19.8808 18.8807 21.0001 17.5 21.0001Z" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""","Leaderboard": """<svg width="800px" height="800px" viewBox="0 0 20 15" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M18 14.75H2.00003C1.73942 14.7581 1.47985 14.7135 1.23685 14.619C0.993841 14.5245 0.772371 14.382 0.585691 14.2C0.399001 14.018 0.250921 13.8002 0.150291 13.5596C0.0496708 13.3191 -0.00143917 13.0607 3.08314e-05 12.8V7.27C0.0130808 6.7483 0.229541 6.2523 0.603201 5.888C0.976871 5.5237 1.47815 5.3198 2.00003 5.32H4.87003C4.92913 5.32 4.98764 5.3084 5.04224 5.2858C5.09683 5.2631 5.14644 5.23 5.18823 5.1882C5.23001 5.1464 5.26316 5.0968 5.28578 5.0422C5.30839 4.98762 5.32003 4.92911 5.32003 4.87001V2.87001C5.33271 2.35683 5.54222 1.86817 5.90521 1.50519C6.26819 1.14221 6.75685 0.93269 7.27003 0.92001H12.83C13.3604 0.92001 13.8691 1.13073 14.2442 1.5058C14.6193 1.88087 14.83 2.38958 14.83 2.92001V7.39C14.83 7.5094 14.8774 7.6238 14.9618 7.7082C15.0462 7.7926 15.1607 7.84 15.28 7.84H18C18.52 7.8556 19.0134 8.0732 19.3756 8.4466C19.7378 8.82 19.9402 9.3198 19.94 9.84V12.8C19.9413 13.0556 19.8921 13.309 19.7952 13.5455C19.6983 13.782 19.5556 13.9971 19.3753 14.1783C19.1951 14.3595 18.9807 14.5033 18.7447 14.6014C18.5087 14.6995 18.2556 14.75 18 14.75ZM2.00003 6.82C1.88242 6.8226 1.77052 6.8712 1.68828 6.9553C1.60604 7.0394 1.56 7.1524 1.56003 7.27V12.8C1.56 12.9176 1.60604 13.0306 1.68828 13.1147C1.77052 13.1988 1.88242 13.2474 2.00003 13.25H18C18.1176 13.2474 18.2295 13.1988 18.3118 13.1147C18.394 13.0306 18.44 12.9176 18.44 12.8V9.74C18.44 9.6224 18.394 9.5094 18.3118 9.4253C18.2295 9.3412 18.1176 9.2926 18 9.29H15.23C14.7081 9.2902 14.2068 9.0863 13.8332 8.722C13.4595 8.3577 13.243 7.8617 13.23 7.34V2.87001C13.23 2.75067 13.1826 2.63621 13.0982 2.55182C13.0138 2.46742 12.8993 2.42001 12.78 2.42001H7.27003C7.15068 2.42001 7.03622 2.46742 6.95183 2.55182C6.86744 2.63621 6.82003 2.75067 6.82003 2.87001V4.87001C6.82019 5.3919 6.61636 5.8932 6.25203 6.2668C5.8877 6.6405 5.39175 6.857 4.87003 6.87L2.00003 6.82Z" fill="#C0D0E7"/>
</svg>
""","Logout": """<svg width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M14 20H6C4.89543 20 4 19.1046 4 18L4 6C4 4.89543 4.89543 4 6 4H14M10 12H21M21 12L18 15M21 12L18 9" stroke="#C0D0E7" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""","Register": """<svg width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M14 4L17.5 4C20.5577 4 20.5 8 20.5 12C20.5 16 20.5577 20 17.5 20H14M15 12L3 12M15 12L11 16M15 12L11 8" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""","Login": """<svg width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M14 4L17.5 4C20.5577 4 20.5 8 20.5 12C20.5 16 20.5577 20 17.5 20H14M15 12L3 12M15 12L11 16M15 12L11 8" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""","My Submissions": """<svg width="800px" height="800px" viewBox="0 0 20 23" fill="none" xmlns="http://www.w3.org/2000/svg">
<path fill-rule="evenodd" clip-rule="evenodd" d="M15.6667 1.66667H6.33335C4.86059 1.66667 3.66669 2.86058 3.66669 4.33334V16.3333C3.66669 17.8061 4.86059 19 6.33335 19H15.6667C17.1394 19 18.3334 17.8061 18.3334 16.3333V4.33334C18.3334 2.86058 17.1394 1.66667 15.6667 1.66667Z" stroke="#C0D0E7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M3.66667 4.33334C2.19391 4.33334 1 5.52725 1 7.00001V17.6667C1 19.8758 2.79086 21.6667 5 21.6667H13C14.4728 21.6667 15.6667 20.4728 15.6667 19" stroke="#C0D0E7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""}
    # adds tailwind classes to svgs and adjusts their stroke and stroke-widths
    for key,svg in svgs.items():
        svg = svg.replace('width="800px" height="800px"','class="h-5 mr-1 "')
        svg = svg.replace('stroke="#000000" stroke-width="1.5"','stroke="#C0D0E7" stroke-width="2.5"')
        svgs[key] = svg
    locked_links = {"Collections": ["dailydoodle:collections",svgs["Collections"]],
                    "My Submissions": ["dailydoodle:submissions",svgs["My Submissions"]],
                    "Profile": ["dailydoodle:profile",svgs["Profile"]],
                    "Leaderboard": ["dailydoodle:leaderboard",svgs["Leaderboard"]],
                    "Logout": ["auth_logout",svgs["Logout"]],
                    }
    if(user.username):
        user_profile_picture = UserProfile.objects.filter(user=user)[0].profile_picture
    all_links = {"Homepage": ["dailydoodle:index",svgs["Homepage"]]}
    non_locked_links = {"Register": ["registration_register",svgs["Register"]],"Login": ["auth_login",svgs["Login"]]}
    return {"all_links": all_links,"non_locked_links": non_locked_links,"locked_links": locked_links,"current_link": current_link,"user":user,"user_profile_picture":user_profile_picture,"MEDIA_URL": MEDIA_URL}

@register.inclusion_tag("dailydoodle/user_snippet.html")
def user_snippet(user_profile_picture=None,username=None,upvotes=None,):
    return {"username": username, "user_profile_picture": user_profile_picture, "upvotes": upvotes ,"MEDIA_URL": MEDIA_URL}