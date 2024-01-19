import glob
import pandas as pd 
import xml.etree.ElementTree as ET 
from datetime import datetime 


log_file = "log_file.txt"
target_file = "transformed_data.csv"

def extract_from_csv(file_to_process:str)-> pd.DataFrame:
    """
    This function gets as input the path to a CSV file
    it uses pandas to read the file and return the DataFrame from the file
    """
    df = pd.read_csv(file_to_process)
    return df


def extract_from_json(file_to_process:str)-> pd.DataFrame:
    """
    This function gets as input the path to a JSON file
    it uses pandas to read the file and return the DataFrame from the file
    """
    # this was giving some issues so.. 
    # but now pandas support reading multiple records..
    # just set lines=True
    df = pd.read_json(file_to_process, lines=True)
    # Note, another (and more memory efficient) way would be something like this:
    # with open(file_to_process) as f:
    #     df = pd.DataFrame(json.loads(line) for line in f)
    return df
    

def extract_from_xml(file_to_process:str)-> pd.DataFrame:
    """
    This function gets as input the path to an XML file
    The function reads the file, converts it a Panas DF and return the content
    """
    # first we create an empty DF
    df = pd.DataFrame(columns=["car_model","year_of_manufacture","price","fuel"])
    #
    # Now we read the xml file and parse it to add entries to the df
    tree = ET.parse(file_to_process)
    root = tree.getroot()
    for car in root:
        car_model = car.find("car_model").text
        year_of_manufacture = car.find("year_of_manufacture").text
        price = car.find("price").text
        fuel = car.find("fuel").text        
        df = pd.concat([df, 
                        pd.DataFrame([{"car_model": car_model, 
                                       "year_of_manufacture": year_of_manufacture, 
                                       "price": price,
                                       "fuel": fuel}
                                       ])
                        ])        
    return df                    


def extract()-> pd.DataFrame:
    """
    This function takes no input and:
    - it parses all csv, json and xml files in the current folder
    - creates a dataframe with car_model,year_of_manufacture,price,fuel for each file
    - concatenate the df together and returns a single Pandas DataFrame
      with the content of all the files 
    """ 
     # create an empty data frame to hold extracted data   
    extracted_data = pd.DataFrame(columns=["car_model","year_of_manufacture","price","fuel"])

    # process all csv files 
    for csvfile in glob.glob("*.csv"): 
        extracted_data = pd.concat([extracted_data, 
                                    pd.DataFrame(extract_from_csv(csvfile))
                                    ], 
                                    ignore_index=True) # if this is not set to True, Pandas will try to
                                                       # keep every row with their own index 
         
    # process all json files 
    for jsonfile in glob.glob("*.json"): 
        extracted_data = pd.concat([extracted_data, 
                                    pd.DataFrame(extract_from_json(jsonfile))
                                    ], 
                                    ignore_index=True) 
     
    # process all xml files 
    for xmlfile in glob.glob("*.xml"): 
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_xml(xmlfile))], ignore_index=True) 
         
    return extracted_data     


def transform(data:pd.DataFrame) -> pd.DataFrame:
    '''
    This function takes as input a Pandas DataFrame and  
    Convert price by rounding to 2 decimal places
    
    The dataframe is then returned with the converted info
    '''
    # Note this required a change with .astype("float") to avoid errors
    data['price'] = round(data['price'].astype("float"), 2) 
 
    return data     


def load_data(target_file:str, data:pd.DataFrame):
    """
    This function takes as input:
    - target_file: str, name of the destination file
    - data: pandas.DataFrame
    and saves the Dataframe back to a the target file as csv
    """    
    data.to_csv(target_file)


def log_progress(message:str):
    """
    This function takes as input a message: <str> and appends it to <log_file>
    which is expected to be a global var 
    Note: the message is prepended with a timestamp in the format
          '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    """    
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open(log_file,"a") as f: 
        f.write(timestamp + ',' + message + '\n') 


########################## ACTUAL MAIN

if __name__ == "__main__":
   # Log the initialization of the ETL process 
   log_progress("ETL Job Started") 
    
   # Log the beginning of the Extraction process 
   log_progress("Extract phase Started") 
   extracted_data = extract() 
    
   # Log the completion of the Extraction process 
   log_progress("Extract phase Ended") 
    
   # Log the beginning of the Transformation process 
   log_progress("Transform phase Started") 
   transformed_data = transform(extracted_data) 
   print("Transformed Data") 
   print(transformed_data) 
    
   # Log the completion of the Transformation process 
   log_progress("Transform phase Ended") 
    
   # Log the beginning of the Loading process 
   log_progress("Load phase Started") 
   load_data(target_file,transformed_data) 
    
   # Log the completion of the Loading process 
   log_progress("Load phase Ended") 
    
   # Log the completion of the ETL process 
   log_progress("ETL Job Ended")          