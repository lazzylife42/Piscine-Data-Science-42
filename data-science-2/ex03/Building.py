import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import matplotlib.dates as mdates
import numpy as np

# Database configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'piscineds',
    'username': 'smonte',
    'password': 'mysecretpassword'
}

DATABASE_URL = f"postgresql://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}?gssencmode=disable"

# Create connection
engine = create_engine(DATABASE_URL)

# Configuration for pandas display
pd.set_option('display.float_format', '{:.6f}'.format)

try:
    # Query 1: 
    query1 = """
    """
    
    # Query 2: 
    query2 = """
    """

    # Retrieve data
    df1 = pd.read_sql(query1, engine)
    df2 = pd.read_sql(query2, engine)
    

    # Configure plot style
    sns.set_style("whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(12, 8))
    fig.suptitle('ex03 - Highest Building', fontsize=14, fontweight='bold')
    
    # Box plot 1: 
    box1 = axes[0].boxplot()
    axes[0].set_title('', fontsize=10, fontweight='bold')
    axes[0].set_xlabel('Price in ₳')
    axes[0].grid(True, alpha=0.3)
    
    # Box plot 2: 
    box2 = axes[1].boxplot()
    axes[1].set_title('', fontsize=10, fontweight='bold')
    axes[1].set_xlabel('Price in ₳')
    axes[1].grid(True, alpha=0.3)
    
    # Adjust layout and show
    plt.subplots_adjust(hspace=0.4)
    plt.show()

except Exception as e:
    print(f"Error during execution: {e}")
finally:
    # Close connection
    engine.dispose()