import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('sample_path')
# parser.add_argument('-o', help='Output file', required=False)
args = parser.parse_args()

def main():
    counter = 0
    file = open(args.sample_path)
    titles = []
    for line in file:

        posts = json.loads(line)
        for post in posts:
            title = post['data']['title']
            titles.append(title)

    average = get_average_length(titles)
    print(f"Average title length: {average}")

    return

def get_average_length(titles):
    total = 0
    for title in titles:
        total += len(title)
    average = total / len(titles)
    return round(average,2)

if __name__ == "__main__":
    main()