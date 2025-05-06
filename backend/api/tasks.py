# tasks.py
from celery import shared_task
import requests
from .models import EHRIntegrationRecord

@shared_task
def send_ehr_payload(log_id):
    log = EHRIntegrationRecord.objects.get(id=log_id)
    
    try:
        response = requests.post(log.system.destination_url, json=log.payload, timeout=5)
        log.status = 'success' if response.status_code < 300 else 'failed'
        log.response_status = response.status_code
        log.response_body = response.text
    except requests.RequestException as e:
        log.status = 'failed'
        log.response_body = str(e)

    log.save()