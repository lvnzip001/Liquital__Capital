
from .company_data import convertToDataFrame


def getWeightingData(filename:str):  
    """ Generates a dictionary, uses the factor as a key and the values of the dictionary are the funding type
    eg 'Quality of liquid security loan coverage': {'Purchase Order Financing': 0.075, 'Invoice Discounting': 0.125, 'Contract Financing': 0.075}"""
    with open(filename) as f:
        lines = (line.rstrip() for line in f) 
        lines = list(line for line in lines if line)
    # comma-seperated file so we split by using "commas"
    headings = lines[0].split(",")
    # create a list of key-value items/dictionaries (heading-data items)
    variables = lines[1:]
    weighting = {}
    for variable in variables:
        data = variable.split(",")
        variableName = data[0]
        weighting[variableName] = {}
        for i in range(1,len(data)):
            weighting[variableName][headings[i]] = float(data[i])
    return weighting

