from corpus import tokenization, detokenize, test_data
from nltk.util import pad_sequence
from nltk.util import ngrams
from nltk.probability import ConditionalFreqDist, FreqDist
import random


class LanguageModel:

    def __init__(self, n):
        self.n = n
        self.n_grams = []
        self.cfdist = ConditionalFreqDist()
        self.dist = FreqDist()

    def train(self, token_sequences):
        updated_n_gram = []
        # create n-grams from the training data
        for token_sequence in token_sequences:
            token = tokenization(token_sequence)
            # padding
            token_n = list(pad_sequence(token,
                                        pad_left=True, left_pad_symbol="<PAD>",
                                        pad_right=True, right_pad_symbol="<PAD>",
                                        n=self.n))
            updated_n_gram.append(list(ngrams(token_n, n=self.n)))
            flat_n_gram = [
                item for sublist in updated_n_gram for item in sublist]
        if self.n > 1:
            for gram in flat_n_gram:
                self.cfdist[gram[:self.n-1]][gram[-1]] += 1
        else:
            for gram in flat_n_gram:
                self.dist[gram] += 1

    def get_prob(self):
        if self.n > 1:
            prob_cfdist = self.cfdist
            for gram in prob_cfdist:
                total_count = float(sum(prob_cfdist[gram].values()))
                for word in prob_cfdist[gram]:
                    prob_cfdist[gram][word] /= total_count
            return prob_cfdist
        else:
            prob_dist = self.dist
            total_count = float(sum(prob_dist.values()))
            for gram in prob_dist:
                prob_dist[gram] /= total_count
            return prob_dist

    def p_next(self, tokens):

        prob_cfdist = self.get_prob()

        if len(tokens) == 0:
            return {prob_cfdist.max()[0]: prob_cfdist[prob_cfdist.max()]}
        elif len(tokens) == 1:
            return dict(prob_cfdist.get((tokens[0],)).items())
        elif len(tokens) >= 2:
            return dict(prob_cfdist.get(tuple(tokens)).items())

    def generate(self):
        prob_cfdist = self.get_prob()

        generate_text = list(random.choice(list(prob_cfdist.keys())))
        if self.n > 1:
            while generate_text[-1] != '<PAD>':
                new_word = prob_cfdist.get(
                    tuple(generate_text[(-self.n + 1):])).max()
                generate_text.append(new_word)
                if len(generate_text) > 20:
                    break
            generate_text = detokenize(generate_text[:-1])
        else:
            while len(generate_text) < 10:
                new_word = prob_cfdist.max()[0]
                generate_text.append(new_word)
            generate_text = detokenize(generate_text)

        return(generate_text)


granny = LanguageModel(3)
granny.train(test_data[:20000])
print(granny.generate())
