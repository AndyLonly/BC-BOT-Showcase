#DB大概是这样子的
#注意，这个还是从Bot里面扒出来的，不是完整的，请勿单独使用
#参考！！！！！

import discord
import logging
import sqlite3
import json
from discord.ext import commands
logger = logging.getLogger('discord.CLASS')
class DB(object):
    local = ''    
  def find(self,sql,mode ='fetchone'):
        connect = sqlite3.connect(self.local)
        pointer = connect.cursor()
        try:
            pointer.execute(sql)
        except Exception as e:
            logger.exception(f'Fail to find data!')
            connect.close()
            return -1
        else:
            if mode == 'fetchone':
                #一元
                try:
                    result = pointer.fetchone()
                except Exception as e:
                    logger.exception(f'Fail to find data!')
                    connect.close()
                    return -1
            elif mode == 'fetchall':
                #二元
                try:
                    result = pointer.fetchall()
                except Exception as e:
                    logger.exception(f'Fail to find data!')
                    connect.close()
                    return -1
            else:
                logger.critical(f'Unknown Error')
            connect.close()
            return result
