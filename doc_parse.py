from dotenv import load_dotenv

import os
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
current_directory = os.getcwd()


load_dotenv()
relative_path = "uploads"
directory = os.path.join(current_directory, relative_path)

file_names = [] 
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        file_names.append(file_path)
        
        




# set up parser
parser = LlamaParse(
    result_type="markdown"  # "markdown" and "text" are available
)

# use SimpleDirectoryReader to parse our file
file_extractor = {".pdf": parser}
documents = SimpleDirectoryReader(directory).load_data()
print(documents)

def doc_parser(f):
    documents = SimpleDirectoryReader([f]).load_data()
    return documents