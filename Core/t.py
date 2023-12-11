import pandas as pd
import datetime

# Example data similar to what the user provided
data = {
    "Time (mS)": [0, 1000, 2000, 3000],
    "Used RAM (MB)": [1185.0, 1186.0, 1205.0, 1206.0],
    # other columns...
}

# Create a DataFrame
df = pd.DataFrame(data)

# Convert 'Time (mS)' to seconds and then to a datetime object
# Assuming the base time is 'Sun Dec 10 15:20:56 UTC 2023'
base_time = datetime.datetime.strptime("Sun Dec 10 15:20:56 UTC 2023", "%a %b %d %H:%M:%S %Z %Y")
df['Timestamp'] = df['Time (mS)'].apply(lambda x: base_time + datetime.timedelta(milliseconds=x))

# Display the first few rows of the modified DataFrame
df.head()

