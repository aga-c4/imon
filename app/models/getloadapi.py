import requests
import logging
import os 
import zipfile
import shutil

class GetLoadAPI:
    
    def __init__(self, *, token:str='', api_url:str='', source:str='', tmp_path:str='', insecure:bool=False):
        self.token = token # API токен
        self.base_url =  api_url # Точка входа в API
        self.source = source # Алиас источника
        self.tmp_path = tmp_path
        if insecure:
            self.verify = False
        else:
            self.verify = True    

    def get_list(self):
        headers = {
            'Authorization': f'OAuth {self.token}',
            'Content-Type': 'application/json'
        }
        params = {}
        url = self.base_url
        if self.base_url.find('?') == -1:
            url += '?'
        url += '?token='+self.token        
        response = requests.get(url, params=params, headers=headers, verify=self.verify)
        # print("GetLoadAPI::get_list::response: ", self.verify)
        # print(response)
        if response.status_code == 200:
            try:   
                return response.json()
            except:
                logging.warning(f"GetLoadAPI.get_list: Error parse json")
                return False
        else:
            return False
               

    def get_files(self, *, file:str='', fr_api:bool=False):    
        try:
        # if True:        
            zip_foldername = self.tmp_path + '/sysload_arch' 
            zipfilename = zip_foldername + '/' + self.source + '_m1_' + file + '.zip'
            foldername = self.tmp_path + '/' + self.source + '_m1_' + file 

            if fr_api:
                # Для принудительного перезабора удалим имеющиеся файлы и папки
                if os.path.exists(zip_foldername): 
                    shutil.rmtree(zip_foldername)
                if os.path.exists(zipfilename): 
                    os.remove(zipfilename)
                if os.path.exists(foldername): 
                    shutil.rmtree(foldername)        
                    
            if not os.path.exists(zip_foldername):  
                os.makedirs(zip_foldername)  

            if not os.path.exists(zipfilename):  
                headers = {
                    'Authorization': f'OAuth {self.token}',
                    'Content-Type': 'application/json'
                }
                url = self.base_url
                if self.base_url.find('?') == -1:
                    url += '?'
                url += '?token='+self.token  
                response = requests.get(url, headers=headers, verify=self.verify)
                if response.status_code == 200: 
                    with open(zipfilename, 'wb') as file:
                        file.write(response.content)
                        file.close()
                else:
                    logging.warning(f"GetLoadAPI.get_files: API Error download file {file}")
                    return False
            
            if not os.path.exists(foldername):  
                os.makedirs(foldername) 
                with zipfile.ZipFile(zipfilename, mode="r") as archive:  
                    archive.extractall(foldername+"/") 

            # Список файлов в папке
            flist = os.listdir(foldername)
            flist.sort()       
            return {
                "zip_foldername": zip_foldername,
                "zipfilename": zipfilename,
                "foldername": foldername,
                "flist": flist
            }  

        except:
        # else:
            logging.warning(f"GetLoadAPI.get_files: Error")
            return False
            
