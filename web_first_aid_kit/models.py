from django.db import models


class Medicine(models.Model):
    id_medicine = models.AutoField(primary_key=True)
    medicine_name = models.TextField()
    medicine_descr = models.TextField()

    def __str__(self):
        return f'{self.medicine_name}\n{self.medicine_descr}'


class Disease(models.Model):
    id_disease = models.CharField(primary_key=True, max_length=10)
    disease_name = models.CharField(max_length=200)

    def __str__(self):
        return self.disease_name


class MedicationUse(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.medicine.medicine_name} - {self.disease.disease_name}"


class Symptom(models.Model):
    id_symptom = models.AutoField(primary_key=True)
    symptom_name = models.CharField(max_length=100)

    def __str__(self):
        return self.symptom_name


class DiseaseCatalog(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.disease.disease_name} - {self.symptom.symptom_name}"


class FirstAidKit(models.Model):
    id_firstaidkit = models.AutoField(primary_key=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    expiration_date = models.DateField()

    def __str__(self):
        return f"{str(self.id_firstaidkit)} - {self.medicine.id_medicine}"
