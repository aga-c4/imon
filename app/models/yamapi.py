import requests
import logging

class YaMAPI:
    base_url_list = {
        'metrica': 'https://api-metrika.yandex.net/stat/v1/data',
        'app_metrica': 'https://api.appmetrica.yandex.ru/stat/v1/data',
        'app_events': 'https://api.appmetrica.yandex.ru/stat/v1/data'
    }

    def __init__(self, *, token:str='', counter_ids:str='', type:str='metrica'):
        self.token = token # API токен
        self.base_url =  YaMAPI.base_url_list.get(type, '')# Точка входа в API
        self.counter_ids = counter_ids # Идентификаторы счетчиков через запятую

    def get_report(self, *, method:str='', params:dict={}, fileto:str=''):
        headers = {
            'Authorization': f'OAuth {self.token}',
            'Content-Type': 'application/x-yametrika+json'
        }
        
        params['ids'] = self.counter_ids
        response = requests.get(self.base_url+method, params=params, headers=headers)

        if response.status_code == 400:
            resp = response.json()
            if not (len(resp.get('data',[])) and len(resp['data'][0].get('metrics',[]))):
                logging.warning('API code ['+str(resp['code'])+'] Message: '+str(resp['message']))
                if resp.get('errors'):
                    logging.warning('API Errors:')
                    for err in resp['errors']:
                        logging.warning('error_type: '+str(err['error_type'])+'; error_message: '+str(err['message']))
                    return False
                return False
        elif response.status_code == 200:
            if fileto!='':
                with open(fileto, "w") as f:
                    f.write(response.text)
                    f.close() 
                return True    
            else:      
                return response.json()
        else:
            return False
