import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Configuration de la base de données
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'piscineds',
    'username': 'smonte',
    'password': 'mysecretpassword'
}

DATABASE_URL = f"postgresql://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}?gssencmode=disable"

# Créer la connexion
engine = create_engine(DATABASE_URL)

# Requête SQL pour récupérer la répartition des event_type
query = """
SELECT event_type, COUNT(*) as count
FROM customers 
GROUP BY event_type
ORDER BY count DESC;
"""

try:
    # Récupérer les données
    df = pd.read_sql(query, engine)
    print("Données récupérées :")
    print(df)
    
    # Configuration du style Seaborn
    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 8))
    
    # Créer le graphique en secteurs avec matplotlib
    colors = sns.color_palette("husl", len(df))
    
    plt.pie(df['count'], 
            labels=df['event_type'], 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            explode=[0.05] * len(df))  # Légère séparation des secteurs
    
    plt.title('Répartition des Types d\'Événements', 
              fontsize=16, fontweight='bold', pad=20)
    
    plt.axis('equal')  # Pour avoir un cercle parfait
    
    # Afficher le graphique
    plt.tight_layout()
    plt.show()
    
    # Afficher aussi un résumé textuel
    print("\nRésumé de la répartition :")
    total = df['count'].sum()
    for _, row in df.iterrows():
        percentage = (row['count'] / total) * 100
        print(f"{row['event_type']}: {row['count']} ({percentage:.1f}%)")

except Exception as e:
    print(f"Erreur lors de l'exécution : {e}")

finally:
    # Fermer la connexion
    engine.dispose()