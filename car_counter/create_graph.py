import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from datetime import datetime
import ast

def make_graph(txt_filename):
    
    # Read the file
    with open(txt_filename, 'r') as f:
        lines = f.readlines()

    # Extract data
    data = []
    for line in lines:
        parts = line.split(' at ')
        if len(parts) >= 2:  # Check if line contains the expected number of parts
            count = int(parts[0].split(': ')[1])
            timestamp = datetime.strptime(parts[1].strip(), '%d_%m_%Y__%H_%M_%S')
            data.append((timestamp, count))

    # Create DataFrame
    df = pd.DataFrame(data, columns=['timestamp', 'count'])

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['timestamp'], df['count'])
    plt.xlabel('Time')
    plt.ylabel('Number of Traffic Objects')
    plt.title('Number of Traffic Objects Over Time')

    # Save the figure
    plt.savefig(f'{txt_filename}{datetime.now().strftime("%d_%m_%Y__%H_%M_%S")}.png', dpi=300)

def make_class_wise_graph(txt_filename):
        # Read the file
    with open(txt_filename, 'r') as f:
        lines = f.readlines()

    # Extract data
    data_dict = {}
    total_data = []
    for line in lines:
        parts = line.split('OBJECTS')
        if len(parts) >= 2:  # Check if line contains the expected number of parts
            timestamp = datetime.strptime(parts[0].strip(), '%d_%m_%Y__%H_%M_%S')
            counts_dict = ast.literal_eval(parts[1].strip())
            total_count = sum(sum(counts.values()) for counts in counts_dict.values())
            total_data.append((timestamp, total_count))
            for category, counts in counts_dict.items():
                total_category_count = sum(counts.values())
                if total_category_count > 0:  # Only include categories with a count > 0
                    if category not in data_dict:
                        data_dict[category] = []
                    data_dict[category].append((timestamp, total_category_count))

    # Create DataFrames
    df_dict = {category: pd.DataFrame(data, columns=['timestamp', 'count']) for category, data in data_dict.items()}
    total_df = pd.DataFrame(total_data, columns=['timestamp', 'count'])

    # Plot
    plt.figure(figsize=(10, 6))
    for category, df in df_dict.items():
        plt.plot(df['timestamp'], df['count'], label=category)
    plt.plot(total_df['timestamp'], total_df['count'], label='Total', color='black')
    plt.xlabel('Time')
    plt.ylabel('Number of Traffic Objects')
    plt.title('Number of Traffic Objects Over Time')
    plt.legend()

    # Save the figure
    plt.savefig(f'{txt_filename}{datetime.now().strftime("%d_%m_%Y__%H_%M_%S")}.png', dpi=300)
