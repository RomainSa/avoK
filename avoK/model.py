import re

from avoK import patterns


class Affaire(object):

    def __init__(self, xml_file):
        """
        :param xml_file: XML file containing affaire text
        :type xml_file: str
        """
        self.xml_file = xml_file
        self.text = None
        self.tags = None
        # other
        self.tags_regex = '<([A-Z_]+)\/?>'

    def parse_xml(self):
        with open(self.xml_file, 'r') as f:
            self.text = f.read()

    def get_tags(self):
        """
        Parse XML tags

        :return:
        """
        if self.text is None:
            raise ValueError('XML must be parsed first')
        else:
            self.tags = []
            for line in self.text.split('\n'):
                match = re.search(self.tags_regex, line)
                if match is not None:
                    self.tags.append(match.group(1))

    def has_lawyer(self):
        """
        Check if trial report contains lawyer or not
        """
        return patterns.has_lawyer.search(self.text) is None
