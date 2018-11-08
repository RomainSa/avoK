import re

from avoK import patterns


class Lawsuit(object):

    def __init__(self, xml_file):
        """
        :param xml_file: XML file containing affaire text
        :type xml_file: str
        """
        self.xml_file = xml_file
        self.text = None
        self.tags = None

    def _parse_xml(self):
        with open(self.xml_file, 'r') as f:
            self.text = f.read()

    def _get_tags(self):
        """
        Parse XML tags

        :return:
        """
        if self.text is None:
            raise ValueError('XML must be parsed first')
        else:
            self.tags = []
            for line in self.text.split('\n'):
                match = patterns.tags_regex.search(line)
                if match is not None:
                    self.tags.append(match.group(1))

    def read(self):
        """
        Function to be called in order to read XML file
        """
        self._parse_xml()
        self._get_tags()

    def get_text(self, tag=None):
        """
        Return lawsuit text (full if no text is specified, else return text corresponding to tags)
        """
        if tag is None:
            return self.text
        elif tag not in self.tags:
            raise ValueError('Tag "%s" is not present in text.' % tag)
        else:
            matches = re.findall(patterns.get_tag_text.format(tag=tag), self.text)
            if len(matches) > 0:
                return matches[0]
            else:
                return None

    def has_lawyer(self):
        """
        Check if trial report contains lawyer or not
        """
        return patterns.has_lawyer.search(self.text) is None
