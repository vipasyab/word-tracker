import re
import sys
from itertools import islice


def take(n, iterable):
    return list(islice(iterable.items(), n))


class WordTracker:
    def __init__(self, word, line, file):
        self.count = 1
        self.word = word
        self.lines = {line}
        self.files = {file}

    def add(self, line, file):
        self.count += 1
        self.lines.add(line)
        self.files.add(file)


common_words = ['-', '?', 'a', 'able', 'about', 'after', 'all', 'also', 'an', 'and', 'any', 'are', 'as', 'at', 'back',
                'be', 'because', 'been', 'but', 'by', 'can', 'could', 'do', 'for', 'from', 'had', 'has', 'have', 'he',
                'her', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'it', "it's", 'me', 'more', 'must', 'my', 'no',
                'not', 'of', 'on', 'one', 'or', 'other', 'our', 'over', 'same', 'she', 'should', 'so', 'than', 'that',
                'that\'s', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'thing', 'this', 'those', 'time',
                'to', 'up', 'us', 'use', 'was', 'we', 'we\'re', 'we\'ve', 'were', 'well', 'what', 'when', 'where',
                'which', 'who', 'will', 'with', 'would', 'you', 'your']

line_map = dict()
word_map = dict()
line_seq = 0


def read_file(filename):
    f = open(filename, "r")
    text = f.read()
    f.close()
    return text


def process_text(filename, content):
    lines = re.split('\\.(\\s+|\n)', content)
    for line in lines:
        global line_seq
        line_seq += 1
        line = line.strip("\n")
        line_map[line_seq] = line
        words = line.split()
        for word in words:
            word = word.lower().strip()
            if word.endswith(','):
                word = word[:-1]
            if word not in common_words:
                if word in word_map:
                    word_map[word].add(line_seq, filename)
                else:
                    word_map[word] = WordTracker(word, line_seq, filename)


def show_data_for_word(word):
    if word not in word_map:
        print('"{}" is not in the read text'.format(word))
    else:
        print_word_data(word_map[word])


def print_word_data(word):
    word_lines = []
    for i in list(word.lines)[:10]:
        word_lines.append(line_map[i])
    print("{} ({}) in files: [{}] and lines:\n\n=> {}".format(word.word, word.count, ', '.join(word.files),
                                                             '\n=> '.join(word_lines)))
    print('-' * 50)


for i in range(1, 7):
    filename = "doc{}.txt".format(i)
    text = read_file("{}".format(filename))
    process_text(filename, text)

ordered = {k: v for k, v in sorted(word_map.items(), key=lambda item: item[1].count, reverse=True)}

if len(sys.argv) > 1 and sys.argv[1].isnumeric():
    topN = int(sys.argv[1])
else:
    topN = 10

print('Showing results for top {} interesting words'.format(topN))
print("="*50)
filtered = take(topN, ordered)
for word in filtered:
    print_word_data(word[1])

if len(sys.argv) > 2:
    for i in range(2, len(sys.argv)):
        show_data_for_word(sys.argv[i])
