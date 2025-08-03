from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq  
from dotenv import load_dotenv
import os

load_dotenv()

def ask_from_video(video_url, question):
    video_id = video_url.split("v=")[-1]

    transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=["en", "hi"])
    transcript = " ".join([snippet.text for snippet in transcript_list])

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.from_documents(chunks, embeddings)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    retrieved_docs = retriever.invoke(question)
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

    prompt = PromptTemplate(
        template="""
        You are an intelligent YouTube Video Analyzer Assistant.
        Your task is to answer questions strictly using the provided video transcript context.
        If the context is insufficient to answer the question, say "I'm not sure based on the given transcript."

         Rules:
            - Do not hallucinate or make assumptions.
            - Always use the provided context to answer the question.
            - If the question is directly answerable from the context, provide a direct answer.
            - If the question is not answerable from the context, respond with "I'm not sure
            - If the question requires summarization.
            - If the question is about the video content, provide a concise answer.
            - Provide a concise summary based on the context.


        {context}
        Question: {question}
        """,
        input_variables=["context", "question"]
    )

    llm = ChatGroq(
        temperature=0.7,
        model_name="compound-beta",  
        groq_api_key=os.getenv("GROQ_API_KEY")  
    )

    final_prompt = prompt.invoke({"context": context_text, "question": question})
    answer = llm.invoke(final_prompt)

    return answer.content
