import re

# compiled patterns
has_lawyer = re.compile("(?:Me|Maître|SELARL|SELAS|SCP)(?:\s|\xa0)")
juri_tag_pair = re.compile("<\/?([^a-z=\/]*?)>")
juri_tag_single = re.compile("<([^a-z=\/ ]*)(?:(?: (?:.*)))?\/>")
html_tags = re.compile("<[a-z]*?\/?>")

# text patterns
get_tag_text_pair = '<{tag}>([\s\S]*?)<\/{tag}>'
get_tag_text_single = '<{tag}(?: ?(.*))?\/>'
