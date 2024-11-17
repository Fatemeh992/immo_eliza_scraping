import pandas as pd

file_path="utils/all_properties_output.csv"
df= pd.read_csv(file_path)
#drops duplicates
df.drop_duplicates(subset=['postal_code','street','number','box'], inplace=True)
#drops the empty rows if there are any.
df.dropna(how='all',inplace=True)
#Changing the dtype to category, better for analysis
df['property_type']=df['property_type'].astype('category')
df['property_subtype']=df['property_subtype'].astype('category')
df['locality']=df['locality'].astype('category')
df['buildingState']=df['buildingState'].astype('category')
#replace missing values with a None
df.map(lambda x: None if pd.isna(x) else x)
df.to_csv("utils/cleaned_dataset.csv",index=False)
