import pandas as pd 
import numpy as np 
import string

letters = np.array(list(string.ascii_lowercase + ' '))

N = int(input("enter the number of records required to create ?"))

df = pd.DataFrame(columns=['Transaction ID','Transaction sale', 'Customer name', 'category of item'])

df['Transaction ID'] = np.arange(N)
df['Transaction sale'] = np.random.randint(1,500000,N,)
df['Customer name'] =  [np.random.choice(letters, size=3) for i in range(N)]
df['category of item'] = np.random.uniform(1,1500,N)

print(df)
df.to_csv("dataset.csv")

