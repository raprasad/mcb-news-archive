"""
Check the static HTML pages for missing image links
"""
from __future__ import print_function
from django.conf import settings
import os, sys
from os.path import isdir, isfile, dirname, join, abspath
from django.template.loader import render_to_string
from story_lookup import pull_stories
from bs4 import BeautifulSoup as Bsoup

CODE_PATH = dirname(abspath(__file__))
BASE_DIR = dirname(CODE_PATH)
OUTPUT_DIR = join(CODE_PATH, 'output')

total_img_cnt = 0
def check_file(fname):
    global total_img_cnt
    content = open(fname, 'r').read()
    #lcontent = content.lower()
    soup = Bsoup(content, features="html.parser")
    img_cnt = 0
    for imgtag in soup.find_all('img'):
        img_cnt +=1
        total_img_cnt += 1
        img_path = imgtag['src']
        print('%d) tag path: %s' % (img_cnt, img_path))
        fullpath = join(OUTPUT_DIR, img_path)
        if not isfile(fullpath):
            print('broken path: %s' % fullpath)
            sys.exit(0)
    print ('looks good! images checked: %s' % img_cnt)


def check_for_missing():
    cnt = 0
    fnames = [x
              for x in os.listdir(OUTPUT_DIR)
              if x.endswith('.html') and not x.startswith('x-')]

    for fname in fnames:
        cnt += 1
        print('-' * 40)
        print('%s) %s' % (cnt, fname))
        print('-' * 40)
        check_file(join(OUTPUT_DIR, fname))
        #break

    print('total_img_cnt: ', total_img_cnt)

if __name__ == '__main__':
    check_for_missing()
