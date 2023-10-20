# Generated by Django 4.2.6 on 2023-10-07 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TGUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.PositiveSmallIntegerField(unique=True)),
                ('username', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='cart',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='user_name',
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='bot.tgusers'),
            preserve_default=False,
        ),
    ]
