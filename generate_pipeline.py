import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
n_orders = 5000

# 1. Génération des commandes
categories = {
    'Technology': ['Phones', 'Accessories', 'Copiers', 'Machines'],
    'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Furnishings'],
    'Office Supplies': ['Storage', 'Binders', 'Paper', 'Art', 'Envelopes']
}

regions = ['Île-de-France', 'Auvergne-Rhône-Alpes', 'Nouvelle-Aquitaine', 'Occitanie', 'Hauts-de-France']
segments = ['Corporate', 'Consumer', 'Home Office']
ship_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']

start_date = datetime(2024, 1, 1)
date_list = [start_date + timedelta(days=int(np.random.randint(0, 730))) for _ in range(n_orders)]

cat_choices = np.random.choice(list(categories.keys()), size=n_orders, p=[0.35, 0.30, 0.35])
subcats = [np.random.choice(categories[c]) for c in cat_choices]

sales = np.round(np.random.exponential(scale=220, size=n_orders) + 15, 2)
quantities = np.random.randint(1, 9, size=n_orders)
discounts = np.random.choice([0.0, 0.1, 0.2, 0.3, 0.5, 0.7], size=n_orders, p=[0.45, 0.20, 0.15, 0.10, 0.07, 0.03])

# Modélisation de la marge (les fortes remises détruisent le profit)
base_margin = np.random.uniform(0.15, 0.45, size=n_orders)
profit = np.round((sales * (base_margin - (discounts * 0.9))), 2)

order_ids = [f"CMD-2024-{10000 + i}" for i in range(n_orders)]
customer_ids = [f"CUST-{np.random.randint(100, 800)}" for _ in range(n_orders)]

df_orders = pd.DataFrame({
    'order_id': order_ids,
    'order_date': [d.strftime('%Y-%m-%d') for d in date_list],
    'ship_date': [(d + timedelta(days=int(np.random.randint(1, 6)))).strftime('%Y-%m-%d') for d in date_list],
    'ship_mode': np.random.choice(ship_modes, size=n_orders),
    'customer_id': customer_ids,
    'segment': np.random.choice(segments, size=n_orders),
    'region': np.random.choice(regions, size=n_orders),
    'category': cat_choices,
    'sub_category': subcats,
    'sales': sales,
    'quantity': quantities,
    'discount': discounts,
    'profit': profit
})

# 2. Table des retours (~8% de taux de retour)
returned_orders = np.random.choice(order_ids, size=int(n_orders * 0.08), replace=False)
df_returns = pd.DataFrame({
    'order_id': returned_orders,
    'returned': 'Yes',
    'return_reason': np.random.choice(['Defective', 'Late Delivery', 'Wrong Item', 'Customer Preference'], size=len(returned_orders))
})

# 3. Table des objectifs annuels par catégorie
df_targets = pd.DataFrame({
    'category': ['Technology', 'Furniture', 'Office Supplies'],
    'target_sales': [450000, 380000, 320000],
    'target_profit_margin': [0.28, 0.15, 0.22]
})

# Export
df_orders.to_csv('orders.csv', index=False)
df_returns.to_csv('returns.csv', index=False)
df_targets.to_csv('targets.csv', index=False)

print("✅ Pipeline terminé : orders.csv, returns.csv et targets.csv générés avec succès.")