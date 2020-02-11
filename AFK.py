#这个从我的BOT里扒出来的部分代码
#设计时是作为每日Task来执行
#代码可能有缺失
#无法正常使用，需要魔改,主要用于参考！
"""
Core.Classes里是的东西就不展示了
Json（）是调用Json去读取设定
system['time']是大扫除时间
system['Afk_days']是可以容许AFK多久
system['Afk_remind_days']是提前几天提醒
除此之外的大概不需要解释了
嗯
大概
DB()是调用sqlite数据库
不会的人可以用Json，只需要记录Discord_id和最后活跃时间

不知道用Json的话可以问，很久以前我是用Json来储存数据的，后来换成数据库，有需要可以发
提示：使用Lens和提取Key

不知道怎么使用最后活跃时间的人先看Discord.py 的API文档里面Event Reference去找on_xxxxxx的东西
还是不会再问
"""
import discord
import json
import asyncio
import datetime
import logging
from discord.ext import commands
from Core.Classes import *
logger = logging.getLogger('discord.TASK')
js = Json()
db =  DB()

class task(Cog_Plugin):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)  

          async def afk_killer():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                now_time = datetime.datetime.now().strftime('%H%M')
                system = js.read('./data/setting.json')
                if now_time == system['time']:
                    #开始清除AFK人口                  
                    print('Kick the afk')
                    member_info = db.find(f'select Discord_id,Last_active from user where State != -1','fetchall')
                    for member_info_buffer in member_info:
                        #计算AFK时间
                        now_time = datetime.datetime.now()
                        last_time = datetime.datetime.strptime(member_info_buffer[1],'%Y-%m-%d')
                        time = now_time - last_time
                        print(time.days)
                        #AFK > 30days
                        if time.days >= int(system['Afk_days']):
                            print(f'{member_info_buffer[0]} user afk_time >= 30days')
                            try:
                                self.guild = self.bot.get_guild(int(system['Guild']))
                                self.user = self.bot.get_user(int(member_info_buffer[0]))
                                await self.guild.kick(self.user,reason='成员AFK')
                            except Exception as e:
                                logger.exception(f'Fail to kick user!')
                            else:
                                await self.user.send(system['Kick_redmind.text']+system['Invit.link'])
                                logger.warning(f'{member_id_buffer[0]} was kicked')
                        #AFK remind
                        elif time.days == (int(system['Afk_days']) - int(system['Afk_remind_days'])):
                            print(f'{member_info_buffer[0]} user was notified afk state')
                            try:
                                self.user = self.bot.get_user(int(member_info_buffer[0]))
                                await self.user.send(system['AFK_remind_text'])
                            except Exception as e:
                                logger.exception(f'Fail to notifiy user!')
                        #AFK warn
                        elif time.days == (int(system['Afk_days']) - 1):
                            print(f'{member_info_buffer[0]} was warned due to afk')
                            try:
                                self.user = self.bot.get_user(int(member_info_buffer[0]))
                                await self.user.send(system['Afk_kick_remind_text'])
                            except Exception as e:
                                logger.exception(f'Fail to warn user!')
                    else:
                        print('Dont have member with state != -1')
                    await asyncio.sleep(60)
                else:
                    await asyncio.sleep(10)
                    pass   
        self.bg_task = self.bot.loop.create_task(afk_killer())
        logger.info('Task is Loaded')

def setup(bot):
    bot.add_cog(task(bot))
