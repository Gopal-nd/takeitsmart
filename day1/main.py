import pandas as pd
data = {
    'name':["gopal","Reddy","ND","superman"],
    'age':[20,23,99,None],
    'work':['remort','in person','user man','stap']
}
df = pd.DataFrame(data)

df.to_csv("raw_logs.csv", index=False)
print("Raw log file created")

df = pd.read_csv("raw_logs.csv")
print(df)

print(df.info())
print(df.isnull().sum())


