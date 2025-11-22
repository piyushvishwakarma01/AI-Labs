import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from hmmlearn.hmm import GaussianHMM

print("Downloading stock data...")

ticker = "AAPL"
start_date = "2014-01-01"
end_date = "2024-01-01"

data = yf.download(ticker, start=start_date, end=end_date)

print("\nFirst 5 rows raw:")
print(data.head())


if isinstance(data.columns, pd.MultiIndex):
    # Take FIRST LEVEL (Close, Open, High, Low, Volume)
    data.columns = data.columns.get_level_values(0)

print("\nColumns after correct fix:")
print(data.columns)


adj_close = data["Close"]

data["Returns"] = adj_close.pct_change()
data = data.dropna()

print("\nProcessed data:")
print(data.head())

# Prepare data
returns = data["Returns"].values.reshape(-1, 1)


print("\nTraining 2-state HMM...")
model = GaussianHMM(
    n_components=2, covariance_type="full", n_iter=1000
).fit(returns)

hidden_states = model.predict(returns)
data["Hidden State"] = hidden_states

print("\nTransition Matrix:")
print(model.transmat_)

plt.figure(figsize=(15, 6))
plt.plot(data.index, data["Close"], label="Adjusted Close")
plt.title("AAPL Adjusted Close Price")
plt.savefig("hmm_price.png")
plt.close()

plt.figure(figsize=(15, 6))
plt.scatter(data.index, hidden_states, c=hidden_states, cmap="coolwarm", s=10)
plt.title("Hidden States (2-State HMM)")
plt.savefig("hmm_hidden_states.png")
plt.close()


print("\nTraining 3-state HMM...")
model3 = GaussianHMM(
    n_components=3, covariance_type="full", n_iter=1000
).fit(returns)

hidden_states_3 = model3.predict(returns)

plt.figure(figsize=(15, 6))
plt.scatter(data.index, hidden_states_3, c=hidden_states_3, cmap="viridis", s=10)
plt.title("Hidden States (3-State HMM)")
plt.savefig("hmm_hidden_states_3.png")
plt.close()

print("\nAll plots saved successfully!")

print("\n--- 2-State HMM Means & Variances ---")
for i in range(2):
    print(f"State {i}: Mean={model.means_[i][0]}, Variance={np.diag(model.covars_[i])[0]}")

print("\n--- 3-State HMM Means & Variances ---")
for i in range(3):
    print(f"State {i}: Mean={model3.means_[i][0]}, Variance={np.diag(model3.covars_[i])[0]}")

