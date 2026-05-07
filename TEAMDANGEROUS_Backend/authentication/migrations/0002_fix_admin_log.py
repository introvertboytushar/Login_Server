from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('admin', '0003_logentry_add_action_flag_choices'),
    ]

    operations = [
        migrations.RunSQL(
            # Forward: constraint drop করো এবং নতুন দাও
            sql="""
                ALTER TABLE django_admin_log 
                DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_auth_user_id;
                
                ALTER TABLE django_admin_log
                ADD CONSTRAINT django_admin_log_user_id_fk
                FOREIGN KEY (user_id) 
                REFERENCES authentication_customuser(id)
                ON DELETE CASCADE
                DEFERRABLE INITIALLY DEFERRED;
            """,
            # Reverse: পুরনো অবস্থায় ফেরত
            reverse_sql="""
                ALTER TABLE django_admin_log
                DROP CONSTRAINT IF EXISTS django_admin_log_user_id_fk;
            """
        ),
    ]
