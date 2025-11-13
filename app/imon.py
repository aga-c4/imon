#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import argparse
import time
from datetime import datetime
from pydoc import locate
import matplotlib.pyplot as plt
import logging
import os

from models.sysbf import SysBf
from config import config
from models.mysqldb import Mysqldb
from models.message import Message
from models.task import Task
from models.job import Job
from models.metric import Metric
from models.robot_yamget import Robot_yamget
from models.robot_yamappevget import Robot_yamappevget
from models.robot_mysql1get import Robot_mysql1get
from models.robot_mgen import Robot_mgen
from models.robot_newsmaker import Robot_newsmaker

start_time = time.time()   

print("path:", os.getcwd())

# Обработка параметров
def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('action', nargs='?', type=str, default='')
    parser.add_argument ('--log_view', choices=['', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='')
    parser.add_argument ('--task_id', type=int, default=0)
    parser.add_argument ('--job_status', choices=['', 'run', 'fin', 'error'], default='')
    parser.add_argument ('--robot', type=str, default="")
    parser.add_argument ('--group_id', type=int, default=0)
    parser.add_argument ('--project_id', type=int, default=0)
    parser.add_argument ('--metric_id', type=int, default=0)
    parser.add_argument ('--active', type=int, default=-1)
    parser.add_argument ('--limit', type=int, default=0)
    parser.add_argument ('--source', choices=config['sources_allow']+[''], default="")
    parser.add_argument ('--fr_api', type=str, default="false")
    parser.add_argument ('--granularity', choices=config['granularity_allow']+[''], default='')
    parser.add_argument ('--datetime_to', type=str, default="")
    parser.add_argument ('--group', type=str, default="")
    parser.add_argument ('--message_lvl', type=str, default="")
    parser.add_argument ('--news_alias', type=str, default="")
    return parser 

# Обработка входных данных
parser = createParser()
namespace = parser.parse_args(sys.argv[1:])

logfile = 'log/imon' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.txt'
if namespace.log_view!='':
    # Настройки логирования
    # logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
    if namespace.log_view=='DEBUG':
        logging.basicConfig(level=logging.DEBUG)
    elif namespace.log_view=='INFO':       
        logging.basicConfig(level=logging.INFO)
    elif namespace.log_view=='WARNING':       
        logging.basicConfig(level=logging.WARNING)
    elif namespace.log_view=='ERROR':       
        logging.basicConfig(level=logging.ERROR)        
    elif namespace.log_view=='CRITICAL':       
        logging.basicConfig(level=logging.CRITICAL)
    else:       
        logging.basicConfig(filename=logfile, filemode='a')    

if namespace.action!='':
    print('action: ', namespace.action)
    db = Mysqldb(config['db'])

if namespace.action == 'runrobot':
    if namespace.robot !='':
        print('robot: ', namespace.robot)
        robot_alias = namespace.robot.strip()

        robot_model = SysBf.class_factory("models.robot_"+robot_alias.lower(), "Robot_"+robot_alias, settings={
            "pid": "nopid", 
            "fr_api": False, 
            "source": namespace.source, 
            "granularity": namespace.granularity, 
            "group_id": namespace.group_id, 
            "project_id": namespace.project_id, 
            "metric_id": namespace.metric_id,
            "datetime_to": namespace.datetime_to
            }, config=config)
        logging.info("Run robot: {0}".format(namespace.robot))
        res = SysBf.call_method_fr_obj(robot_model, "run")
        if type(res) is dict:
            message_str = f"Run robot {namespace.robot} fin, comment: \n" + res.get('comment',"")   
            if 'telemetry' in res:
                message_str += " \n" + f"exec_sec:{res['telemetry']['job_execution_sec']}, maxmem_kb:{res['telemetry']['job_max_mem_kb']}"
            Message.send(message_str, lvl='log')
            print(message_str)
elif namespace.action == 'yamget':
    if namespace.source in ('metrica', 'app_metrica'):
        robot = Robot_yamget(settings={
            "pid": "nopid", 
            "fr_api": False, 
            "source": namespace.source, 
            "granularity": namespace.granularity, 
            "group_id": namespace.group_id, 
            "metric_id": namespace.metric_id,
            "datetime_to": namespace.datetime_to
            }, config=config)
        res = robot.run()
        message_str = f"YamGet {namespace.source} fin, comment: \n" + res['comment']
        if 'telemetry' in res:
            message_str += " \n" + f"exec_sec:{res['telemetry']['job_execution_sec']}, maxmem_kb:{res['telemetry']['job_max_mem_kb']}"
        Message.send(message_str, lvl='log')
        print(message_str)

elif namespace.action == 'yamappeventsget':
    robot = Robot_yamappevget(settings={
        "pid": "nopid", 
        "fr_api": False, 
        "source": "app_events", 
        "granularity": namespace.granularity, 
        "group_id": namespace.group_id, 
        "metric_id": namespace.metric_id,
        "datetime_to": namespace.datetime_to
        }, config=config)
    res = robot.run()
    message_str = "YamAppEventsGet fin, comment: \n" + res['comment']
    if 'telemetry' in res:
        message_str += " \n" + f"exec_sec:{res['telemetry']['job_execution_sec']}, maxmem_kb:{res['telemetry']['job_max_mem_kb']}"
    Message.send(message_str, lvl='log')
    print(message_str)

elif namespace.action == 'mysql1get':  
    robot = Robot_mysql1get(settings={ 
        "source": "mysql1",
        "granularity": namespace.granularity, 
        "group_id": namespace.group_id, 
        "metric_id": namespace.metric_id,
        "datetime_to": namespace.datetime_to
        }, config=config)
    res = robot.run()
    message_str = "Mysql1Get fin, comment: \n" + res['comment']
    if 'telemetry' in res:
        message_str += " \n" + f"exec_sec:{res['telemetry']['job_execution_sec']}, maxmem_kb:{res['telemetry']['job_max_mem_kb']}"
    Message.send(message_str, lvl='log')
    print(message_str)  

elif namespace.action == 'mgen':
    robot = Robot_mgen(settings={ 
        "granularity": namespace.granularity, 
        "group_id": namespace.group_id, 
        "metric_id": namespace.metric_id,
        "project_id": namespace.project_id, 
        }, config=config)
    res = robot.run()
    message_str = "MGen fin, comment: \n" + res['comment']
    if 'telemetry' in res:
        message_str += " \n" + f"exec_sec:{res['telemetry']['job_execution_sec']}, maxmem_kb:{res['telemetry']['job_max_mem_kb']}"
    Message.send(message_str, lvl='log')
    print(message_str)


elif namespace.action == 'newsmaker':
    message_str = "Newsmaker fin, comment: \n"
    for cur_news_alias, news in config["newsmaker"].items():
        if (namespace.news_alias!='' and cur_news_alias==namespace.news_alias) or ( \
                (namespace.group=='' or news["group"]==namespace.group) \
                and (namespace.project_id==0 or news["project_id"]==namespace.project_id) \
                and (news["granularity"]==namespace.granularity) \
            ):

            if namespace.message_lvl!='':
                news["message_lvl"] = namespace.message_lvl   

            robot = Robot_newsmaker(settings=news, config=config)
            res = robot.run()
            message_str = res['comment'] + "\n"
            if 'telemetry' in res:
                message_str += " \n" + f"exec_sec:{res['telemetry']['job_execution_sec']}, maxmem_kb:{res['telemetry']['job_max_mem_kb']}"
    
    Message.send(message_str, lvl='log')
    print(message_str)    

elif namespace.action == 'monitor':
    task_list = Task.get_list(db=db, active=1, project_id=namespace.project_id)
    task_counter = 0
    all_comment = ''   
    for task_info in task_list:
        task = Task.get_task(db=db, id=task_info['id'])
        if task:
            if namespace.granularity!="" and task.info['granularity']!=namespace.granularity:
                continue

            if namespace.task_id!=0 and task.id!=namespace.task_id:
                continue

            if namespace.metric_id!=0 and namespace.metric_id!=task.info['metric_id']:
                continue             
            
            if not 'data' in task.info['task_settings']:
                task.info['task_settings']['data'] = {}       
            task.info['task_settings']['data']['project_id'] = task.project_id
            task.info['task_settings']['data']['metric_tag_id'] = 0
            task.info['task_settings']['data']['metric_id'] = task.info['metric_id']
            task.info['task_settings']['data']['granularity'] = task.info['granularity']
            task.info['task_settings']['message_lvl'] = task.info['message_lvl']

            job_id = task.create_job()
            logging.info(f"Create job [{job_id}] for task [{task.id}] with robot {task.info['task_robot']}")
    
            Robot_class = locate('models.robot_'+task.info['task_robot']+'.Robot_'+task.info['task_robot'])  
            robot = Robot_class(settings=task.info['task_settings'], config=config)
            robot_res = robot.run()
            job_telemetry = robot_res["telemetry"]
            formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            task.update_job(job_execution_sec=job_telemetry["job_execution_sec"], 
                            job_max_mem_kb=job_telemetry["job_max_mem_kb"], 
                            job_dt_fin=formatted_time, job_status='fin', job_comment=robot_res["comment"])
            
            if robot_res["comment"]!='':
                all_comment += robot_res["comment"] + "\n"
            logging.info(f"Fin job [{job_id}] for task [{task.id}], job_execution_sec: {job_telemetry['job_execution_sec']}")
            logging.info("----------------")
            task_counter += 1

    all_execution_sec = round(time.time() - start_time, 4)
    message_str = "Monitor fin, comment: \n" + all_comment
    message_str += f"tasks:{task_counter}; exec_sec:{all_execution_sec}"
    Message.send(message_str, lvl='log')
    print(message_str)

elif namespace.action == 'metrics_list':      
    result = Metric.get_list(db=db, group_id=0)
    for row in result:
        print(row)
    print(f'Count {len(result)} items')        

elif namespace.action == 'metric_groups_list':        
    result = Metric.get_groups(db=db)
    for row in result:
        print(row)
    print(f'Count {len(result)} items')    

elif namespace.action == 'tasks_list':      
    result = Task.get_list(db=db, active=namespace.active)
    for row in result: 
        print(row)
    print(f'Count {len(result)} items')    

elif namespace.action == 'task_info':      
    if not namespace.task_id:
        print ("please input --task_id")
    else:
        task = Task.get_task(db=db, id=namespace.task_id)
        print(task.get_info())

elif namespace.action == 'job_list':      
    result = Job.get_list(db=db, task_id=namespace.task_id, status=namespace.job_status, limit=namespace.limit)
    for row in result: 
        print(row)
    print(f'Count {len(result)} items')    

elif namespace.action == 'delete_jobs':      
    Job.delete_jobs(db=db, status=namespace.job_status, task_id=namespace.task_id)                                           

elif namespace.action == 'truncate_jobs':
    Job.truncate_jobs(db=db)

elif namespace.action == 'truncate_anoms':
    Metric.truncate_anoms(db=db, granularity=namespace.granularity)

elif namespace.action == 'truncate_values':
    Metric.truncate_values(db=db)    

elif namespace.action == 'truncate_tasks':
    Task.truncate_tasks(db=db)

elif namespace.action == 'delete_jobs':
    task = Task.get_task(db=db, id=namespace.task_id)
    task.delete_jobs(status=namespace.job_status)

elif namespace.action == 'create_tasks_for_all_metrics':
    print('Create tasks: ', Task.create_tasks_for_metrics(db=db, group_id=namespace.group_id, project_id=namespace.project_id))

else:
    print("""
#####################          
## Incident monitor
#####################
          
Synopsys:
    python3 imon.py [Command1] [Param1] [Command2] [Param2] ...
        
Commands:
    runrobot
    yamget
    yamappeventsget
    mysql1get 
    mgen                       
    monitor
    newsmaker      
    metrics_list      
    metric_groups_list      
    tasks_list
    task_info
    job_list
    delete_jobs                                              
    truncate_jobs
    truncate_values        
    truncate_anoms  
    truncate_tasks 
    create_tasks_for_all_metrics      

Params:
    --log_view (DEBUG | INFO | WARNING | ERROR | CRITICAL) - run with log level (WARNING by default)
    --task_id (int) the task number for filtering output or cleaning
    --job_status (run | fin | error) job status for filtering output or clearing
    --robot (str) the robot alias to run      
    --source ('' | metrica | app_metrica), ('' by default)
    --group_id (int) the group id for filtering or create tasks  
    --project_id (int) the project id for filtering or create tasks        
    --metric_id (int) the metric id for filtering        
    --active (int) the activity marker (-1 by default)      
    --limit items limit (10 by default)
    --fr_api (true | false by default) from file, not from file
    --granularity (m1,h1,d1,w1,mo1...)      
    --datetime_to (str) default="" (ISO format)   
    --group (str) the group alias for filtering news and other
    --message_lvl (str) for custom value in news sending    
    --news_alias (str) news alias from config to send            
The incident monitor is configured from the database!       

Examples:
    imon.sh runrobot --log_view INFO --robot getload --source sysload --project_id 1   
    imon.sh yamget --granularity h1 --source metrica --project_id 1
    imon.sh yamget --granularity h1 --source app_metrica --project_id 1
    imon.sh yamappeventsget --granularity h1 --project_id 1
    imon.sh mysql1get --granularity h1 --project_id 1
    imon.sh mgen --granularity h1 --project_id 1  
    imon.sh monitor --granularity h1 --project_id 1   
    imon.sh newsmaker --granularity d1 --project_id 1                 
    imon.sh newsmaker --granularity w1 --project_id 1                 
    imon.sh newsmaker --granularity m1 --project_id 1     
    imon.sh create_tasks_for_all_metrics --project_id 1 
    ./dockerimon.sh runrobot --log_view INFO --robot getload --source sysload --datetime_to 2025-02-01 --project_id 1                 
""")
    

print("----------------")    