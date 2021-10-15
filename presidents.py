# Imports
import pandas
import numpy
from datetime import datetime
import matplotlib.pyplot as plt

# Import the CSV into dataframe
dataframe=pandas.read_csv('data.csv', sep=',',header=0)
dataframe = dataframe[:-1]

# Parse Year of Birth
dataframe["year_of_birth"] = pandas.DatetimeIndex(dataframe["BIRTH DATE"]).year.astype(int)

# Change all unknown locations of death to "Living"
dataframe["LOCATION OF DEATH"].fillna('Living', inplace=True)

# Creating variable "most_recent_date_living" to calculate lived_dates, lived_months and lived_years.
# This was done to include currently living Presidents as well, since their death dates come as NaN in the dataset.
today_date = datetime.now().strftime("%b %d, %Y")
dataframe["most_recent_date_living"] = dataframe["DEATH DATE"]
dataframe["most_recent_date_living"].fillna(today_date, inplace=True)

# Calculating lived_dates, lived_months and lived_years
difference_in_dates = pandas.DatetimeIndex(dataframe["most_recent_date_living"]) - pandas.DatetimeIndex(dataframe["BIRTH DATE"])
dataframe["lived_days"] = (difference_in_dates/ numpy.timedelta64(1, "D"))
dataframe["lived_months"] = difference_in_dates / numpy.timedelta64(1, "M")
dataframe["lived_years"] = difference_in_dates / numpy.timedelta64(1, "Y")

# Since calculations are now done, replace NaN death date values with "Living".
dataframe["DEATH DATE"].fillna('Living', inplace=True)

# Function to return style to highlight living presidents.
def highlight_living(s):
    if s['DEATH DATE'] == 'Living':
        return ['background-color: #55efc4'] * len(s)
    else:
        return ['background-color: transparent'] * len(s)


# Sorting data by lived days in dsecending order, and then picking the top 10.
top_10_oldest_df = dataframe.sort_values("lived_days", ascending=False).head(10)
# Converting lived years to integer
top_10_oldest_df["lived_years"] = top_10_oldest_df["lived_years"].astype(int)
# Changing lived_years column name to AGE
top_10_oldest_df.rename(columns={"lived_years": "AGE"}, inplace=True)

top_10_oldest = top_10_oldest_df.style
# Hide index
top_10_oldest.hide_index()
# Hide columns we used as variables
top_10_oldest.hide_columns(["most_recent_date_living","year_of_birth", "lived_days", "lived_months"])
# Highlight living presidents
top_10_oldest.apply(highlight_living, axis=1)
# Set title of the table
top_10_oldest.set_caption("Top 10 Presidents of the United States by age lived, oldest first")
# Show the table
top_10_oldest

# Similar to the above, except sorting in ascending order and then picking top 10
top_10_youngest_df = dataframe.sort_values("lived_days", ascending=True).head(10)
top_10_youngest_df["lived_years"] = top_10_youngest_df["lived_years"].astype(int)
top_10_youngest_df.rename(columns={"lived_years": "AGE"}, inplace=True)

top_10_youngest = top_10_youngest_df.style
top_10_youngest.hide_index()
top_10_youngest.hide_columns(["most_recent_date_living", "year_of_birth", "lived_months", "lived_days"])
top_10_youngest.apply(highlight_living, axis=1)
top_10_youngest.set_caption("Top 10 Presidents of the United States by age lived, youngest first")
top_10_youngest

# Extracting necessary cols
lived_days_col = dataframe["lived_days"]
lived_years_col = dataframe["lived_years"].astype(int)
value_counts = lived_years_col.value_counts()

# Calculating weights
weights = []
for i in range(len(lived_years_col)):
    year = lived_years_col[i]
    # Using the frequency of a year as the weight
    weights.append(value_counts[year])
weights = numpy.array(weights)
# Getting weighted values
weighted_values = weights * lived_days_col

# Calculating the statistics
mean = lived_days_col.mean()
weighted_mean = weighted_values.sum() / weights.sum()
median = lived_days_col.median()
mode = lived_years_col.mode() * 365
max = lived_days_col.max()
min = lived_days_col.min()
std = lived_days_col.std()

# Tabularizing by appending everything to a dictionary
data = {
    "Statistic": ["Mean Age", "Weighted Mean Age", "Median Age", "Mode Age", "Maximum Age", "Minimum Age", "Standard Deviation"],
    "Age (Days)": [mean, weighted_mean, median, list(mode), max, min, std],
    "Age (Years)": [mean / 365, weighted_mean / 365, median / 365, [x / 365 for x in list(mode)], max / 365, min / 365, std / 365]
}

# Creating dataframe from the dictionary
dataframe_stats = pandas.DataFrame.from_dict(data)
dataframe_stats.style.hide_index()

x_axis = ["Mean", "Weighted Mean", "Median", "Maximum", "Minimum"]
x_axis_positions = range(len(x_axis))
y_axis = [mean, weighted_mean, median, max, min]
plt.figure(figsize=(8, 6))
plt.bar(x_axis_positions, y_axis)
plt.ylabel("Age (in Days)")
plt.title("Statistics of Presidential Ages")

plt.axhline(y = mean + std, color = 'r', linestyle = '--', label='Standard Deviation')
plt.axhline(y = mean, color = 'gray', linestyle = '-.', label='Mean')
plt.axhline(y = mean - std, color = 'r', linestyle = '--')

plt.legend(labels=['Standard Deviation', 'Mean'])

plt.xticks(x_axis_positions, x_axis)
plt.show()

# Plotting frequency distribution using matplotlib
x_axis_positions = [i for i in range(len(value_counts))]
plt.figure(figsize=(15, 4))
plt.bar(x_axis_positions, value_counts)
plt.xlabel("Age (years)")
plt.ylabel("Number of Presidents")
plt.title("Frequency of Presidential Ages")

plt.xticks(x_axis_positions, value_counts.keys())
plt.yticks(range(value_counts.max() + 1))
plt.show()