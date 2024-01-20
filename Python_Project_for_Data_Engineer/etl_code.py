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
    # the problem is in the data files which is in the format
    # {<record1>}
    # {<record2>}
    # {<record3>}
    # but should be in the format:        
    # [ {<record1>},
    #   {<record2>},
    #   {<record3>} ]    
    df = pd.read_json(file_to_process)
    return df
    

def extract_from_xml(file_to_process:str)-> pd.DataFrame:
    """
    This function gets as input the path to an XML file
    The function reads the file, converts it a Panas DF and return the content
    """
    # first we create an empty DF
    df = pd.DataFrame(columns=["name","height","weight"])
    #
    # Now we read the xml file and parse it to add entries to the df
    tree = ET.parse(file_to_process)
    root = tree.getroot()
    for person in root:
        name = person.find("name").text
        height = person.find("height").text
        weight = person.find("weight").text
        df = pd.concat([df, 
                        pd.DataFrame([{"name": name, "height": height, "weight": weight}])
                        ])        
    return df                    


def extract()-> pd.DataFrame:
    """
    This function takes no input and:
    - it parses all csv, json and xml files in the current folder
    - creates a dataframe with name, height, weight for each file
    - concatenate the df together and returns a single Pandas DataFrame
      with the content of all the files 
    """ 
    extracted_data = pd.DataFrame(columns=['name','height','weight']) # create an empty data frame to hold extracted data 
     
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
    Convert inches to meters and round off to two decimals 
    1 inch is 0.0254 meters 
    Convert pounds to kilograms and round off to two decimals 
    1 pound is 0.45359237 kilograms
    
    The dataframe is then returned with the converted info
    '''
    print(type(data['height']))
    # Note this required a change with .astype("float") to avoid errors
    data['height'] = round(data['height'].astype("float") * 0.0254, 2) 
 
    data['weight'] = round(data['weight'].astype("float") * 0.45359237, 2) 
    
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