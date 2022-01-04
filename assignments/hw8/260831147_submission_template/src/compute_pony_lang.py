import argparse
import json
import math

parser = argparse.ArgumentParser()
parser.add_argument('-c', help='Input file', required=False)
parser.add_argument('-n', help='Number of words', required=False)
args = parser.parse_args()

def main():
    with open(args.c,"r") as input:
        words_dict = json.load(input)

    tf_idf_dict = get_tf_idf_dict(words_dict)
    if args.n:
        n = int(args.n)
    else:
        n = 3
    output_dict = get_output_dict(tf_idf_dict,n)
    print(output_dict)

    return

def get_output_dict(tf_idf_dict,n):
    output_dict = {}

    for pony in tf_idf_dict:
        high_list = get_n_highest(tf_idf_dict[pony], n)
        output_dict[pony] = high_list

    return output_dict

def get_tf_idf_dict(words_dict):
    ponies = ["twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy"]
    tf_idf_dict = {key: {} for key in ponies}
    for pony in words_dict:
        for word in words_dict[pony]:
            tf_idf = get_tf_idf(word, pony, words_dict) #tf-idf for that pony and for that word
            tf_idf_dict[pony][word] = tf_idf
    return tf_idf_dict

def get_n_highest(tf_idf_dict, n):

    mlist = []
    if tf_idf_dict:
        sorted_tuples = sorted(tf_idf_dict.items(), key=lambda item: item[1], reverse=True)
        # print(tf_idf_dict)
        # print(len(sorted_tuples))
        for i in range(n):
            mlist.append(sorted_tuples[i][0])
    return mlist

def get_tf_idf(word, pony, words_dict):
    tf = float(words_dict[pony][word])
    ponies_using = 0

    for this_pony in words_dict:
        if word in words_dict[this_pony]:
            ponies_using += 1
    idf = math.log(float(6/ponies_using), 10)
    tf_idf = tf * idf
    return round(tf_idf, 4)


if __name__ == "__main__":
    main()