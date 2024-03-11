from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.template.loader import render_to_string
from healthcare.models import Patient


def send_interaction_email(patient_id, interaction_completed, note, tasks_completed):
    try:
        # Retrieve patient's email from the database
        patient = Patient.objects.get(pk=patient_id)
        patient_email = patient.email
        patient = patient.first_name

        # Admin's email
        admin_email = 'your@email_to_receive_messages'

        # Context data to pass to the template
        context = {
            'patient': patient,
            'patient_email': patient_email,
            'interaction_completed': interaction_completed,
            'note': note,
            'tasks_completed': tasks_completed,
        }

        # Render the email content from the template
        html_message = render_to_string('email_template.html', context)

        # Sending email
        send_mail(
            'Автоматично съобщение от хелфен ЕООД',
            None,  # plain text message (unused)
            'info@helfen.bg',
            [patient_email, admin_email],
            html_message=html_message,  # specify HTML content
            fail_silently=False,
        )
    except ObjectDoesNotExist:
        # Handle the case where the patient with the given ID doesn't exist
        # For example, you can log the error or send a notification to the admin
        pass  # or handle the exception in an appropriate way
