AUTHOR = 'SnDream'
SITENAME = 'GBZ80编程'
SITEURL = ""

PATH = "content"

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh_CN'

# Plugins
PLUGIN_PATHS = ["plugins"]
PLUGINS = ["filetime_from_git"]

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

STATIC_PATHS = ["images"]

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# Theme
THEME = "themes/Flex"

# Flex Theme Configs

MAIN_MENU = True

from datetime import datetime
COPYRIGHT_YEAR = datetime.now().year
COPYRIGHT_NAME = "SnDream"

THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True

GITHUB_CORNER_URL = "https://github.com/SnDream"

SITELOGO = '/images/sitelogo.png'
FAVICON = '/images/favicon.ico'

# FILETIME_FROM_GIT
GIT_WARN_NOT_COMMITED = True
GIT_WARN_NOT_MANAGED = True
