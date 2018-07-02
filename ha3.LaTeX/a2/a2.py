"""
@Author Tom Schmidt (216204224)
@Author Stefan Poggenberg (218100161)
@Author Samuel Schöpa (216203821)
@Author Bjarne Hiller (216203851)

@License CC BY
"""

import pandas
import numpy

class HMM():
    def __init__(self, states, observations, transition_model, observation_model):
        self.states = states
        self.observations = observations
        self.transition_model = transition_model
        self.observation_model = observation_model

    def trans(self, x):
        """Berechne p(x_{t+1}|x_t=x)."""
        return pandas.DataFrame(self.transition_model[x]).T

    def likelihood(self, y, x):
        """Gibt p(y|x), d.h. die Wahrscheinlichkeit einer bestimmten Beobachtung, gegeben ein Zustand x, aus."""
        if y in self.observations and x in self.states:
            return self.observation_model[x][y]
        else:
            raise ValueError

    def predict(self, prior):
        """Gegeben eine Prior-Verteilung von Zustaenden p(x_t), berechne die Verteilung nach dem Predict-Schritt, d.h. p(x_{t+1}|x_t)."""
        prediction = pandas.DataFrame(index=['distribution'])
        for state in self.states:
            probability = 0
            for s in self.states:
                probability += prior[s]['distribution']*transition_model[s][state]
            prediction[state] = probability
        return prediction

    def update(self, prior, y):
        """Berechne p(x_t|y_t)."""
        post = pandas.DataFrame(index=['distribution'])
        for state in self.states:
            pass
        return post

    def filter(self, p, y):
        pass


if __name__=='__main__':
    states = ['awake','asleep']
    observations = ['no_movement', 'movement']
    transition_model = pandas.DataFrame(data=numpy.array([[0.8, 0.3], [0.2, 0.7]]), index=states, columns=states)
    observation_model = pandas.DataFrame(data=numpy.array([[0.4, 0.95], [0.6, 0.05]]), index=observations, columns=states)
    hmm = HMM(states, observations, transition_model, observation_model)

    prior = pandas.DataFrame(data=numpy.array([[0.5, 0.5]]), index=['distribution'], columns=states)
    print(hmm.predict(prior))
