# Generated migration for Shipper model and Order shipper fields

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('food_store', '0010_alter_customer_options_alter_order_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20, verbose_name='Số điện thoại')),
                ('vehicle_type', models.CharField(choices=[('bike', 'Xe đạp'), ('motorbike', 'Xe máy'), ('car', 'Ô tô')], default='motorbike', max_length=20, verbose_name='Loại phương tiện')),
                ('vehicle_number', models.CharField(max_length=50, verbose_name='Biển số xe')),
                ('current_latitude', models.FloatField(blank=True, null=True, verbose_name='Vĩ độ hiện tại')),
                ('current_longitude', models.FloatField(blank=True, null=True, verbose_name='Kinh độ hiện tại')),
                ('last_location_update', models.DateTimeField(blank=True, null=True, verbose_name='Cập nhật vị trí lần cuối')),
                ('status', models.CharField(choices=[('available', 'Sẵn sàng'), ('busy', 'Đang giao hàng'), ('offline', 'Không hoạt động')], default='offline', max_length=20, verbose_name='Trạng thái')),
                ('is_active', models.BooleanField(default=True, verbose_name='Đang hoạt động')),
                ('total_deliveries', models.IntegerField(default=0, verbose_name='Tổng số đơn đã giao')),
                ('rating', models.DecimalField(decimal_places=2, default=5.0, max_digits=3, verbose_name='Đánh giá')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')),
                ('delivery_zones', models.ManyToManyField(blank=True, to='food_store.deliveryzone', verbose_name='Khu vực giao hàng')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Người dùng')),
            ],
            options={
                'verbose_name': 'Shipper',
                'verbose_name_plural': 'Shippers',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='assigned_shipper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_orders', to='food_store.shipper', verbose_name='Shipper phụ trách'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipper_assigned_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Thời gian gán shipper'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipper_picked_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Thời gian lấy hàng'),
        ),
    ]
