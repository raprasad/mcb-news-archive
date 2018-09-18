import hashlib
from django.db import models
from django.template.defaultfilters import slugify
from tags.models import Tag
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.db.models import Q
from mcb_website.utils.url_shortener import shorten_url
from django.contrib.sites.models import Site
try:
    from mcb_twitter.tweet_mcb.views_news import get_tweet_news_url
except:
    pass


PREVIEW_ID = 'preview_id'

class Writer(models.Model):
    fname = models.CharField('First name', max_length=70)
    mi = models.CharField('MI', max_length=10, blank=True)
    lname = models.CharField('Last name', max_length=70)
    email = models.EmailField(blank=True)
    is_faculty_member = models.BooleanField(default=False, help_text='Used for creating a news story byline.')

    def __unicode__(self):
        if self.mi:
            return '%s, %s %s' % (self.lname, self.mi, self.fname, )
        else:
            return '%s, %s' % (self.lname, self.fname)

    def fname_lname(self):
        if self.mi:
            return '%s %s %s' % (self.fname, self.mi, self.lname )
        else:
            return '%s %s' % (self.fname, self.lname)

    class Meta:
        ordering = ( 'lname', 'fname',)


class NewsStory(models.Model):
    """
    Model for an MCB News Story
    """
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)

    visible = models.BooleanField(default=True)

    short_url = models.URLField(blank=True, help_text='auto-generated on save')
    slug = models.SlugField(max_length=255, blank=True)
    writers = models.ManyToManyField(Writer, blank=True, null=True)

    pub_date = models.DateField('post date')

    #is_public =  models.BooleanField(default=False)
    show_on_frontpage = models.BooleanField(default=True)

    is_research_story = models.BooleanField(default=False)
    is_education_story = models.BooleanField(default=False)

    is_chosen_story = models.BooleanField(default=False)
    chosen_story_position = models.IntegerField('Story position', default=0)

    story = models.TextField()
    teaser = models.TextField(blank=True, help_text='appears in archive listing')

    tags = models.ManyToManyField(Tag, blank=True, null=True)

    thumbnail_image = models.FileField(max_length=255, upload_to='imgs/news/thumb', blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    id_hash = models.CharField(max_length=100, blank=True)

    def preview_story(self):
        """
        View the story before it is officially "published"
        This view isn't password protected--e.g., if someone had the preview link for an unpublished story, it could be shared, etc.
        """
        story_url = reverse('view_news_story'\
                            , kwargs={'story_id': self.id, 'story_slug':self.slug})
        lnk = '%s?%s=%s' % (story_url, PREVIEW_ID, self.id_hash)
        return '<a href="%s" target="_blank">preview</a>' % lnk
    preview_story.allow_tags = True

    def tweet_story(self):
        try:
            return '<a href="%s" target="_tweet_it">Tweet Story</a>'% get_tweet_news_url(self.title, self.short_url)
        except:
            return 'n/a'
    tweet_story.allow_tags = True

    def get_writers_for_byline(self):
        return self.writers.all().order_by('is_faculty_member', 'lname', 'fname')

    def visible_tags(self):
        return self.tags.filter(visible=True)

    def tag_list(self):
        return ', '.join(map(lambda x: str(x), self.visible_tags()))
    tag_list.allow_tags = True

    def thumbnail_img(self):
        if self.thumbnail_image:
            return '<img src="%s" />' % self.thumbnail_image.url
        return '(no image)'
    thumbnail_img.allow_tags = True

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if self.id is None or not self.slug:
            return None

        try:
            return reverse('view_news_story', \
                            kwargs={'story_id':self.id,\
                            'story_slug':self.slug })
        except:
            return None

    def get_writers_fmt(self):
        #return 'blah'
        num_writers = self.writers.count()
        print num_writers
        if num_writers == 0:
            return None
        elif num_writers == 1:
            return self.writers.all()[0]
        elif num_writers == 2:
            return ' and '.join(self.writers.all())
        elif num_writers > 2:
            return ', '.join(self.writers.all()[01]) #+ ' and ' + self.writers.all()[-1]

        return None

    @staticmethod
    def update_image_homepage_flags(sender, **kwargs):
        """
        Find news stories with this criteria:
            (1) show_on_frontpage = True
            (2) chosen_story_position > 4 or chosen_story_position < 1
        Change to:
            (1) show_on_frontpage = False
            (2) chosen_story_position = 99
        """
        post_save.disconnect(NewsStory.update_image_homepage_flags, sender=NewsStory)

        for ns in NewsStory.objects.filter(show_on_frontpage=True).filter(Q(chosen_story_position__gt=4) | Q(chosen_story_position__lt=1)):
            ns.chosen_story_position = 99
            ns.show_on_frontpage = False
            ns.save()

        """
        Find news stories with this criteria:
            (1) show_on_frontpage = False
            (2) chosen_story_position != 99
        Change to:
            (1) chosen_story_position = 99
        """
        for ns in NewsStory.objects.filter(show_on_frontpage=False).exclude(chosen_story_position=99):
            ns.chosen_story_position = 99
            ns.save()

        post_save.connect(NewsStory.update_image_homepage_flags, sender=NewsStory)

    def set_short_url(self):
        print 'set_short_url'
        if self.id is None or not self.slug:
            self.short_url = ''
            return

        full_url = '%s%s' % (Site.objects.get_current(), self.get_absolute_url())
        short_url = shorten_url(full_url)
        if short_url is None:
            self.short_url = ''
        else:
            self.short_url = short_url

    def short_url_link(self):
        if not self.short_url:
            return 'n/a'
        return '<a href="%s">%s</a>' % (self.short_url, self.short_url)
    short_url_link.allow_tags = True

    def save(self):
        self.slug =  slugify(self.title)
        if self.id is None:
            super(NewsStory, self).save()

        self.title = self.title.encode("ascii", "ignore")

        self.set_short_url()

        self.id_hash =  hashlib.sha1('%s%s' % (self.id, self.title)).hexdigest()

        if self.chosen_story_position > 4 or self.chosen_story_position < 1:
            self.chosen_story_position = 99
            self.show_on_frontpage = False

        super(NewsStory, self).save()        # Call the "real" save() method.

    class Meta:
        ordering = ('-show_on_frontpage', '-pub_date',)
        verbose_name_plural = 'News Stories'


class NewsImage(models.Model):
    """Image uploads for a specific story.
    Note!  This is no longer needed!"""

    news_story = models.ForeignKey(NewsStory)
    caption = models.CharField(max_length=255, blank=True)
    show_caption = models.BooleanField(default=True)

    image_file = models.FileField(max_length=255, upload_to='imgs/news')
    entry_time = models.DateTimeField(auto_now_add=True)

    def web_url(self):
        #return '<h1>blah</h1>'
        return '<img src="%s" width="100" /><br /><input type="text" value="%s" />' % ( self.image_file.url,\
                                        self.image_file.url )
    web_url.allow_tags = True

    def __unicode__(self):
        if self.caption:
            return '%s - %s' % (self.news_story, self.caption)
        else:
            return '%s' % self.news_story

    class Meta:
        ordering = ('news_story', 'caption', )


post_save.connect(NewsStory.update_image_homepage_flags, sender=NewsStory)
