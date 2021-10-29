import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("sales_data.csv")
print(data)
print(data["total_profit"])

data["total_profit"].plot()
plt.show()

data["total_profit"].plot(label="Profit data of last year", color="r",marker="o" , markerfacecolor="k",  linestyle="-", linewidth=3 )
# plt.rcParams['linestyle'] = "."
plt.legend()
plt.show()

