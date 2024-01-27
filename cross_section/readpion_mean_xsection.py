import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def read_data(filename):
    # Read the content of the text file
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Initialize an empty dictionary to store data columns
    data_dict = {}

    # Extract labels from the comments
    for line in lines:
        if line.startswith('#ATTRIBUTE LABEL:'):
            line = line.replace('#ATTRIBUTE LABEL:', '', 1)
            labels = line.split()[1:]  # Splitting by whitespace and removing the '#NAME:' prefix
            labels = ["Bin_Min"] + labels  # Include "Bin_Min" as the first label
            break

    species = labels[2:]  # get all the species

    # Extract data from the lines after the '#DATA:' comment
    data_lines = [line for line in lines if not line.startswith('#')]
    for line in data_lines:
        values = line.split()
        for label, value in zip(labels, values):
            value = float(value)
            if label not in data_dict:
                data_dict[label] = []
            data_dict[label].append(value)

    return {"species": species, "names": labels, "dict" :data_dict}