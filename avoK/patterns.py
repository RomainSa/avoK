import re

# text patterns
get_tag_text_pair = '<{tag}>([\s\S]*?)<\/{tag}>'
get_tag_text_single = '<{tag}(?: ?(.*))?\/>'
name = '[A-Z][a-zà-ÿ]+(?:-[A-Z][a-zà-ÿ]+)?'
surname = '[A-Z]+'

# compiled patterns
has_lawyer = re.compile(r"(?:Me|Maître|SELARL|SELAS|SCP)(?:\s|\xa0)")
juri_tag_pair = re.compile(r"<\/?([^a-z=\/]*?)>")
juri_tag_single = re.compile(r"<([^a-z=\/ ]*)(?:(?: (?:.*)))?\/>")
html_tags = re.compile(r"<[a-z]*?\/?>")
multiple_line_breaks = re.compile(r"\n+")
lawyer_name = re.compile(r"(?:Me|Maître|SELARL|SELAS|SCP)(?:\s|\xa0)({name}(?:\s|\xa0){surname})".format(
    name=name, surname=surname
))

