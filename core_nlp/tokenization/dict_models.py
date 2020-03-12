from core_nlp.tokenization.base_tokenizer import BaseTokenizer
from core_nlp.tokenization.utils import load_n_grams, clean_accent_ngrams
import pkg_resources
import logging as logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# pkg_resources.resource_filename('core_nlp', 'tri_grams.txt')
BI_DATA_PATH = pkg_resources.resource_filename('core_nlp', 'tokenization/bi_grams.txt')
TRI_DATA_PATH = pkg_resources.resource_filename('core_nlp', 'tokenization/tri_grams.txt')

# __author__ = "Ha Cao Thanh"
# __copyright__ = "Copyright 2018, DeepAI-Solutions"



class LongMatchingTokenizer(BaseTokenizer):
    def __init__(self, bi_grams_path=BI_DATA_PATH, tri_grams_path=TRI_DATA_PATH, is_accented = True, is_left_right = True, sep_tok = '_'):
        """
        Initial config
        :param bi_grams_path: path to bi-grams set
        :param tri_grams_path: path to tri-grams set
        """
        # logging.info(bi_grams_path)
        # logging.info(tri_grams_path)
        self.is_left_right = is_left_right
        self.sep_tok = sep_tok
        if is_accented:
            self.bi_grams = load_n_grams(bi_grams_path)
            self.tri_grams = load_n_grams(tri_grams_path)
        else:
            self.bi_grams = clean_accent_ngrams(bi_grams_path)
            self.tri_grams = clean_accent_ngrams(tri_grams_path)

    def tokenize(self, text):
        """
        Tokenize text using long-matching algorithm
        :param text: input text
        :return: tokens
        """
        syllables = LongMatchingTokenizer.syllablize(text)
        # print('syllables: ', syllables)
        syl_len = len(syllables)
        curr_id = 0
        word_list = []
        done = False
        # Direction lookup from left to right
        if self.is_left_right:
            while (curr_id < syl_len) and (not done):
                curr_word = syllables[curr_id]
                if curr_id >= (syl_len - 1):
                    word_list.append(curr_word)
                    done = True
                else:
                    next_word = syllables[curr_id + 1]
                    pair_word = ' '.join([curr_word, next_word])
                    if curr_id >= (syl_len - 2):
                        if pair_word in self.bi_grams:
                            word_list.append(self.sep_tok.join([curr_word, next_word]))
                            curr_id += 2
                        else:
                            word_list.append(curr_word)
                            curr_id += 1
                    else:
                        next_next_word = syllables[curr_id + 2]
                        triple_word = ' '.join([pair_word, next_next_word])
                        if triple_word in self.tri_grams:
                            word_list.append(self.sep_tok.join([curr_word, next_word, next_next_word]))
                            curr_id += 3
                        elif pair_word in self.bi_grams:
                            word_list.append(self.sep_tok.join([curr_word, next_word]))
                            curr_id += 2
                        else:
                            word_list.append(curr_word)
                            curr_id += 1
            return word_list
        # If revert lookup direction from right to left
        else:
            curr_id = syl_len - 1
            while (curr_id >= 0) and (not done):
                curr_word = syllables[curr_id]
                if curr_id <= 0:
                    word_list.append(curr_word)
                    done = True
                else:
                    next_word = syllables[curr_id-1]
                    pair_word = ' '.join([next_word, curr_word])
                    if curr_id <= 1:
                        if pair_word in self.bi_grams:
                            word_list.append(self.sep_tok.join([next_word, curr_word]))
                            curr_id -= 2
                        else:
                            word_list.append(curr_word)
                            curr_id -= 1
                    else:
                        next_next_word = syllables[curr_id-2]
                        triple_word = ' '.join([next_next_word, pair_word])
                        if triple_word in self.tri_grams:
                            word_list.append(self.sep_tok.join([next_next_word, next_word, curr_word]))
                            curr_id -= 3
                        elif pair_word in self.bi_grams:
                            word_list.append(self.sep_tok.join([next_word, curr_word]))
                            curr_id -= 2
                        else:
                            word_list.append(curr_word)
                            curr_id -= 1
            return word_list[::-1]


"""Tests"""


def test():
    lm_tokenizer = LongMatchingTokenizer()
    tokens = lm_tokenizer.tokenize("Thuế thu nhập cá nhân")
    print(tokens)


if __name__ == '__main__':
    test()

