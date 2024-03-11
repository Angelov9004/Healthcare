#Assigned patients to the staff
from healthcare.models import Patient


def assigned_patients(current_user):
    assigned_patients = Patient.objects.filter(assigned_user=current_user)
    return assigned_patients