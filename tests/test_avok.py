import unittest

from avoK.model import Lawsuit


class TestLawsuitMethods(unittest.TestCase):

    def setUp(self):
        self.raw_text = """
        <ID>JURITEXT000</ID>
        <TITRE>Cour d'appel de Paris, 1 juin 2018, 15/130157</TITRE>
        <DATE_DEC>2099-06-01</DATE_DEC>
        <PUBLI_BULL publie="non"/>
        <JURIDICTION>Cour d'appel de Paris</JURIDICTION>
        <SOLUTION>Confirme la décision déférée dans toutes ses dispositions, à l'égard de toutes les parties au recours</SOLUTION>
        <AVOCAT_GL/>
        <CONTENU>
        <br/>Copies exécutoires RÉPUBLIQUE FRANÇAISE<br/>délivrées aux parties le : AU NOM DU PEUPLE FRANÇAIS<br/>
        <br/>COUR D'APPEL DE PARIS<br/>Pôle 66 - Chambre 12<br/>
        <br/>ARRÊT DU 01 JUIN 2099<br/>
        <br/>APPELANTS<br/>
        <br/>Monsieur B... U...<br/>né le [...] à Boston (Texas)
        <br/>et
        <br/>Madame Marie-Thérèse F... épouse Y...<br/>née le [...] à Narnya (75033)<br/>
        <br/>demeurant [...]<br/>
        <br/>Représentés tous deux et assistés sur l'audience par Me Marco PANTANI
        <br/>
        <br/>INTIMÉS<br/>
        <br/>Monsieur Gérard D...<br/>né le [...]  à Pessac<br/>et<br/>Madame Véronique S...<br/>née le [...] à Mérignac<br/>
        <br/>demeurant [...]<br/>
        <br/>Représentés tous deux et assistés sur l'audience par Me Bernard LAVILLIERS, avocat au barreau de NEW-YORK, toque : R666<br/>
        <br/>
        </CONTENU>
        """
        self.lawsuit = Lawsuit(xml_file='')
        self.lawsuit.text = self.raw_text
        self.lawsuit._get_tags()

    def test_get_tags(self):
        tags = ['ID', 'TITRE', 'DATE_DEC', 'PUBLI_BULL', 'JURIDICTION', 'SOLUTION', 'AVOCAT_GL', 'CONTENU']
        self.assertEqual(set(tags), set(self.lawsuit.tags))

    def test_get_text_full(self):
        self.assertEqual(self.lawsuit.get_text(tag=None), self.raw_text)

    def test_get_text_id(self):
        self.assertEqual('JURITEXT000', self.lawsuit.get_text(tag='ID'))

    def test_get_text_avocatgl(self):
        self.assertEqual('', self.lawsuit.get_text(tag='AVOCAT_GL'))

    def test_get_text_publi(self):
        self.assertEqual('publie="non"', self.lawsuit.get_text(tag='PUBLI_BULL'))

    def test_get_contenu(self):
        contenu = """
        <br/>Copies exécutoires RÉPUBLIQUE FRANÇAISE<br/>délivrées aux parties le : AU NOM DU PEUPLE FRANÇAIS<br/>
        <br/>COUR D'APPEL DE PARIS<br/>Pôle 66 - Chambre 12<br/>
        <br/>ARRÊT DU 01 JUIN 2099<br/>
        <br/>APPELANTS<br/>
        <br/>Monsieur B... U...<br/>né le [...] à Boston (Texas)
        <br/>et
        <br/>Madame Marie-Thérèse F... épouse Y...<br/>née le [...] à Narnya (75033)<br/>
        <br/>demeurant [...]<br/>
        <br/>Représentés tous deux et assistés sur l'audience par Me Marco PANTANI
        <br/>
        <br/>INTIMÉS<br/>
        <br/>Monsieur Gérard D...<br/>né le [...]  à Pessac<br/>et<br/>Madame Véronique S...<br/>née le [...] à Mérignac<br/>
        <br/>demeurant [...]<br/>
        <br/>Représentés tous deux et assistés sur l'audience par Me Bernard LAVILLIERS, avocat au barreau de NEW-YORK, toque : R666<br/>
        <br/>
        """
        self.assertEqual(contenu, self.lawsuit.get_text(tag='CONTENU'))

    def test_has_lawyer(self):
        self.assertTrue(self.lawsuit.has_lawyer())

    def test_get_names(self):
        raise NotImplementedError()


if __name__ == '__main__':
    unittest.main()
