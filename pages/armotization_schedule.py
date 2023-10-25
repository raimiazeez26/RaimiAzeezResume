
#import required libraries
import pandas as pd
import numpy as np
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import numpy_financial as npf

pd.set_option('display.max_rows', None)



#Actual Ammortization Function
def ammortization (Principal, month_number_list, date_range_list, interest_rate_list):
    """
      Function which calculates payment made montly.
      Inputs:
        Principal (int): Principal loan amount
        Month Numbers (list): A list of month numbers from 1st month to last month of the schedule
        Date Range List (list): A list of 1st of every month from the 1st month of ammortization to the last month of ammortization
        Interest Rate list (list) : A list of Annual Interest Rates for each month from the 1st day of the schedule to the last day of the schedule

      Outputs (DataFrame):
        A dataframe of armortization schedule
    """

    details={'Month_Number' : month_number_list, 'Date' : date_range_list, 'Annual_Interest_Rate' : interest_rate_list}
    Final_df=pd.DataFrame(details)

    #Converting Annual Interest Rate from Percentage to decimal
    Final_df['Annual_Interest_Rate']=Final_df['Annual_Interest_Rate']/100

    for index in range(0,Final_df.shape[0]):
        if index==0:
            Final_df.at[index,'Principal_Balance']= Principal

        #Formula for Interest Paid = Interest Rate * Principal Remaining
        Final_df.at[index, "Interest_Paid"] =Final_df['Principal_Balance'][index]  * Final_df['Annual_Interest_Rate'][index] / 12

        #Using "Numpy pmt" function to calculate total Interest needed to be paid for the respectiveInterest rate for the month
        Final_df.at[index, 'Monthly_Payment'] = -npf.pmt( Final_df['Annual_Interest_Rate'][index] / 12 , Final_df.shape[0]-Final_df['Month_Number'][index], Final_df['Principal_Balance'][index])

        #Amount of Principal paid in monthly payments = Calculated Monthly Payment - Interest Payment for the month
        Final_df.at[index, "Principal_Paid"] =Final_df['Monthly_Payment'][index] - Final_df['Interest_Paid'][index]

        #Principal left to be paid after Monthly Payment
        Final_df.at[index,"Principal_Remaining"]=Final_df['Principal_Balance'][index]-Final_df["Principal_Paid"][index]
        if index!= Final_df.shape[0]-1:
            Final_df.at[index+1 , 'Principal_Balance']=Final_df["Principal_Remaining"][index]

    Final_df['Total_Interest_Paid'] = Final_df["Interest_Paid"].cumsum()
    return Final_df


# In[18]:


## Adding Day 0 column in a dataframe and shifting the dataframe down by 1 row
def Adding_Day_Zero_Details(Date_string, Initial_Principal, df):
    '''
    This function adds the Day 0 details and shifts the dataframe down by 1 row

    '''
    #Creating a dictionary of Day Zero Details
    newRow={"Month_Number":0,"Date":pd.to_datetime(f'{Date_string}') ,'Annual_Interest_Rate': 0,"Principal_Balance": Initial_Principal,
       'Interest_Paid': 0 , "Monthly_Payment": 0 , "Principal_Paid": 0 , "Principal_Remaining": Initial_Principal, 'Total_Interest_Paid': 0}
    row_df=pd.DataFrame([newRow])
    df=pd.concat([row_df,df], ignore_index=True)
    df['Month_Number']=df.index

    #Converting Anual & Monthly Interest Rates to Percentage(%)
    df['Annual_Interest_Rate']= round(df['Annual_Interest_Rate']*100,8)
    #df['Monthly_Interest_Rate']= round(df['Monthly_Interest_Rate']*100,8)
    #df.rename(columns={'Monthly_Interest_Rate' : "Monthly_Interest_Rate(in_%)"}, inplace=True)
    df.rename(columns={'Annual_Interest_Rate' : "Annual_Interest_Rate(in_%)"}, inplace=True)

    df=df[['Month_Number','Date','Annual_Interest_Rate(in_%)','Principal_Balance', 'Monthly_Payment', 'Interest_Paid', 'Principal_Paid' ,'Principal_Remaining', 'Total_Interest_Paid']]
    return df


def run_armotization(principal, fixed_rate, years, start_date):
    
    #variables for 30-Year 4% Fixed Interest Rate
    Principal = principal
    years = years
    Fixed_Rate=fixed_rate
    start_date = pd.to_datetime(start_date) #'1993-01-01'
    no_months = int(years*12)
    #print(f'no_months:{no_months}, type:{type(no_months)}')
    end_date = start_date + relativedelta(months=no_months)

    dates= pd.date_range(start_date,end_date , freq='1M')-pd.offsets.MonthBegin(1)
    month_no=list(range(0,no_months))

    # Appending 30*12 times because we are paying interest rate monthly for 30 Years
    Total_Rate_List=[]
    for i in range(0,no_months):
        Total_Rate_List.append(Fixed_Rate)
    del(i)
    
    final_df=ammortization(Principal, month_no, dates, Total_Rate_List)
    final_df=Adding_Day_Zero_Details(start_date,Principal,final_df)
    arm_sch= final_df.round(2)
    arm_sch = arm_sch.drop('Annual_Interest_Rate(in_%)', axis = 1)
    
    return arm_sch



