#!/usr/bin/env python
# coding: utf-8

# # Extractive Text Summary using tfidf representation of text

# This approach summarize a given text by discovering the important sentences with the help of sentences scores
# obtained from the presence of important words. And this importance is measured by a metric known as tf-idf,which
# tells how often any word appear in a document (tf:term frequency) and how often the documents contain the word (idf
# :inverse document frequency)                                                                                                                                                                                                                    .

# In[1]:


#importing libraries
import math
import re
from nltk.corpus import stopwords 
import pickle   


# In[2]:


#for intake of text to be summarized
text=input("Enter Text to be Summarized:\n\n")


# In[3]:


len(text)


# In[4]:


#sentences tokenization
sents=re.split('।',text)


# In[5]:


print(sents)


# In[6]:


documents_size = len(sents)


# In[7]:


documents_size


# In[8]:


words=text.split()


# ## creating word frequency

# In[9]:


def create_frequency_matrix(sentences):
    frequency_matrix = {}
    stopWords = set(stopwords.words("nepali"))

    for sent in sentences:
        freq_table = {}
        words=sent.split()
        for word in words:
            if word in stopWords:
                continue

            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        frequency_matrix[sent[:10]] = freq_table

    return frequency_matrix


# In[10]:


freq_matrix = create_frequency_matrix(sents)


# In[11]:


freq_matrix


# ## creating term frequency matrix

# In[12]:


def create_tf_matrix(freq_matrix):
    tf_matrix = {}

    for sent, f_table in freq_matrix.items():
        tf_table = {}

        count_words_in_sentence = len(f_table)
        for word, count in f_table.items():
            tf_table[word] = count / count_words_in_sentence

        tf_matrix[sent] = tf_table

    return tf_matrix


# In[13]:


tf_matrix = create_tf_matrix(freq_matrix)


# In[14]:


tf_matrix


# ## calculating docs per words

# In[15]:


def create_documents_per_words(freq_matrix):
    word_per_doc_table = {}

    for sent, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in word_per_doc_table:
                word_per_doc_table[word] += 1
            else:
                word_per_doc_table[word] = 1

    return word_per_doc_table


# In[16]:


count_doc_per_words = create_documents_per_words(freq_matrix)


# In[17]:


count_doc_per_words


# ## creating inverse document frequency matrix

# In[18]:


def create_idf_matrix(freq_matrix, count_doc_per_words, documents_size):
    idf_matrix = {}

    for sent, f_table in freq_matrix.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = math.log10(documents_size / float(count_doc_per_words[word]))

        idf_matrix[sent] = idf_table

    return idf_matrix


# In[19]:


idf_matrix = create_idf_matrix(freq_matrix, count_doc_per_words, documents_size)


# In[20]:


idf_matrix


# ## term frequency and inverse document frequency matrix

# In[21]:


def create_tf_idf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

        tf_idf_table = {}

        for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                    f_table2.items()):  
            tf_idf_table[word1] = float(value1 * value2)

        tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix


# In[22]:


tf_idf_matrix = create_tf_idf_matrix(tf_matrix, idf_matrix)


# In[23]:


tf_idf_matrix


# ## calculate sentence scores

# In[24]:


def sentence_scores(tf_idf_matrix) -> dict:
    

    sentenceValue = {}

    for sent, f_table in tf_idf_matrix.items():
        total_score_per_sentence = 0

        count_words_in_sentence = len(f_table)
        for word, score in f_table.items():
            total_score_per_sentence += score
        if count_words_in_sentence !=0:
            sentenceValue[sent] = total_score_per_sentence / count_words_in_sentence
        else:
            sentenceValue[sent]=0
    return sentenceValue


# In[25]:


sentence_scores = sentence_scores(tf_idf_matrix)


# In[26]:


print(sentence_scores)


# ## finding average to set threshold

# In[27]:


def find_average_score(sentenceValue) -> int:
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original summary_text
    average = (sumValues / len(sentenceValue))

    return average


# In[28]:


#average sentence score is set as threshold, ..can try other
threshold = find_average_score(sentence_scores)


# In[29]:


threshold


# ## Finally Generate Summary

# In[30]:


def generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = []

    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] >= (threshold):
            summary.append(sentence)
            sentence_count += 1

    return summary


# In[37]:


summary = '।'.join(generate_summary(sents, sentence_scores,0.8*threshold ))

# In[38]:
filename='model.pkl'
pickle.dump(summary,open(filename,'wb'))
# In[39]:

# In[ ]:





# In[ ]:




