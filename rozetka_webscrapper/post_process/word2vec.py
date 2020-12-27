#pip install git+https://github.com/mit-nlp/MITIE.git
from mitie import *
from collections import defaultdict
from scipy import sparse
import re
import json

import numpy as np

from tqdm import tqdm
from keras.models import Input, Model
from keras.layers import Dense

import settings
from model.item import Item

import files.file_writer as fw
import files.file_reader as fr


#preprocessing
def clean_text(
    string: str, 
    punctuations=r'''!()-[]{};:'"\,<>./?@#$%^&*_~''',
    stop_words=['и', 'или', 'иначе', 'это', 'так', 'будут', 'быть', 'что', 'то', 'как', 'або', 'чи', 'потому']) -> str:
    """
    A method to clean text 
    """
    # Cleaning the urls
    string = re.sub(r'https?://\S+|www\.\S+', ' ', string)

    # Cleaning the html elements
    string = re.sub(r'<.*?>', ' ', string)
    
    # Cleaning not words symbols
    string = re.sub(r'\W+', ' ', string)

    # Removing the punctuations
    for x in string.lower(): 
        if x in punctuations: 
            string = string.replace(x, ' ')

    # Converting the text to lower
    string = string.lower()

    # Removing stop words
    string = ' '.join([word for word in string.split() if word not in stop_words])

    # Cleaning the whitespaces
    string = re.sub(r'\s+', ' ', string).strip()

    return string

def parse_item(
        item: Item,
        use_preprocessor : bool = True
    ):
    return clean_text(item.description) if use_preprocessor else item.description.replace('\\','').replace('"','').replace('\'','').lower()

def create_pairs(texts, window_size = 2):

    # Creating a placeholder for the scanning of the word list
    word_lists = []
    all_text = []

    for text in texts:
        #split to words
        text = text.split(' ')
        # Appending to the all text list
        all_text += text 

        # Creating a context dictionary
        for i, word in enumerate(text):
            for w in range(window_size):
                # Getting the context that is ahead by *window* words
                if i + 1 + w < len(text): 
                    word_lists.append([word] + [text[(i + 1 + w)]])
                # Getting the context that is behind by *window* words
                if i - w - 1 >= 0:
                    word_lists.append([word] + [text[(i - w - 1)]])
    return word_lists, all_text

def create_unique_word_dict(text:list) -> dict:
    """
    A method that creates a dictionary where the keys are unique words
    and key values are indices
    """
    # Getting all the unique words from our text and sorting them alphabetically
    words = list(set(text))
    words.sort()

    # Creating the dictionary for the unique words
    unique_word_dict = {}
    for i, word in enumerate(words):
        unique_word_dict.update({
            word: i
        })

    return unique_word_dict 


def create_matrices(unique_word_dict, word_lists, max_iterations_count = 0):

    # Defining the number of features (unique words)
    n_words = len(unique_word_dict)

    # Creating the X and Y matrices using one hot encoding
    X = np.empty([0, n_words], dtype=float)
    Y = np.empty([0, n_words], dtype=float)

    for i, word_list in tqdm(enumerate(word_lists)):
        if max_iterations_count > 0 and i >= max_iterations_count:
            break
        # Getting the indices
        main_word_index = unique_word_dict.get(word_list[0])
        context_word_index = unique_word_dict.get(word_list[1])

        # Creating the placeholders   
        X_row = np.zeros(n_words)
        Y_row = np.zeros(n_words)

        # One hot encoding the main word
        X_row[main_word_index] = 1

        # One hot encoding the Y matrix words 
        Y_row[context_word_index] = 1

        # Appending to the main matrices
        X = np.append(X, [X_row], axis=0) #extremely slow
        Y = np.append(Y, [Y_row], axis=0) #extremely slow

    return X, Y


def model_fit(X, Y, unique_word_dict, embed_size=2):
    # Defining the neural network
    inp = Input(shape=(X.shape[1],))
    x = Dense(units=embed_size, activation='linear')(inp)
    x = Dense(units=Y.shape[1], activation='softmax')(x)
    model = Model(inputs=inp, outputs=x)
    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam')

    # Optimizing the network weights
    model.fit(
        x=X, 
        y=Y, 
        batch_size=512, #256
        epochs=1000 #700 #1000
        )

    # The input layer 
    weights = model.get_weights()[0]
    words = list(unique_word_dict.keys())

    # Creating a dictionary to store the embeddings in. The key is a unique word and 
    # the value is the numeric vector
    embedding_dict = {}
    for word in words: 
        embedding_dict.update({
            word: weights[unique_word_dict.get(word)].tolist() #save as py array
            })
    return embedding_dict


