import pandas as pd
data= pd.read_csv("sales_data.csv")

df = pd.DataFrame(
    {
        "Name": [
            "Braund, Mr. Owen Harris",
            "Allen, Mr. William Henry",
            "Bonnell, Miss. Elizabeth",
        ],
        "Age": [22, 35, 58],
        "Sex": ["male", "male", "female"],
    }
)

print("Data frame:\n",df)
print("Series:\n",df["Age"])

#When selecting a single column of a pandas DataFrame, the result is a pandas Series. To select the column, use the column label in between square brackets

#Serie from scratch:

ages = pd.Series([22, 35, 58], name="Age")
print(ages)

