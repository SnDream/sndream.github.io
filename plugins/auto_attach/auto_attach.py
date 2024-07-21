# -*- coding: utf8 -*-
from markdown.extensions import Extension
# import markdown.inlinepatterns as inlinepatterns
from markdown.inlinepatterns import LinkInlineProcessor
from markdown.inlinepatterns import ImageInlineProcessor
# import xml.etree.ElementTree as etree
from pelican import signals
import logging
from os import path

# Pattern must not consume characters
# ATTACH_IMAGE_RE = r'\!\[(?=[^\]]*?\]\(\./)'
# ATTACH_LINK_RE = r'\[(?=[^\]]*?\]\(\./)'

# Support path like '../path/to/file'
ATTACH_IMAGE_RE = r'\!\[(?=[^\]]*?\]\(\.\.?/)'
ATTACH_LINK_RE = r'\[(?=[^\]]*?\]\(\.\.?/)'

ATTACH_STATIC_PATHS = []
ATTACH_PATH = ""
ATTACH_CONTENT_PATH = ""
ATTACH_CONTENTS = []

def link_type(link):
    link = path.normpath(path.join(path.dirname(ATTACH_CONTENT_PATH), link))
    if not path.exists(link):
        logging.warn(link + " is not exist")

    # static check
    for static_path in ATTACH_STATIC_PATHS:
        try:
            if path.commonpath([link, static_path]) == static_path:
                return '{static}'
        except ValueError:
            continue

    # attach check
    try:
        if path.commonpath([link, ATTACH_PATH]) != ATTACH_PATH:
            return '{attach}'
    except ValueError:
        return '{attach}'
    
    return '{filename}'

class AttachImageInlineProcessor(ImageInlineProcessor):
    def handleMatch(self, m, data):
        # Process image as usual
        el, start, index = super().handleMatch(m, data)

        # Postprocessing
        if el is not None and el.get("src"):
            el_oldsrc = el.get("src")
            el.set("src", link_type(el_oldsrc) + el_oldsrc)
            logging.debug(f"Coercing src '{el_oldsrc}' to '{el.get('src')}'")

        return el, start, index

class AttachLinkInlineProcessor(LinkInlineProcessor):
    def handleMatch(self, m, data):
        # Process image as usual
        el, start, index = super().handleMatch(m, data)

        # Postprocessing
        if el is not None and el.get("href"):
            el_oldsrc = el.get("href")
            el.set("href", link_type(el_oldsrc) + el_oldsrc)
            logging.debug(f"Coercing href '{el_oldsrc}' to '{el.get('href')}'")

        return el, start, index

class AutoAttachExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(AttachImageInlineProcessor(ATTACH_IMAGE_RE, md), 'attach_image', 170 + 1)
        md.inlinePatterns.register(AttachLinkInlineProcessor(ATTACH_LINK_RE, md), 'attach_link', 160 + 1)

def pelican_init(pelican_obj):
    pelican_obj.settings['MARKDOWN'].setdefault('extensions', []).append(AutoAttachExtension())

def content_path_get(gene, c_paths, c_exclude):
    global ATTACH_PATH, ATTACH_STATIC_PATHS, ATTACH_CONTENT_PATH, ATTACH_CONTENTS

    ATTACH_PATH = path.normpath(gene.settings.get("PATH", ""))
    paths = gene.settings.get("STATIC_PATHS", [])
    ATTACH_STATIC_PATHS = [ path.normpath(path.join(ATTACH_PATH, x)) for x in paths ]

    if len(ATTACH_CONTENTS) == 0:
        # I don't know how to get markdown filename without this.
        for f in gene.get_files(gene.settings[c_paths], exclude=gene.settings[c_exclude]):
            if gene.get_cached_data(f, None): continue
            ATTACH_CONTENTS.append(f)
        ATTACH_CONTENTS.reverse()

    f = ATTACH_CONTENTS.pop()
    logging.debug("Guess next content: " + f)
    ATTACH_CONTENT_PATH = path.normpath(path.join(gene.path, f))

def page_path_final(content):
    # Since content_path_get uses an informal way of fetching files,
    # its method may be invalid due to a Pelican version update, 
    # so check when you can get the filename.
    global ATTACH_CONTENT_PATH, ATTACH_GUESS_FAIL_FIRSTTIME

    real_attach_ext = path.splitext(content.source_path)[1].lower()
    content_path_actual = content.source_path
    content_path_guessed = ATTACH_CONTENT_PATH
    ATTACH_CONTENT_PATH = ""

    if real_attach_ext not in (".md", ".markdown", ".mkd", ".mdown"):
        return

    if content_path_guessed != content_path_actual:
        logging.fatal(
            "Dir to the guessed: %s\n"%content_path_guessed +
            "Dir to the actual: %s\n"%content_path_actual +
            "Failed to guess Markdown file path.\n" +
            "Failure may be due to a Python or Pelican version change.\n" +
            "Please disable the auto_attach plugin or look for plugin updates. ")
        raise UserWarning("Failed to guess Markdown file path")

def article_path_get(gene):
    return content_path_get(gene, "ARTICLE_PATHS", "ARTICLE_EXCLUDES")

def page_path_get(gene):
    return content_path_get(gene, "PAGE_PATHS", "PAGE_EXCLUDES")

def register():
    """Plugin registration"""
    signals.initialized.connect(pelican_init)
    signals.article_generator_preread.connect(article_path_get)
    signals.page_generator_preread.connect(page_path_get)
    signals.content_object_init.connect(page_path_final)
