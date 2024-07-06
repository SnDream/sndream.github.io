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
ATTACH_CONTENT_DIR = ""

def link_type(link):
    link = path.normpath(path.join(ATTACH_CONTENT_DIR, link))

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
    global ATTACH_PATH, ATTACH_STATIC_PATHS
    ATTACH_PATH = path.normpath(pelican_obj.settings["PATH"])
    if "STATIC_PATHS" in pelican_obj.settings:
        paths = pelican_obj.settings["STATIC_PATHS"]
        ATTACH_STATIC_PATHS = [ path.normpath(path.join(ATTACH_PATH, x)) for x in paths ]
    pelican_obj.settings['MARKDOWN'].setdefault('extensions', []).append(AutoAttachExtension())

def pelican_content_dir_get(content):
    global ATTACH_CONTENT_DIR
    ATTACH_CONTENT_DIR = path.dirname(content.source_path)

def register():
    """Plugin registration"""
    signals.initialized.connect(pelican_init)
    signals.content_object_init.connect(pelican_content_dir_get)
