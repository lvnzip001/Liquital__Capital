from numpy import rad2deg
import pandas as pd

""" This script serves to bring in the template of the model, not of the actual model inputs are used
    Those are under the data.py module"""



def getRatingsData(filename):  
    """ Provides the possible outcomes for each Factor
    Eg. 'No. similar transactions completed': ['6', '5', '4', '3', '2', '1', '0']

    Not influenced by DataInput
    """
    with open(filename) as f:
        lines = (line.rstrip() for line in f) 
        lines = list(line for line in lines if line)
    # comma-seperated file so we split by using "commas"
    headings = lines[0].split(",")
    # create a list of key-value items/dictionaries (heading-data items)
    variables = lines[1:]
    rating = {}
    for variable in variables:
        data = variable.split(",")
        variableName = data[0]
        rating[variableName] = []
        for i in range(2,len(data)):
            rating[variableName].append(data[i])
     
    return rating


def getScoresData(filename):
    """ States the crediting scoring eg {'AAA': '4.65', 'AA': '3.8', 'A': '3.15', 'BAA': '2.6', 'BA': '2.15', 'B': '1.75', 'CAA': '1.3'}, 
        
        This can be referenced from the excel model sheet ModelTemplate, is not influenced by current inputs
    """
    with open(filename) as f:
        lines = (line.rstrip() for line in f) 
        lines = list(line for line in lines if line)
    # create a list of key-value items/dictionaries (heading-data items)
    pairs = lines[1:]
    rating_score = {}
    for pair in pairs:
        data = pair.split(",")
        rating = data[0]
        score = data[1]
        rating_score[rating] = score
    return rating_score



def getHeaders(filename='model/sme_rating/ratings.txt'):
    """ Simply brings in the ratings.txt as a dataframe
    
        Referencing the model in the excel spreadsheet this takes
        in the ModelTemplate sheet
    """
    data = pd.read_csv(filename)
   
    return data



def getFactors(filename):

    """ Provides the dictionary of the considered varaibles under each factor as a key
        Eg Factor1:Contract Performance Risk consists of 
                - No. similar transactions completed
                - Sourcing of  the Service Rendered
                - Likelihood of service delivery delay
           Factor2:Debt Service Cover Ratio
           Factor5:Quality of liquid security loan coverage

        This is returned in the form of a dictionary
        
    """

    with open(filename) as f:
        lines = (line.rstrip() for line in f) 
        
        lines = list(line for line in lines if line)
        
    # comma-seperated file so we split by using "commas"
    headings = lines[0].split(",")
    # create a list of key-value items/dictionaries (heading-data items)
    variables = lines[1:]
    rating = {}
    for variable in variables:
        data = variable.split(",")
        variableName = data[0]
        factor = data[1]
        rating[variableName] = factor
   
    return rating


def getRatingsByDefaultProbability(pd_rating_tbl):
    """ function that calcualtes the PD Implied Credit Rating Score within the CreditRating sheet.
        Returns the table in dictionary form
        
        """
    #! Need to improve this function and that should be easy enough , Pd table should be stored at a dataframe
    filename= pd_rating_tbl
    sheet_name='CreditRating'
    xl_file = pd.ExcelFile(filename)
    sheet_data = pd.read_excel(xl_file, sheet_name)
    ratings =  sheet_data[3:24].iloc[:, list(range(14,17))]
    ratings = ratings.to_dict()
    minimums = ratings[list(ratings.keys())[1]]
    maximums = ratings[list(ratings.keys())[2]]
    ratings = ratings[list(ratings.keys())[0]]
    all_ratings = []
    for i in range(1,len(list(ratings.values()))):
        prob_rating = {}
        prob_rating["Rating"] =list(ratings.values())[i]
        prob_rating["Min"] =list(minimums.values())[i]
        # print("max: "+str(list(maximums.values())[i]))
        prob_rating["Max"] =float(str(list(maximums.values())[i]).replace("nan","1"))
        all_ratings.append(prob_rating)
    return all_ratings

