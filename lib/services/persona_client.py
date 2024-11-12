import logging
import time
import hashlib
import hmac


import requests
from lib.cache import PrefixedRedisCache
from exchange.settings.kyc import PERSONA_API_KEY

logger = logging.getLogger(__name__)
cache = PrefixedRedisCache.get_cache(prefix='persona-app-cache-')


class PersonaClient:
    session = requests.Session()
    HOST = 'https://withpersona.com/api/v1'

    def post(self, url, return_result=True, data={}):
        try:
            headers = {"Authorization": "Bearer "+ PERSONA_API_KEY}
            response = requests.post(url, data=data, headers=headers)
            response.raise_for_status()
            if return_result:
                return response.json()
        except Exception:
            logger.error(f'error on {url}: {data}', exc_info=True)
            raise

    def get(self, url):
        try:
            headers = {"Authorization": "Bearer "+ PERSONA_API_KEY}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception:
            logger.error(f'error on {url}', exc_info=True)
            raise

    def get_applicant_data(self, applicantId):
        return self.get(f'{HOST}/inquiries/{applicantId}').fields