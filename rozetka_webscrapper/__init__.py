import rozetka_webscrapper

import settings

from model.category import Category

from post_process import postprocess
from rozetka_webscrapper import run




def main() :
    data = run()
    postprocessed = postprocess(data)







if __name__ == "__main__":
    main()
