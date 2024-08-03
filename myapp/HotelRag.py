import pymongo
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
import os
import getpass


huggingface_api_token = "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"
if huggingface_api_token:
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = huggingface_api_token
else:
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = getpass.getpass()

def get_mongo_client(mongo_uri):
    try:
        client = pymongo.MongoClient(mongo_uri)
        print("Your connection is successful!!!!")
        return client
    except Exception as e:
        print("improper connection string", e)

def get_embedding_function():
    model_name = "BAAI/bge-large-en"
    model_kwargs = {"device":"cpu"}
    encode_kwargs = {"normalize_embeddings":True}
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return embeddings



mongo_client = get_mongo_client("mongodb+srv://adhimulamlalith22:Lalith321@hotel1.mb9zxfp.mongodb.net/?retryWrites=true&w=majority&appName=Hotel1")
DB_NAME = "Hotel1-G1"
COLLECTION_NAME = "BasicInfo"

db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

vector_store = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=get_embedding_function(),
    index_name="vector_index",
    relevance_score_fn="cosine",
)

def push_query(query_text):
    query_results = vector_store.similarity_search_with_relevance_scores(query_text)
    if len(query_results) != 0:
        filtered_query_result = lambda embedding_suggestion: embedding_suggestion[0].page_content if embedding_suggestion[1]>0.1 else None
        filtered_query_results = [result for result in map(filtered_query_result, query_results) if result is not None]
    else:
        print("unable to find matching results!")

    # print(query_results)
    # print(len(filtered_query_results))
    # print(filtered_query_results)

    PROMPT_TEMPLATE = """Answer the question based only on the following context: 
    {context}
    ---

    Answer the question based on the above context: {query}"""


    context_text = "'\n'\n---\n\n".join([doc for doc in filtered_query_results])
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    # prompt = prompt_template.format(context=context_text, query=query_text)
    # print(prompt_template)

    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
    llm = HuggingFaceEndpoint(
        repo_id=repo_id,
        temperature=0.5,
        huggingfacehub_api_token="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",
        add_to_git_credential=True,
    )

    chain = prompt | llm
    output = chain.invoke({"context": context_text, "query": query_text})
    return(output)