"""."""
from wordcloud import WordCloud, STOPWORDS
from datetime import datetime
import matplotlib.pyplot as pyplot
import pandas
import nltk
import string


class DataAnalysis(object):
    """."""

    def __init__(self, id):
        """."""
        self.id = id
        # _columns_names = list(_df.columns.values)

    def _obter_dados(self):
        """."""
        r = pandas.read_csv("../essays.csv")

        return r

    def _tokenizer(self, text):
        """."""
        try:
            tokens = nltk.tokenize.word_tokenize(
                text)

            _stopwords = nltk.corpus.stopwords.words("portuguese")

            _punctuation = list(string.punctuation)

            tokens = [
                t for t in tokens if t not in _stopwords and
                t not in _punctuation
            ]

            return tokens

        except:

            nltk.download("punkt")
            nltk.download("stopwords")

            return self._tokenizer(text=text)

    def filtrar_essays(self):
        """."""
        _df = self._obter_dados()

        _themes = _df.groupby("theme_title")

        # Pegamos as essays com as maiores notas
        _res = _df.loc[_df["total_score"] >= 650.0]

        # Iteramos sobre os temas
        _themes = [theme for theme in _themes.indices]

        # Uma lista com dataframes agrupados por tema
        r = [_res.loc[_res["theme_title"] == theme] for theme in _themes]

        return r

    def _gerar_imagem(self, nome_img, text, stopwords=[]):
        """."""
        _stopwords = set(STOPWORDS)
        _stopwords.update(stopwords)

        _wordcloud = WordCloud(
            stopwords=_stopwords).generate(text=text)

        pyplot.imshow(_wordcloud, interpolation="bilinear")
        pyplot.axis("off")
        pyplot.savefig("../images/" + nome_img)

    def gerar_melhores_essays(self):
        """."""
        try:
            stopwords = nltk.corpus.stopwords.words("portuguese")
            stopwords = [w.encode("utf-8") for w in stopwords]

        except:
            nltk.download("stopwords")

            return self.gerar_melhores_essays()

        _list_df = self.filtrar_essays()

        for df in _list_df:

            nome_img = datetime.now().date().isoformat()

            # Agrupando os temas
            theme = list(set([d for d in df["theme_title"]]))

            for t in theme:
                nome_img += t

            nome_img += ".png"

            text = "".join(d for d in df["essay_text"])

            if len(text) > 0:

                self._gerar_imagem(
                    nome_img=nome_img, text=text, stopwords=stopwords)

        return "Yas"

    def a(self):
        """."""
        pass
