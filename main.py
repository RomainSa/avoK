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
    print('{n_lawsuits_with_solution} lawsuits out of {n_lawsuits} have a solution.'
          .format(n_lawsuits=len(lawsuits),
                  n_lawsuits_with_solution=sum([1 for l in lawsuits if l.get_text('SOLUTION') is not None])))
    print('{n_lawsuits_with_solution} lawsuits out of {n_lawsuits} have a lawyer.'
          .format(n_lawsuits=len(lawsuits),
                  n_lawsuits_with_solution=sum([1 for l in lawsuits if l.has_lawyer()])))
