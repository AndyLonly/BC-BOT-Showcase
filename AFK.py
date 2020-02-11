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
