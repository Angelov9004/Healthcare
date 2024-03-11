from healthcare.models import Patient

def worker_patient_count(current_user):
    patient_count = Patient.objects.filter(assigned_user=current_user).count()
    return patient_count
