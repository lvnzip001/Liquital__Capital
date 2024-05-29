from asyncio.windows_events import NULL
import math
from libcst import And
import pandas as pd
import numpy as np

from .company_data import convertToDataFrame, getCompanyData, getcompanybyname

from .ratings_data import getRatingsData, getScoresData, getFactors, getRatingsByDefaultProbability
from .variable_weighting_data import getWeightingData

print("="*50)

"""

Data Input for the model is utilized in this spreadsheet. The dataInput is then process with the model template from the other 
modules such as the rating.py and weightings.py ...

"""

# Get the order at h


def getRating(data, key, value, filename):
    ratings_head = list(pd.read_csv(filename).columns)
    
    values = data[key]

    
    # convert value to "float" type where applicable
    # instead of map and lambda use values.count(".")
    if True in (list(map(lambda x: x.count(".") > 0, values))):
        #this checks if the string is a value

        values = list(map(lambda x: float(x), values))
       
        value = float(value)
        
        print("trrigggered")
    

    elif False not in list(map(lambda x: x.isdigit(), values)):

        values = list(map(lambda x: int(x), values))
        value = int(value)

    # print(key+": "+str(values)+" -> value = "+str(value))
    #values = sorted(values)
    
    elif isinstance(value, str):

        return ratings_head[2:][values.index(value)]

    print(key,'==',value)
    
    

    for i in range(len(values)):
        #if key == 'Debt ratio (D/A)':
        #    breakpoint()
        if value <= values[i] and values[i] == min(values):
            
            return ratings_head[2:][i]
        
        elif value >= values[i] and values[i] == max(values):
            
            return ratings_head[2:][i]
        
        elif value >= values[i+1] and value < values[i] :
            
            return ratings_head[2:][i+1]
        
        elif value == values[i]:
            return ratings_head[2:][i]
            #    # ratings_head ['AAA', 'AA', 'A', 'BAA', 'BA', 'B', 'CAA']

    for i in range(len(values)):
        if (str not in [type(values[i]), type(value)]):
            if (value > values[i]):
                return ratings_head[2:][i]
    
    
    return ""


def getCompanyRatings(company, ratings_data, score_data):
    """ This function calculates the ratings as per the symbol for each Factor in the CreditRating Sheet
        eg AAA;	AA;	A;	BBB; BB; B;

        QA: currently give 17 Factors as per the model
        Bug: Not populating the correct rating (issue stems from the rating function) (cross reference with spreadsheet currently spreadsheet is not corresponding)
    """
    # company_copy = company copying a list like this causes the list to reference one object which changes everything
    company_copy = company.copy()
    
    ratings = getRatingsData(ratings_data)
    # TODO asl Miz about the Timing of liquid assets repayment, Quality of liquid security loan coverage
    # TODO How do we calculate these values
    # variables = list(ratings.keys())[:-2] #This removes factors:  Timing of liquid assets repayment ,Quality of liquid security loan coverage
    variables = list(ratings.keys())
    

  
    #variables gives us all we need in terms of the metrics considered for each factor. So here we should first check if 
    # the variable exists in the company data, if not we plug it in and then give it the lowest rating.
    #Get distinct list of all the variables in the company, check for each variable and then add if it doesnt exist
    # get the variable and give the lowest rating 
    
    #company_copy.pop("No. similar transactions completed")
    company_variables = list(company_copy.keys())
    
    for variable in variables:
        if variable not in company_variables:
            #penalize missing data, removing it
            company_copy[variable] = ratings[variable][-1]
            print(variable," removed!!!!!!!")
            #TODO make sure to remove the below
        #variable = 'Current Ratio'
        company_copy[variable] = getRating(
            ratings, variable, company_copy[variable], ratings_data)

    # the come out empty 'Current Ratio': '', 'Debt ratio (D/A)': ''
    scores = getScoresData(score_data)
    
    for key in list(company_copy.keys()):
        if company_copy[key] not in list(scores.keys()) and key != "Entity Name":
            del company_copy[key]

  
    return company_copy


def getCompanyScores(company, score_data, ratings_data):
    """ gets the score assocaited with the credit score
        eg  AA:3.8; BBB:2.6 etc
        """
    scores = getScoresData(score_data)
    company_copy = getCompanyRatings(company, ratings_data, score_data)
    
    factors = list(company_copy.keys())[1:]
    for variable in factors:

        company_copy[variable] = float(scores[company_copy[variable]])
    
    return company_copy


def getWeightedScores(company_name, company_data, weightings_data, score_data, ratings_data):
   
    company = getcompanybyname(company_name, company_data)
    funding_type = company["Funding Type"]
            
    # Company is coming in as a dictionary and it shouldnt be ofcause
    scores = getCompanyScores(company,score_data, ratings_data)
    weightings = getWeightingData(weightings_data)
    variables = list(scores.keys())[1:]
    sum_product = 0

    for variable in variables:
       
        weight = weightings[variable][funding_type]
        score = scores[variable]
        scores[variable] = score * weight
        sum_product += scores[variable]
    scores["Stand Alone Credit Score"] = sum_product
    return scores


def getWeightedScoresByFactor(company):
    variable_factors = getFactors()
    weighted_scores = getWeightedScores(company)
    variables = list(weighted_scores.keys())[1:-1]
    factors = list(set(list(variable_factors.values())))
    for factor in factors:
        score = 0
        for variable in variables:
            if variable_factors[variable] == factor:
                score += weighted_scores[variable]
                del company[variable]
        company[factor] = score
    return company
# print(getWeightedScores('Mizz Inc (Pty) Ltd'))


