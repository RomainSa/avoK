"""
Some basic stats on lawsuits
"""

from pathlib import Path

from avoK.model import Lawsuit


if __name__ == '__main__':

    # get all xml files
    p = Path('data/').glob('**/*')
    xml_paths = [x for x in p if x.is_file() and x.suffix == '.xml']

    # turn them ot lawsuits and read data
    lawsuits = [Lawsuit(p) for p in xml_paths]
    for l in lawsuits:
        l.read()

    # some stats
    n_lawsuits = len(lawsuits)

    print('{n_empty_lawsuits} lawsuits out of {n_lawsuits} are empty.'
          .format(n_lawsuits=n_lawsuits,
                  n_empty_lawsuits=sum([1 for l in lawsuits if len(l.get_text()) == 0])))

    print('{n_lawsuits_with_solution} lawsuits out of {n_lawsuits} have a solution.'
          .format(n_lawsuits=n_lawsuits,
                  n_lawsuits_with_solution=sum([1 for l in lawsuits if l.get_text('SOLUTION') is not None])))

    print('{n_lawsuits_with_solution} lawsuits out of {n_lawsuits} have a lawyer.'
          .format(n_lawsuits=n_lawsuits,
                  n_lawsuits_with_solution=sum([1 for l in lawsuits if l.has_lawyer()])))

    print('Average number of tags per lawsuit is: {avg_n_tags}.'
          .format(avg_n_tags=sum([len(l.tags) for l in lawsuits]) / n_lawsuits))
