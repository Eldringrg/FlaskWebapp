# -*- coding: utf-8 -*-

import os
from nltk.corpus import stopwords
import re
import math


def myfunc1(text):
    print(len(text))
    sen = re.split('।', text)
    length = len(sen)
    words = text.split()

    def frequency_count(sentences):
        freq_cn = {}
        stopWords = set(stopwords.words("nepali"))

        for sent in sentences:
            freq_table = {}
            words = sent.split()
            for word in words:
                if word in stopWords:
                    continue

                if word in freq_table:
                    freq_table[word] += 1
                else:
                    freq_table[word] = 1

            freq_cn[sent[:10]] = freq_table

        return freq_cn

    freq_matrix = frequency_count(sen)
# print(freq_matrix)

    def create_tf_matrix(freq_matrix):
        tf_matrix = {}

        for sent, f_table in freq_matrix.items():
            tf_table = {}

            count_words_in_sentence = len(f_table)
            for word, count in f_table.items():
                tf_table[word] = count / count_words_in_sentence

            tf_matrix[sent] = tf_table

        return tf_matrix

    tf_matrix = create_tf_matrix(freq_matrix)

    def create_idf_matrix(freq_matrix, count_doc_per_words, length):
        idf_matrix = {}

        for sent, f_table in freq_matrix.items():
            idf_table = {}

            for word in f_table.keys():
                idf_table[word] = math.log10(
                    length / float(count_doc_per_words[word]))

            idf_matrix[sent] = idf_table

        return idf_matrix

    def create_documents_per_words(freq_matrix):
        word_per_doc_table = {}

        for sent, f_table in freq_matrix.items():
            for word, count in f_table.items():
                if word in word_per_doc_table:
                    word_per_doc_table[word] += 1
                else:
                    word_per_doc_table[word] = 1

        return word_per_doc_table

    count_doc_per_words = create_documents_per_words(freq_matrix)

    idf_matrix = create_idf_matrix(freq_matrix, count_doc_per_words, length)

    def create_tf_idf_matrix(tf_matrix, idf_matrix):
        tf_idf_matrix = {}

        for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

            tf_idf_table = {}

            for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                        f_table2.items()):
                tf_idf_table[word1] = float(value1 * value2)

            tf_idf_matrix[sent1] = tf_idf_table

        return tf_idf_matrix

    tf_idf_matrix = create_tf_idf_matrix(tf_matrix, idf_matrix)

    def sentence_scores(tf_idf_matrix) -> dict:

        sentenceValue = {}

        for sent, f_table in tf_idf_matrix.items():
            total_score_per_sentence = 0

            count_words_in_sentence = len(f_table)
            for word, score in f_table.items():
                total_score_per_sentence += score
            if count_words_in_sentence != 0:
                sentenceValue[sent] = total_score_per_sentence / \
                    count_words_in_sentence
            else:
                sentenceValue[sent] = 0
        return sentenceValue

    sentence_scores = sentence_scores(tf_idf_matrix)

    def find_average_score(sentenceValue) -> int:
        sumValues = 0
        for entry in sentenceValue:
            sumValues += sentenceValue[entry]

    # Average value of a sentence from original summary_text
        average = (sumValues / len(sentenceValue))

        return average

    threshold = find_average_score(sentence_scores)

    def generate_summary(sentences, sentenceValue, threshold):
        sentence_count = 0
        summary = []

        for sentence in sentences:
            if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] >= (threshold):
                summary.append(sentence)
                sentence_count += 1

        return summary

    summary = '।'.join(generate_summary(sen, sentence_scores, 0.8*threshold))

    return(summary)
    # return(len(summary))
    # return(text)
