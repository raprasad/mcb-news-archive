from __future__ import print_function
from collections import OrderedDict
import json
from os.path import isdir, isfile, dirname, join, abspath

CODE_PATH = dirname(abspath(__file__))
BASE_DIR = dirname(CODE_PATH)
OUTPUT_DIR = join(BASE_DIR, 'output')
NEWS_DATA_FNAME = join(BASE_DIR, 'news-data', '2018-0819-news.json')
assert isfile(NEWS_DATA_FNAME), 'file not found: %s' % NEWS_DATA_FNAME


def pull_tag_names():

    tag_info = {} # id: name
    writer_info = {}

    content = open(NEWS_DATA_FNAME, 'r').read()
    info_dict = json.loads(content,
                           object_pairs_hook=OrderedDict)

    for item in info_dict:
        if item['model'] == 'tags.tag':
            tag_info[item['pk']] = item['fields']['name']

        elif item['model'] == 'news.writer':
            if item['fields']['mi'] != '':
                writer_name = '%s %s. %s' % \
                                (item['fields']['fname'],
                                 item['fields']['mi'],
                                 item['fields']['lname'])
            else:
                writer_name = '%s %s' % \
                                (item['fields']['fname'],
                                 item['fields']['lname'])
            writer_info[item['pk']] = writer_name



    #print(tag_info)
    print(writer_info)


if __name__ == '__main__':
    pull_tag_names()
