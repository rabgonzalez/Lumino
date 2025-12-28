from django_rq import job
import subject.models as pm

@job
def deliver_certificate(base_url, student):
    pass