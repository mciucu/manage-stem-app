from django.contrib.postgres.operations import CITextExtension
import django.contrib.postgres.fields.citext
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import {{project_main_app}}.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('localization', '0002_country'),
    ]

    operations = [
        CITextExtension(),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('username', django.contrib.postgres.fields.citext.CICharField(blank=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and ./_ only.', max_length=30, null=True, unique=True, validators=[django.core.validators.RegexValidator(code='invalid', message='Enter a valid username. This value may contain at most one consecutive separator( . or _ characters).', regex='^((?![_.]{2,}).)*$'), django.core.validators.RegexValidator(code='invalid', message='Enter a valid username. This value may contain only letters,numbers and separators ( . or _ characters).', regex='^[\\w.]+$'), django.core.validators.RegexValidator(code='invalid', message='Enter a valid username. This value may not start with a separator ( . or _ characters).', regex='^[^._]'), django.core.validators.RegexValidator(code='invalid', message='Enter a valid username. This value may not end with a separator ( . or _ characters).', regex='[^._]$')])),
                ('locale_language', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='localization.Language')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', {{project_main_app}}.models.UserManager()),
            ],
        ),
    ]
