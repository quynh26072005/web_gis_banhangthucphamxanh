"""
Migration to rename Farm to Store
"""
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    
    dependencies = [
        ('food_store', '0003_order_delivery_distance_km_and_more'),
    ]
    
    operations = [
        # Đổi verbose_name của model Farm
        migrations.AlterModelOptions(
            name='farm',
            options={'verbose_name': 'Cửa hàng', 'verbose_name_plural': 'Cửa hàng'},
        ),
        
        # Đổi verbose_name của các fields
        migrations.AlterField(
            model_name='product',
            name='farm',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, 
                to='food_store.farm', 
                verbose_name='Cửa hàng'
            ),
        ),
        
        migrations.AlterField(
            model_name='order',
            name='assigned_farm',
            field=models.ForeignKey(
                blank=True, 
                help_text='Cửa hàng gần nhất được tự động gán để giao hàng',
                null=True, 
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='assigned_orders', 
                to='food_store.farm',
                verbose_name='Cửa hàng được gán'
            ),
        ),
    ]
