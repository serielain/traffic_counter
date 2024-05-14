import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from datetime import datetime

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

    plt.show()










# import torch
# import torchvision

# print("PyTorch version:", torch.__version__)
# print("Torchvision version:", torchvision.__version__)
# print("PyTorch CUDA version:", torch.version.cuda)
# print("CUDA available:", torch.cuda.is_available())

# # If CUDA is available, print the CUDA device name
# if torch.cuda.is_available():
#     print("CUDA device name:", torch.cuda.get_device_name(0))


# print("PyTorch version:", torch.__version__)
# print("Torchvision version:", torchvision.__version__)