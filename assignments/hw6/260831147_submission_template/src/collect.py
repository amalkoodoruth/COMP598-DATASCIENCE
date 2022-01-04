import requests
import os.path as osp
import requests.auth
import os, sys
import json

CACHE_FILE = 'n.cache.json'
path = os.getcwd()
SAMPLE1 = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), 'sample1.json')
SAMPLE2 = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), 'sample2.json')
# CLIENT_ID = '-vTkW9j8N_bLhOjqtQpthA'
CLIENT_ID = 'cui56X5nsYbwPKcp4rX23Q'
# SECRET = '-u5GPcmtHxFTOMA79k83AdQYcXoMpQ'
SECRET = 'HytxTa_SBatcGFpasvtnTcJPS7F_mw'
USER_AGENT = 'data science'


def main():
    sample1 = ["funny", "AskReddit", "gaming", "aww", "pics", "Music", "science", "worldnews", "videos", "todayilearned"]
    # sample1 = ["mcgill"]
    sample2 = ["AskReddit", "memes", "politics", "nfl", "nba", "wallstreetbets", "teenagers", "PublicFreakout", "leagueoflegends", "unpopularopinion"]
    base_url = "https://oauth.reddit.com/r/"

    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET)

    data = {
        'grant_type': 'password',
        'username': 'Senior-Advantage5844',
        'password': "7j'xnPfb!uWvhv&"
    }

    headers = {'User-Agent': 'MyAPI/0.0.1'}

    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)

    print('------')
    print(res.json())
    TOKEN = res.json()['access_token']

    headers['Authorization'] = f'bearer {TOKEN}'

    sample1_posts = []
    sample2_posts = []
    for subr in sample1:
        url = base_url + subr + "/new.json?limit=100"

        posts = get_titles(url, headers)
        sample1_posts.append(posts)
    with open(SAMPLE1, 'w') as outfile:
        for idx in range(len(sample1_posts)):
            json.dump(sample1_posts[idx], outfile)
            if idx != len(sample1_posts) - 1:
                outfile.write("\n")


    for subr in sample2:
        url = base_url + subr + "/new.json?limit=100"
        posts = get_titles(url, headers)
        sample2_posts.append(posts)
        # print(len(titles))
    with open(SAMPLE2, 'w') as outfile:
        for idx in range(len(sample2_posts)):
            json.dump(sample2_posts[idx], outfile)
            if idx != len(sample2_posts) - 1:
                outfile.write("\n")
    return

def get_titles(url, headers):

    print(f"Getting URL: {url}")
    r = requests.get(url, headers=headers)
    root_elem = r.json()
    posts = root_elem['data']['children']

    return posts

if __name__ == "__main__":
    main()