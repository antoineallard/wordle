# -*- coding: utf-8 -*-
# @author: Antoine Allard <antoineallard.info>


import json


class wordle_solver:
    """Set of methods to help solve wordle puzzles."""

    def __init__(self):
        self.information = self.get_empty_information()
        self.load_possible_words()


    def is_word_compatible(self, word, info=None):
        info = self.information if info is None else info
        if any(c in word for c in info['exclude_letters']):
            return False
        if all(c in word for c in info['include_letters']):
            if all(word[i] == info['known_positions'][i] for i in range(5) if info['known_positions'][i]!='*'):
                for wrong_position in info['wrong_positions']:
                    if any(word[i] == wrong_position[i] for i in range(5) if wrong_position[i]!='*'):
                        return False
                return True
            else:
                return False
        else:
            return False


    def get_compatible_word_scores(self):
        compatible_words = self.list_compatible_words(words=self.words, info=self.information)
        scores = [self.get_word_score(word, compatible_words) for word in compatible_words]
        scores, compatible_words =  zip(*sorted(zip(scores, compatible_words)))
        return compatible_words, scores


    def get_empty_information(self):
        return {'include_letters': [], 'exclude_letters': [], 'known_positions': '*****', 'wrong_positions': []}


    def get_word_score(self, word, compatible_words):
        score = 0
        for target in compatible_words:
            if target == word:
                score += 1
            else:
                info = self.get_empty_information()
                self.update_information(word, self.validate_word(word, target), info=info)
                score += len(self.list_compatible_words(words=compatible_words, info=info))
        return score
    

    # Extract the word list from https://www.powerlanguage.co.uk/wordle/main.814b2d17.js (array Ta=[...], downloaded on Jan 10th, 2022).
    # This function is very specific to that file. Inspection of the file is required should it be replaced by a more up-to-date one.
    def load_possible_words(self, fname='main.814b2d17.js', start='Ta=', stop=',Ca='):
        with open(fname, 'r') as file:
            line = file.readline()
            line = line.split(start)[1].split(stop)[0]
            self.words = json.loads(line)


    def list_compatible_words(self, words=None, info=None):
        words = self.words if words is None else words
        info = self.information if info is None else info
        return sorted([word for word in words if self.is_word_compatible(word, info)])


    def update_information(self, word, result, info=None):
        info = self.information if info is None else info
        wrong_position = ''
        known_positions = list(info['known_positions'])
        for i in range(5):
            if result[i] == 'g':
                if word[i] not in info['include_letters']:
                    info['include_letters'].append(word[i])
                known_positions[i] = word[i]
            if result[i] == 'b':
                if word[i] not in info['exclude_letters']:
                    if word[i] not in info['include_letters']:
                        info['exclude_letters'].append(word[i])
            if result[i] == 'y':
                if word[i] not in info['include_letters']:
                    info['include_letters'].append(word[i])
                wrong_position += word[i]
            else:
                wrong_position += '*'
        info['known_positions'] = ''.join(known_positions)
        if wrong_position != '*****':
            info['wrong_positions'].append(wrong_position)


    def validate_word(self, word, solution):
        word = list(word)
        solution = list(solution)
        result = []
        black_letters = []
        for i in range(5):
            if word[i] == solution[i]:
                result.append('g')
            else:
                result.append('b')
                black_letters.append(solution[i])
        for i in range(5):
            if result[i] == 'b':
                if word[i] in black_letters:
                    result[i] = 'y'
        return ''.join(result)
