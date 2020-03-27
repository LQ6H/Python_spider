#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author LQ6H

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import jieba

words=pd.read_csv('stopwords_zh.txt',error_bad_lines=False,engine='python',names=['stopword'])

stopwords=set('')
stopwords.update(words['stopword'])

with open('comments.txt','r',encoding='utf-8') as f:
    text=' '.join(jieba.cut(f.read(),cut_all=False))

backgroud_Image=plt.imread('kobe.jpg')

wc=WordCloud(
    background_color='white',
    mask=backgroud_Image,
    font_path='hei.ttf',
    max_words=200,
    max_font_size=200,
    min_font_size=8,
    random_state=50,
    stopwords=stopwords,
)

word_cloud=wc.generate_from_text(text)

process_word=WordCloud.process_text(wc,text)
sort=sorted(process_word.items(),key=lambda e:e[1],reverse=True)
sort_after=sort[:50]
print(sort_after)

df=pd.DataFrame(sort_after)

# 保证不乱码
df.to_csv('sort_after.csv',encoding='utf_8_sig')

plt.imshow(word_cloud)
plt.axis('off')

wc.to_file('word_kobe.jpg')