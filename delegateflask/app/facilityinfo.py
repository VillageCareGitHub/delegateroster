import psycopg2
import sqlalchemy as sc
import sqlalchemy_redshift
import pandas as pd
import configparser
import datetime
from datetime import datetime
from flask import jsonify
import xlsxwriter
import xlrd
import re

class FacilityInfo:

    def __init__(self):
        self.pk=None
    
    def listToDict(lst,val):
        op = dict.fromkeys(lst , val)
        return op

    def facility_list():
        # Using config parser to retrieve credentials from config file
        initConfig = configparser.ConfigParser()
        initConfig.read("C:\\Users\\Public\\Documents\\VillageCare\\DELEGATE_UPLOAD\\delegateflask\\app\\AWS_List.config")

        # Connect to Prod Redshift and gather data
        # conn=psycopg2.connect(dbname= 'vcdwh', host=initConfig.get('profile prod', 'prodhost'), 
        # port= initConfig.get('profile prod', 'port'), user= initConfig.get('profile prod', 'dbuser'), password= initConfig.get('profile prod', 'dbpwd')) 

        conn=psycopg2.connect(dbname= 'dev', host=initConfig.get('profile prod', 'testhost'), 
        port= initConfig.get('profile prod', 'port'), user= initConfig.get('profile prod', 'dbuser'), password= initConfig.get('profile prod', 'dbpwd')) 

        # getting cursor
        cur = conn.cursor()

        # File date time stamp
        filedatetimestamp=datetime.today().strftime("%m%d%Y")

        # Vendor Facilities SQL
        with cur:
        
            SQL=f"""
            select vendor_id,vendor
            from provider.tbl_delegate_vendor
            order by vendor asc

            """

            providerdf=pd.read_sql_query(SQL,conn)

        # Constructing Facility Information into dropdown format
        flh=[]
        for newindex,newrow in providerdf.iterrows():
            new_row = {'value':str(newrow['vendor_id']).strip(),'label':str(newrow['vendor']).strip()}
            flh.append(new_row)



        # flh=[{'value':'ifh','label':'Institute for Family Health'},
        #     {'value':'integrap','label':'Integra Partners'},
        #     {'value':'ecap','label':'Eastern Chinese American IPA'},]

        return flh

    def import_delegate_roster(file_name,vendor_name):
        # Using config parser to retrieve credentials from config file
        initConfig = configparser.ConfigParser()
        initConfig.read("C:\\Users\\Public\\Documents\\VillageCare\\DELEGATE_UPLOAD\\delegateflask\\app\\AWS_List.config")

        # Connect to Prod Redshift and gather data
        # conn=psycopg2.connect(dbname= 'vcdwh', host=initConfig.get('profile prod', 'prodhost'), 
        # port= initConfig.get('profile prod', 'port'), user= initConfig.get('profile prod', 'dbuser'), password= initConfig.get('profile prod', 'dbpwd')) 

        conn=psycopg2.connect(dbname= 'dev', host=initConfig.get('profile prod', 'testhost'), 
        port= initConfig.get('profile prod', 'port'), user= initConfig.get('profile prod', 'dbuser'), password= initConfig.get('profile prod', 'dbpwd'))

        # getting cursor
        cur = conn.cursor()

        # Getting ILS Panda dataframe
        with cur:
        
            SQL=f"""
            select vendor.delete_row,vendor.field_concatenation,vendor.fields,vendor.multiple_sheets,vendor.row,
            vendor.sheet_name,vmap.*
            from provider.tbl_delegate_vendor vendor join provider.tbl_delegate_mapping vmap on vendor.vendor_id=vmap.vendor_id
            where vendor.vendor_id='{vendor_name}'

            """

            mappingdf=pd.read_sql_query(SQL,conn)

        # Creating empty dataframe for ILS Export to csv file
        ils_mapping_column_list=[]
        for colindex,col in mappingdf.iterrows():
            ils_mapping_column_list.append(str(col['ils_autoload_fields']))

        ils_autoload_df=pd.DataFrame(columns=ils_mapping_column_list) # columns=ils_mapping_column_list

        # Getting Vendor Document information
        exceldoc = xlrd.open_workbook(file_name)        
        sheets = exceldoc.sheets()

        # Getting Variables from Vendor Table
        with cur:
        
            SQL=f"""
            select vendor.delete_row,vendor.field_concatenation,vendor.fields,vendor.multiple_sheets,vendor.row,
            vendor.sheet_name
            from provider.tbl_delegate_vendor vendor
            where vendor.vendor_id='{vendor_name}'

            """

            vendorvardf=pd.read_sql_query(SQL,conn)
        
        # initializing variables
        headerrow=1
        field_con=''
        field_info=''
        multiple_sheet=''
        vendor_row=1
        vendor_sheetname=''

        for vindex,vrow in vendorvardf.iterrows():
            headerrow=vrow['delete_row']
            field_con=vrow['field_concatenation']
            field_info=vrow['fields']
            multiple_sheet=vrow['multiple_sheets']
            vendor_row=int(vrow['row'])
            vendor_sheetname=vrow['sheet_name']

        # Will need to read table to determine if there are multiple sheets
        i=0
        
        for sheet in sheets:
            i=i+1
            if i==1 and str(multiple_sheet).lower()!='y':
                if str(headerrow).lower()=='y':
                    exceldf=pd.read_excel(file_name,sheet=sheet.name,header=vendor_row) 
                else:
                    exceldf=pd.read_excel(file_name,sheet=sheet.name,header=0)  
            else:
                # parsing multiple sheets by variables and assigning different pandas in an array to append to each other
                # When that is completed it will append to the final exceldf for processing
                # parsing names based on vendor table
                if i==1:
                    if str(headerrow).lower()=='y':
                        exceldf=pd.read_excel(file_name,sheet=sheet.name,header=vendor_row) 
                    else:
                        exceldf=pd.read_excel(file_name,sheet=sheet.name,header=0)
                else:
                    vs=str(vendor_sheetname).split(',')
                    for ms in vs:
                        if str(headerrow).lower()=='y':
                            mdf=pd.read_excel(file_name,sheet=ms,header=vendor_row)
                            exceldf.append([mdf]) 
                        else:
                            mdf=pd.read_excel(file_name,sheet=ms,header=0)
                            exceldf.append([mdf]) 


        # Will need to check for removal of header row
        # print(exceldf.head())
        # exceldf2=exceldf.drop(index=0)

        # main code looping through Vendor Mapping Table to match excel document
        # trying to match information to dynamically create ILS File

        print(exceldf.head())

        

        ils_info_holder={}
        for eindex,erow in exceldf.iterrows():
            # creating row of data to append to ILS dataframe
            # Getting Column names from
            
            
            for mindex,mrow in mappingdf.iterrows():
                new_const=True
                for ecol in exceldf.columns: 
                    #print(ecol)   
                   
                    if str(mrow['constant_variable']).lower()=='y' and new_const==True:
                        # print('hitting constant variable')
                        # print(mrow['constant_variable_detail'])
                        if mrow['constant_variable_detail']==None:                                                    
                            
                            ihh=[]
                            ihh.append(mrow['ils_autoload_fields'])
                            ih=FacilityInfo.listToDict(ihh,'')                            
                            ils_info_holder.update(ih)                            
                            new_const=False
                        else:
                            
                            ihh=[]
                            ihh.append(mrow['ils_autoload_fields'])
                            ih=FacilityInfo.listToDict(ihh,str(mrow['constant_variable_detail']))                            
                            ils_info_holder.update(ih)                                                       
                            new_const=False
                        
                    if re.sub('[^A-Za-z0-9]+', '', str(mrow['vendor_fields']).lower())==re.sub('[^A-Za-z0-9]+', '', str(ecol).lower()):
                                                                      
                        ihh=[]
                        ihh.append(mrow['ils_autoload_fields'])
                        ih=FacilityInfo.listToDict(ihh,str(erow[ecol]))                        
                        ils_info_holder.update(ih)
                              
                        
                    if str(mrow['field_concatenation']).lower()=='y':
                        fcc=str(mrow['fields']).split(',')
                        fstr=[]
                        for fs in fcc:
                            if str(mrow['vendor_fields']).strip()==str(fs).strip():
                                fstr.append(erow[ecol])
                                #ils_info_holder.append(''.join(fstr))
                        
                
                
            #print(ils_info_holder)            
            ils_autoload_df=ils_autoload_df.append(ils_info_holder,ignore_index=True)
            #print('clearing list')
            ils_info_holder.clear()
            
                            

              
        return ils_autoload_df





        

