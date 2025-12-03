import requests
import logging
import os 
import zipfile
import shutil

class GetLoadAPI:
    
    def __init__(self, *, token:str='', api_url:str='', source:str='', tmp_path:str='', insecure:bool=False, headers:dict=None):
        self.token = token # API токен
        self.base_url =  api_url # Точка входа в API
        self.source = source # Алиас источника
        self.tmp_path = tmp_path
        if insecure:
            self.verify = False
        else:
            self.verify = True    
        self.headers = {
            'Authorization': f'OAuth {self.token}',
            'Content-Type': 'application/json'
        }    
        if not headers is None:
            self.headers.update(headers)    

    def get_list(self):
        # Выдадим то, что есть в папке архивов по данному источнику и в выдаче из API источника, объединим, уберем дубли и отсортируем по дате
        zip_foldername = self.tmp_path + '/source_arch/' + self.source + '/' 
        if os.path.exists(zip_foldername):  
            result = os.listdir(zip_foldername)  
        else:
            result = []           

        flist = False
        try:     
            params = {}
            url = self.base_url
            if self.base_url.find('?') == -1:
                url += '?token='+self.token   
            else:    
                url += '&token='+self.token        
            response = requests.get(url, params=params, headers=self.headers, verify=self.verify)
            # print("GetLoadAPI::get_list::response: ", self.verify)
            # print(response)
            if response.status_code == 200:
                try:   
                    flist = response.json()
                except:
                    logging.warning(f"GetLoadAPI.get_list: Error parse json")
        except:
            logging.warning(f"GetLoadAPI.get_list: Error get files")

        if not flist is False:
            result.extend(flist)
            result = list(set(result))
        if len(result)>0:
            result.sort()
            return list(map(lambda name: name.replace('.zip', ''), result)) 
        else:
            return False
               

    def get_files(self, *, file:str='', fr_api:bool=False):    
        try:
        # if True:        
            zip_foldername = self.tmp_path + '/source_arch' 
            tmp_foldername = self.tmp_path + '/source_tmp'  
            zipfilename = zip_foldername + '/' + self.source + '/' + file + '.zip'
            foldername = tmp_foldername + '/' + self.source + '/' + file 

            if fr_api:
                # Для принудительного перезабора удалим имеющиеся файлы и папки
                if os.path.exists(zip_foldername): 
                    shutil.rmtree(zip_foldername)
                if os.path.exists(tmp_foldername): 
                    shutil.rmtree(tmp_foldername)    
                if os.path.exists(zipfilename): 
                    os.remove(zipfilename)
                if os.path.exists(foldername): 
                    shutil.rmtree(foldername)        
                    
            if not os.path.exists(zip_foldername):  
                os.makedirs(zip_foldername)  
            if not os.path.exists(tmp_foldername):  
                os.makedirs(tmp_foldername)      

            if not os.path.exists(zipfilename):  
                url = self.base_url
                if self.base_url.find('?') == -1:
                    url += '?token='
                else:    
                    url += '&token='
                url += self.token + '&file=' + file   
                response = requests.get(url, headers=self.headers, verify=self.verify)
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
            
