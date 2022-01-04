import json
import argparse
from bs4 import BeautifulSoup
import hashlib
import requests
import os,sys

parser = argparse.ArgumentParser()
parser.add_argument('-c', help='Config file', required=True)
parser.add_argument('-o', help='Output file', required=True)
args = parser.parse_args()

def main():
    config_file = open(args.c)
    config = json.load(config_file)
    cache_dir = config['cache_dir']
    path = os.getcwd()
    abs_cache_dir = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), cache_dir)
    ## if the directory doesn't exist, create it
    if not os.path.isdir(abs_cache_dir):
        os.mkdir(abs_cache_dir)

    celebs = config['target_people']
    data = {}
    for celeb in celebs:
        hash = hashlib.sha1(celeb.encode("UTF-8")).hexdigest()
        ## if the cache exists
        celeb_path = os.path.join(abs_cache_dir, (hash + '.html'))
        if os.path.isfile(celeb_path):
            # read from cache
            print("===READING===")
            relationships = get_rel(celeb_path)

        else:
            print("===FETCHING===")
            with open(celeb_path, 'w') as f:
                content = extract_html(celeb)
                f.write(content)
            relationships = get_rel(celeb_path)

        data[celeb] = relationships

    with open(args.o, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def extract_html(celeb):
    base = 'https://www.whosdatedwho.com/dating/'
    url = base + celeb
    html_content = requests.get(url).text
    return html_content

def get_rel(celeb_path):
    soup = BeautifulSoup(open(celeb_path,'r'),'html.parser')
    d = soup.find_all('div',id=lambda x: x and x.startswith('dating-'))
    relationships= []
    if not d:
        return relationships
    else:
        for row in d:
            raw = row.h4.text
            step1 = raw.split()
            relationship = " ".join(step1)
            relationships.append(relationship)
        return relationships

if __name__ == "__main__":
    main()
