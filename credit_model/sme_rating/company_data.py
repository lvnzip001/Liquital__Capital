import pandas as pd




def convertToDataFrame(dictionary):
    "convert dictionary to dataframe"
    if str(type(dictionary)) == "<class 'dict'>":
        return pd.DataFrame.from_dict(dictionary, orient="index")
    if str(type(dictionary)) == "<class 'list'>":
        return pd.DataFrame.from_dict(dictionary)


# def extractData(filename):
   
    
#     with open(filename) as f:
#         lines = (line.rstrip() for line in f)
#         lines = list(line for line in lines if line)
#         breakpoint()
#     # comma-seperated file so we split by using "commas"
#     headings = lines[0].split(",")
#     # create a list of key-value items/dictionaries (heading-data items)
#     rows = lines[1:]
#     companies = []
#     dataFrames = []
#     for row in rows:
#         company = {}
#         data = row.split(",")
#         #if data[0]== 'Pirates (Pty) Ltd':
#         #    breakpoint()
#         for i in range(len(data)):
#             try:
#                 company[headings[i]] = data[i]
#                 companies.append(company)
#             except:
#                 continue
            
        

#     return companies

def extractData(filename):
    count = 0
    with open(filename) as f:
        lines = (line.rstrip() for line in f)
        lines = list(line for line in lines if line)
    # comma-seperated file so we split by using "commas"
    headings = lines[0].split(",")
    # create a list of key-value items/dictionaries (heading-data items)
    rows = lines[1:]
    companies = []
    dataFrames = []
    for row in rows:
        company = {}
        data = row.split(",")
        #if data[0]== 'Pirates (Pty) Ltd':
        #    breakpoint()
        for i in range(len(data)):
            
            company
            count += 1
            company[headings[i]] = data[i]
           
       
            
        companies.append(company)

    return companies


def currentRatio(currentAssets, currentLiabilities):
    try:
        return float(currentAssets) / float(currentLiabilities)
    except:
        return 0.5


def debtServiceRatio(OperatingIncome, InterestExpense, PrincipalRepayment):
    """under the input_data sheet, implement the debtserviceRatio calculations"""
    try:
        return float(OperatingIncome) / (float(InterestExpense) + float(PrincipalRepayment))
    except:
        return 0.5


def debtRatio(totalAssets, totalLiabilities):
    """under the input_data sheet, implement the debtRatio calculations"""
    try:
        if float(totalLiabilities) / float(totalAssets) == 0:
            return 0.8
        else:
            return float(totalLiabilities) / float(totalAssets)
    except:
        return 0.8



def unencumberedAssetsToUnsecuredDebt(unencumberedAssets, unsecuredDebt):
    """under the input_data sheet, implement the unencumberedAssetsToUnsecuredDebt calculations"""
    try:
        return float(unencumberedAssets) / float(unsecuredDebt)
    except:
        return 0.5



def liquidAssetLoanCoverageRatio(outstandingInvoicesTotal, requiredFunding):
    """under the input_data sheet, implement the liquidAssetLoanCoverageRatio calculations"""
    try:
        return float(outstandingInvoicesTotal) / float(requiredFunding)
    except:
        return 0.2



def addDebtServiceCoverageRatio(company):
    """Adds the ratio calculations which would happen to the InputData sheet and deletes the existing value key pairs"""
   
    try:
        operatingIncome = company["Off-Taker Net Operating Income"]
    except:
        breakpoint()
    del company["Off-Taker Net Operating Income"]
    interestExpense = company["Interest Expense"]
    del company["Interest Expense"]
    principalRepayment = company["Principal Repayment"]
    del company["Principal Repayment"]
    debt_service_ratio = debtServiceRatio(
        operatingIncome, interestExpense, principalRepayment
    )
    company["Debt Service Cover Ratio"] = debt_service_ratio


def addCurrentRatio(company):
    """Adds the ratio calculations which would happen to the InputData sheet and deletes the existing value key pairs"""
    currentAssets = company["Current Assets"]
    del company["Current Assets"]
    currentLiabilities = company["Current Liabilities"]
    del company["Current Liabilities"]
    current_ratio = currentRatio(currentAssets, currentLiabilities)
    company["Current Ratio"] = current_ratio


