from django_rq import job
from django.core.mail import EmailMessage
from weasyprint import HTML
from django.conf import settings
from pathlib import Path
from django.template.loader import render_to_string

@job
def deliver_certificate(base_url, student):
    output_dir = Path(settings.MEDIA_ROOT) / 'certificates'
    output_path = f'{output_dir}/{student.username}_grade_certificate.pdf'
    
    html_string = render_to_string('certificate.html', {'student': student})
    HTML(string=html_string, base_url=base_url).write_pdf(output_path)
    email = EmailMessage(
        subject=f'{student.username} grades certificate',
        to=[student.email],
    )
    email.content_subtype = 'html'
    email.attach_file(output_path)
    email.send()