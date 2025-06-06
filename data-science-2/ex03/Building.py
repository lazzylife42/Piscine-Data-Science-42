import matplotlib
matplotlib.use('Qt5Agg', force=True)
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine

# Database configuration
DATABASE_CONFIG = {
  'host': 'localhost',
  'port': '5432',
  'database': 'piscineds',
  'username': 'smonte',
  'password': 'mysecretpassword'
}

DATABASE_URL = f"postgresql://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}?gssencmode=disable"

engine = create_engine(DATABASE_URL)

try:
   # Simple SQL queries
   query1 = """
   SELECT 
       user_id,
       COUNT(*) as purchase_frequency
   FROM customers 
   WHERE event_type = 'purchase'
   GROUP BY user_id;
   """
   
   query2 = """
   SELECT 
       user_id,
       SUM(price) as total_spent
   FROM customers 
   WHERE event_type = 'purchase'
   GROUP BY user_id;
   """
   
   # Retrieve data
   df1 = pd.read_sql(query1, engine)
   df2 = pd.read_sql(query2, engine)
   
   # Create intervals with pandas
   bins_freq = [0, 10, 20, 30, 40, float('inf')]
   labels_freq = ['0', '10', '20', '30', '40+']
   df1['fz_range'] = pd.cut(df1['purchase_frequency'], bins=bins_freq, labels=labels_freq, right=True)
   freq_counts = df1['fz_range'].value_counts().sort_index()
   
   bins_spending = [0, 50, 100, 150, 200, 250, float('inf')]
   labels_spending = ['0', '50', '100', '150', '200', '200+']
   df2['spending_range'] = pd.cut(df2['total_spent'], bins=bins_spending, labels=labels_spending, right=False)
   spending_counts = df2['spending_range'].value_counts().sort_index()
   
   # Purchase Frequency Analysis
   print("=" * 50)
   print(" " * 10 + "PURCHASE FREQUENCY ANALYSIS")
   print("=" * 50)
   print(f"Total number of users     :   {len(df1)}")
   print(f"Minimum purchase frequency:   {df1['purchase_frequency'].min()}")
   print(f"Maximum purchase frequency:   {df1['purchase_frequency'].max()}")
   print(f"Average purchase frequency:   {df1['purchase_frequency'].mean():.2f}")
   print("-" * 50)
   print("Distribution by frequency ranges")
   print("-" * 50)
   print(freq_counts)
   
   # Spending Analysis
   print("\n" + "=" * 50)
   print(" " * 15 + "SPENDING ANALYSIS")
   print("=" * 50)
   print(f"Total number of users: \t{len(df2)}")
   print(f"Minimum amount spent : \t{df2['total_spent'].min():.2f} ₳")
   print(f"Maximum amount spent : \t{df2['total_spent'].max():.2f} ₳")
   print(f"Average amount spent : \t{df2['total_spent'].mean():.2f} ₳")
   print("-" * 50)
   print("Distribution by spending ranges")
   print("-" * 50)
   print(spending_counts)

   # Plot
   sns.set_style("whitegrid")
   fig, axes = plt.subplots(1, 2, figsize=(12, 6))
   fig.suptitle('ex03 - Highest Building', fontsize=14, fontweight='bold')
   
   # Plot 1
   axes[0].bar(range(len(freq_counts)), freq_counts.values, 
               color='lightblue', alpha=0.8, edgecolor='darkblue', linewidth=1)
   axes[0].set_title('Purchase Frequency Distribution', fontsize=10, fontweight='bold')
   axes[0].set_xlabel('Frequency')
   axes[0].set_ylabel('Customers', rotation=90)
   axes[0].set_xticks(range(len(freq_counts)))
   axes[0].set_xticklabels(freq_counts.index)
   axes[0].grid(True, alpha=0.3)
   
   # Plot 2
   axes[1].bar(range(len(spending_counts)), spending_counts.values, 
               color='lightcoral', alpha=0.8, edgecolor='darkred', linewidth=1)
   axes[1].set_title('₳ Spent Distribution', fontsize=10, fontweight='bold')
   axes[1].set_xlabel('Monetary value in ₳')
   axes[1].set_ylabel('Customers', rotation=90)
   axes[1].set_xticks(range(len(spending_counts)))
   axes[1].set_xticklabels(spending_counts.index)
   axes[1].grid(True, alpha=0.3)
   
   plt.tight_layout()
   plt.show()

except Exception as e:
   print(f"Error during execution: {e}")
finally:
   engine.dispose()