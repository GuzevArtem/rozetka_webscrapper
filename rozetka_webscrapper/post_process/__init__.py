from post_process.bow_processing import Bow
from post_process.model.bag import Bag

import settings

import files.file_reader as fr
import files.file_writer as fw

import json

def check_postprocess_mode(postprocess_mode_str) :
    for str in settings.POSTPROCESS_MODES_LIST:
        if str == postprocess_mode_str :
            return True
    return False

def postprocess_bow_and_bigramms(data):
    bags = []
    bigramms = []

    total_comment_counter = 0
    for category in data:
        for group in category.groups:
            for item in group.items:
                comment_counter = 0
                first_comment = total_comment_counter + 1
                last_comment = total_comment_counter + len(item.comments)
                bow_file_str_arr = []
                bigramm_file_str_arr = []
                for comment in item.comments:
                    bow = Bow.map_bow(comment.text)
                    bags.append(bow)
                    bigramm = Bow.map_bigramm(comment.text)
                    bigramms.append(bigramm)

                    bow_file_str_arr.append(bow.toJson())
                    bigramm_file_str_arr.append(json.dumps(bigramm, ensure_ascii = False))
                    comment_counter += 1
                    total_comment_counter += 1
                    print("Processed", total_comment_counter, "comments", end='\r')
                fw.write_plain(
                        settings.BOW_RELATIVE_FILE_PATH_STRING.format(str(first_comment)+'-'+str(last_comment)) ,
                        '[' + ','.join(bow_file_str_arr) + ']',
                        encoding='utf-8',
                        mode = 'w'
                        )
                fw.write_plain(
                        settings.BIGRAMM_RELATIVE_FILE_PATH_STRING.format(str(first_comment)+'-'+str(last_comment)),
                        '[' + ','.join(bigramm_file_str_arr) + ']',
                        encoding='utf-8',
                        mode = 'w'
                        )

    print("Processed bows and bigramms saved to files!")
    return bags, bigramms

def word2vec(data):

    pass

def postprocess(data) :
    mode = settings.POSTPROCESS_MODE
    if not check_postprocess_mode(mode):
        print("Error!", "Postprocess mode:", mode, "not found in list", settings.POSTPROCESS_MODES_LIST)
        raise RuntimeError(" ".join(["Postprocess mode:", mode, "not found in list", settings.POSTPROCESS_MODES_LIST]))

    mode_runner_map = {
        settings.POSTPROCESS_MODES_LIST[0] : lambda d: postprocess_bow_and_bigramms(d),
        settings.POSTPROCESS_MODES_LIST[1] : lambda d: word2vec(d)
        }
    return mode_runner_map[mode](data)
