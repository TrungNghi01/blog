# Generated by Django 4.0 on 2024-10-22 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('posted_at', models.DateTimeField(auto_now_add=True, verbose_name='Posted at')),
            ],
            options={
                'verbose_name_plural': 'this is Blog',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('content', models.CharField(max_length=1000, verbose_name='Content')),
                ('image1', models.ImageField(upload_to='product', verbose_name='image1')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='product', verbose_name='image2')),
                ('posted_at', models.DateTimeField(auto_now_add=True, verbose_name='Posted at')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.category', verbose_name='Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customuser', verbose_name='User')),
            ],
        ),
    ]
