from healthcare.models import Medications


def assigned_medications(current_user):
    assigned_medications = Medications.objects.filter(assigned_user=current_user)
    return assigned_medications