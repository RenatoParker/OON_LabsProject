import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("sales_data.csv")

print(data)
data.plot()
plt.legend()
plt.show()

# 4
data.plot.scatter(x="toothpaste", y="month_number", alpha=0.5)
plt.legend()
plt.show()

# 5
print(data["bathingsoap"])
data.plot.bar( x="month_number" ,y="bathingsoap")
plt.show()

# 6
print(data["total_profit"])
data.plot.bar( x="month_number" ,y="bathingsoap")
plt.show()

data.plot(subplots=True)
plt.show()
# subplots=True

