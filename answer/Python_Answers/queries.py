from collections import Counter
import numpy as np
import datetime
import operator
import time
inf=10000000000000000000000000


class queries():
    def __init__(self):
        self.total_days=0
        self.answer_dict={}
        self.ques_id=0
        pass
    def get_total_days(self,df):
        days_array=[]
        for index in range(0,df.shape[0]):
            day=int(df['event_time'][index][8]+df['event_time'][index][9])
            days_array.append(day)
        counter=Counter(days_array)
        self.total_days=len(counter)
    def get_month(self,df):
        month_name=['jan','feb','march','apr','may','june','july','aug','sept','oct','nov','dec']
        array=[]
        
        for index in range(0,df.shape[0]):
            month=int(df['event_time'][index][5]+df['event_time'][index][6] )
            array.append(month)
            
        counter=Counter(array)
        if len(counter)==1:
            return month_name[array[0]-1]
        array=[]
        for ele in counter:
            array.append(ele)
        array.sort()
        combined_month=month_name[array[0]]
        for index in range(1,len(array)):
            combined_month=combined_month+'_'+month_name[array[index]]
        return combined_month
        
    def get_answer_1(self,df):
        counter=Counter(df['app_name'])
        # print(counter[max(counter,key=counter.get)])
        return max(counter,key=counter.get)
    
    def get_answer_2(self,df):
        counter=Counter(df['app_name'])
        return min(counter,key=counter.get)

    def get_answer_3(self,df):
        array=[]
        for index in range(0,df.shape[0]):
            if df['agent_type'][index] ==0:
                array.append(df['app_name'][index])
        counter=Counter(array)
        return max(counter,key=counter.get)
    def get_answer_4(self,df):
        array=[]
        for index in range(0,df.shape[0]):
            if df['agent_type'][index] >0:
                array.append(df['app_name'][index])
        counter=Counter(array)
        return min(counter,key=counter.get)
    def get_answer_5(self,df):
        df=df.astype({'agent_type':'int'})
        counter=Counter(df['agent_type'])
        types_of_application_counter_array=[0,0,0,0,0,0]
        application_name_array=['Non_process_application','desktop_or_navtive_application','browser_based_application','java_based_application','mainframe_application','web_extension_based_application']
        

        for application_type in counter:

            if application_type==0:
                types_of_application_counter_array[0]+=counter[application_type]
                
            if application_type == 2:
                types_of_application_counter_array[1]=counter[application_type]
                

            if application_type>2 and application_type<9:
                types_of_application_counter_array[2]+=counter[application_type]
                
            if application_type==9:
                types_of_application_counter_array[3]+=counter[application_type]


            if application_type>=10 and application_type<=11:
                types_of_application_counter_array[4]+=counter[application_type]

            if application_type>=100:
                types_of_application_counter_array[5]+=counter[application_type]
        application_type_count_array=[]

        for index in range(0,6):
            application_type_count_array.append((types_of_application_counter_array[index],application_name_array[index]))
        application_type_count_array.sort()
        return application_type_count_array[5][1]      
    def get_answer_6(self,df):
        df=df.astype({'agent_type':'int'})
        counter=Counter(df['agent_type'])
        types_of_application_counter_array=[0,0,0,0,0,0]
        application_name_array=['Non_process_application','desktop_or_navtive_application','browser_based_application','java_based_application','mainframe_application','web_extension_based_application']
        

        for application_type in counter:

            if application_type==0:
                types_of_application_counter_array[0]+=counter[application_type]
                
            if application_type == 2:
                types_of_application_counter_array[1]=counter[application_type]
                

            if application_type>2 and application_type<9:
                types_of_application_counter_array[2]+=counter[application_type]
                
            if application_type==9:
                types_of_application_counter_array[3]+=counter[application_type]


            if application_type>=10 and application_type<=11:
                types_of_application_counter_array[4]+=counter[application_type]

            if application_type>=100:
                types_of_application_counter_array[5]+=counter[application_type]
        application_type_count_array=[]

        for index in range(0,6):
            application_type_count_array.append((types_of_application_counter_array[index],application_name_array[index]))
        application_type_count_array.sort()
        ans=''
        for index in range(0,6):
            if application_type_count_array[index][0]>0:
                ans=application_type_count_array[index][1]
                break

        return ans
    def get_answer_7(self,df):
        participant_clipboard_count_dict={}
        
        for index in range(0,df.shape[0]):
            if df['participant_name'][index] in participant_clipboard_count_dict:
                participant_clipboard_count_dict.update({df['participant_name'][index]:participant_clipboard_count_dict[df['participant_name'][index]]+df['clipboard'][index]})
                
            else:
                participant_clipboard_count_dict.update({df['participant_name'][index]:df['clipboard'][index]})
        
        
        mx = max(participant_clipboard_count_dict.items(), key = operator.itemgetter(1))[0]
        return mx
    def get_answer_8(self,df):
        participant_clipboard_count_dict={}
        for index in range(0,df.shape[0]):
            if df['participant_name'][index] in participant_clipboard_count_dict:
                participant_clipboard_count_dict.update({df['participant_name'][index]:participant_clipboard_count_dict[df['participant_name'][index]]+df['clipboard'][index]})
                
            else:
                participant_clipboard_count_dict.update({df['participant_name'][index]:df['clipboard'][index]})

        mn = min(participant_clipboard_count_dict.items(), key = operator.itemgetter(1))[0]
        return mn
    def get_answer_9(self,df):
        persona_app_dict={}
        for index in range(0,df.shape[0]):
            current=[]
            if df['persona_name'][index] in persona_app_dict:
                current=persona_app_dict[df['persona_name'][index]]

                
            current.append(df['app_name'][index])
            persona_app_dict.update({df['persona_name'][index]:current})

        ans=0
        ans1=''
        for persona,array in persona_app_dict.items():
            counter=Counter(array)
            if ans<len(counter):
                ans=len(counter)
                ans1=persona


        return ans1
        

    def get_answer_10(self,df):
        persona_app_dict={}
        for index in range(0,df.shape[0]):
            current=[]
            if df['persona_name'][index] in persona_app_dict:
                current=persona_app_dict[df['persona_name'][index]]

                
            current.append(df['app_name'][index])
            persona_app_dict.update({df['persona_name'][index]:current})

        ans=inf
        ans1=''
        for persona,array in persona_app_dict.items():
            counter=Counter(array)
            if ans>len(counter):
                ans=len(counter)
                ans1=persona


        return ans1
    def get_answer_11(self,df):
        counter=Counter(df['participant_name'])
        return max(counter,key=counter.get)
    def get_answer_12(self,df):
        counter=Counter(df['participant_name'])
        return min(counter,key=counter.get)
    def get_answer_13(self,df):
        counter=Counter(df['persona_name'])
        return max(counter,key=counter.get)
    def get_answer_14(self,df):
        counter=Counter(df['persona_name'])
        return min(counter,key=counter.get)
    def get_answer_15(self,df):
        hour_event_dict={}
        for index in range(0,df.shape[0]):
            hour=int(df['event_time'][index][11]+df['event_time'][index][12])
            if hour in hour_event_dict:
                hour_event_dict.update({hour:hour_event_dict[hour]+1})
        
            else:
                hour_event_dict.update({hour:1})
           
        return max(hour_event_dict.items(), key = operator.itemgetter(1))[0]
        

    def get_answer_16(self,df):
        persona_hours_dict={}
        for index in range(0,df.shape[0]):
            hour=df['event_time'][index][11]+df['event_time'][index][12]
            persona_hours_array=[]
            if df['persona_name'][index] in persona_hours_dict:
                persona_hours_array=persona_hours_dict[df['persona_name'][index]]
                
            persona_hours_array.append(hour)
            persona_hours_dict.update({df['persona_name'][index]:persona_hours_array})
        
        answer_list_for_ques_16=[]
        for persona, hour_array in persona_hours_dict.items():
            counter=Counter(hour_array)
            answer_list_for_ques_16.append((persona,max(counter,key=counter.get)))
            
        return answer_list_for_ques_16
    
    def get_specific_answer_16(self,df,value):
        
        persona_hours_array=[]
        for index in range(0,df.shape[0]):
            hour=df['event_time'][index][11]+df['event_time'][index][12]
            if df['persona_name'][index] == value:
                persona_hours_array.append(hour)
        
        counter=Counter(persona_hours_array)
        return max(counter,key=counter.get)
    def get_answer_17(self,df):
        hour_event_dict={}
        
        for index in range(0,df.shape[0]):
            hour=int(df['event_time'][index][11]+df['event_time'][index][12])
            if hour in hour_event_dict:
                hour_event_dict.update({hour:hour_event_dict[hour]+1})
        
            else:
                hour_event_dict.update({hour:1})
        
        return min(hour_event_dict.items(), key = operator.itemgetter(1))[0]
    
    def get_answer_18(self,df):
        persona_hours_dict={}
        for index in range(0,df.shape[0]):
            hour=df['event_time'][index][11]+df['event_time'][index][12]
            persona_hours_array=[]
            if df['persona_name'][index] in persona_hours_dict:
                persona_hours_array=persona_hours_dict[df['persona_name'][index]]
                persona_hours_array.append(hour)
                persona_hours_dict.update({df['persona_name'][index]:persona_hours_array})

        answer_list_for_ques_18=[]
        for persona, hour_array in persona_hours_dict.items():
            counter=Counter(hour_array)
            answer_list_for_ques_18.append((persona,min(counter,key=counter.get)))
     
        return answer_list_for_ques_18
    
    def get_specific_answer_18(self,df,value):
        persona_hours_array=[]
        for index in range(0,df.shape[0]):
            hour=df['event_time'][index][11]+df['event_time'][index][12]
            if df['persona_name'][index] == value:
                persona_hours_array.append(hour)
        
        counter=Counter(persona_hours_array)
        # print(counter)
        return min(counter,key=counter.get)
    
    
    def get_answer_19(self,df):
        
        week_days_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        array=[]
        for index in range(0,df.shape[0]):
            date=df['event_time'][index][8]+df['event_time'][index][9]+' '+df['event_time'][index][5]+df['event_time'][index][6]+' '+df['event_time'][index][0]+df['event_time'][index][1]+df['event_time'][index][2]+df['event_time'][index][3]
            day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
            array.append(day)
            
        counter=Counter(array)
        return week_days_name[int(max(counter,key=counter.get))]
    
        
    def get_answer_20(self,df):
        
        week_days_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        array=[]
        for index in range(0,df.shape[0]):
            date=df['event_time'][index][8]+df['event_time'][index][9]+' '+df['event_time'][index][5]+df['event_time'][index][6]+' '+df['event_time'][index][0]+df['event_time'][index][1]+df['event_time'][index][2]+df['event_time'][index][3]
            day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
            array.append(day)
            
        counter=Counter(array)
        return week_days_name[int(min(counter,key=counter.get))]
    
    def get_answer_21(self,df):
        week_days_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        persona_day_dict={}

        for index in range(0,df.shape[0]):
            
            date=df['event_time'][index][8]+df['event_time'][index][9]+' '+df['event_time'][index][5]+df['event_time'][index][6]+' '+df['event_time'][index][0]+df['event_time'][index][1]+df['event_time'][index][2]+df['event_time'][index][3]
            day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
            day_name=week_days_name[day]

            persona_days_array=[]
            if df['persona_name'][index] in persona_day_dict:
                persona_days_array=persona_day_dict[df['persona_name'][index]]
                
            persona_days_array.append(day_name)
            persona_day_dict.update({df['persona_name'][index]:persona_days_array})
        
        answer_list_for_ques_21=[]
        for persona, days_array in persona_day_dict.items():
            counter=Counter(days_array)
            
            answer_list_for_ques_21.append((persona,max(counter,key=counter.get)))
            
                   
        return answer_list_for_ques_21
    
    def get_specific_answer_21(self,df,value):
        persona_days_array=[]
        week_days_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        for index in range(0,df.shape[0]):
            
            date=df['event_time'][index][8]+df['event_time'][index][9]+' '+df['event_time'][index][5]+df['event_time'][index][6]+' '+df['event_time'][index][0]+df['event_time'][index][1]+df['event_time'][index][2]+df['event_time'][index][3]
            day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
            day_name=week_days_name[day]
            
            if df['persona_name'][index] ==value:
                persona_days_array.append(day_name)
        
        counter=Counter(persona_days_array)
        return max(counter,key=counter.get)
    
    
    def get_answer_22(self,df):
        week_days_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        persona_day_dict={}

        for index in range(0,df.shape[0]):
            
            date=df['event_time'][index][8]+df['event_time'][index][9]+' '+df['event_time'][index][5]+df['event_time'][index][6]+' '+df['event_time'][index][0]+df['event_time'][index][1]+df['event_time'][index][2]+df['event_time'][index][3]
            day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
            day_name=week_days_name[day]
            
            persona_days_array=[]
            if df['persona_name'][index] in persona_day_dict:
                persona_days_array=persona_day_dict[df['persona_name'][index]]
                
            persona_days_array.append(day_name)
            persona_day_dict.update({df['persona_name'][index]:persona_days_array})

        
        answer_list_for_ques_22=[]
        for persona, days_array in persona_day_dict.items():
            counter=Counter(days_array)
            answer_list_for_ques_22.append((persona,min(counter,key=counter.get)))
                   
        return answer_list_for_ques_22      
    
    def get_specific_answer_22(self,df,value):
        week_days_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        persona_days_array=[]
        for index in range(0,df.shape[0]):
            
            date=df['event_time'][index][8]+df['event_time'][index][9]+' '+df['event_time'][index][5]+df['event_time'][index][6]+' '+df['event_time'][index][0]+df['event_time'][index][1]+df['event_time'][index][2]+df['event_time'][index][3]
            day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
            day_name=week_days_name[day]
            
            if df['persona_name'][index] ==value:
                persona_days_array.append(day_name)
        
        counter=Counter(persona_days_array)
        return min(counter,key=counter.get)  

    def get_answer_23(self,df):
        return round(df.shape[0]/self.total_days)

    def get_answer_24(self,df):
        ans_for_ques_24=[]
        counter=Counter(df['persona_name'])
        for persona in counter:
            ans_for_ques_24.append((persona,counter[persona]/self.total_days))
        return ans_for_ques_24
    
    def get_specific_answer_24(self,df,value):

        counter=Counter(df['persona_name'])
        return counter[value]/self.total_days
    def get_answer_25(self,df):
        total_time_in_process_application=0
        for index in range(0,df.shape[0]):
            if df['agent_type'][index]==0:
                continue
            
            else:
                total_time_in_process_application+=df['active_time'][index]
        
        return total_time_in_process_application
        
    def get_answer_26(self,df):
        total_time_in_non_process_application=0
        for index in range(0,df.shape[0]):
            if df['agent_type'][index]==0:
                total_time_in_non_process_application+=df['active_time'][index]
        
        return total_time_in_non_process_application
        
    def get_answer_27(self,df):
        
        persona_total_time_spent_on_process_application_dict={}
        for index in range(0,df.shape[0]):
            if df['agent_type'][index]==0:
                continue
            
            else:
                if df['persona_name'][index] in persona_total_time_spent_on_process_application_dict:
                    persona_total_time_spent_on_process_application_dict.update({df['persona_name'][index]:persona_total_time_spent_on_process_application_dict[df['persona_name'][index]]+df['active_time'][index]})
                else:
                    persona_total_time_spent_on_process_application_dict.update({df['persona_name'][index]:df['active_time'][index]})
        
        
        return persona_total_time_spent_on_process_application_dict  

    def get_specific_answer_27(self,df,value):
        time=0
        for index in range(0,df.shape[0]):
            if df['agent_type'][index]==0:
                continue
            
            else:
                if df['persona_name'][index] ==value:
                    time+=df['active_time'][index]
        
        return time
    
    def get_answer_28(self,df):
        
        persona_total_time_spent_on_non_process_application_dict={}
        for index in range(0,df.shape[0]):
            if df['agent_type'][index]==0:
                if df['persona_name'][index] in persona_total_time_spent_on_non_process_application_dict:
                    persona_total_time_spent_on_non_process_application_dict.update({df['persona_name'][index]:persona_total_time_spent_on_non_process_application_dict[df['persona_name'][index]]+df['active_time'][index]})
                else:
                    persona_total_time_spent_on_non_process_application_dict.update({df['persona_name'][index]:df['active_time'][index]})
            
        
        
        return persona_total_time_spent_on_non_process_application_dict 



    def get_answer_29(self,df):
        total_time_in_non_process_application=0
        for index in range(0,df.shape[0]):
            if df['agent_type'][index]==0:
                total_time_in_non_process_application+=df['active_time'][index]            
        
        
        return total_time_in_non_process_application/(self.total_days)
        
    def get_answer_30(self,df):
        total_time_in_process_application=0
        for index in range(0,df.shape[0]):
            if df['agent_type'][index]==0:
                continue
            
            else:
                total_time_in_process_application+=df['active_time'][index]
        return total_time_in_process_application/(self.total_days)
    def get_answer_31(self,df):
        persona_total_time_spent_on_non_process_application_dict={}
        for index in range(0,df.shape[0]):
            if df['agent_type'][index]==0:
                if df['persona_name'][index] in persona_total_time_spent_on_non_process_application_dict:
                    persona_total_time_spent_on_non_process_application_dict.update({df['persona_name'][index]:persona_total_time_spent_on_non_process_application_dict[df['persona_name'][index]]+df['active_time'][index]})
                else:
                    persona_total_time_spent_on_non_process_application_dict.update({df['persona_name'][index]:df['active_time'][index]})
        
        per_persona_total_time_per_day_for_non_process_application={}
        for persona,total_time in persona_total_time_spent_on_non_process_application_dict.items():
            per_persona_total_time_per_day_for_non_process_application.update({persona:total_time/(self.total_days)})

        return per_persona_total_time_per_day_for_non_process_application
        
    def get_answer_32(self,df):
        persona_total_time_spent_on_process_application_dict={}
        for index in range(0,df.shape[0]):
            if df['agent_type'][index]==0:
                continue
            else:
                if df['persona_name'][index] in persona_total_time_spent_on_process_application_dict:
                    persona_total_time_spent_on_process_application_dict.update({df['persona_name'][index]:persona_total_time_spent_on_process_application_dict[df['persona_name'][index]]+df['active_time'][index]})
                else:
                    persona_total_time_spent_on_process_application_dict.update({df['persona_name'][index]:df['active_time'][index]})
        
        per_persona_total_time_per_day_for_process_application={}
        for persona,total_time in persona_total_time_spent_on_process_application_dict.items():
            per_persona_total_time_per_day_for_process_application.update({persona:total_time/(self.total_days)})
        return per_persona_total_time_per_day_for_process_application
    
    def get_answer_33(self,df):
        persona_case_id_dict={}
        for index in range(0,df.shape[0]):
            current=[]
            if df['persona_name'][index] in persona_case_id_dict:
                current=persona_case_id_dict[df['persona_name'][index]]
            current.append(df['case_id_value'][index])
            persona_case_id_dict.update({df['persona_name'][index]:current})
        answer_for_ques_33=[]
        for persona,case_array in persona_case_id_dict.items():
            counter=Counter(case_array)
            answer_for_ques_33.append((persona,len(counter)))
        return answer_for_ques_33

    def get_answer_34(self,df):
        persona_tat_dict={}
        for index in range(0,df.shape[0]):
            (total_time,array)=(0,[])
            if df['persona_name'][index] in persona_tat_dict:
                (total_time,array)=persona_tat_dict[df['persona_name'][index]]
            array.append(df['case_id_value'][index])
            persona_tat_dict.update({df['persona_name'][index]:(total_time+df['tat_event'][index],array)})
        ans_for_ques_34=[]
        for persona,(time,array) in persona_tat_dict.items():
            counter=Counter(array)
            size=len(counter)
            ans_for_ques_34.append((persona,time/(size)))
        return ans_for_ques_34

    def get_answer_35(self,df):
        persona_case_id_dict={}
        for index in range(0,df.shape[0]):
            current=[]
            if df['persona_name'][index] in persona_case_id_dict:
                current=persona_case_id_dict[df['persona_name'][index]]
            current.append(df['case_id_value'][index])
            persona_case_id_dict.update({df['persona_name'][index]:current})
        answer_for_ques_35=[]
        for persona,case_array in persona_case_id_dict.items():
            counter=Counter(case_array)
            answer_for_ques_35.append((persona,len(counter)))
        return answer_for_ques_35
        
    def get_answer_36(self,df):
        participant_total_processing_time_dict={}
        for index in range(0,df.shape[0]):
            current=0
            if df['participant_name'][index] in participant_total_processing_time_dict:
                current=participant_total_processing_time_dict[df['participant_name'][index]]
            participant_total_processing_time_dict.update({df['participant_name'][index]:current+df['processing_time'][index]})

        return min(participant_total_processing_time_dict.items(), key = operator.itemgetter(1))[0]
    def get_answer_37(self,df):
        participant_total_processing_time_dict={}
        for index in range(0,df.shape[0]):
            current=0
            if df['participant_name'][index] in participant_total_processing_time_dict:
                current=participant_total_processing_time_dict[df['participant_name'][index]]
            participant_total_processing_time_dict.update({df['participant_name'][index]:current+df['processing_time'][index]})
        
        return max(participant_total_processing_time_dict.items(), key = operator.itemgetter(1))[0]
    def get_answer_38(self,df):
        participant_average_processing_time_per_case_dict={}
        for index in range(0,df.shape[0]):
            (array,time)=([],0)
            if df['participant_name'][index] in participant_average_processing_time_per_case_dict:
                (array,time)=participant_average_processing_time_per_case_dict[df['participant_name'][index]]
            array.append(df['case_id_value'][index])
            participant_average_processing_time_per_case_dict.update({df['participant_name'][index]:(array,df['processing_time'][index]+time)})

        answer_for_ques_38=''
        max_average_time=0
        for participant,(array,time) in participant_average_processing_time_per_case_dict.items():
            counter=Counter(array)
            size=len(counter)
            if time/size > max_average_time:
                max_average_time=time/size
                answer_for_ques_38=participant
            
        return answer_for_ques_38


    def get_answer_39(self,df):
        participant_average_processing_time_per_case_dict={}
        for index in range(0,df.shape[0]):
            (array,time)=([],0)
            if df['participant_name'][index] in participant_average_processing_time_per_case_dict:
                (array,time)=participant_average_processing_time_per_case_dict[df['participant_name'][index]]
            array.append(df['case_id_value'][index])
            participant_average_processing_time_per_case_dict.update({df['participant_name'][index]:(array,df['processing_time'][index]+time)})

        
        answer_for_ques_39=''
        min_average_time=inf

        for participant,(array,time) in participant_average_processing_time_per_case_dict.items():
            counter=Counter(array)
            size=len(counter)
            if time/size < min_average_time:
                min_average_time=time/size
                answer_for_ques_39=participant
        return answer_for_ques_39
    def get_answer_40(self,df):
        persona_total_processing_time_dict={}
        for index in range(0,df.shape[0]):
            current=0
            if df['persona_name'][index] in persona_total_processing_time_dict:
                current=persona_total_processing_time_dict[df['persona_name'][index]]
            persona_total_processing_time_dict.update({df['persona_name'][index]:current+df['processing_time'][index]})
        
        return min(persona_total_processing_time_dict.items(), key = operator.itemgetter(1))[0]
        
    def get_answer_41(self,df):
        persona_total_processing_time_dict={}
        for index in range(0,df.shape[0]):
            current=0
            if df['persona_name'][index] in persona_total_processing_time_dict:
                current=persona_total_processing_time_dict[df['persona_name'][index]]
            persona_total_processing_time_dict.update({df['persona_name'][index]:current+df['processing_time'][index]})
        return max(persona_total_processing_time_dict.items(), key = operator.itemgetter(1))[0]
    
    def get_answer_42(self,df):
        
        participant_total_cases_dict={}
        for index in range(0,df.shape[0]):
            array=[]
            if df['participant_name'][index] in participant_total_cases_dict:
                array=participant_total_cases_dict[df['participant_name'][index]]
            array.append(df['case_id_value'][index])
            participant_total_cases_dict.update({df['participant_name'][index]:array})

        answer_for_ques_42=''
        max=0
        for participant,array in participant_total_cases_dict.items():
            counter=Counter(array)
            size=len(counter)
            if size > max:
                max=size
                answer_for_ques_42=participant
            
        return answer_for_ques_42
        
    def get_answer_43(self,df):
        participant_total_cases_dict={}
        for index in range(0,df.shape[0]):
            array=[]
            if df['participant_name'][index] in participant_total_cases_dict:
                array=participant_total_cases_dict[df['participant_name'][index]]
            array.append(df['case_id_value'][index])
            participant_total_cases_dict.update({df['participant_name'][index]:array})

        answer_for_ques_43=''
        min=inf

        for participant,array in participant_total_cases_dict.items():
            counter=Counter(array)
            size=len(counter)
            if size < min:
                min=size
                answer_for_ques_43=participant
        return answer_for_ques_43

    def get_answer_44(self,df):
        counter=Counter(df['activity_id'])
        return max(counter,key=counter.get)
    
    def get_answer_45(self,df):
        persona_activity_dict={}
        for index in range(0,df.shape[0]):
            current=[]
            if df['persona_name'][index] in persona_activity_dict:
                current=persona_activity_dict[df['persona_name'][index]]
            current.append(df['activity_id'][index])
            persona_activity_dict.update({df['persona_name'][index]:current})
        answer_for_ques_45=[]
        for persona,activity_dict in persona_activity_dict.items():
            counter=Counter(activity_dict)
            
            answer_for_ques_45.append((persona,max(counter,key=counter.get)))

        return answer_for_ques_45
    def get_answer_46(self,df):
        counter=Counter(df['activity_id'])
        return min(counter,key=counter.get)

        
    def get_answer_47(self,df):
        counter=Counter(df['mouse_wheel'])
        count_of_zero=0
        if 0 in counter:
            count_of_zero=counter[0]
        
        if 2*count_of_zero>=df.shape[0]:
            return 'No'
        else:
            return 'Yes'
        
    def get_answer_48(self,df):
        message='This question cannot be answered'
        return message
    def get_answer_49(self,df):
        counter=Counter(df['case_id_value'])
        return len(counter)/self.total_days

    def get_answer_50(self,df):
        persona_average_cases_per_day_dict={}
        for index in range(0,df.shape[0]):
            current=[]
            if df['persona_name'][index] in persona_average_cases_per_day_dict:
                current=persona_average_cases_per_day_dict[df['persona_name'][index]]
            current.append(df['case_id_value'][index])
            persona_average_cases_per_day_dict.update({df['persona_name'][index]:current})
        ans_to_ques_50=[]
        for persona,case_ids in persona_average_cases_per_day_dict.items():
            counter=Counter(case_ids)
            ans_to_ques_50.append((persona,len(counter)/self.total_days))
        return ans_to_ques_50
    def get_answer_51(self,df):
        participant_idle_time_dict={}
        
        for index in range(0,df.shape[0]):
            current=0
            if df['participant_name'][index] in participant_idle_time_dict:
                current=participant_idle_time_dict[df['participant_name'][index]]
               
            participant_idle_time_dict.update({df['participant_name'][index]:current+df['idle_time'][index]})

        return max(participant_idle_time_dict.items(), key = operator.itemgetter(1))[0]
        
        
    def get_answer_52(self,df):
        participant_idle_time_dict={}
        
        for index in range(0,df.shape[0]):
            current=0
            if df['participant_name'][index] in participant_idle_time_dict:
                current=participant_idle_time_dict[df['participant_name'][index]]
              
            participant_idle_time_dict.update({df['participant_name'][index]:current+df['idle_time'][index]})
        
        return min(participant_idle_time_dict.items(), key = operator.itemgetter(1))[0]
        
        
    def get_answer_53(self,df):
        
        persona_idle_time_dict={}
        for index in range(0,df.shape[0]):
            current2=0
            if df['persona_name'][index] in persona_idle_time_dict:
                current2=persona_idle_time_dict[df['persona_name'][index]]
            persona_idle_time_dict.update({df['persona_name'][index]:current2+df['idle_time'][index]})   
        
        return max(persona_idle_time_dict.items(), key = operator.itemgetter(1))[0]
        
    def get_answer_54(self,df):
        
        persona_idle_time_dict={}
        for index in range(0,df.shape[0]):
            current2=0
            if df['persona_name'][index] in persona_idle_time_dict:
                current2=persona_idle_time_dict[df['persona_name'][index]]
            persona_idle_time_dict.update({df['persona_name'][index]:current2+df['idle_time'][index]})   
            
        return min(persona_idle_time_dict.items(), key = operator.itemgetter(1))[0]
    def get_answer_55(self,df): 
        participant_total_wait_time_dict={}
        for index in range(0,df.shape[0]):
            current=0
            if df['participant_name'][index] in participant_total_wait_time_dict:
                current=participant_total_wait_time_dict[df['participant_name'][index]]
            participant_total_wait_time_dict.update({df['participant_name'][index]:current+df['wait_time'][index]})

        
        return min(participant_total_wait_time_dict.items(), key = operator.itemgetter(1))[0]
        
    def get_answer_56(self,df):
       
        persona_total_wait_time_dict={}
        for index in range(0,df.shape[0]):
            current2=0
            if df['persona_name'][index] in persona_total_wait_time_dict:
                current2=persona_total_wait_time_dict[df['persona_name'][index]]
            persona_total_wait_time_dict.update({df['persona_name'][index]:current2+df['wait_time'][index]})   
            
        return max(persona_total_wait_time_dict.items(), key = operator.itemgetter(1))[0]
        
    def get_answer_57(self,df):
        
        persona_total_wait_time_dict={}
        for index in range(0,df.shape[0]):
            current2=0
            if df['persona_name'][index] in persona_total_wait_time_dict:
                current2=persona_total_wait_time_dict[df['persona_name'][index]]
            persona_total_wait_time_dict.update({df['persona_name'][index]:current2+df['wait_time'][index]})   
        
        return min(persona_total_wait_time_dict.items(), key = operator.itemgetter(1))[0]
    def get_answer_58(self,df):
        persona_application_switch_dict={}
        for index in range(0,df.shape[0]):
            current=0
            if df['persona_name'][index] in persona_application_switch_dict:
                current=persona_application_switch_dict[df['persona_name'][index]]

            if df['app_switch'][index]:
                persona_application_switch_dict.update({df['persona_name'][index]:current+1})
        
        return max(persona_application_switch_dict.items(), key = operator.itemgetter(1))[0]
        
    def get_answer_59(self,df):
        persona_application_switch_dict={}
        for index in range(0,df.shape[0]):
            current=0
            if df['persona_name'][index] in persona_application_switch_dict:
                current=persona_application_switch_dict[df['persona_name'][index]]

            if df['app_switch'][index]:
                persona_application_switch_dict.update({df['persona_name'][index]:current+1})
        
        return min(persona_application_switch_dict.items(), key = operator.itemgetter(1))[0]
    def get_answer_60(self,df):
        counter=Counter(df['activity_abstraction_level_name'])
        return max(counter,key=counter.get)
    
    def get_answer_61(self,df):
        persona_activity_abstraction_dict={}
        for index in range(0,df.shape[0]):
            current2=[]
            if df['persona_name'][index] in persona_activity_abstraction_dict:
                current2=persona_activity_abstraction_dict[df['persona_name'][index]]
            current2.append(df['activity_abstraction_level_name'][index])
            persona_activity_abstraction_dict.update({df['persona_name'][index]:current2})


        answer_for_ques_61=[]
        for persona,activity_abstraction_array in persona_activity_abstraction_dict.items():
            counter=Counter(activity_abstraction_array)
            
            answer_for_ques_61.append((persona,max(counter,key=counter.get)))

        return answer_for_ques_61
    def get_answer_62(self,df):
        counter=Counter(df['activity_abstraction_level_name'])
        return min(counter,key=counter.get)

    def get_answer_63(self,df):
        message='This question cannot be answered'
        return message
    def get_answer_64(self,df):
        counter=Counter(df['activity_abstraction_level_name'])
        return max(counter,key=counter.get)
    def get_answer_65(self,df):
        counter=Counter(df['activity_abstraction_level_name'])
        return min(counter,key=counter.get)

    def get_answer_66(self,df):
        persona_case_switch_dict={}
        for index in range(0,df.shape[0]):
            current=0
            if df['persona_name'][index] in persona_case_switch_dict:
                current=persona_case_switch_dict[df['persona_name'][index]]

            if df['case_switch'][index]:
                persona_case_switch_dict.update({df['persona_name'][index]:current+1})
        
        return max(persona_case_switch_dict.items(), key = operator.itemgetter(1))[0]
    def get_answer_67(self,df):
        participant_case_switch_dict={}
        for index in range(0,df.shape[0]):
            current=0
            if df['participant_name'][index] in participant_case_switch_dict:
                current=participant_case_switch_dict[df['participant_name'][index]]

            if df['case_switch'][index]:
                participant_case_switch_dict.update({df['participant_name'][index]:current+1})
        
        return max(participant_case_switch_dict.items(), key = operator.itemgetter(1))[0]
    def get_answer_68(self,df):
        persona_average_case_switch_dict={}
        for index in range(0,df.shape[0]):
            current=0
            if df['persona_name'][index] in persona_average_case_switch_dict:
                current=persona_average_case_switch_dict[df['persona_name'][index]]

            if df['case_switch'][index]:
                persona_average_case_switch_dict.update({df['persona_name'][index]:current+1})
        
        ans_for_ques_68=[]
        for persona,case_switch_count in persona_average_case_switch_dict.items():
            ans_for_ques_68.append((persona,case_switch_count/self.total_days))

        return ans_for_ques_68
    def get_answer_69(self,df):
        application_title_dict={}
        for index in range(0,df.shape[0]):
            current=[]
            if df['app_name'][index] in application_title_dict:
                current=application_title_dict[df['app_name'][index]]
            current.append(df['title'][index])
            application_title_dict.update({df['app_name'][index]:current})
        unique_title_count=0
        application_with_highest_unique_title_count=''
        for app,title in application_title_dict.items():
            value,count=np.unique(title,return_counts=True)
            if len(value)>unique_title_count:
                unique_title_count=len(value)
                application_with_highest_unique_title_count=app
        return application_with_highest_unique_title_count
    def get_answer_70(self,df):
        app_keypress_dict={}
        
        for index in range(0,df.shape[0]):
            current=0
            if df['app_name'][index] in app_keypress_dict:
                current=app_keypress_dict[df['app_name'][index]]
            app_keypress_dict.update({df['app_name'][index]:current+df['navigation_key_count'][index]+df['alpha_key_count'][index]+df['number_key_count'][index]})
        
        mx=max(app_keypress_dict.items(), key = operator.itemgetter(1))[0]
        return mx
        
    def get_answer_71(self,df):
        app_mouse_click_dict={}
        for index in range(0,df.shape[0]):
            current2=0
            if df['app_name'][index] in app_mouse_click_dict:
                current2=app_mouse_click_dict[df['app_name'][index]]
            
            app_mouse_click_dict.update({df['app_name'][index]:current2+df['mouse_count'][index]})
        
        mx=max(app_mouse_click_dict.items(), key = operator.itemgetter(1))[0]
        return mx
    def get_answer_72(self,df):
        participant_average_utilization_dict={}
        for index in range(0,df.shape[0]):
            current1=0
            if df['participant_name'][index] in participant_average_utilization_dict:
                current1=participant_average_utilization_dict[df['participant_name'][index]]
            
            participant_average_utilization_dict.update({df['participant_name'][index]:current1+df['active_time'][index]})
            
        return max(participant_average_utilization_dict.items(), key = operator.itemgetter(1))[0]
    def get_answer_73(self,df):
        participant_average_utilization_dict={}
        for index in range(0,df.shape[0]):
            current1=0
            if df['participant_name'][index] in participant_average_utilization_dict:
                current1=participant_average_utilization_dict[df['participant_name'][index]]
            
            participant_average_utilization_dict.update({df['participant_name'][index]:current1+df['active_time'][index]})
        
        return min(participant_average_utilization_dict.items(), key = operator.itemgetter(1))[0]
    def get_answer_74(self,df):
        participant_average_utilization_dict_in_process={}
        for index in range(0,df.shape[0]):
            current2=0
            if df['participant_name'][index] in participant_average_utilization_dict_in_process:
                current2=participant_average_utilization_dict_in_process[df['participant_name'][index]]
            
            if df['agent_type'][index]!=0:
                participant_average_utilization_dict_in_process.update({df['participant_name'][index]:current2+df['active_time'][index]})
        
        return max(participant_average_utilization_dict_in_process.items(), key = operator.itemgetter(1))[0]
    
    def get_answer_75(self,df):
        participant_average_utilization_dict_in_non_process={}
        for index in range(0,df.shape[0]):
            current3=0
            if df['participant_name'][index] in participant_average_utilization_dict_in_non_process:
                current3=participant_average_utilization_dict_in_non_process[df['participant_name'][index]]
            
            if df['agent_type'][index]!=0:
                continue
            else:
                participant_average_utilization_dict_in_non_process.update({df['participant_name'][index]:current3+df['active_time'][index]})
        
        return max(participant_average_utilization_dict_in_non_process.items(), key = operator.itemgetter(1))[0]
        
    def get_answer_76(self,df):
        average_daily_utilization_in_process=0
        for index in range(0,df.shape[0]):
            if df['agent_type'][index]==0:
                continue
            else:
                average_daily_utilization_in_process+=df['active_time'][index]
        
        return average_daily_utilization_in_process/(self.total_days)
        
    def get_answer_77(self,df):
        average_daily_utilization_in_non_process=0
        for index in range(0,df.shape[0]):
            if df['agent_type'][index]==0:
                average_daily_utilization_in_non_process+=df['active_time'][index]
        
        return average_daily_utilization_in_non_process/(self.total_days)
    
    def get_answer_78(self,df):
        participant_average_utilization_dict_in_process={}
        for index in range(0,df.shape[0]):
            current2=0
            if df['participant_name'][index] in participant_average_utilization_dict_in_process:
                current2=participant_average_utilization_dict_in_process[df['participant_name'][index]]
            
            if df['agent_type'][index]!=0:
                participant_average_utilization_dict_in_process.update({df['participant_name'][index]:current2+df['active_time'][index]})
        
        
        return min(participant_average_utilization_dict_in_process.items(), key = operator.itemgetter(1))[0]
        
    def get_answer_79(self,df):
        participant_average_utilization_dict_in_non_process={}
        for index in range(0,df.shape[0]):
            current3=0
            if df['participant_name'][index] in participant_average_utilization_dict_in_non_process:
                current3=participant_average_utilization_dict_in_non_process[df['participant_name'][index]]
            
            if df['agent_type'][index]!=0:
                continue
            else:
                participant_average_utilization_dict_in_non_process.update({df['participant_name'][index]:current3+df['active_time'][index]})
        
        return min(participant_average_utilization_dict_in_non_process.items(), key = operator.itemgetter(1))[0]
        

    def get_answer_80(self,df):
        counter=Counter(df['app_name'])
        array=[]
        for ele in counter:
            array.append((counter[ele],ele))
        array.sort()
        size=len(array)
        return ((array[size-1][1],array[size-2][1],array[size-3][1]))
        

    def get_answer_81(self,df):
        persona_application_dict={}
        for index in range(0,df.shape[0]):
            current=[]
            if df['persona_name'][index] in persona_application_dict:
                current=persona_application_dict[df['persona_name'][index]]
            current.append(df['app_name'][index])
            persona_application_dict.update({df['persona_name'][index]:current})
        for persona,app in persona_application_dict.items():
            persona_application_dict[persona]=Counter(app)
        init_persona=df['persona_name'][0]
        answer='None'
        max_count=0
        for application in persona_application_dict[init_persona]:
            cnt=inf
            f=1
            for persona,counter in persona_application_dict.items():
                if application in persona_application_dict[persona]:
                    cnt=min(cnt,counter[application])
                else:
                    f=0
                    break
            if max_count<cnt and f==1:
                answer=application
                max_count=cnt
        return answer

    def get_answer_82(self,df):
        message='This question cannot be answered'
        return message
    def get_answer_83(self,df):
        
        message='This question cannot be answered'
        return message
    def get_answer_84(self,df):
        array=[]
        for index in range(0,df.shape[0]):
            if df['agent_type'][index]==2:
                array.append(df['app_name'][index])
        cntr=Counter(array)
        return max(cntr,key=cntr.get)
    def get_answer_85(self,df):
        perosna_mainframe_application_dict={}
        for persona in df['persona_name']:
            perosna_mainframe_application_dict.update({persona:'NO'})
        for index in range(0,df.shape[0]):
            if df['agent_type'][index]>=10 and df['agent_type'][index]<=11:
                perosna_mainframe_application_dict.update({df['persona_name'][index]:'YES'})

        return perosna_mainframe_application_dict
    def get_answer_86(self,df):
        persona_event_dict={}

        for index in range(0,df.shape[0]):
            tot_time_in_seconds=int(df['event_time'][index][11]+df['event_time'][index][12])*60*60+int(df['event_time'][index][14]+df['event_time'][index][15])*60+int(df['event_time'][index][17]+df['event_time'][index][18])
            day=int(df['event_time'][index][8]+df['event_time'][index][9])
            current=[]
            if df['persona_name'][index] in persona_event_dict:
                current=persona_event_dict[df['persona_name'][index]]
            current.append((day,tot_time_in_seconds))
            persona_event_dict.update({df['persona_name'][index]:current})
        ans_for_86=[]
        
        for persona,array in persona_event_dict.items():
            cnt=[86500 for i in range(0,32)]
            for day,time in array:
                cnt[day]=min(cnt[day],time)
            
            counter=Counter(cnt)
            max_count=0
            first_event=0
            for ele in counter:
                if ele < 86500:
                    if max_count<counter[ele]:
                        max_count=counter[ele]
                        first_event=ele
            
            hr=int(first_event/3600)
            rem=first_event-(hr*3600)
            mn=int(rem/60)
            sec=int(rem-(mn*60))
            tm=str(hr)+':'+str(mn)+':'+str(sec)
            ans_for_86.append((persona,tm))
        return ans_for_86
        

           
    def get_answer_87(self,df):
        persona_event_dict={}

        for index in range(0,df.shape[0]):
            hour=int(df['event_time'][index][11]+df['event_time'][index][12])*60*60
            minute=int(df['event_time'][index][14]+df['event_time'][index][15])*60
            second=int(df['event_time'][index][17]+df['event_time'][index][18])
            tot_time_in_seconds=hour+minute+second
            day=int(df['event_time'][index][8]+df['event_time'][index][9])
            current=[]
            if df['persona_name'][index] in persona_event_dict:
                current=persona_event_dict[df['persona_name'][index]]
            current.append((day,tot_time_in_seconds))
            persona_event_dict.update({df['persona_name'][index]:current})
        
        ans_for_87=[]
        for persona,array in persona_event_dict.items():
            cnt2=[-1 for i in range(0,32)]
            for day,time in array:
                cnt2[day]=max(cnt2[day],time)
            
            counter_2=Counter(cnt2)
            lst_event=0
            max_count_2=0
            
            for ele in counter_2:
                if ele > -1:
                    if max_count_2<counter_2[ele]:
                        max_count_2=counter_2[ele]
                        lst_event=ele
            
            hr=int(lst_event/3600)
            rem=lst_event-(hr*3600)
            mn=int(rem/60)
            sec=int(rem-(mn*60))
            tm=str(hr)+':'+str(mn)+':'+str(sec)
            ans_for_87.append((persona,tm))
        return ans_for_87
    def get_answer_88(self,df):
        participant_active_days_dict={}

        for index in range(0,df.shape[0]):
            date=df['event_time'][index][8]+df['event_time'][index][9]+' '+df['event_time'][index][5]+df['event_time'][index][6]+' '+df['event_time'][index][0]+df['event_time'][index][1]+df['event_time'][index][2]+df['event_time'][index][3]
            day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
            days_count_array=[0 for element in range(31)]
            if df['participant_name'][index] in participant_active_days_dict:
                days_count_array=participant_active_days_dict[df['participant_name'][index]]
        
            days_count_array[day]=1    
            participant_active_days_dict.update({df['participant_name'][index]:days_count_array})


        most_active_participant=''
        most_active_participant_days_count=0
        

        for participant,active_day_array in participant_active_days_dict.items():
            active_days=np.sum(active_day_array)
            if most_active_participant_days_count<active_days:
                most_active_participant_days_count=active_days
                most_active_participant=participant

        return most_active_participant
        
    def get_answer_89(self,df):
        

        participant_active_days_dict={}

        for index in range(0,df.shape[0]):
            date=df['event_time'][index][8]+df['event_time'][index][9]+' '+df['event_time'][index][5]+df['event_time'][index][6]+' '+df['event_time'][index][0]+df['event_time'][index][1]+df['event_time'][index][2]+df['event_time'][index][3]
            day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
            days_count_array=[0 for element in range(31)]
            
            if df['participant_name'][index] in participant_active_days_dict:
                days_count_array=participant_active_days_dict[df['participant_name'][index]]
            
            days_count_array[day]=1
            participant_active_days_dict.update({df['participant_name'][index]:days_count_array})
        
        least_active_participant=''
        least_active_participant_count=0

        for participant,active_day_array in participant_active_days_dict.items():
            active_days=np.sum(active_day_array)
            inactive_days=self.total_days-active_days    
            if least_active_participant_count<inactive_days:
                least_active_participant_count=inactive_days
                least_active_participant=participant
        return least_active_participant
        
    def get_answer_90(self,df):
        message='This question cannot be answered'
        return message
    def get_answer_91(self,df):
        message='This question cannot be answered'
        return message
    def get_answer_92(self,df):
        message='This question cannot be answered'
        return message
    def get_answer_93(self,df):
        application_user_dict={}
        for index in range(0,df.shape[0]):
            current=[]
            application_name=''
            if df['agent_type'][index]==0:
                application_name='Non_process_application'
            if df['agent_type'][index]==2:
               application_name='desktop_or_navtive_application' 
            if df['agent_type'][index]>=3 and df['agent_type'][index]<=8:
                application_name='browser_based_application'
            if df['agent_type'][index]==9:
                application_name='java_based_application'
            if df['agent_type'][index]>=10 and df['agent_type'][index]<=11:
                application_name='mainframe_application'
            if df['agent_type'][index]>=100:
                application_name='web_extension_based_application'

            if application_name in application_user_dict:
                current=application_user_dict[application_name]
            current.append(df['participant_name'][index])
            application_user_dict.update({application_name:current})
        answer_for_ques_93=[]
        for application,users in application_user_dict.items():
            counter=Counter(users)
            answer_for_ques_93.append((application,len(counter)))
        return answer_for_ques_93
    def get_answer_94(self,df):
        participant_active_days_dict={}
        for index in range(0,df.shape[0]):
            hour=df['event_time'][index][11]+df['event_time'][index][12]
            hour=int(hour)
            
            date=df['event_time'][index][8]+df['event_time'][index][9]+' '+df['event_time'][index][5]+df['event_time'][index][6]+' '+df['event_time'][index][0]+df['event_time'][index][1]+df['event_time'][index][2]+df['event_time'][index][3]
            day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
            
            days_count_array=[0 for element in range(31)]
            if df['participant_name'][index] in participant_active_days_dict:
                days_count_array=participant_active_days_dict[df['participant_name'][index]]
            
            days_count_array[day]=1
            participant_active_days_dict.update({df['participant_name'][index]:days_count_array})

        persona_average_leave_of_user_dict={}
        for index in range(0,df.shape[0]):
            current=[]
            if df['persona_name'][index] in persona_average_leave_of_user_dict:
                current=persona_average_leave_of_user_dict[df['persona_name'][index]]
            current.append(df['participant_name'][index])
            persona_average_leave_of_user_dict.update({df['persona_name'][index]:current})
        ans_for_ques_94=[]
        for persona,participant_array in persona_average_leave_of_user_dict.items():
            counter=Counter(participant_array)
            
            total_count_of_inactive_days_in_persona=0
            for unique_participant in counter:

                active_days=np.sum(participant_active_days_dict[unique_participant])
                inactive_days=self.total_days-active_days
                total_count_of_inactive_days_in_persona+=inactive_days
            ans_for_ques_94.append((persona,total_count_of_inactive_days_in_persona/(self.total_days)))
        return ans_for_ques_94     
    def get_answer_95(self,df):
        
        participant_most_productive_hour_dict={}
        for index in range(0,df.shape[0]):
            hour=df['event_time'][index][11]+df['event_time'][index][12]
            hour=int(hour)
            hour_array={}
            if df['participant_name'][index] in participant_most_productive_hour_dict:
                hour_array=participant_most_productive_hour_dict[df['participant_name'][index]]
            # hour_array[hour]+=df['active_time'][index]
            curr=df['active_time'][index]
            if hour in hour_array:
                curr+=hour_array[hour]
            hour_array.update({hour:curr})


            participant_most_productive_hour_dict.update({df['participant_name'][index]:hour_array})
        answer_for_ques_95=[]
        
        for participant,hour_array in participant_most_productive_hour_dict.items():
            
            answer_for_ques_95.append((participant,int(max(hour_array.items(), key = operator.itemgetter(1))[0])))

        return answer_for_ques_95
    def get_answer_96(self,df):
        participant_most_productive_hour_dict={}
        for index in range(0,df.shape[0]):
            hour=df['event_time'][index][11]+df['event_time'][index][12]
            hour=int(hour)
            hour_array={}
            if df['participant_name'][index] in participant_most_productive_hour_dict:
                hour_array=participant_most_productive_hour_dict[df['participant_name'][index]]
            curr=df['active_time'][index]
            if hour in hour_array:
                curr+=hour_array[hour]
            hour_array.update({hour:curr})


            participant_most_productive_hour_dict.update({df['participant_name'][index]:hour_array})
        answer_for_ques_96=[]
        
        for participant,hour_array in participant_most_productive_hour_dict.items():
            
            answer_for_ques_96.append((participant,int(min(hour_array.items(), key = operator.itemgetter(1))[0])))

        return answer_for_ques_96
    def get_answer_97(self,df):
        week_days_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        participant_most_productive_day_dict={}
        for index in range(0,df.shape[0]):
            date=df['event_time'][index][8]+df['event_time'][index][9]+' '+df['event_time'][index][5]+df['event_time'][index][6]+' '+df['event_time'][index][0]+df['event_time'][index][1]+df['event_time'][index][2]+df['event_time'][index][3]
            day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
            day_array={}
            if df['participant_name'][index] in participant_most_productive_day_dict:
                day_array=participant_most_productive_day_dict[df['participant_name'][index]]
            curr=df['active_time'][index]
            if day in day_array:
                curr+=day_array[day]
            day_array.update({day:curr})
            
            participant_most_productive_day_dict.update({df['participant_name'][index]:day_array})
        
        answer_for_ques_97=[]
        for participant,day_array in participant_most_productive_day_dict.items():
            answer_for_ques_97.append((participant,week_days_name[ int(min(day_array.items(), key = operator.itemgetter(1))[0])]))
        return answer_for_ques_97    
    def get_answer_98(self,df):
        week_days_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        participant_most_productive_day_dict={}
        for index in range(0,df.shape[0]):
            date=df['event_time'][index][8]+df['event_time'][index][9]+' '+df['event_time'][index][5]+df['event_time'][index][6]+' '+df['event_time'][index][0]+df['event_time'][index][1]+df['event_time'][index][2]+df['event_time'][index][3]
            day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
            day_array={}
            if df['participant_name'][index] in participant_most_productive_day_dict:
                day_array=participant_most_productive_day_dict[df['participant_name'][index]]
            curr=df['active_time'][index]
            if day in day_array:
                curr+=day_array[day]
            day_array.update({day:curr})
            
            participant_most_productive_day_dict.update({df['participant_name'][index]:day_array})
        
        answer_for_ques_98=[]
        for participant,day_array in participant_most_productive_day_dict.items():
            answer_for_ques_98.append((participant,week_days_name[ int(max(day_array.items(), key = operator.itemgetter(1))[0])]))
        return answer_for_ques_98
    def get_answer_99(self,df):
        participant_persona_dict={}
        for index in range(0,df.shape[0]):
            current=[]
            if df['participant_name'][index] in participant_persona_dict:
                current=participant_persona_dict[df['participant_name'][index]]
            current.append(df['persona_name'][index])
            participant_persona_dict.update({df['participant_name'][index]:current})

        answer_for_ques_99=[]
        for participant,persona in participant_persona_dict.items():
            value,count=np.unique(persona,return_counts=True)
            
            if len(value)>1:
                answer_for_ques_99.append(participant)
        return answer_for_ques_99
        

    def get_answer_100(self,df):
        message='This question cannot be answered'
        return message
    
    def get_answer_1000(self,df):
        return self.get_specific_answer_16(df,'LES')
    def get_answer_1001(self,df):
        return self.get_specific_answer_16(df,'CES')
    def get_answer_1002(self,df):
        return self.get_specific_answer_16(df,'Do Not Use')
    def get_answer_1003(self,df):
        return self.get_specific_answer_16(df,'TEST')
    
    def get_answer_1004(self,df):
        return self.get_specific_answer_18(df,'LES')
    def get_answer_1005(self,df):
        return self.get_specific_answer_18(df,'CES')
    def get_answer_1006(self,df):
        return self.get_specific_answer_18(df,'Do Not Use')
    def get_answer_1007(self,df):
        return self.get_specific_answer_18(df,'TEST')
    
    def get_answer_1008(self,df):
        return self.get_specific_answer_21(df,'LES')
    def get_answer_1009(self,df):
        return self.get_specific_answer_21(df,'CES')
    def get_answer_1010(self,df):
        return self.get_specific_answer_21(df,'Do Not Use')
    def get_answer_1011(self,df):
        return self.get_specific_answer_21(df,'TEST')
    
    def get_answer_1012(self,df):
        return self.get_specific_answer_22(df,'LES')
    def get_answer_1013(self,df):
        return self.get_specific_answer_22(df,'CES')
    def get_answer_1014(self,df):
        return self.get_specific_answer_22(df,'Do Not Use')
    def get_answer_1015(self,df):
        return self.get_specific_answer_22(df,'TEST')
    
    def get_answer_1016(self,df):
        return self.get_specific_answer_24(df,'LES')
    def get_answer_1017(self,df):
        return self.get_specific_answer_24(df,'CES')
    def get_answer_1018(self,df):
        return self.get_specific_answer_24(df,'Do Not Use')
    def get_answer_1019(self,df):
        return self.get_specific_answer_24(df,'TEST')
    
    def get_answer_1020(self,df):
        return self.get_specific_answer_27(df,'LES')
    def get_answer_1021(self,df):
        return self.get_specific_answer_27(df,'CES')
    def get_answer_1022(self,df):
        return self.get_specific_answer_27(df,'Do Not Use')
    def get_answer_1023(self,df):
        return self.get_specific_answer_27(df,'TEST')
    

    def get_answer_1024(self,df):
        return self.get_specific_answer_28(df,'LES')
    def get_answer_1025(self,df):
        return self.get_specific_answer_28(df,'CES')
    def get_answer_1026(self,df):
        return self.get_specific_answer_28(df,'Do Not Use')
    def get_answer_1027(self,df):
        return self.get_specific_answer_28(df,'TEST')
    

    def get_answer_1028(self,df):
        return self.get_specific_answer_31(df,'LES')
    def get_answer_1029(self,df):
        return self.get_specific_answer_31(df,'CES')
    def get_answer_1030(self,df):
        return self.get_specific_answer_31(df,'Do Not Use')
    def get_answer_1031(self,df):
        return self.get_specific_answer_31(df,'TEST')
    
    def get_answer_1032(self,df):
        return self.get_specific_answer_32(df,'LES')
    def get_answer_1033(self,df):
        return self.get_specific_answer_32(df,'CES')
    def get_answer_1034(self,df):
        return self.get_specific_answer_32(df,'Do Not Use')
    def get_answer_1035(self,df):
        return self.get_specific_answer_32(df,'TEST')
    
    def get_answer_1036(self,df):
        return self.get_specific_answer_33(df,'LES')
    def get_answer_1037(self,df):
        return self.get_specific_answer_33(df,'CES')
    def get_answer_1038(self,df):
        return self.get_specific_answer_33(df,'Do Not Use')
    def get_answer_1039(self,df):
        return self.get_specific_answer_33(df,'TEST')
    

    def get_answer_1040(self,df):
        return self.get_specific_answer_34(df,'LES')
    def get_answer_1041(self,df):
        return self.get_specific_answer_34(df,'CES')
    def get_answer_1042(self,df):
        return self.get_specific_answer_34(df,'Do Not Use')
    def get_answer_1043(self,df):
        return self.get_specific_answer_34(df,'TEST')
    
    def get_answer_1044(self,df):
        return self.get_specific_answer_45(df,'LES')
    def get_answer_1045(self,df):
        return self.get_specific_answer_45(df,'CES')
    def get_answer_1046(self,df):
        return self.get_specific_answer_45(df,'Do Not Use')
    def get_answer_1047(self,df):
        return self.get_specific_answer_45(df,'TEST')
    
    def get_answer_1048(self,df):
        return self.get_specific_answer_50(df,'LES')
    def get_answer_1049(self,df):
        return self.get_specific_answer_50(df,'CES')
    def get_answer_1050(self,df):
        return self.get_specific_answer_50(df,'Do Not Use')
    def get_answer_1051(self,df):
        return self.get_specific_answer_50(df,'TEST')
    
    def get_answer_1052(self,df):
        return self.get_specific_answer_61(df,'LES')
    def get_answer_1053(self,df):
        return self.get_specific_answer_61(df,'CES')
    def get_answer_1054(self,df):
        return self.get_specific_answer_61(df,'Do Not Use')
    def get_answer_1055(self,df):
        return self.get_specific_answer_61(df,'TEST')
    
    def get_answer_1056(self,df):
        return self.get_specific_answer_68(df,'LES')
    def get_answer_1057(self,df):
        return self.get_specific_answer_68(df,'CES')
    def get_answer_1058(self,df):
        return self.get_specific_answer_68(df,'Do Not Use')
    def get_answer_1059(self,df):
        return self.get_specific_answer_68(df,'TEST')
    
    def get_answer_1060(self,df):
        return self.get_specific_answer_85(df,'LES')
    def get_answer_1061(self,df):
        return self.get_specific_answer_85(df,'CES')
    def get_answer_1062(self,df):
        return self.get_specific_answer_85(df,'Do Not Use')
    def get_answer_1063(self,df):
        return self.get_specific_answer_85(df,'TEST')
    
    def get_answer_1064(self,df):
        return self.get_specific_answer_86(df,'LES')
    def get_answer_1065(self,df):
        return self.get_specific_answer_86(df,'CES')
    def get_answer_1066(self,df):
        return self.get_specific_answer_86(df,'Do Not Use')
    def get_answer_1067(self,df):
        return self.get_specific_answer_86(df,'TEST')
    
    def get_answer_1068(self,df):
        return self.get_specific_answer_87(df,'LES')
    def get_answer_1069(self,df):
        return self.get_specific_answer_87(df,'CES')
    def get_answer_1070(self,df):
        return self.get_specific_answer_87(df,'Do Not Use')
    def get_answer_1071(self,df):
        return self.get_specific_answer_87(df,'TEST')
    
    def get_answer_1072(self,df):
        return self.get_specific_answer_90(df,'LES')
    def get_answer_1073(self,df):
        return self.get_specific_answer_90(df,'CES')
    def get_answer_1074(self,df):
        return self.get_specific_answer_90(df,'Do Not Use')
    def get_answer_1075(self,df):
        return self.get_specific_answer_90(df,'TEST')
    

    def get_answer_1076(self,df):
        return self.get_specific_answer_91(df,'LES')
    def get_answer_1077(self,df):
        return self.get_specific_answer_91(df,'CES')
    def get_answer_1078(self,df):
        return self.get_specific_answer_91(df,'Do Not Use')
    def get_answer_1079(self,df):
        return self.get_specific_answer_91(df,'TEST')
    
    def get_answer_1080(self,df):
        return self.get_specific_answer_94(df,'LES')
    def get_answer_1081(self,df):
        return self.get_specific_answer_94(df,'CES')
    def get_answer_1082(self,df):
        return self.get_specific_answer_94(df,'Do Not Use')
    def get_answer_1083(self,df):
        return self.get_specific_answer_94(df,'TEST')
    
    def get_answer_1084(self,df):
        return self.get_specific_answer_95(df,'CAAJE')
    def get_answer_1085(self,df):
        return self.get_specific_answer_95(df,'BAB16')
    def get_answer_1086(self,df):
        return self.get_specific_answer_95(df,'G8C19')
    def get_answer_1087(self,df):
        return self.get_specific_answer_95(df,'GUP22')
    def get_answer_1088(self,df):
        return self.get_specific_answer_95(df,'gig19')
    def get_answer_1089(self,df):
        return self.get_specific_answer_95(df,'BKA20')
    
    def get_answer_1090(self,df):
        return self.get_specific_answer_96(df,'CAAJE')
    def get_answer_1091(self,df):
        return self.get_specific_answer_96(df,'BAB16')
    def get_answer_1092(self,df):
        return self.get_specific_answer_96(df,'G8C19')
    def get_answer_1093(self,df):
        return self.get_specific_answer_96(df,'GUP22')
    def get_answer_1094(self,df):
        return self.get_specific_answer_96(df,'gig19')
    def get_answer_1095(self,df):
        return self.get_specific_answer_96(df,'BKA20')
    
    def get_answer_1096(self,df):
        return self.get_specific_answer_97(df,'CAAJE')
    def get_answer_1097(self,df):
        return self.get_specific_answer_97(df,'BAB16')
    def get_answer_1098(self,df):
        return self.get_specific_answer_97(df,'G8C19')
    def get_answer_1099(self,df):
        return self.get_specific_answer_97(df,'GUP22')
    def get_answer_1100(self,df):
        return self.get_specific_answer_97(df,'gig19')
    def get_answer_1101(self,df):
        return self.get_specific_answer_97(df,'BKA20')
    
    def get_answer_1102(self,df):
        return self.get_specific_answer_98(df,'CAAJE')
    def get_answer_1103(self,df):
        return self.get_specific_answer_98(df,'BAB16')
    def get_answer_1104(self,df):
        return self.get_specific_answer_98(df,'G8C19')
    def get_answer_1105(self,df):
        return self.get_specific_answer_98(df,'GUP22')
    def get_answer_1106(self,df):
        return self.get_specific_answer_98(df,'gig19')
    def get_answer_1107(self,df):
        return self.get_specific_answer_98(df,'BKA20')
    
    
    
    
    
    
      
    
    
    
    def get_specific_answer_28(self,df,value):
        time=0
        for index in range(0,df.shape[0]):
            if df['agent_type'][index]==0:
                if df['persona_name'][index] ==value:
                    time+=df['active_time'][index]
        
        return time
    def get_specific_answer_31(self,df,value):
        time=0
        for index in range(0,df.shape[0]):
            if df['agent_type'][index]==0:
                if df['persona_name'][index] == value:
                    time+=df['active_time'][index]
        
        return time/(self.total_days)
        
    def get_specific_answer_32(self,df,value):
        time=0
        for index in range(0,df.shape[0]):
            if df['agent_type'][index]!=0:
                if df['persona_name'][index] == value:
                    time+=df['active_time'][index]
        
        return time/(self.total_days)
    
    def get_specific_answer_33(self,df,value):
        current=[]
        for index in range(0,df.shape[0]):
            current=[]
            if df['persona_name'][index] == value:
                current.append(df['case_id_value'][index])
            
            
        counter=Counter(current)
        return len(counter)
    
    def get_specific_answer_34(self,df,value):

        (total_time,array)=(0,[])
        for index in range(0,df.shape[0]):
            if df['persona_name'][index] == value:
                array.append(df['case_id_value'][index])
                (total_time,array)=(total_time+df['tat_event'][index],array)
        
        counter=Counter(array)
        size=len(counter)
        return total_time/(size)
    
    def get_specific_answer_45(self,df,value):
        current=[]
        for index in range(0,df.shape[0]):
            
            if df['persona_name'][index] == value:
                current.append(df['activity_id'][index])
        
        counter=Counter(current)
        return max(counter,key=counter.get)
    
    def get_specific_answer_50(self,df,value):
        current=[]
        for index in range(0,df.shape[0]):
            
            if df['persona_name'][index] ==value:
                current.append(df['case_id_value'][index])
        
        counter=Counter(current)
        return len(counter)/self.total_days
    
    def get_specific_answer_61(self,df,value):
        current2=[]
        for index in range(0,df.shape[0]):
            if df['persona_name'][index] ==value:
                current2.append(df['activity_abstraction_level_name'][index])
        
        counter=Counter(current2)
        # print(counter)
        return max(counter,key=counter.get)
    
    def get_specific_answer_68(self,df,value):
        current=0
        for index in range(0,df.shape[0]):
            if df['persona_name'][index]==value:
                if df['case_switch'][index]:
                    current+=1
        return current/self.total_days
    
    def get_specific_answer_85(self,df,value):
        perosna_mainframe_application_dict={}
        for persona in df['persona_name']:
            perosna_mainframe_application_dict.update({persona:'NO'})
        for index in range(0,df.shape[0]):
            if df['agent_type'][index]>=10 and df['agent_type'][index]<=11 and df['persona_name'][index] == value:
                return 'yes'
        return 'no'
    
    def get_specific_answer_86(self,df,value):
        current=[]
        for index in range(0,df.shape[0]):
            tot_time_in_seconds=int(df['event_time'][index][11]+df['event_time'][index][12])*60*60+int(df['event_time'][index][14]+df['event_time'][index][15])*60+int(df['event_time'][index][17]+df['event_time'][index][18])
            day=int(df['event_time'][index][8]+df['event_time'][index][9])
            if df['persona_name'][index] ==value:
                current.append((day,tot_time_in_seconds))
        
       
        cnt=[86500 for i in range(0,32)]
        for day,time in current:
            cnt[day]=min(cnt[day],time)
        
        counter=Counter(cnt)
        max_count=0
        first_event=0
        for ele in counter:
            if ele < 86500:
                if max_count<counter[ele]:
                    max_count=counter[ele]
                    first_event=ele
        
        hr=int(first_event/3600)
        rem=first_event-(hr*3600)
        mn=int(rem/60)
        sec=int(rem-(mn*60))
        tm=str(hr)+':'+str(mn)+':'+str(sec)

        return tm
        
    def get_specific_answer_87(self,df,value):
        current=[]

        for index in range(0,df.shape[0]):
            hour=int(df['event_time'][index][11]+df['event_time'][index][12])*60*60
            minute=int(df['event_time'][index][14]+df['event_time'][index][15])*60
            second=int(df['event_time'][index][17]+df['event_time'][index][18])
            tot_time_in_seconds=hour+minute+second
            day=int(df['event_time'][index][8]+df['event_time'][index][9])
            
            if df['persona_name'][index] == value:         
                current.append((day,tot_time_in_seconds))
        
        
        # ans_for_87=[]
        # for persona,array in persona_event_dict.items():
        cnt2=[-1 for i in range(0,32)]
        for day,time in current:
            cnt2[day]=max(cnt2[day],time)
        
        counter_2=Counter(cnt2)
        lst_event=0
        max_count_2=0
        
        for ele in counter_2:
            if ele > -1:
                if max_count_2<counter_2[ele]:
                    max_count_2=counter_2[ele]
                    lst_event=ele
        
        hr=int(lst_event/3600)
        rem=lst_event-(hr*3600)
        mn=int(rem/60)
        sec=int(rem-(mn*60))
        tm=str(hr)+':'+str(mn)+':'+str(sec)
        
        return tm
    def get_specific_answer_90(self,df,value):
        message='This question cannot be answered'
        return message
    def get_specific_answer_91(self,df,value):
        message='This question cannot be answered'
        return message
    def get_specific_answer_94(self,df,value):
        participant_active_days_dict={}
        for index in range(0,df.shape[0]):
            hour=df['event_time'][index][11]+df['event_time'][index][12]
            hour=int(hour)
            
            date=df['event_time'][index][8]+df['event_time'][index][9]+' '+df['event_time'][index][5]+df['event_time'][index][6]+' '+df['event_time'][index][0]+df['event_time'][index][1]+df['event_time'][index][2]+df['event_time'][index][3]
            day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
            
            days_count_array=[0 for element in range(31)]
            if df['participant_name'][index] in participant_active_days_dict:
                days_count_array=participant_active_days_dict[df['participant_name'][index]]
            
            days_count_array[day]=1
            participant_active_days_dict.update({df['participant_name'][index]:days_count_array})

        
        current=[]
        for index in range(0,df.shape[0]):
            if df['persona_name'][index] == value:
                current.append(df['participant_name'][index])
        
        
        counter=Counter(current)
        total_count_of_inactive_days_in_persona=0
        for unique_participant in counter:
            active_days=np.sum(participant_active_days_dict[unique_participant])
            inactive_days=self.total_days-active_days
            total_count_of_inactive_days_in_persona+=inactive_days
            
        return total_count_of_inactive_days_in_persona/(self.total_days) 
    def get_specific_answer_95(self,df,value):
        
        hour_array={}
        for index in range(0,df.shape[0]):
            hour=df['event_time'][index][11]+df['event_time'][index][12]
            hour=int(hour)
            curr=df['active_time'][index]
            if df['participant_name'][index] ==value:
                if hour in hour_array:
                    curr+=hour_array[hour]
                hour_array.update({hour:curr})
        
        return max(hour_array.items(), key = operator.itemgetter(1))[0]
    

    def get_specific_answer_96(self,df,value):
        hour_array={}
        for index in range(0,df.shape[0]):
            hour=df['event_time'][index][11]+df['event_time'][index][12]
            hour=int(hour)
            curr=df['active_time'][index]
            if df['participant_name'][index] ==value:
                if hour in hour_array:
                    curr+=hour_array[hour]
                hour_array.update({hour:curr})
        
        
        print(hour_array)
        return min(hour_array.items(), key = operator.itemgetter(1))[0]
    
    def get_specific_answer_97(self,df,value):
        week_days_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']

        day_array={}
        for index in range(0,df.shape[0]):
            date=df['event_time'][index][8]+df['event_time'][index][9]+' '+df['event_time'][index][5]+df['event_time'][index][6]+' '+df['event_time'][index][0]+df['event_time'][index][1]+df['event_time'][index][2]+df['event_time'][index][3]
            day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
            curr=df['active_time'][index]
            if df['participant_name'][index] ==value:
                if day in day_array:
                    curr+=day_array[day]
                day_array.update({day:curr})
        
        
        
        
        return week_days_name[int(min(day_array.items(), key = operator.itemgetter(1))[0])]
        
    
    def get_specific_answer_98(self,df,value):
        week_days_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']

        day_array={}
        for index in range(0,df.shape[0]):
            date=df['event_time'][index][8]+df['event_time'][index][9]+' '+df['event_time'][index][5]+df['event_time'][index][6]+' '+df['event_time'][index][0]+df['event_time'][index][1]+df['event_time'][index][2]+df['event_time'][index][3]
            day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
            curr=df['active_time'][index]
            if df['participant_name'][index] ==value:
                if day in day_array:
                    curr+=day_array[day]
                day_array.update({day:curr})
        
        return week_days_name[int(max(day_array.items(), key = operator.itemgetter(1))[0])]
    
    def get_answer(self,id,df):

        function = getattr(queries, 'get_answer_'+str(int(id)))
        return function(self,df)
