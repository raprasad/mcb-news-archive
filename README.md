# MCB News Archive: Nov 1, 2003 - Jan 6, 2017

This directory contains a static version of the Harvard University's Department of Molecular and Cellular Biology's News pages from Nov 1, 2003 - Jan 6, 2017.

It may be browsed by opening the `site/index.html` file in a browser.

This directory also includes the scripts and JSON input used to create the static pages.  It may be of future use if someone wanted to repurpose the data in the JSON files.

The structure of this site is:

```
mcb-news-archive/
|
├── code
|     - Contains the scripts and JSON input used to make the static HTML files
|     - This directory contains its own README.md
|
├── README.md
|
└── site
    ├── assets
    |       - Files for css, javascript, and some general images)
    |
    ├── index.html
    |       - Starting page for the website. Defaults to year 2016.
    |
    ├── news_images:
    |       - Thumbnail and story images used by the web pages
    |
    ├── news_year_[YYYY].html
    |       - 15 news listing pages by year, from 2003 to 2017
    |
    ├── news_story-[YYYY]-[id]-[description].html
            - 651 individual story, from 2003 to 2017
            - The 'id' in the file name corresponds to the 'id' in the
              input data file: 'code/news-data/2018-0819-news.json'
```
