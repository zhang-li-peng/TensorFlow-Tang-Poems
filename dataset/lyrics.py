
import collections
import os
import sys
import numpy as np
from utils.clean_cn import clean_cn_corpus
import jieba
import pickle
import codecs

start_token = 'G'
end_token = 'E'

segment_list_file = os.path.abspath('./dataset/data/lyric_seg.pkl')


def process_lyrics(file_name):
    base_dir = os.path.dirname(file_name)
    save_file = os.path.join(base_dir, os.path.basename(file_name).split('.')[0] + '_cleaned.txt')
    start_token = 'G'
    end_token = 'E'
    if not os.path.exists(save_file):
        clean_cn_corpus(file_name, clean_level='all', is_save=False)
    else:
        pass

    with codecs.open(save_file, 'r', encoding="utf-8") as f:
        lyrics = []
        for line in f.readlines():
            if len(line) < 40:
                continue
            line = start_token + line + end_token
            lyrics.append(line)
        lyrics = sorted(lyrics, key=lambda line: len(line))
        print('all %d songs...' % len(lyrics))

    # if not os.path.exists(os.path.dirname(segment_list_file)):
    #     os.mkdir(os.path.dirname(segment_list_file))
    # if os.path.exists(segment_list_file):
    #     print('load segment file from %s' % segment_list_file)
    #     with open(segment_list_file, 'rb') as p:
    #         all_words = pickle.load(p)
    # else:
    all_words = []
    for lyric in lyrics:
        all_words += jieba.lcut(lyric, cut_all=False)
        # with open(segment_list_file, 'wb') as p:
        #     pickle.dump(all_words, p)
        #     print('segment result have been save into %s' % segment_list_file)

    # calculate how many time appear per word
    counter = collections.Counter(all_words)
    print(counter['E'])
    # sorted depends on frequent
    counter_pairs = sorted(counter.items(), key=lambda x: -x[1])
    words, _ = zip(*counter_pairs)
    print('E' in words)

    words = words[:len(words)] + (' ',)
    word_int_map = dict(zip(words, range(len(words))))
    # translate all lyrics into int vector
    lyrics_vector = [list(map(lambda word: word_int_map.get(word, len(words)), lyric)) for lyric in lyrics]
    return lyrics_vector, word_int_map, words


def generate_batch(batch_size, lyrics_vec, word_to_int):
    # split all lyrics into n_chunks * batch_size
    n_chunk = len(lyrics_vec) // batch_size
    x_batches = []
    y_batches = []
    for i in range(n_chunk):
        start_index = i * batch_size
        end_index = start_index + batch_size

        batches = lyrics_vec[start_index:end_index]
        # very batches length depends on the longest lyric
        length = max(map(len, batches))
        # 填充一个这么大小的空batch，空的地方放空格对应的index标号
        x_data = np.full((batch_size, length), word_to_int[' '], np.int32)
        for row in range(batch_size):
            x_data[row, :len(batches[row])] = batches[row]
        y_data = np.copy(x_data)
        # y的话就是x向左边也就是前面移动一个
        y_data[:, :-1] = x_data[:, 1:]
        """
        x_data             y_data
        [6,2,4,6,9]       [2,4,6,9,9]
        [1,4,2,8,5]       [4,2,8,5,5]
        """
        x_batches.append(x_data)
        y_batches.append(y_data)
    return x_batches, y_batches

