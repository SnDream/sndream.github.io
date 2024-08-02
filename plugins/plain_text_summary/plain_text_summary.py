from pelican import signals
from bs4 import BeautifulSoup
from pelican.utils import truncate_html_words

def plain_text_summary(instance):
    if "summary" in instance.metadata:
        return

    summary_html = truncate_html_words(
        instance._content, # Just plain text, no need to update links
        instance.settings["SUMMARY_MAX_LENGTH"],
        instance.settings["SUMMARY_END_SUFFIX"],
    )
    summary_raw = BeautifulSoup(summary_html, 'html.parser').get_text()

    # I'm not familiar with BeautifulSoup, there should be a better way.
    summary = "".join(["<p>%s</p>\n"%(line) for line in summary_raw.split('\n')])

    # I'm not familiar with Pelican either, and it won't work unless it's all set up.
    instance.metadata["summary"] = summary
    instance._summary = summary

def plain_text_summary_articles(generator):
    for article in generator.articles:
        plain_text_summary(article)

def plain_text_summary_pages(generator):
    for pages in generator.pages:
        plain_text_summary(pages)

def register():
    # The summary plugins are commonly registered in this location. 
    # However, I can't get it to work properly here.
    # signals.all_generators_finalized.connect(why_here)

    # Is this a good location? I don't know.
    signals.article_generator_finalized.connect(plain_text_summary_articles)
    signals.page_generator_finalized.connect(plain_text_summary_pages)
