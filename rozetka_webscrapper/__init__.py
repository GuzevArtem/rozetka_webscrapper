import rozetka_webscrapper

import settings
import files.file_reader as fr
import files.file_writer as fw

import json

from model.category import Category



def check_application_mode(application_mode_str) :
    for str in settings.APPLICATION_MODES_LIST:
        if str == application_mode_str :
            return True
    return False



def run_clean() :
    print("Running reading from site sequence")
    result = rozetka_webscrapper.scrap_rozetka_web_site()
    print("Scraped", len(result), "categories.")
    return result



def run_from_file() :
    print("Running reading from previously stored data sequence")
    filenames = fr.get_all_filenames('./'+settings.RESULT_FOLDER_NAME, settings.SITE_SCRAP_RESULT_FILE_NAME_PREFIX)
    
    def parse_file_data (file_data) :
        parsed_as_json = json.loads(file_data)
        parsed = []
        for cat in parsed_as_json:
            parsed.append(Category(cat))
        return parsed
    
    result = []
    for filename in filenames:
        categories = fr.read_file_as(filename, lambda file_data : parse_file_data(file_data) )
        result += categories
    print("Loaded", len(result), "categories.")
    return result



def run() :
    mode = settings.APPLICATION_MODE
    if not check_application_mode(mode):
        print("Error!", "App mode:", mode, "not found in list", settings.APPLICATION_MODES_LIST)
        raise RuntimeError(" ".join(["App mode:", mode, "not found in list", settings.APPLICATION_MODES_LIST]))

    mode_runner_map = {
        settings.APPLICATION_MODES_LIST[0] : lambda : run_clean(),
        settings.APPLICATION_MODES_LIST[1] : lambda : run_from_file()
        }
    return mode_runner_map[mode]()

from post_process.bow_processing import Bow
from post_process.model.bag import Bag

def main() :
    data = run()

    bags = []
    bigramms = []
    
    counter = 0
    for category in data:
        for group in category.groups:
            for item in group.items:
                for comment in item.comments:
                    bow = Bow.map_bow(comment.text)
                    bags.append(bow)
                    bigramm = Bow.map_bigramm(comment.text)
                    bigramms.append(bigramm)
                    fw.write_plain(
                        settings.BOW_RELATIVE_FILE_PATH_STRING .format(str(counter)) ,
                        bow.toJson(),
                        encoding='utf-8'
                        )
                    fw.write_plain(
                        settings.BIGRAMM_RELATIVE_FILE_PATH_STRING.format(str(counter)),
                        json.dumps(bigramm),
                        encoding='utf-8'
                        )
                    counter += 1
                    print("Processed", counter, "comments", end='\r')

    print("Processed bows and bigramms saved to files!")

#    print("Saving bows to files!")
#    counter = 0
#    for b in bags:
#        #print(b)
#        fw.write_plain(
#            settings.BOW_RELATIVE_FILE_PATH_STRING .format(str(counter)) ,
#            b.toJson(),
#            encoding='utf-8'
#            )
#        counter += 1
#
#    print("Saving bigramms to files!")
#    counter = 0
#    for b in bigramms:
#        #print(b)
#        fw.write_plain(
#            settings.BIGRAMM_RELATIVE_FILE_PATH_STRING.format(str(counter)),
#            json.dumps(b),
#            encoding='utf-8'
#            )
#        counter += 1





if __name__ == "__main__":
    main()
