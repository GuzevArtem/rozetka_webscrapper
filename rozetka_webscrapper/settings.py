# scrap setup. Estimated comments count == multiplication of next values below
COMMENTS_PER_PAGE_LIMIT = 30
ITEMS_PER_GROUP_LIMIT = 30
GROUPS_PER_CATEGORY_LIMIT = 10
CATEGORIES_LIMIT = 10

#Saving: Path & file templates
SITE_SCRAP_RESULT_FILE_NAME_PREFIX = 'results'
BOW_RESULT_FILE_NAME_PREFIX = 'bow'
BIGRAMM_RESULT_FILE_NAME_PREFIX = 'bigramm'
WORD2VEC_RESULT_FILE_NAME_PREFIX = "word2vec"

RESULT_FOLDER_NAME = "results"
RESULT_BOW_SUB_FOLDER_NAME = "bow"
RESULT_BIGRAMM_SUB_FOLDER_NAME = "bigramm"
RESULT_WORD2VEC_SUB_FOLDER_NAME = "word2vec"

SITE_SCRAP_RELATIVE_FILE_PATH_STRING = RESULT_FOLDER_NAME + "/" + SITE_SCRAP_RESULT_FILE_NAME_PREFIX + "_{}.json"
BOW_RELATIVE_FILE_PATH_STRING = RESULT_FOLDER_NAME + "/" + RESULT_BOW_SUB_FOLDER_NAME + "/" + BOW_RESULT_FILE_NAME_PREFIX + "_{}.json"
BIGRAMM_RELATIVE_FILE_PATH_STRING = RESULT_FOLDER_NAME + "/" + RESULT_BIGRAMM_SUB_FOLDER_NAME + "/" + BIGRAMM_RESULT_FILE_NAME_PREFIX + "_{}.json"
WORD2VEC_RELATIVE_FILE_PATH_STRING = RESULT_FOLDER_NAME + "/" + RESULT_WORD2VEC_SUB_FOLDER_NAME + "/" + WORD2VEC_RESULT_FILE_NAME_PREFIX + "_{}.json"

#Scrapper driver to render web pages with script driven UI
DEFAULT_SELENIUM_DRIVER = "Chrome"

#Application work mode
APPLICATION_MODE = "from_file"
APPLICATION_MODES_LIST = ["clean", "from_file"] #append new
#Post process work mode
POSTPROCESS_MODE = "word2vec"
POSTPROCESS_MODES_LIST = ["bow", "word2vec" ]

#Additional
POSTPROCESS_WORD2VEC_FROM_FILE = True
POSTPROCESS_WORD2VEC_PREVIEW = True
POSTPROCESS_WORD2VEC_PREVIEW_START = 1000
POSTPROCESS_WORD2VEC_PREVIEW_SIZE = 1000
POSTPROCESS_WORD2VEC_MIN_DESCRIPTION_LENGTH = 100
POSTPROCESS_WORD2VEC_MAT_PAIRS_ITERATIONS = 1000


#ner models
#PATH_TO_NER_MODEL = '../../../ru_model.dat'