def process_from_scratch(data):
    texts_list = []
    print("Collecting descriptions")
    descriptions_counter = 0
    for c in data:
        for g in c.groups:
            for i in g.items:
                if len(i.description) > settings.POSTPROCESS_WORD2VEC_MIN_DESCRIPTION_LENGTH: #if description is valuable
                    x = parse_item(i, use_preprocessor = True)
                    texts_list.append(x)
                    descriptions_counter += 1
                    print('Descriptions collected:', descriptions_counter, end = '\r')
    print('Descriptions collected:', descriptions_counter)

    print("Creating pairs")
    word_lists, all_text = create_pairs(texts_list)
    print("Select distinct words")
    unique_dict = create_unique_word_dict(all_text)
    print("Create matrices for deep learning")
    x, y = create_matrices(unique_dict, word_lists, settings.POSTPROCESS_WORD2VEC_MAT_PAIRS_ITERATIONS)
    print("\nModel fitting")
    embedding_dict = model_fit(x, y, unique_dict,  2)

    print("Save word2vec in file")
    fw.write_plain(
        settings.WORD2VEC_RELATIVE_FILE_PATH_STRING.format('dictionary'),
        json.dumps(embedding_dict, ensure_ascii = False, indent = 4)
    )
    return process_w2v_data(embedding_dict)





import matplotlib.pyplot as plt
from post_process.kNN import ClusterWorker, distance

def clear_if_distance_to_origin_more(points, max_distance):
    changed = []
    for p in points:
        if distance(p, [0.0, 0.0]) <= max_distance:
            changed.append(p)
    return changed


def preview_annotated(w2v_dict, preview_start, preview_size):
    print("Displaying cloud of size:", min(preview_size, max(0, len(w2v_dict) - preview_start)))
    prepared_count = 0
    x_arr = []
    y_arr = []
    for word in list(w2v_dict.keys()):
        prepared_count += 1
        if preview_start > prepared_count:
            continue
        if prepared_count >= preview_size:
            break
        coord = w2v_dict.get(word)
        x_arr.append(coord[0])
        y_arr.append(coord[1])
        plt.annotate(word, (coord[0], coord[1]))
    plt.scatter(x_arr, y_arr)
    plt.show()


def process_w2v_data(w2v_dict):
    print("Displaying cloud of size:", len(w2v_dict))

    prepared_count = 0
    x_arr = []
    y_arr = []
    for word in list(w2v_dict.keys()):
        coord = w2v_dict.get(word)
        x_arr.append(coord[0])
        y_arr.append(coord[1])
        #plt.annotate(word, (coord[0], coord[1])) #too slow and messy
        #prepared_count += 1
    plt.figure(1)
    plt.scatter(x_arr, y_arr)
    plt.draw()
    plt.pause(0.001)
    #plt.show()

    #Clusterize
    print("K-nearest-neighbours clusterization")
    #Clear small messy words #TODO
    points = list(w2v_dict.values()) #clear_if_distance_to_origin_more(list(w2v_dict.values()), 1.0)
    cw = ClusterWorker(points, 10, [0.0, 0.0], [1.5, 1.5])
    clusters, variation_history = cw.solve(12)
    print("plot clusters")
    plt.figure(2)
    plt.plot(variation_history)
    plt.draw()
    plt.pause(0.001)
    
    plt.figure(3)
    ClusterWorker.plot(clusters)
    plt.show()
    return clusters


def process_from_file(data):
    w2v_dict = json.loads(fr.read_file(settings.WORD2VEC_RELATIVE_FILE_PATH_STRING.format('dictionary')))
    if settings.POSTPROCESS_WORD2VEC_PREVIEW:
        preview_annotated(w2v_dict, settings.POSTPROCESS_WORD2VEC_PREVIEW_START, settings.POSTPROCESS_WORD2VEC_PREVIEW_SIZE)
    else:
        return process_w2v_data(w2v_dict)


def process(data):
    if settings.POSTPROCESS_WORD2VEC_FROM_FILE:
        return process_from_file(data)
    else:
        return process_from_scratch(data)
