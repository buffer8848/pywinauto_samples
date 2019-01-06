import pandas as pd

path = 'C:/Users/24233/Desktop/fundList.xlsx'
data = pd.read_excel(path)
data = pd.DataFrame(data)
print(list(data['基金']))
print(list(data['可选基金']))
