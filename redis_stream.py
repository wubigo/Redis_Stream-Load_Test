#!/usr/bin/python3
"""
This is a script to test Redis Stream Server for load testing.
"""

import json
import time
import sys
from locust import User, events, TaskSet, task
import redis
import gevent.monkey
gevent.monkey.patch_all()
import settings
from random import randint
from getpass import getpass
from mysql.connector import connect, Error


def load_config():
    """For loading the connection details of Redis"""
    configs = {
        "host":settings.redis_host,
        "port":settings.redis_port,
        "password":settings.redis_password
    }
    
    redis_db = redis.Redis(host=settings.redis_host, port=settings.redis_port)

    if not redis_db.ping():
        logging.error('Redis unavailable')
        raise Exception('Redis unavailable')
    
    stream_name = "test"
    msg = {
                "camera_id": "test",                
                "width": 5
                }
    
    return redis_db, configs, msg, sys.getsizeof(msg["camera_id"])


def conn_db():
    try:
        with connect(
            host="10.166.43.247",
            user="admin",
            password="1IllI1|1Il",
            database="LOG",
        ) as connection:
            count = "SELECT count(*) from EFPointValues "
            records = 0
            with connection.cursor() as cursor:
                cursor.execute(count)
                for items in cursor:
                    print(items)
                    records = items

            size = 3000
            offset = 10
            while offset < 100:
                select_movies_query = "SELECT EntityId, Id, StationId, StringValue, IntValue, DoubleValue, " \
                                      "EquipmentId, BoolValue, `Type`, `Time`, IsAlarm, IsEvent, IsBad, " \
                                      "IOType, Orignal, LogTime, Timeframe, DwordValue, LongValue, " \
                                      "ServerTime, CreateTime FROM EFPointValues LIMIT " + str(offset) + "," + str(size)
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(select_movies_query)
                    result = cursor.fetchall()
                    for row in result:
                        print(row['EntityId'])
                        print(row)
                offset += size
    except Error as e:
        print(e)


class RedisLocust(User):
    
    min_wait = 10
    max_wait = 20
    
    @task(1)
    class MyTaskSet(TaskSet):
        
        def on_start(self):
            self.redis, self.configs, self.msg, self.size_msg = load_config()
            self.stream_name="test"

        # Choose the weight of each task for example here the weight will be (1/(1+5))
        @task(1)
        def read(self, command='READ'):
            """Function to Test GET operation on Redis"""
            result = None
            start_time = time.time()
            try:
                result = self.redis.xrevrange(self.stream_name, max=b'+', count=1)
                if result is not None:
                    total_time = int((time.time() - start_time) * 1000)
                    events.request_success.fire(request_type=command, name='read_frame',  response_time=total_time, response_length=self.size_msg)
                else:
                    raise Exception('We could not send the frame to redis')          
                    total_time = int((time.time() - start_time) * 1000)
                    events.request_failure.fire(request_type=command, name='read_frame', response_time=total_time, response_length=self.size_msg, exception=e)
            except Exception as e:
                total_time = int((time.time() - start_time) * 1000)
                events.request_failure.fire(request_type=command, name='read_frame', response_time=total_time, response_length=self.size_msg, exception=e)
            return result

        # Choose the weight of each task for example here the weight will be (5/(1+5))
        @task(5)
        def write(self, command='WRITE'):
            """Function to Test SET operation on Redis"""
            result = None
            start_time = time.time()
            try:
                result = self.redis.xadd(self.stream_name, self.msg, maxlen=500)
                if result is not None:
                    total_time = int((time.time() - start_time) * 1000)
                    events.request_success.fire(request_type=command, name='write',  response_time=total_time, response_length=self.size_msg)
                else:
                    raise Exception('We could not send the frame to redis')          
                    total_time = int((time.time() - start_time) * 1000)
                    events.request_failure.fire(request_type=command, name='write', response_time=total_time, response_length=self.size_msg, exception=e)
            except Exception as e:
                total_time = int((time.time() - start_time) * 1000)
                events.request_failure.fire(request_type=command, name='write', response_time=total_time, response_length=self.size_msg, exception=e)
            return result


conn_db()
