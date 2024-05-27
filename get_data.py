from config import Db_Config, Message
import datetime
import pandas as pd

class DatabaseManager:

    def __init__(self,config : Db_Config, message : Message):
        self.config = config
        
        self.message = message

    def perform_opeartion(self):
        self.connection = self.config.get_connection()
        if self.connection:
            try:
                current_date = datetime.datetime.now().date()
                current_time  = datetime.datetime.now().time().strftime('%#I%p')
                current_time = '12NN' if current_time == '12PM' else current_time
                cursor = self.connection.cursor()
                cursor.execute("""SELECT TechRegion, Count(SiteID) as SiteCount, sum(Status='DOWN' ) as SiteDown, sum(TechRCA2='') as noRCAcount,  sum(WebRCA3='') as noRCA3count 
                                  from SiteDownEMC
                                   WHERE ReportDate = %(current_date)s and SUBSTRING_INDEX(SUBSTRING_INDEX(ReportTime, '(', -1), ')', 1) = %(current_time)s 
                                    and ForReporting='YES' and  (technology LIKE '2G' or PoleSite LIKE 'YES') and 
                                    (classification='MAJOR' or classification='SLA')  group by TechRegion order by TechRegion """, 
                                    {'current_date': current_date, 
                                    'current_time': current_time})
                rows = cursor.fetchall() #fetch data from query

                data = pd.DataFrame(rows, columns=['TechRegion','SiteCount','SiteDown','NoTechRca2','NoEmcRca3']) #convert to dataframe
                print(data)

                self.message.send_message(data) #sendsms


            except Exception as e:
                print("an error occured",e)

            finally:
                cursor.close()
                self.connection.close()


if __name__ =="__main__":
    config = Db_Config()
    message = Message()

    db_manager = DatabaseManager(config,message)

    db_manager.perform_opeartion()



            


        
        
       

