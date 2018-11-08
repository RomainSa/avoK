import re

# compiled patterns
has_lawyer = re.compile("(?:Me|Maître|SELARL|SELAS|SCP)(?:\s|\xa0)")
juri_tags = re.compile("<\/?([^a-z=\/]*?)>")
html_tags = re.compile("<[a-z]*?\/?>")

# text patterns
get_tag_text = '<{tag}>(.*?)<\/{tag}>'
