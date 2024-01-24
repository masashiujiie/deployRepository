from django.db import migrations, models
import datetime
import logging

logger = logging.getLogger(__name__)

def generate_unique_username(apps, schema_editor):
    User = apps.get_model('flick_seeker', 'User')
    for user in User.objects.all():
        try:
            unique_username = f'user_{user.id}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")}'
            user.username = unique_username
            user.save()
            logger.info(f"Set username for user ID {user.id} to {unique_username}")
        except Exception as e:
            logger.error(f"Error setting username for user ID {user.id}: {e}")
            raise e

class Migration(migrations.Migration):
    dependencies = [
        ('flick_seeker', '0005_alter_user_managers_remove_user_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, verbose_name='ユーザー名'),
        ),
        migrations.RunPython(generate_unique_username, reverse_code=migrations.RunPython.noop),
    ]
