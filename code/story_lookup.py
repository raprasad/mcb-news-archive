from __future__ import print_function
from collections import OrderedDict
import json
from datetime import datetime

from os.path import isdir, isfile, dirname, join, abspath

from writer_lookup import writer_dict
from tag_lookup import tag_dict


CODE_PATH = dirname(abspath(__file__))
BASE_DIR = dirname(CODE_PATH)
OUTPUT_DIR = join(CODE_PATH, 'output')
NEWS_DATA_FNAME = join(CODE_PATH, 'news-data', '2018-0819-news.json')
assert isfile(NEWS_DATA_FNAME), 'file not found: %s' % NEWS_DATA_FNAME


def pull_stories(selected_year):

    all_story_info = {} # id: name

    content = open(NEWS_DATA_FNAME, 'r').read()
    info_dict = json.loads(content,
                          object_pairs_hook=OrderedDict)

    for item in info_dict:
        if item['model'] != 'news.newsstory':
            continue

        # -------------------------------------
        # Is this the right year and visible?
        # -------------------------------------
        if item['fields']['pub_date'][:4] != str(selected_year):
            continue
        elif item['fields']['visible'] is False:
            continue

        # Get the data!
        #
        story_lookup = item['fields']
        story_lookup['pk'] =  item['pk']    # add the PK


        # -------------------------
        # Format link
        # -------------------------
        short_slug = story_lookup['slug']#[:20]
        if short_slug.endswith('-'):
            short_slug = short_slug[:-1]
        page_link = 'story-%s-%s-%s.html' % \
                        (selected_year,
                         story_lookup['pk'],
                         short_slug)

        story_lookup['link'] = page_link


        # -------------------------
        # Format Tags
        # -------------------------
        tag_ids = story_lookup['tags']
        story_lookup['tag_ids'] = tag_ids

        # convert tags from ids to names
        tag_list = [tag_dict[tag_id] for tag_id in tag_ids]
        tag_list.sort()
        story_lookup['tags'] = tag_list

        # -------------------------
        # Format Authors
        # -------------------------
        writer_ids = story_lookup['writers']
        story_lookup['writer_ids'] = writer_ids

        # convert tags from ids to names
        writer_list = [writer_dict[writer_id] for writer_id in writer_ids]
        #tag_list.sort()
        story_lookup['writers'] = writer_list


        # -------------------------
        # Format pubdate
        # -------------------------
        pub_date_str = story_lookup['pub_date']
        story_lookup['pub_date_str'] = pub_date_str
        pub_date_obj = datetime.strptime(pub_date_str, '%Y-%m-%d')
        story_lookup['pub_date'] = pub_date_obj

        # -------------------------
        # Format thumbnail_image
        # -------------------------
        orig_thumb = story_lookup['thumbnail_image']
        story_lookup['orig_thumb'] = orig_thumb
        if orig_thumb == '':
            story_lookup['thumbnail_image'] = orig_thumb
        else:
            story_lookup['thumbnail_image'] = 'news_images/%s' % orig_thumb

        # -------------------------
        # Story images
        # -------------------------
        # /mcb_files/media/editor_uploads -> news_images/editor_uploads
        content = story_lookup['story']

        replace_pairs = [\

            ('"http://mcbpublic.unix.fas.harvard.edu/mcb_files/media/editor_uploads',
             '"news_images/editor_uploads'),

            ('http://www.mcb.harvard.edu/Faculty/Images/Burton.jpg',
             'assets/images/faculty/burton6a.jpg'),

            ('http://www.mcb.harvard.edu/Faculty/Images/Cluzel.jpg',
             'assets/images/faculty/Cluzel_1.jpg'),

            ('http://www.mcb.harvard.edu/Faculty/Images/Denic.jpg',
             'assets/images/faculty/denic_vlad.png'),

            ('http://www.mcb.harvard.edu/Faculty/Images/Needleman.jpg',
             'assets/images/faculty/needleman_dan_lg_DSC9096.png'),

            ('<img height=\"4\" width=\"5\" src=\"5\">', ''),

            ('http://www.mcb.harvard.edu/Faculty/Images/Ramanathan.jpg',
             'assets/images/faculty/Ramanathan_1.jpg'),

            ('"/mcb_files/media/editor_uploads', '"news_images/editor_uploads'),

            ('.ezp-prod1.hul.harvard.edu', ''),

            ('/mcb_files/static/imgs/spacer.gif', 'assets/images/spacer.gif'),

        ]
        for old_val, new_val in replace_pairs:
            content = content.replace(old_val, new_val)

        story_lookup['content'] = content

        # add to the overall list
        #
        all_story_info.setdefault(pub_date_str, []).append(story_lookup)

    # Sort it
    #
    date_keys = all_story_info.keys()
    date_keys.sort()
    date_keys.reverse()

    sorted_list = []
    for dk in date_keys:
        sorted_list += all_story_info.get(dk)

    return sorted_list

if __name__ == '__main__':
    stories = pull_stories(2016)
    print(stories)
    #for s in stories:
    #    print(s['pub_date_str'])
    print(len(stories))
