import pandas as pd

dic = {'one':1,'two':2}

df = pd.DataFrame(columns=['one','two'])

df.append({'one':1,'two':2},ignore_index=True)
print(df)


dfObj = pd.DataFrame()


dfObj['one'] = [dic['one']]
dfObj['two'] = ['Riti']


print(dfObj)