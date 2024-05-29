from aifc import Error
from audioop import add
from posixpath import split
from tkinter import Y
import pandas as pd
from os.path import exists

#from company_data import getCompanyData, convertToDataFrame, extractData

# company_data_file = 'dummy_companies.txt'                             # Essentailly our exisiting Db
#excel_input_file = 'Demo sme_rating Model.xlsx'
# excel_input_data_sheet = 'InputData'                                             # Excel sheet


def extract_from_excel_file(excel_input_file):
    """
    This function is to extract specific company information, eg excel sheet is populated by "company analyst"
    
    Args:
    InputData excel sheet

    Usage: check if what is input in the InputData sheet processed correct. Variables are temp_dictionary and company data . 

    Returns:
     Company Data in form a dictionary
    """

    #global excel_input_data_file
    #global excel_input_data_sheet

    xl_file = pd.ExcelFile(excel_input_file)
    input_data = pd.read_excel(xl_file, 'InputData')
   
    company = input_data.iloc[0:4, [1, 2]]
    variables = input_data.iloc[6:, [3, 4]]
    company = company.to_dict()
    variables = variables.to_dict()
    
    
    def valid_key_value_pair(key, keys, values):
        valueNotNull = str(values[keys.index(key)]).lower() != "nan"
        keyIsText = not str(key).replace(".", "").isdigit()
        return valueNotNull and keyIsText

    # add company specific variables
    company_data = {}
    keys = list(company[list(company.keys())[0]].values())
    values = list(company[list(company.keys())[1]].values())
   
    for key in keys:
        if valid_key_value_pair(key, keys, values):
            company_data[key] = values[keys.index(key)]
    # add other variables
   
    keys = list(variables[list(variables.keys())[0]].values())
    values = list(variables[list(variables.keys())[1]].values())

    # turn to dictionary
    temp_dictionary = {}
    i = 0
    for key in keys:
        temp_dictionary[key] = values[i]
        i += 1
    
    # fix missing values
    list_to_clean = keys[0:keys.index('Required Fundiing')+1]
    clean_list = [x for x in list_to_clean if pd.isnull(x) == False]
    default_values = [0, 'Fully Outsourced', 'Highly Unlikely', 0, 0, 0, 0,
                      0, 0, 0, 0, 'Irreconcilable', 'Totally Tainted', 8, 
                      'Totally Tainted','Poor',0,0,0,0,0]
    
    for i in range(len(clean_list)):
        if pd.isnull(temp_dictionary[clean_list[i]]):
           temp_dictionary[clean_list[i]] = default_values[i]
    
    keys = list(temp_dictionary.keys())
    values = list(temp_dictionary.values())

    for key in keys:
        if valid_key_value_pair(key, keys, values):
            # print("valid")
            company_data[key] = values[keys.index(key)]

    # for now I simply calculate Timing of liquid assets and quality of securities from here 
    date_metric = input_data.iloc[37:52, [3,4,5]]
    date_metric = date_metric.dropna(axis = 0)
    loan_metric =  input_data.iloc[52, [3,4,5]]
    payment_quality = list(input_data.iloc[55:70, 7])
    

    asset_repayment_list = []
    quality_security_list = []
    for i in range(len(date_metric)):
        
        if date_metric.iloc[i,2] > loan_metric[2]:
            asset_repayment_list.append(date_metric.iloc[i,1])

        if payment_quality[i] == "High Quality":
            quality_security_list.append(date_metric.iloc[i,1])

    #Invoices, we dont need them anymore
    #breakpoint()
    for i in range(15):
        company_data.pop(f'Invoice {i+1}')
    #company_data.pop('Loan Amount')

    company_data['Timing of liquid assets repayment'] = sum(asset_repayment_list)/loan_metric[1]

    company_data['Quality of Security'] = sum(quality_security_list)/ sum(date_metric.iloc[:,1])

    
    
    return(company_data)


def company_exists(company_name=None, filename='model/sme_rating/dummy_companies.txt'):
    """
    Function to identify whether a company exists within the dictionary of existing companies

    Usecase:
    First check is to see if the file exists (refering to the database). why are we giving this option? would each company not have one database/list of companies
    (I guess use case is if we have access to multiple databases)
    We check that a company is exists. If not then they us#er would have to fill in the Input datasheet, 
    and process the file using the extract_from_excel_file function


    Returns:
     Company Data in form a dictionary
    """
    # if not exists(filename):
    #    filename = input(
    #        "Please specify filename that you would like to add company data to (e.g. 'data/company_data.csv'): ")
    with open(filename) as f:
        lines = (line.rstrip() for line in f)
        lines = list(line for line in lines if line)
    headings = lines[0]
    #print("headings = "+str(headings.split(",")))
    entity_name_index = headings.split(",").index("Entity Name")
    rows = lines[1:]
    for row in rows:
        # split rows from comma-sepertad string to a list and store as "values"
        values = row.split(",")
        if (company_name == values[entity_name_index]):
            return True
    # return False, "C"
