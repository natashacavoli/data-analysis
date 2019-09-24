"""."""
from wordcloud import WordCloud, STOPWORDS
from datetime import datetime
import collections
import matplotlib.pyplot as pyplot
import nltk
import pandas
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

    def _filtrar_essays(self):
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

        _list_df = self._filtrar_essays()

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

        except Exception as e:

            nltk.download("punkt")
            nltk.download("stopwords")

            raise Exception(e)

        return

    def _obter_frequencia(self, tokens):
        """."""
        frequency = collections.Counter(tokens)

        frequency = frequency.most_common()

        return frequency

    def teste(self):
        """."""
        _list_df = self._filtrar_essays()

        # Um df com diversas essays agrupadas
        _df = _list_df[0]

        # Primeira essay
        _essay = _df.iloc[0]

        # Pensar em uma forma de obter a melhor essay

        _text = _essay["essay_text"]
        # Removendo o encode p/ nao causar conflitos
        _text = _text.decode("utf-8")

        _tokens = self._tokenizer(text=_text)

        _frequency = self._obter_frequencia(tokens=_tokens)

        return _frequency
