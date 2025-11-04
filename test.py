with open("it_asset_inventory_cleaned.csv", encoding='utf-8') as f:
      data = f.read()[1:]  
with open("it_asset_inventory_cleaned-2.csv", "w", encoding='utf-8') as f:
      f.write(data)