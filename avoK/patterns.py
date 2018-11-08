import re

has_lawyer = re.compile("(?:Me|Maître|SELARL|SELAS|SCP)(?:\s|\xa0)")
tags_regex = '<([A-Z_]+)\/?>'
get_tag_text = '<{tag}>(.*?)<\/{tag}>'
