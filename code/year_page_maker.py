from __future__ import print_function
from django.conf import settings
from os.path import isdir, isfile, dirname, join, abspath
from django.template.loader import render_to_string
from story_lookup import pull_stories

CODE_PATH = dirname(abspath(__file__))
BASE_DIR = dirname(CODE_PATH)
OUTPUT_DIR = join(CODE_PATH, 'output')
NEWS_DATA_FNAME = join(CODE_PATH, 'news-data', '2018-0819-news.json')
assert isfile(NEWS_DATA_FNAME), 'file not found: %s' % NEWS_DATA_FNAME

settings.configure(DEBUG=True,
                   TEMPLATE_DEBUG=True,
                   TEMPLATE_DIRS=(join(CODE_PATH, 'templates'),))

class PageMaker(object):
    """make a year page"""

    def __init__(self, selected_year, make_story_pages=False):
        """make pages"""
        self.selected_year = selected_year
        self.make_story_pages = make_story_pages
        self.make_listing_page()

    def make_listing_page(self):
        """generate menu for top of page"""

        page_info = self.get_year_info(self.selected_year)

        page_info['stories'] = self.get_story_list(self.selected_year)

        #rendered = render_to_string('news/news_year_menu2.html', info)
        rendered = render_to_string('news/news-list.html',
                                    page_info)

        #print (rendered[51110:51120])
        fname = join(OUTPUT_DIR,
                     self.get_listing_page_name(self.selected_year))

        open(fname, 'w').write(rendered)
        print('file written: ', fname)

        # write out the index page
        #
        if self.selected_year == 2016:
            index_fname = join(OUTPUT_DIR, 'index.html')
            open(index_fname, 'w').write(rendered)

            print('file written: ', index_fname)


        if self.make_story_pages:
            self.make_news_pages(page_info['stories'])


    def make_news_pages(self, stories):
        """Make a web page for each story"""
        max_idx = len(stories) - 1
        for idx, story in enumerate(stories):
            story_info = dict(selected_year=self.selected_year,
                              story=story)

            if idx > 0:
                story_info['next_story'] = stories[idx-1]

            if idx < max_idx:
                story_info['prev_story'] = stories[idx+1]


            rendered = render_to_string('news/news-story.html',
                                        story_info)

            #print (rendered[5250:5276])

            fname = join(OUTPUT_DIR,
                         story['link'])

            open(fname, 'w').write(rendered)
            print('file written: ', fname)
            #break

    def get_listing_page_name(self, selected_year):

        return 'news_year_%s.html' % selected_year

    def get_year_info(self, selected_year):

        info = dict(year_menu=range(2017, 2002, -1),
                    news_year=selected_year)

        return info

    def get_story_list(self, selected_year):
        """retrieve the list of selected stories"""
        return pull_stories(selected_year)

if __name__ == '__main__':
    if 1:
        for yr in range(2003, 2018):
            pm = PageMaker(yr, make_story_pages=True)

    #pm = PageMaker(2018, make_story_pages=True)
