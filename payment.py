#this was the hardest 
import os

CHAPA_CONFIG = {
    'PUBLIC_KEY': os.environ.get('CHAPA_PUBLIC_KEY'),
    'SECRET_KEY': os.environ.get('CHAPA_SECRET_KEY'),
    'API_URL': 'https://api.chapa.co/v1/transaction/initialize',
    'VERIFY_URL': 'https://api.chapa.co/v1/transaction/verify/'
}
