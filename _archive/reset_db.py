
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean_food_gis.settings')
django.setup()

def reset():
    print("🔄 Resetting database tables for food_store...")
    with connection.cursor() as cursor:
        # Order matters strictly speaking but CASCADE handles it.
        # But safest to drop children first.
        tables = [
            'food_store_cartitem', 'food_store_cart', 
            'food_store_orderitem', 'food_store_order', 
            'food_store_product', 
            'food_store_customer', 
            'food_store_farm', 
            'food_store_deliveryzone', 
            'food_store_category'
        ]
        for t in tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {t} CASCADE;")
                print(f"Dropped {t}")
            except Exception as e:
                print(f"Error dropping {t}: {e}")
            
        try:
            cursor.execute("DELETE FROM django_migrations WHERE app = 'food_store';")
            print("Cleaned django_migrations.")
        except Exception as e:
            print(f"Error cleaning migrations: {e}")
            
    print("✅ RESET COMPLETE.")

if __name__ == '__main__':
    reset()
