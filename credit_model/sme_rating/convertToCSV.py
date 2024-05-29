import pandas as pd
from os.path import exists

from company_data import getCompanyData


def extract_from_excel_file():
    excel_input_data_file = 'sme_rating\Demo sme_rating Model.xlsx'
    excel_input_data_sheet = 'InputData'

    xl_file = pd.ExcelFile(excel_input_data_file)
    input_data = pd.read_excel(xl_file, excel_input_data_sheet)
    company = input_data[0:4].iloc[:, [1, 2]]
    variables = input_data[6:].iloc[:, [3,4]]
    company = company.to_dict()
    variables = variables.to_dict()
    

    def valid_key_value_pair(key, keys, values):
        valueNotNull = str(values[keys.index(key)]).lower() != "nan"
        keyIsText = not str(key).replace(".","").isdigit()
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
    for key in keys:
        # print(str(key)+": "+str(values[keys.index(key)]))
        if valid_key_value_pair(key, keys, values):
            # print("valid")
            company_data[key] = values[keys.index(key)]
    return(company_data)


def company_exists(company_name, filename='sme_rating\dummy_companies.txt'):
    if not exists(filename):
        filename = input("Please specify filename that you would like to add company data to (e.g. 'data/company_data.csv'): ")
    with open(filename) as f:
        lines = (line.rstrip() for line in f) 
        lines = list(line for line in lines if line)
    headings = lines[0]
    print("headings = "+str(headings.split(",")))
    entity_name_index = headings.split(",").index("Entity Name")
    rows = lines[1:]
    for row in rows:
        # split rows from comma-sepertad string to a list and store as "values"
        values = row.split(",")
        if (company_name == values[entity_name_index]):
            return True
    return False


def changes_detected(company):

    # print("company: ")
    # print(convertToDataFrame(company))
    # print()
    companies = getCompanyData()
    company_names = list(map(lambda x: x["Entity Name"], companies))
    # print("company names = "+str(company_names))
    if (company_exists(company["Entity Name"])):
        index = company_names.index(company["Entity Name"])
        # print("index = "+str(index))
        # print(convertToDataFrame(companies[index]))
        for key in list(company.keys()):
            if key in list(companies[index].keys()):
                if (str(company[key]) != str(companies[index][key])):
                    print(key+": company = "+str(company[key])+" vs companies[index] = "+str(companies[index][key]))
                    print(str(type(company[key]))+" vs "+str(type(companies[index][key])))
                    return True
    return False


def add_to_csv_file(filename='sme_rating\dummy_companies.txt'):
    
    company_data = extract_from_excel_file()

    if not company_exists(company_data["Entity Name"], filename):
        row_data = ""
        for value in list(company_data.values()):
            row_data += str(value)+","
        if row_data.count("NaN") > 0:
            print("There is missing data, please update before upload.\n")
        else:    
            with open(filename, 'a') as f:
                f.write("\n"+row_data[:-1])
    else:
        update_company_data = "no"
        if changes_detected(company_data):
            update_company_data = input("Would you like to update "+company_data["Entity Name"]+"'s data? (y/n) ")
        if update_company_data[0].lower() == "y":
            #update the current file
            row_data = ""
            for value in list(company_data.values()):
                row_data += str(value)+","
            # print("row_data = "+row_data+"\n")
            if row_data.count("NaN") > 0:
                print("There is missing data, please update before upload.\n")
            else:
                with open(filename, 'r') as f:
                    lines = (line.rstrip() for line in f)
                    lines = list(line for line in lines if line)
                for line in lines:
                    if line.split(",")[0] == company_data["Entity Name"]:
                        lines[lines.index(line)] = row_data[:-1]
                with open(filename, 'w') as f:
                    f.write('\n'.join(lines))

