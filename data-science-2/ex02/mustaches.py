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
    # Query 1: All individual item prices
    query1 = """
    SELECT price
    FROM customers
    WHERE event_type = 'purchase';
    """
    
    # Query 2: Average basket price per user
    query2 = """
    SELECT user_id, AVG(price) as avg_basket_price
    FROM customers
    WHERE event_type = 'purchase'
    GROUP BY user_id;
    """
    
    # Retrieve data
    df_all_prices = pd.read_sql(query1, engine)
    df_basket_avg = pd.read_sql(query2, engine)
    
    # Create cleaned version of prices (with first and last quartile)
    df_clean_prices = df_all_prices[(df_all_prices['price'] >= 1.590000) & (df_all_prices['price'] <= 5.400000)]
    
    # Print statistics as required by the exercise
    print('=' * 45)
    print(f"{'ITEMS STATISTICS (ALL DATA)':^45}")
    print('=' * 45)
    stats = df_all_prices['price'].describe()
    for stat, value in stats.items():
        print(f"{stat:<15} │ {value:<15.6f}")
    print('=' * 45)
    
    # Configure plot style
    sns.set_style("whitegrid")
    fig, axes = plt.subplots(3, 1, figsize=(8, 12))
    fig.suptitle('ex02 - My Beautiful Mustache', fontsize=14, fontweight='bold')
    
    # Box plot 1: ALL price of items purchased (with outliers)
    box1 = axes[0].boxplot(df_all_prices['price'], vert=False, widths=0.6,
                           showfliers=True,
                           flierprops=dict(marker='d', markersize=1, alpha=0.3),
                           patch_artist=True)
    axes[0].set_title('Price of Items Purchased (All Data)', fontsize=10, fontweight='bold')
    axes[0].set_xlabel('Price in ₳')
    axes[0].grid(True, alpha=0.3)
    
    # Box plot 2: CLEANED price of items purchased (without extreme outliers)
    box2 = axes[1].boxplot(df_clean_prices['price'], vert=False, widths=0.6,
                           showfliers=True,
                           flierprops=dict(marker='o', markersize=2, alpha=0.5),
                           patch_artist=True)
    axes[1].set_title('Price of Items Purchased (Cleaned Data without Q1 and Q4)', fontsize=10, fontweight='bold')
    axes[1].set_xlabel('Price in ₳')
    axes[1].grid(True, alpha=0.3)
    
    # Box plot 3: Average basket price per user
    box3 = axes[2].boxplot(df_basket_avg['avg_basket_price'], vert=False, widths=0.6,
                           showfliers=False,
                           patch_artist=True)
    axes[2].set_title('Average Basket Price per User', fontsize=10, fontweight='bold')
    axes[2].set_xlabel('Price in ₳')
    axes[2].grid(True, alpha=0.3)
    
    # Make the boxes more visible with colors
    for patch in box1['boxes']:
        patch.set_facecolor('lightblue')
        patch.set_alpha(0.7)
    
    for patch in box2['boxes']:
        patch.set_facecolor('lightgreen')
        patch.set_alpha(0.7)
        
    for patch in box3['boxes']:
        patch.set_facecolor('lightcoral')
        patch.set_alpha(0.7)
    
    # Adjust layout and show
    plt.subplots_adjust(hspace=0.4)
    plt.show()

except Exception as e:
    print(f"Error during execution: {e}")
finally:
    # Close connection
    engine.dispose()