import argparse
import json
from datetime import datetime
import dateutil.parser
import pytz
# from json import JSONDecoder
# from functools import partial

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='Input file', required=False)
parser.add_argument('-o', help='Output file', required=False)
args = parser.parse_args()

def main():
    if args.o[-5:] != '.json':
        print("Output file should have extension .json")
        exit(0)
    json_data = []
    file = open(args.i)
    count = 0
    tcount = 0
    for line in file:
        tcount += 1
        # print("we're at line: ", count)
        # if not valid, go to next

        if not valid_json(line):
            continue
        json_line = json.loads(line)
        # if key is 'title_text', change it to 'title'

        if not validate_title(json_line):
            continue

        if 'title_text' in json_line.keys():
            json_line['title'] = json_line.pop('title_text')

        # check if in iso format, else go to next
        if check_iso(json_line):
            json_line['createdAt'] = convert_utc(json_line['createdAt'])
        else:
            continue

        # if 'author' field is somehow blank, go to next
        if not check_author(json_line):
            continue
        # if there is a 'total_count' field, try casting to int
        # else, do nothing

        # if is_totalcount(json_line):
        if 'total_count' in json_line.keys():
            # if we cannot cast it to int, go to next
            if not cast_int(json_line):
                continue
        # if there is a 'tags' field, separate the words
        # else, do nothing
        if 'tags' in json_line.keys():
            json_line['tags'] = get_tags(json_line)

        count += 1
        json_data.append(json_line)
        # print(f'Line {tcount} is good')
    print(f'Total count: {tcount}\nValid count: {count}')
    print(json_data)

    out_file = args.o
    with open(out_file, 'w') as outfile:
        for idx in range(len(json_data)):
            json.dump(json_data[idx], outfile)
            if idx != len(json_data) - 1:
                outfile.write("\n")

def cast_int(json_line):
    val = json_line['total_count']
    this_type = type(val)
    # we just need to check if the string can be cast into a float.
    # if we can make it a float, we will be able to make it an int
    if this_type == str:
        try:
            nval = float(val)
            return True
        except:
            return False

    else:
        return True

def valid_json(line):
    try:
        json_line = json.loads(line)
        return True
    except:
        return False

def check_author(json_line):
    '''

    :param json_line:
    :return: False if author field is null, N/A or empty, True otherwise
    '''
    if 'author' not in json_line.keys() or json_line['author'] == None or json_line['author'] == "" or json_line['author'] == "N/A" or not json_line['author']:
        return False
    else:
        return True

def is_totalcount(json_line):
    if 'total_count' in json_line.keys():
        return True
    else:
        return False

def get_tags(json_line):
    tag_list = []
    mylist = json_line['tags']
    for element in mylist:
        elem_list = element.split()
        for word in elem_list:
            tag_list.append(word)
    return tag_list

def check_iso(json_line):
    mdate = json_line['createdAt']
    try:
        d = datetime.strptime(mdate, "%Y-%m-%dT%H:%M:%S%z")
        return True
    except ValueError:
        return False

def convert_utc(mdate):
    d = pytz.UTC.normalize(dateutil.parser.parse(mdate))
    return str(d)

def validate_title(json_line):
    if "title" in json_line.keys() or "title text" in json_line.keys():
        return True
    else:
        return False

if __name__ == "__main__":
    main()
