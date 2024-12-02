import pandas as pd
import matplotlib.pyplot as plt

# Define the clusters
cluster_a_ips = ['172.31.28.57', '172.31.18.248', '172.31.27.166', '172.31.26.206']
cluster_b_ips = ['172.31.28.111', '172.31.17.102', '172.31.27.88', '172.31.16.143']

# Load data from CSV
file_path = './aws_single_az/20241115_212944_request_times.csv'  # Replace with your file path
df = pd.read_csv(file_path)

# Sort data by Start Time to ensure sequential processing
df = df.sort_values("Start Time")

df['Start Time'] = df['Start Time'] - df['Start Time'].min()

# Add a cluster column
df['Cluster'] = df['Server IP'].apply(
    lambda ip: 'Cluster A' if ip in cluster_a_ips else ('Cluster B' if ip in cluster_b_ips else 'Other')
)

# Define the rolling window size
rolling_window = 5  # Adjust as needed for smoothing



# Plotting
plt.figure(figsize=(12, 6))
for cluster in ['Cluster A', 'Cluster B']:
    cluster_data = df[df['Cluster'] == cluster]
    # Aggregate the rolling mean of durations
    smoothed_duration = cluster_data['Duration'].rolling(rolling_window).mean()
    plt.plot(cluster_data['Start Time'], smoothed_duration, label=cluster)

# Calculate average number of responses per second for each cluster
results = {}
for cluster in ['Cluster A', 'Cluster B']:
    cluster_data = df[df['Cluster'] == cluster]
    total_responses = len(cluster_data)
    total_time = cluster_data['Start Time'].max() - cluster_data['Start Time'].min()
    avg_responses_per_second = total_responses / total_time if total_time > 0 else 0
    results[cluster] = avg_responses_per_second

# Display the results
print("Average Number of Responses per Second:")
for cluster, avg_responses in results.items():
    print(f"{cluster}: {avg_responses:.2f} responses/s")

# Customize the plot
plt.title("Overload-Handoff Scenario")
plt.xlabel("Time (s)")
plt.ylabel("Response Time (s)")
plt.legend(title="Cluster")
plt.grid()
plt.show()

