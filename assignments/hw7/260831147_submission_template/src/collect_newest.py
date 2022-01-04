import requests
import os.path as osp
import requests.auth
import os, sys
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', help='Output file', required=True)
parser.add_argument('-s', help='Subreddit', required=True)
args = parser.parse_args()

path = os.getcwd()
if args.s == '/r/mcgill':
    destination = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), args.o)
elif args.s == '/r/concordia':
    destination = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), args.o)
else:
    exit(0)
# CLIENT_ID = '-vTkW9j8N_bLhOjqtQpthA'
CLIENT_ID = 'cui56X5nsYbwPKcp4rX23Q'
# SECRET = '-u5GPcmtHxFTOMA79k83AdQYcXoMpQ'
SECRET = 'HytxTa_SBatcGFpasvtnTcJPS7F_mw'
USER_AGENT = 'data science'

def main():

    base_url = "https://oauth.reddit.com"

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

    subr = args.s
    url =  base_url + subr + "/new.json?limit=100"

    posts, names = get_titles_and_names(url, headers)

    with open(destination, 'w') as outfile:
        print("Writing...")
        for idx in range(len(posts)):
            dict = {}
            dict[names[idx]] = posts[idx]
            json.dump(dict, outfile)
            if idx != len(posts)-1:
                outfile.write("\n")

    print("Complete!")

    return

def get_titles_and_names(url, headers):
    titles = []
    names = []
    print(f"Getting URL: {url}")
    r = requests.get(url, headers=headers)
    root_elem = r.json()
    posts = root_elem['data']['children']

    for post in posts:
        title = post['data']['title']
        titles.append(title)

        name = post['data']['name']
        names.append(name)

    return titles, names

if __name__ == "__main__":
    main()