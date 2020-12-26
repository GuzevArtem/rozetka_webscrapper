import sys, os
# Make sure you put the mitielib folder into the python search path.  There are
# a lot of ways to do this, here we do it programmatically with the following
# two statements:
parent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(parent + '/../../mitielib')

from mitie import *
from collections import defaultdict


def process(data):
    print("loading NER model...")
    ner = named_entity_extractor('../../MITIE-models/english/ner_model.dat')
    print("\nTags output by this NER model:", ner.get_possible_ner_tags())


