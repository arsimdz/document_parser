from dotenv import load_dotenv

import os
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader,VectorStoreIndex
current_directory = os.getcwd()


load_dotenv()
#for SimpleDirectoryReader to parse the document need LlamaCloud API key.
#documents is already in a form that is usable for a LLM. With 3 additional lines are able to query the documents.

def doc_parser(directory):
    documents = SimpleDirectoryReader(directory).load_data()
    return documents


def documents_to_markdown(documents, output_file='output.md'):
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, doc in enumerate(documents, 1):
            # Write the filename as a header
            f.write(f"# Document {i}: {os.path.basename(doc.metadata['file_path'])}\n\n")
            
            # Write metadata
            f.write("## Metadata\n\n")
            for key, value in doc.metadata.items():
                f.write(f"- **{key}:** {value}\n")
            f.write("\n")
            
            # Write the document content
            f.write("## Content\n\n")
            f.write(doc.text)
            f.write("\n\n---\n\n")  # Separator between documents

    print(f"Markdown file created: {output_file}")
    return output_file



#query_doc will query the documents and return the response need OpenAI API key to work
def query_doc(question,documents):
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    return response
