from django.contrib import admin
from .models import Medicine, MedicationUse, Disease, DiseaseCatalog, Symptom
from .forms import MedicineForm, MedicationUseForm, DiseaseCatalogInlineForm, DiseaseForm


class MedicationUseInline(admin.StackedInline):
    model = MedicationUse
    # form = MedicationUseForm
    extra = 0
    min_num = 0
    max_num = 20
    can_add = True


class MedicationUseAdmin(admin.ModelAdmin):
    form = MedicationUseForm


class MedicineAdmin(admin.ModelAdmin):
    form = MedicineForm
    inlines = [MedicationUseInline]


class DiseaseCatalogInline(admin.TabularInline):
    model = DiseaseCatalog
    form = DiseaseCatalogInlineForm
    extra = 1


class DiseaseAdmin(admin.ModelAdmin):
    form = DiseaseForm
    inlines = [DiseaseCatalogInline]


class SymptomAdmin(admin.ModelAdmin):
    list_display = ['id_symptom', 'symptom_name']


admin.site.register(Symptom, SymptomAdmin)
admin.site.register(Disease, DiseaseAdmin)
admin.site.register(Medicine, MedicineAdmin)
#admin.site.register(MedicationUse, MedicationUseAdmin)
