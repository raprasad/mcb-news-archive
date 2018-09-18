# MCB Archives Scripts

This directory contains scripts for reading the news archives from a JSON file and outputting static HTML pages.

The code was meant for a "one-time" job, e.g. don't expect a lot of documentation.  However, the original JSON files may be of re-use for future repurposing of the content.

Below are instructions to run the scripts.

```
# From within the "code" directory
#
# Make a virtualenv and install the requirements
# - This was run in python2.7 in order to use django 1.4 -- which may not be
#   a hard/fast requirement. e.g. original site was Django 1.4 but only
#   templating code is used in these scripts--thought would be using more
#   Django libs but it was not needed.
#
pip install -r requirements.txt

# Create the output pages
#  - Edit the bottom of the script to select a year to output)
#  - The input is defined at the top, in the variable: NEWS_DATA_FNAME
#
python year_page_maker.py

# Check the pages for missing images
# - Note: this would fail unless these directories are copied:
#    - copy `mcb-news-archive/site/assets` to `mcb-news-archive/code/output/assets`
#    - copy `mcb-news-archive/site/news_images` to `mcb-news-archive/code/output/news_images`
#
python check_for_missing.py

```


---

# Notes for retrieving data from the server


## dump fixtures

- login: `ssh (username)@mcbpublic.unix.fas.harvard.edu`
- Dump fixtures:

```
#
cd /var/webapps/django/MCB-Website/mcb_website

# Dump everything (in case)
#
python manage.py dumpdata --indent=4 --exclude=sessions --exclude=admin.logentry --exclude=auth.user --exclude=cms_page_revision --exclude=auth.permission --exclude=contenttypes > ../fixtures/2018-0819-all.json

# Targeted toward news--which should be enough
#
sudo python manage.py dumpdata --indent=4 tags news > ../fixtures/2018-0819-news.json

# Download to local machine
#
scp (username)@mcbpublic.unix.fas.harvard.edu:/var/webapps/django/MCB-Website/fixtures/2018-0819-all.json .
scp (username)@mcbpublic.unix.fas.harvard.edu:/var/webapps/django/MCB-Website/fixtures/2018-0819-news.json .

```
