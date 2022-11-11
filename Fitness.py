# Fitness
import numpy as np
heuristic_map = {0:0, 1:10, 2:5, 3:3, 4:3, 5:1, 6:7}

def fitness(environment, organism):
    fit = 0
    for i in range(4):
        fit += fitness_chord(environment[i*4, i*4+4], organism[i*4, i*4+4])
    return fit
def fitness_chord(chord, organism):
    fit = 0
    for note in organism:
        fit += heuristic(chord, note)
def heuristic(chord, note):
    heur = 0
    for tone in chord:
        tone_diff = abs(tone-note) % 12
        if tone_diff > 6:
            tone_diff = 12-tone_diff
        heur += heuristic_map[tone_diff]