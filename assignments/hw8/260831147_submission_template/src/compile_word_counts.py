import pandas as pd
import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument('-o', help='Output file', required=False)
parser.add_argument('-d', help='Dataset', required=False)
args = parser.parse_args()

def main():

    out_dir, file_name = os.path.split(args.o)
        # if directory does not exist, create it
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    df = pd.read_csv(args.d)

    stopwords = get_stopwords()
    word_count = get_counts(df, stopwords)
    words_dict = get_counts_pony(df, stopwords, word_count)

    with open(args.o, "w") as out:
        json.dump(words_dict, out, indent=4)

    return 0

def get_counts_pony(df, stopwords, word_count):
    ponies = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]
    words_dict = {key: {} for key in ponies}
    for index, row in df.iterrows():
        pony = row['pony']
        pony = pony.lower()
        if pony in ponies:
            text = row['dialog']
            tokenized_text = clean_text(text, stopwords)
            for word in tokenized_text:
                if word_count[word] >= 5:
                    if word in words_dict[pony]:
                        words_dict[pony][word] += 1
                    else:
                        words_dict[pony][word] = 1

    return words_dict

def get_counts(df, stopwords):
    word_count = {}
    ponies = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]
    for index, row in df.iterrows():
        pony = row['pony']
        pony = pony.lower()
        if pony in ponies:
            text = row['dialog']
            tokenized_text = clean_text(text, stopwords)
            for word in tokenized_text:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
    return word_count

def clean_text(text, stopwords):
    text = str(text)
    # text = ''.join([i for i in text if not i.isdigit()])
    text = text.lower()
    for x in ["(", ")", "[", "]", ",", "-", ".", "?", "!", ":", ";", "#", "&", '"']:
        text = text.replace(x, " ")
    lower = text.split()
    mylist = []
    for word in lower:
        # if not any(char.isdigit() for char in word):
        if word.isalpha():
            if word not in stopwords:
                mylist.append(word)
    return mylist


def get_stopwords():
    stopwords = []
    yourpath = os.getcwd()
    parent = os.path.abspath(os.path.join(yourpath, os.pardir))
    folder = os.path.basename(parent)
    if folder == 'submission_template':
        dir = parent + "/data/stopwords.txt"
    else:
        dir = yourpath + "/data/stopwords.txt"
    # dir = dir + "/data/stopwords.txt"
    with open(dir) as stop:
        for line in stop:
            if line[0] == "#":
                continue
            if line[-1:] == "\n":
                length = len(line)
                stopwords.append(line[0:length-1])
            else:
                stopwords.append(line)
    return stopwords

if __name__ == "__main__":
    main()