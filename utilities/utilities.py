import re
import logging
from html import escape

logger = logging.getLogger(__name__)

EMOJI_RE = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
SPLIT_RE = re.compile(r'(.*)\s+\|\s+(.*)')


def strip_emojis(string):
    return EMOJI_RE.sub(r'', string)


def html_escape(string):
    return escape(string)


def split_li_item(string, index=0):
    match = SPLIT_RE.search(string)
    if not match:
        return string
    else:
        return match.group(index + 1)
