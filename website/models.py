# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = True
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Disease(models.Model):
    id_disease = models.CharField(primary_key=True, max_length=10)
    disease_name = models.CharField(max_length=200)

    class Meta:
        managed = True
        db_table = 'disease'


class DiseaseCatalog(models.Model):
    id_disease = models.OneToOneField(Disease, models.DO_NOTHING, db_column='id_disease', primary_key=True)  # The composite primary key (id_disease, id_symptom) found, that is not supported. The first column is selected.
    id_symptom = models.ForeignKey('Symptom', models.DO_NOTHING, db_column='id_symptom')

    class Meta:
        managed = True
        db_table = 'disease_catalog'
        unique_together = (('id_disease', 'id_symptom'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'django_session'


class Firstaidkit(models.Model):
    id_firstaidkit = models.AutoField(primary_key=True)
    id_medicine = models.ForeignKey('Medicine', models.DO_NOTHING, db_column='id_medicine')
    expiration_date = models.DateField()

    class Meta:
        managed = True
        db_table = 'firstaidkit'


class MedicationUse(models.Model):
    id_medicine = models.OneToOneField('Medicine', models.DO_NOTHING, db_column='id_medicine', primary_key=True)  # The composite primary key (id_medicine, id_disease) found, that is not supported. The first column is selected.
    id_disease = models.ForeignKey(Disease, models.DO_NOTHING, db_column='id_disease')

    class Meta:
        managed = True
        db_table = 'medication_use'
        unique_together = (('id_medicine', 'id_disease'),)


class Medicine(models.Model):
    id_medicine = models.AutoField(primary_key=True)
    medicine_name = models.TextField()
    medicine_descr = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'medicine'


class Symptom(models.Model):
    id_symptom = models.AutoField(primary_key=True)
    symptom_name = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'symptom'
