import rozetka_webscrapper

import settings

from model.category import Category

from post_process import postprocess
from rozetka_webscrapper import run

import datetime


def main() :
    start = datetime.datetime.now()
    data = run()
    mid = datetime.datetime.now()
    print("Run took:", mid - start)
    postprocessed = postprocess(data)
    end = datetime.datetime.now()
    print("Postprocess took:", end - mid)
    print("Total time spent:", end - start)

if __name__ == "__main__":
    main()
