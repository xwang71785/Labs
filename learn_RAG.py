"""
example code for learning Retrieval-Augmented Generation (RAG) with ChromaDB and Google GenAI
pip install -U sentence-transformers
"""

from typing import List
from sentence_transformers import SentenceTransformer
import chromadb
from sentence_transformers import CrossEncoder
from dotenv import load_dotenv
from google import genai


def split_into_chunks(doc_file: str) -> List[str]:
    '''Splits the content of a doc file into chunks based on paragraphs.'''
    with open(doc_file, 'r', encoding='UTF-8') as file:
        content = file.read()

    return [chunk for chunk in content.split("\n\n")]

# Initialize the embedding model
embedding_model = SentenceTransformer("shibing624/text2vec-base-chinese")
def embed_chunk(chunk: str) -> List[float]:
    '''Embeds a chunk of text using the specified embedding model.'''
    embedding = embedding_model.encode(chunk, normalize_embeddings=True)
    return embedding.tolist()

# Initialize ChromaDB client and collection
chromadb_client = chromadb.EphemeralClient()
chromadb_collection = chromadb_client.get_or_create_collection(name="default")

def save_embeddings(chunks: List[str], embeddings: List[List[float]]) -> None:
    '''Saves the chunks and their embeddings to the ChromaDB collection.'''
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        chromadb_collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[str(i)]
        )

def retrieve(query: str, top_k: int) -> List[str]:
    '''Retrieves the top_k chunks that are most similar to the query.'''
    query_embedding = embed_chunk(query)
    results = chromadb_collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results['documents'][0]

# Initialize the cross-encoder for reranking
cross_encoder = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1')
def rerank(query: str, retrieved_chunks: List[str], top_k: int) -> List[str]:
    '''Reranks the retrieved chunks based on their relevance to the query using a cross-encoder.'''
    pairs = [(query, chunk) for chunk in retrieved_chunks]
    scores = cross_encoder.predict(pairs)

    scored_chunks = list(zip(retrieved_chunks, scores))
    scored_chunks.sort(key=lambda x: x[1], reverse=True)

    return [chunk for chunk, _ in scored_chunks][:top_k]


load_dotenv()
google_client = genai.Client()

def generate(query: str, chunks: List[str]) -> str:
    '''Generates an answer to the query based on the provided chunks using Google GenAI.'''
    prompt = f"""你是一位知识助手，请根据用户的问题和下列片段生成准确的回答。
    用户问题: {query}
    相关片段:
    {"\n\n".join(chunks)}
    请基于上述内容作答，不要编造信息。"""

    print(f"{prompt}\n\n---\n")

    response = google_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

def main():
    '''Main function to run the RAG process.'''
    # 拆分文档
    chunks = split_into_chunks("doc.md")
    for i, chunk in enumerate(chunks):
        print(f"[{i}] {chunk}\n")
    # 生成嵌入
    embeddings = [embed_chunk(chunk) for chunk in chunks]
    print(len(embeddings))
    print(embeddings)
    # 保存嵌入到ChromaDB
    save_embeddings(chunks, embeddings)

    query = "哆啦A梦使用的3个秘密道具分别是什么？"
    # 检索与query相关片段
    retrieved_chunks = retrieve(query, 5)
    for i, chunk in enumerate(retrieved_chunks):
        print(f"[{i}] {chunk}\n")
    # 重新排序片段
    reranked_chunks = rerank(query, retrieved_chunks, 3)
    for i, chunk in enumerate(reranked_chunks):
        print(f"[{i}] {chunk}\n")
    # 调用LLM参考文档片段基于query生成回答
    answer = generate(query, reranked_chunks)
    print(answer)

if __name__ == "__main__":
    main()
    