def getProbabilityOfDefault(score):
    return (math.e ** (score)) ** (-1)


def getRatingFromDefaultProbability(pr_default):
    probability_ratings = getRatingsByDefaultProbability()
    for rating in probability_ratings:
        if pr_default >= rating["Min"] and pr_default < rating["Max"]:
            return rating["Rating"]


# def overallCreditScore(company):
#    name = company["Entity Name"]
#    company = getCompanyByName(name)
#    track_record = float(company["Track Record with the Fund"])
#    management_behavioural_risk = float(company["Management Behavioural Risk"])
#    scores = getCompanyScores(company)
#    breakpoint()
#    stand_alone_score = scores["Stand Alone Credit Score"]

def overallCreditScore(company_name, 
                       company, 
                       company_data, 
                       weightings_data, 
                       score_data, 
                       ratings_data,
                       pd_rating_tbl):
    """Get the summary values"""

    stand_alone_credit_score = convertToDataFrame(
        getWeightedScores(company_name, company_data, weightings_data, score_data, ratings_data)).iloc[-1, 0]
    overall_credit_score = stand_alone_credit_score*(1-(float(company['Track Record with the Fund']) + float(company['Management Behavioural Risk'])))+float(
        company['Management Behavioural Risk'])*float(company['Rating Score'])+float(company['Track Record & Reference Checks'])*float(company['Track Record with the Fund'])
    
    probability_of_default = (1+np.exp(overall_credit_score)**(-1))-1
    pd_implied_rating = convertToDataFrame(getRatingsByDefaultProbability(pd_rating_tbl))

    for i in range(len(pd_implied_rating)):
        if probability_of_default >= pd_implied_rating.iloc[i, 1] and probability_of_default < pd_implied_rating.iloc[i, 2]:
            credit_rating = pd_implied_rating.iloc[i, 0]

    credit_summary = {'stand_alone_credit_score':stand_alone_credit_score,
                     'overall_credit_score':overall_credit_score,
                     'probability_of_default':probability_of_default,
                     'credit_rating':credit_rating   
                     }
    return credit_summary
# This is the guy that pulls everything together to make the magic happen.
# Find the input variable first and then that should indicate the direction.
def creditrating():
    """ Function that puts everything into a dataframe"""
    pass

def convert_to_df(data: dict):
    df = pd.DataFrame()

    for k in data.keys():
        df[f"{k}"] = [data[f"{k}"]]
       
    return df

def run_all_credit_func(company, ratings_data, weightings_data, score_data):
    outcomes = company
    factors = getFactors(ratings_data)
    scores = getCompanyScores(company, score_data, ratings_data)
    weighting = getWeightingData(weightings_data)
    rating = getCompanyRatings(company, ratings_data, score_data)

    df_combine = pd.DataFrame()
    df_combine['factors'] = factors.values()
    df_combine['measure'] = factors.keys()
    df_combine['outcomes'] = NULL
    df_combine['scores'] = NULL
    df_combine['weighting'] = NULL
    df_combine['rating'] = NULL

    

    
    for i in range(len(df_combine)) :
        df_combine['outcomes'].at[i] = outcomes[df_combine['measure'][i]] 
        df_combine['scores'].at[i] = scores[df_combine['measure'][i]] 
        df_combine['weighting'].at[i] = weighting[df_combine['measure'][i]][outcomes['Funding Type']]  
        df_combine['rating'].at[i] = rating[df_combine['measure'][i]]
    
    return(df_combine)
    

def main():
    companies = getCompanyData()
    breakpoint()
    overallCreditScore(companies[0])
    run_all_credit_func(companies[0])
    df_variable_factors = convertToDataFrame(getFactors())
    df_scores_by_variable = convertToDataFrame(getCompanyScores(companies[0]))
    df_rating_by_variable = convertToDataFrame(getCompanyRatings(companies[0]))
    companies = getCompanyData()
    overallCreditScore(companies[0])
    df_weighting = convertToDataFrame(getWeightingData())[
        [companies[0]['Funding Type']]]
    df_weighted_scores_by_variable = convertToDataFrame(
        getWeightedScores(companies[0]))

    companies = getCompanyData()
    companies = convertToDataFrame(companies[0])
    companies.drop(companies.index[1:4], inplace=True)
    # breakpoint()
    # df_scores_by_factor = convertToDataFrame(getWeightedScoresByFactor(companies[0]))
    df_score_rating = convertToDataFrame(getRatingsByDefaultProbability())

    print("Get Outcomes")
    print(companies)
    print()
    print("scores (by variable)")
    print(df_scores_by_variable)
    print()
    print(df_rating_by_variable)
    print("="*20)
    print()
    companies = getCompanyData()
    funding_type = companies[0]["Funding Type"]
    print(companies[0]["Entity Name"]+" funding type: "+funding_type)
    print(df_weighting)
    print()
    print("="*20)
    print("weighted scores (by variable)")
    print(df_weighted_scores_by_variable)
    print()
    print("="*20)
    print("variable factors:")
    print(df_variable_factors)
    print()
    print("="*20)
    print("weighted scores by factor")
    # print(df_scores_by_factor)
    # print()
    print("="*20)
    print("credit_sumary")
    print(convertToDataFrame(overallCreditScore(companies[0])))
    print("score rating table")
    print(df_score_rating)
    print()
    print("="*20)


#companies = getCompanyData()
#
#print(combine(companies[0]))
#print(convertToDataFrame(overallCreditScore(companies[0])))
#print(combine(getCompanyData([0])))
#print(overallCreditScore(getCompanyData([0])))

# lass CreditRating(): create a class from all of these
