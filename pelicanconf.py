AUTHOR = 'SnDream'
SITENAME = 'GBZ80编程'
SITEURL = ""

PATH = "content"

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh_CN'

DEFAULT_DATE_FORMAT = ("zh_CN.utf8", '%Y.%m.%d %A')
DATE_FORMATS = {
    'en': ("en_US.utf8", '%a, %d %b %Y'),
    'zh_CN': ("zh_CN.utf8", '%Y.%m.%d %A'),
}

LOCALE = ("zh_CN.utf8", "en_US.utf8")

ARTICLE_URL = '{category}/{slug}.html'
ARTICLE_SAVE_AS = '{category}/{slug}.html'
ARTICLE_LANG_URL = '{category}/{slug}-{lang}.html'
ARTICLE_LANG_SAVE_AS = '{category}/{slug}-{lang}.html'

FILENAME_METADATA = '(?P<title>.*)'

# Fix Chinese tag conflict
SLUGIFY_USE_UNICODE = True

# Plugins
PLUGIN_PATHS = ["plugins"]
PLUGINS = [
    "filetime_from_git",
    "i18n_subsites",
    "auto_attach",
    "featured_image",
    "plain_text_summary",
]
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}

# Markdown
MARKDOWN = {
    'extensions': [
        'pymdownx.tilde',
        'pymdownx.tasklist',
    ],
    'extension_configs': {
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'guess_lang': False,
        },
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        "pymdownx.tilde": {
            "subscript": False,
        },
    },
    'output_format': 'html5',
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("网盘", "http://sndream.ysepan.com/"),
    ("PanDocs中文版", "https://sndream.github.io/PanDocs/"),
    ("English", "/pages/english-pages-en.html"),
)

# Social widget
SOCIAL = (
    ("weibo", "https://weibo.com/xingyzh"),
)

MENUITEMS = (
    ("Archives", "/archives.html"),
    ("Categories", "/categories.html"),
    ("Tags", "/tags.html"),
)

DEFAULT_PAGINATION = 10

STATIC_PATHS = ["images", "assets"]

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# Theme
THEME = "themes/Flex"

# Flex Theme Configs

MAIN_MENU = True

from datetime import datetime
COPYRIGHT_YEAR = datetime.now().year
COPYRIGHT_NAME = "SnDream. In memory of …… ."

THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True

GITHUB_CORNER_URL = "https://github.com/SnDream"

SITELOGO = '/assets/sitelogo.png'
FAVICON = '/assets/favicon.ico'

USE_LESS = False

OG_LOCALE = "zh_CN"

ARTICLE_HIDE_TRANSLATION = False

# FILETIME_FROM_GIT
GIT_WARN_MODIFIED = True
GIT_WARN_NOT_COMMITED = True
GIT_WARN_NOT_MANAGED = True

# I18N_SUBSITES
I18N_SUBSITES = {
    # Currently not working, disabled
    # 'en': {
    #     'SITENAME': 'GBZ80 Programming',
    # },
}

I18N_TEMPLATES_LANG = "en"
