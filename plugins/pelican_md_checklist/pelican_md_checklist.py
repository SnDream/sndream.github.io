# -*- coding: utf8 -*-
import re
from pelican import signals

import xml.etree.ElementTree as ET

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

item_pattern = re.compile(r"^\[([ Xx])\](.*)$")


class CheckboxExtension(Extension):
    def extendMarkdown(self, md) -> None:
        md.treeprocessors.register(CheckboxTreeProcessor(), "checklist", 9999)


class CheckboxTreeProcessor(Treeprocessor):
    def run(self, root) -> None:
        for el in root.iter("li"):
            if not el.text:
                continue
            match = item_pattern.match(el.text)
            if match:
                check = ET.Element("input", attrib={"type": "checkbox", "disabled": ""})
                if match[1].lower() == "x":
                    check.attrib["checked"] = ""
                el.insert(0, check)
                el.text = None
                check.tail = match[2]

def pelican_init(pelican_obj):
    pelican_obj.settings['MARKDOWN'].setdefault('extensions', []).append(CheckboxExtension())

def register():
    """Plugin registration"""
    signals.initialized.connect(pelican_init)
