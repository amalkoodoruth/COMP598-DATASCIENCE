import os
import argparse
import json
import random

parser = argparse.ArgumentParser()
parser.add_argument('-o', help='Output file', required=True)
parser.add_argument('json_file', help='JSON file')
parser.add_argument('num_posts_to_output', help='Number of posts to output')
args = parser.parse_args()

def main():
    path = os.getcwd()
    json_file = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), args.json_file)
    out_file = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), args.o)
    num_posts = int(args.num_posts_to_output)
    with open(json_file,'r') as jf:
        print("Reading json file...")
        count = 0
        names = []
        titles = []
        for line in jf:
            count += 1
            post = json.loads(line)
            for name, title in post.items():
                names.append(name)
                titles.append(title)
    print("Read!")
    if num_posts < count:
        indices = random.sample(range(0, count), num_posts)
        indices.sort()
    else:
        indices = [x for x in range(count)]

    with open(out_file, 'w') as f:
        print("Writing output file...")
        f.write('{}\t{}\t{}\n'.format("Name", "title", "coding"))
        for idx in indices:
            if idx != indices[-1]:
                f.write('{}\t{}\t\n'.format(names[idx], '"'+ titles[idx] + '"'))
            else:
                f.write('{}\t{}\t'.format(names[idx], '"' + titles[idx] + '"'))
    print("Complete!")


if __name__ == "__main__":
    main()