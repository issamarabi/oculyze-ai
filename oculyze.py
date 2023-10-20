import logging
import sys
import openai

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index import (
    SimpleDirectoryReader,
    LLMPredictor,
    ServiceContext,
    GPTVectorStoreIndex,
)
from llama_index.response.pprint_utils import pprint_response
from llama_index.llms import OpenAI

openai.api_key = "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"#os.getenv("OPENAI_API_KEY")

llm = OpenAI(temperature=0, model="gpt-4")
service_context = ServiceContext.from_defaults(llm=llm)

# Create dictionaries to store the documents and indexes for each task
documents_per_task = {}
indexes_per_task = {}

# Loop from task 1 to 6
for task_number in range(1, 7):
    task_folder_name = f'task{task_number}_files'
    
    # Load data from the respective directory
    documents = SimpleDirectoryReader(task_folder_name).load_data()
    
    # Store documents in the dictionary using the task number as a key
    documents_per_task[task_number] = documents

    # Create index from documents
    index = GPTVectorStoreIndex.from_documents(documents)

    # Store index in the dictionary using the task number as a key
    indexes_per_task[task_number] = index

expedia_task_1_engine = indexes_per_task[1].as_query_engine(
    similarity_top_k=3, service_context=service_context
)
expedia_task_2_engine = indexes_per_task[2].as_query_engine(
    similarity_top_k=3, service_context=service_context
)
expedia_task_3_engine = indexes_per_task[3].as_query_engine(
    similarity_top_k=3, service_context=service_context
)
kayak_task_1_engine = indexes_per_task[4].as_query_engine(
    similarity_top_k=3, service_context=service_context
)
kayak_task_2_engine = indexes_per_task[5].as_query_engine(
    similarity_top_k=3, service_context=service_context
)
kayak_task_3_engine = indexes_per_task[6].as_query_engine(
    similarity_top_k=3, service_context=service_context
)

from llama_index.tools import QueryEngineTool, ToolMetadata


query_tool_expedia_task_1 = QueryEngineTool.from_defaults(
    query_engine=expedia_task_1_engine,
    name="expedia_task_1",
    description=f"Expedia task 1: URLs and accessibility trees of webpages",
)
query_tool_expedia_task_2 = QueryEngineTool.from_defaults(
    query_engine=expedia_task_2_engine,
    name="expedia_task_2",
    description=f"Expedia task 2: URLs and accessibility trees of webpages",
)
query_tool_expedia_task_3 = QueryEngineTool.from_defaults(
    query_engine=expedia_task_3_engine,
    name="expedia_task_3",
    description=f"Expedia task 2: URLs and accessibility trees of webpages",
)
query_tool_kayak_task_1 = QueryEngineTool.from_defaults(
    query_engine=kayak_task_1_engine,
    name="kayak_task_1",
    description=f"Provides information about URLs and accessibility trees of webpages accessed in Kayak task 1 .",
)
query_tool_kayak_task_2 = QueryEngineTool.from_defaults(
    query_engine=kayak_task_2_engine,
    name="kayak_task_2",
    description=f"Provides information about URLs and accessibility trees of webpages accessed in Kayak task 2",
)
query_tool_kayak_task_3 = QueryEngineTool.from_defaults(
    query_engine=kayak_task_3_engine,
    name="kayak_task_3",
    description=f"Provides information about URLs and accessibility trees of webpages accessed in Kayak task 3",
)