#print(company_exists('Mizz Inc (Pty) Ltd', filename=company_data_file), "Okay it Ran")


def update_or_add_data(company_data, filename, option: str = 'update'):
    """

    This function is to update or add data, currently it write to the txt database we have set up.
    The option variable takes a string of 'update' by default, thus if you want to add data specify add.

    """
    row_data = ""
    for value in list(company_data.values()):
        row_data = ""
        for value in list(company_data.values()):
            row_data += str(value)+","
        print(row_data)
        # print("row_data = "+row_data+"\n")
        if row_data.count("NaN") > 0:
            print("There is missing data, please update before upload.\n")
        else:
            if option == 'add':
                with open(filename, 'a') as f:
                    f.write("\n"+row_data[:-1])
                    return ("Company Added")
            else:
                with open(filename, 'r') as f:
                    lines = (line.rstrip() for line in f)
                    lines = list(line for line in lines if line)
                for line in lines:
                    if line.split(",")[0] == company_data["Entity Name"]:
                        lines[lines.index(line)] = row_data[:-1]
                with open(filename, 'w') as f:
                    f.write('\n'.join(lines))

                    return(company_data["Entity Name"] + " Entity data updated")


def add_to_csv_file(filename, company_name=None, excel_input_file=None, update='y'):
    """
    Main Function of the extract process
    This function populates the company_data_file , so if the company doesnt exist than it is added using this function. 
    We know what company we are dealing with because of the person adding the inputData sheet.

    UseCase:
    1. Client choose from a list if your company is there. Currently, just use function input to choose company or leave as blank default to none. 
    2. If company the client chooses is new or doesnt exist, the client will upload the InputData sheet. (feature built in the UI)

    """

    # Placeholder to give the client a chance to chose the company by calling it up
    if not company_exists(company_name, filename):
        print("Provided company doesnt exist, please upload InputData")

        company_data = extract_from_excel_file(excel_input_file)

        # if not true, if company doesnt exist
       
        if company_exists(company_data["Entity Name"], filename):
            update_company_data = update
            if update_company_data[0].lower() == "y":
                # update the current file
                update_or_add_data(company_data,filename ,'update')
            else:
                return("Okay No Update")
        else:
            update_or_add_data(company_data, 'add')

    else:
        # update_company_data = input(
        #    "Would you like to update " + company_name + "'s data? (y/n) ")  # if  true, company exist
        update_company_data = update
        if update_company_data[0].lower() == "y":
            "Upload InputData"
            company_data = extract_from_excel_file()
            # update the current file
            update_or_add_data(company_data, 'update')
        else:
            return("Okay no update")



def del_company_data(company_name, filename='model/sme_rating/dummy_companies.txt'):
    """
    Delete Company Entry when we needed.
    """
    row_data = ""
    with open(filename, 'r') as f:
        lines = (line.rstrip() for line in f)
        lines = list(line for line in lines if line)
    for line in lines:
        if line.split(",")[0] == company_name:
            lines[lines.index(line)] = row_data[:-1]
    with open(filename, 'w') as f:
        f.write('\n'.join(lines))
    return(company_name + " Entry Deleted")


#print(company_exists('Mizz I (Pty) Ltd',filename=company_data_file), '---->>>>>')

# print(add_to_csv_file( filename=company_data_file), '---->>>>>')   #test should say doesnt exist, and then load the InputData Sheet

# TODO company exists from function input, so should simply ask for update
#print(add_to_csv_file('Jazz Inc (Pty) Ltd',filename= 'dummy_companies.txt' ), '---->>>>>')

# TODO (Below Scenario) Spelling wrong should say company doesnt exist, asks for  excel inputdata will say company exists, and ask for update
#print(add_to_csv_file('Mizz In (Pty) Ltd', filename=company_data_file), '---->>>>>')

# TODO (Below Scenario) Deleted Mizz entry, so it should says doesnt exist and add the data
#print(del_company_data('Mizz Inc (Pty) Ltd'))


#print(add_to_csv_file('Mizz Inc (Pty) Ltd',filename=company_data_file), '---->>>>>')
