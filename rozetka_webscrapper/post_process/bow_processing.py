
from post_process.model.bag import Bag
import re

class Bow:

    def map_bigramm_sentence(sentence, separator = ' ') :
        words = re.split('[\W]+', sentence)
        result = []

        words = [w for w in words if len(w) > 0] #filter from mess

        if len(words) > 1 :
            for i in range(len(words)-1) :
                result.append(separator.join([words[i], words[i+1]]))
        return result

    def map_bigramm(str, separator = ' ') :
        result = []

        sentences = re.split('[.?!]+', str)

        for sentence in sentences:
            result += Bow.map_bigramm_sentence(sentence, separator)

        return result


    def map_bow(str) :
        result = Bag({}) #WA to prevent random access to last created dict

        words = re.split('[\W]+', str)

        for word in words:
            if len(word) > 0:
                result.add_word(word)
        return result



