import rozetka_webscrapper

import settings
import files.file_reader as fr

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

def run_from_file() :
    print("Running reading from previously stored data sequence")
    filenames = fr.get_all_filenames('./'+settings.RESULT_FOLDER_NAME, settings.RESULT_FILE_NAME_PREFIX)
    def parse_file_data (file_data) :
        parsed_as_json = json.loads(file_data)
        parsed = []
        for cat in parsed_as_json:
            parsed.append(Category(cat))
        return parsed
    result = []
    for filename in filenames:
        category = fr.read_file_as(filename, lambda file_data : parse_file_data(file_data) )
        result.append(category)
    return result


def run() :
    mode = settings.APPLICATION_MODE
    if not check_application_mode(mode):
        print ("Error!", "App mode:", mode, "not found in list", settings.APPLICATION_MODES_LIST)
        return

    mode_runner_map = {
        "clean" : lambda : run_clean(),
        "from_file" : lambda : run_from_file()
        }
    mode_runner_map[mode]()


if __name__ == "__main__":
   run()