def addDebtRatio(company):
    """Adds the ratio calculations which would happen to the InputData sheet and deletes the existing value key pairs"""
    totalLiabilities = company["Total Liabilities"]
    del company["Total Liabilities"]
    totalAssets = company["Total Assets"]
    del company["Total Assets"]
    debt_ratio = debtRatio(totalAssets, totalLiabilities)
    company["Debt ratio (D/A)"] = debt_ratio


def addUnencumberedAssetsToUnsecuredLoan(company):
    """Adds the ratio calculations which would happen to the InputData sheet and deletes the existing value key pairs"""
    unencumberedAssets = company["Unencumbered Assets"]
    del company["Unencumbered Assets"]
    unsecuredDebt = company["Unsecured Debt"]
    del company["Unsecured Debt"]
    unencumbered_assets_to_unsecured_debt = unencumberedAssetsToUnsecuredDebt(
        unencumberedAssets, unsecuredDebt
    )
    company[
        "Unencumbered Assets to the Unsecured Debt"
    ] = unencumbered_assets_to_unsecured_debt


def addLiquidAssetLoanCoverageRatio(company):
    """Adds the ratio calculations which would happen to the InputData sheet and deletes the existing value key pairs"""
    outstandingInvoicesTotal = company["Value of All Outstanding Invoices"]
    del company["Value of All Outstanding Invoices"]
    requiredFunding = company["Required Fundiing"]
    del company["Required Fundiing"]
    liquid_asset_loan_coverage_ratio = liquidAssetLoanCoverageRatio(
        outstandingInvoicesTotal, requiredFunding
    )
    company["Liquid Asset Loan Coverage Ratio"] = liquid_asset_loan_coverage_ratio

def liquid_assets_repayment(company):
    
    pass


def updateData(companies):
    for company in companies:
        # add "Debt Service Coverage Ratio"
       
        addDebtServiceCoverageRatio(company)
        # add "Current Ratio"
        addCurrentRatio(company)
        # add "Debt Ratio"
        addDebtRatio(company)
        # add "Unencumbered Assets to the Unsecured Debt"
        addUnencumberedAssetsToUnsecuredLoan(company)
        # add "Liquid Asset Loan Coverage Ratio"
        addLiquidAssetLoanCoverageRatio(company)


def getCompanyData(filename):

    """Function that returns the inoput data of the files"""
    # step ONE: extract data and store it in a dictionary (map)
    # TODO change this back to companies
    companies = extractData(filename)
    companies_1 = extractData(filename)

    # create and calculate all the relevant variables
    updateData(companies)
    # for item in companies_1[0].items():
    #    print (item)

    company = []
    company.append(companies[-1])
    return company


# def getCompanyData_t(filename="dummy_companies.txt"):
#     """Function that returns the inoput data of the files"""
#     # step ONE: extract data and store it in a dictionary (map)
#     # TODO change this back to companies
#     breakpoint()
#     company = extractData(filename)
#     companies_1 = extractData(filename)

#     updateData(company)

#     return company, companies_1


def getcompanybyname(company_name, filename):
    
    companies = extractData(filename)
    # create and calculate all the relevant variables
    updateData(companies)
    

    for company in companies:

        if "Timing of liquid assets repayment" not in company.keys():
            company["Timing of liquid assets repayment"] = 0.7
            company["Quality of liquid security loan coverage"] = 0.25

        if company["Entity Name"] == company_name:
            return company
    return {}



def getallcompanynames(filename):
    """Function that returns the all the company name in our current database in
    the form of 'dummy_companies.txt'"""
    # step ONE: extract data and store it in a dictionary (map)
    # TODO change this back to companies
    companies = extractData(filename)

    updateData(companies)

    name_dict = {}
    i = 0
    for company_info in companies:
        name_dict[f"company_{i}"] = company_info["Entity Name"]
        i += 1

    entity_names = {"entity_names": [name_dict]}
    # breakpoint()
    return entity_names
