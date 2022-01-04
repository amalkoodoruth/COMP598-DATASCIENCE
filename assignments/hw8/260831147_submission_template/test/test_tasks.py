import unittest
from pathlib import Path
import os, sys
import json
import pandas as pd


from src.compile_word_counts import get_counts_pony, get_counts, get_stopwords
from src.compute_pony_lang import get_tf_idf_dict, get_output_dict

parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        
        

    def test_task1(self):
        # use  self.mock_dialog and self.true_word_counts; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        df = pd.read_csv(self.mock_dialog)
        stopwords = get_stopwords()
        word_count = get_counts(df, stopwords)
        words_dict = get_counts_pony(df, stopwords, word_count)
        with open(self.true_word_counts,'r') as file:
            mdict = json.load(file)
        self.assertDictEqual(words_dict, mdict)


    def test_task2(self):
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)

        with open(self.true_word_counts, 'r') as file:
            words_dict = json.load(file)

        tf_idf_dict = get_tf_idf_dict(words_dict)

        # output_dict = get_output_dict(tf_idf_dict,3)

        with open(self.true_tf_idfs,'r') as tf:
            mdict = json.load(tf)
        # print(tf_idf_dict)
        self.assertDictEqual(tf_idf_dict, mdict)
        
    
if __name__ == '__main__':
    unittest.main()