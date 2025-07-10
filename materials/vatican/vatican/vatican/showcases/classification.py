from ..database import VaticanMongoDb


class PopeBayesianClassifier(object):

    def __init__(self, pope: str, db: VaticanMongoDb, alpha: float = 0.0001):
        self.db = db
        self.pope = pope
        self.words_frequencies = db.term_count(normalized=True)
        self.pope = pope
        self.pope_probs = db.pope_term_count(pope, normalized=True)
        pope_stats = {}
        for pope in db.popes:
            pope_freq = db.pope_term_count(pope)
            pope_stats[pope] = pope_freq.sum()
        self._prior = pope_stats[self.pope] / sum(v for v in pope_stats.values())
        self.alpha = alpha

    @property
    def prior(self):
        return self._prior

    def p_word(self, word: str):
        return self.words_frequencies.get(word, default=self.alpha)

    def p_word_pope(self, word: str):
        return self.pope_probs.get(word, default=self.alpha)