import json
import random
import math
import string
import enum

from Config import *

# MMSeg
# text ->> sentence -> chunks -> chunk
class NinjaNLP(object):
    class Word(object):
        def __init__(self, data='', freq=0):
            self.data = data
            self.freq = freq
            self.length = len(data)

    class Chunk(object):
        def __init__(self, words=[]):
            self.words = words

        def total_length(self):
            length = 0
            for word in self.words:
                length += len(word.data)
            return length

        def average_length(self):
            if len(self.words) == 0:
                return 0
            return float(self.total_length()) / len(self.words)

        # standard_deviation ^ 2
        def variance(self):
            if len(self.words) == 0:
                return 0
            average = self.average_length()
            result = 0.0
            for word in self.words:
                tmp = (len(word.data) - average)
                result += tmp * tmp
            return result / len(self.words)
      
        def ln_frequency(self):
            result = 0
            for word in self.words:
                result += math.log(word.freq)
            return result

    class Text(object):
        chinese_punctuation = '·×—‘’“”…、。《》『』【】！（），：；？'

        def __init__(self, data=''):
            self.data = data
            self.length = len(data)
            self.pos = 0;

        def __iter__(self):
            while True:
                sentence, type = self.get_sentence()
                if sentence is None:
                    raise StopIteration
                yield sentence, type

        def get_sentence(self):
            while self.pos < self.length:
                if NinjaNLP.Text.is_punctuation(self.data[self.pos]):
                    self.pos += 1
                else:
                    break
            if self.pos >= self.length:
                return None, None

            begin = self.pos
            if NinjaNLP.Text.is_chinese(self.data[self.pos]):
                while self.pos < self.length and NinjaNLP.Text.is_chinese(self.data[self.pos]):
                    self.pos += 1
                return self.data[begin:self.pos], 0
            elif NinjaNLP.Text.is_english(self.data[self.pos]):

                while self.pos < self.length and NinjaNLP.Text.is_english(self.data[self.pos]):
                    self.pos += 1
                return self.data[begin:self.pos], 1
            else:
                return None, None


        @staticmethod
        def is_punctuation(ch):
            if ch in string.whitespace:
                return True
            elif ch in string.punctuation:
                return True
            elif NinjaNLP.Text.is_chinese_punctuation(ch):
                return True

        @staticmethod
        def is_english(ch):
            if ch in string.whitespace:
                return False
            elif ch in string.punctuation:
                return False
            return ch in string.printable

        @staticmethod
        def is_chinese(ch):
            return 0x4E00 <= ord(ch) <= 0x9FA5

        @staticmethod
        def is_chinese_punctuation(ch):
            return ch in NinjaNLP.Text.chinese_punctuation

    class Filter(object):
        def __init__(self):
            pass

        def filter(self, chunks):
            if len(chunks) == 0:
                return None
            if len(chunks) > 1:
                chunks = self.total_length_filter(chunks)
            if len(chunks) > 1:
                chunks = self.average_length_filter(chunks)
            if len(chunks) > 1:
                chunks = self.variance_filter(chunks)
            if len(chunks) > 1:
                chunks = self.ln_frequency_filter(chunks)
            return chunks[0]

        def total_length_filter(self, chunks):
            comparator = lambda x, y : x.total_length() - y.total_length()
            return self.filter_executor(chunks, comparator)

        def average_length_filter(self, chunks):
            comparator = lambda x, y : x.average_length() - y.average_length()
            return self.filter_executor(chunks, comparator)

        def variance_filter(self, chunks):
            comparator = lambda x, y : y.variance() - x.variance()
            return self.filter_executor(chunks, comparator)

        def ln_frequency_filter(self, chunks):  
            comparator = lambda x, y : x.ln_frequency() - y.ln_frequency()
            return self.filter_executor(chunks, comparator)

        def filter_executor(self, chunks, comparator):
            result = [chunks[0], ]
            for chunk in chunks[1:]:
                diff = comparator(result[0], chunk)
                if diff < 0:
                    result = [chunk, ]
                elif diff == 0:
                    result.append(chunk)
            return result

    def __init__(self):
        self.dict_data = {}
        self.load_dict()
        self.reply_data = {}
        self.load_reply()

        self.filter = NinjaNLP.Filter()
        pass

    # ----------------------------------------------------------------------------------------------------
    def parse(self, text):
        text = NinjaNLP.Text(text)

        result = []
        for sentence, type in text:
            if type == 0:
                chunks = self.sentence_to_chunks(sentence)
                chunk = self.filter.filter(chunks)
                result += chunk.words
            elif type == 1:
                result.append(sentence)
        return result
        # return ' '.join([sentence for sentence, type in text])

        # unknown_list = self.reply_data['unknown']
        # num = len(unknown_list)
        # if num != 0:
        #     return unknown_list[random.randint(0, num - 1)]
        # return '• ^ •'
        pass

    # data
    # ----------------------------------------------------------------------------------------------------
    def load_dict(self):
        try:
            fin = open(config['dict_path'], 'r')
            for line in fin.readlines():
                word, freq = line.split(' ')
                word = unicode(word.strip(), 'utf-8')
                self.dict_data[word] = self.Word(word, freq)
            fin.close()
        except:
            print('Load dict data fail!')
            return
    
    def load_reply(self):
        try:
            fin = open(config['reply_path'], 'r')
            self.reply_data = json.loads(fin.read())
            fin.close()
        except:
            print('Load reply data fail!')
            return

    # tools
    # ----------------------------------------------------------------------------------------------------
    def sentence_to_chunks(self, sentence):
        return [NinjaNLP.Chunk(), NinjaNLP.Chunk()]
        pass

    def match_words(self, sentence):
        words = []