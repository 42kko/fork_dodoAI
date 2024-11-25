from ktb_prompts import *
from ktb_settings import *
from ktb_func import *

import os
from typing import List, Dict, Optional, Any, Generator
from pathlib import Path
import logging
import asyncio
import aiofiles

"""**FUNCTION FOR CHAT**"""
# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def search_file(repo_path, filename):
    repo_path = Path(repo_path)

    # 경로 안의 모든 파일과 폴더를 탐색
    for file_path in repo_path.rglob(filename):
        return file_path  # 첫 번째로 찾은 파일 반환

    return None  # 파일이 없으면 None 반환



def get_embedding(texts: List[str], model: str = EMBEDDING_MODEL) -> List[float]:
    """
    Get embeddings for a list of texts using OpenAI's embedding model.

    Args:
        texts (List[str]): List of texts to embed
        model (str): Name of the embedding model to use

    Returns:
        List[float]: The embedding vector
    """
    try:
        # Clean texts by replacing newlines with spaces
        #cleaned_texts = [text.replace("\n", " ") for text in texts]
        response = client_gpt.embeddings.create(input=texts, model=model)
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error generating embedding: {str(e)}")
        raise


async def add_data_to_db(repo_name: str, path: str) -> int:
    """
    Process files by chunking them, generating embeddings, and storing in ChromaDB.

    Args:
        repo_name (str): Name of the repository/collection
        path (str): Path to the repository directory

    Returns:
        int: Number of documents in the collection
    """
    try:
        # Get or create collection
        vector_store = chroma_client.get_or_create_collection(
            name=repo_name,
            embedding_function=embedding_function,
            metadata=DISTANCE
        )

        # Convert path to Path object for better path handling
        repo_path = Path(path)

        # Initialize counter for chunk IDs
        chunk_id_counter = 0
        total_files_processed = 0
        for root, dirs, files in os.walk(repo_path):
            for filename in files:
                if filename == '.DS_Store':
                    continue
                if filename.endswith('.md'):
                    try:
                        file_path = search_file(repo_path, filename)
                        # Check if file exists
                        if not file_path.exists():
                            logger.warning(f"File not found: {file_path}")
                            continue

                        # Check if file is readable
                        if not file_path.is_file():
                            logger.warning(f"Not a valid file: {file_path}")
                            continue

                        async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
                            doc = await file.read()
                            if doc.strip():  # Only process non-empty documents
                                # Create metadata for the current file
                                file_metadata = {
                                    "filename": filename,
                                    "path": str(file_path),
                                    "repository": repo_name
                                }

                                # Split document into chunks
                                chunks = markdown_splitter.split_text(doc)

                                if chunks:  # Only process if we have chunks
                                    # Process chunks and clean text
                                    chunk_contents = [
                                        chunk.page_content.replace('\n', ' ').strip()
                                        for chunk in chunks
                                        if chunk.page_content.strip()  # Skip empty chunks
                                    ]

                                    if chunk_contents:  # Only add if we have valid chunks
                                        # Generate IDs for current chunks
                                        chunk_ids = [
                                            f"{repo_name}_{i}"
                                            for i in range(chunk_id_counter, chunk_id_counter + len(chunk_contents))
                                        ]

                                        # Create metadata list for all chunks from this file
                                        chunk_metadatas = [file_metadata for _ in range(len(chunk_contents))]

                                        # Add chunks to vector store
                                        vector_store.add(
                                            documents=chunk_contents,
                                            metadatas=chunk_metadatas,
                                            ids=chunk_ids
                                        )

                                        # Update counter and log success
                                        chunk_id_counter += len(chunk_contents)
                                        total_files_processed += 1
                                        print(f"Successfully processed file: {filename} - Added {len(chunk_contents)} chunks")
                                    else:
                                        logger.warning(f"No valid chunks found in file: {filename}")
                                else:
                                    logger.warning(f"No chunks generated from file: {filename}")
                            else:
                                logger.warning(f"Empty file skipped: {filename}")

                    except UnicodeDecodeError as e:
                        logger.error(f"Unicode decode error in file {filename}: {str(e)}")
                        continue
                    except Exception as e:
                        logger.error(f"Error processing file {filename}: {str(e)}")
                        continue

        if total_files_processed == 0:
            raise ValueError("No valid files were processed")

        total_chunks = vector_store.count()
        print(f"Successfully processed {total_files_processed} files with total {total_chunks} chunks in {repo_name}")
        return total_chunks

    except Exception as e:
        logger.error(f"Error adding data to DB: {str(e)}")
        raise

def db_search(query: str, db: Any, n_results: int = 5) -> Dict[str, Any]:
    """
    Search the vector database for similar documents.

    Args:
        query (str): Search query
        db: ChromaDB collection
        n_results (int): Number of results to return
        threshold (float): Similarity threshold

    Returns:
        Dict[str, Any]: Search results including documents and metadata
    """
    try:
        results = db.query(
            query_texts=query,
            n_results=n_results
        )
        return results

    except Exception as e:
        logger.error(f"Error searching DB: {str(e)}")
        raise

def generate_response(query: str, db: Any, chat_history: Optional[List[dict]] = None) -> Generator[Any, Any, Any]:
    """model: Optional[str] = MODEL,
    Generate a response using LLM based on retrieved documents.

    Args:
        query (str): User query
        db: ChromaDB collection

    Returns:
        str: Generated response
    """
    try:
        retrieved_docs = db_search(query, db)

        # Construct prompt
        system_prompt = CHATBOT_PROMPT
        
        user_prompt = f"""Context: {retrieved_docs['documents']}

User Query / Instruct: {query}
"""

        full_prompt = [{"role": "system", "content": system_prompt}]
        if chat_history : full_prompt.extend(chat_history)  # Include previous conversation history
        full_prompt.append({"role": "user", "content": user_prompt})
        # Generate response using OpenAI
        response = client_gpt.chat.completions.create(
            model="GPT_MODEL",  # Updated from deprecated davinci-003
            messages=full_prompt,
            temperature=0.12,
            stream = True
        )
        
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        raise

def codebase_chat(query: str, repo_url: str, chat_history: List[dict] = []) -> Any:
    """
    Chat with a codebase by querying the vector store and generating responses.

    Args:
        query (str): User query
        repo_name (str): Name of the repository/collection to search
        threshold (float): Similarity threshold for relevant documents

    Returns:
        Tuple[str, Dict[str, Any]]: Generated response and retrieved documents with metadata
    """
    repo_name, _ = parse_repo_url(repo_url)
    try:
        # Validate repository exists
        vector_store = chroma_client.get_collection(
            name=repo_name,
            embedding_function=embedding_function
        )
        
        # Get the collection
        db = vector_store

        # Generate response and get retrieved documents
        if chat_history :
            response = generate_response(query, db, chat_history)
        else: 
            response = generate_response(query, db)

        # Log the interaction
        print(f"""
            Chat Interaction:
            Repository: {repo_url}
            Query: {query}
            """)

        return response

    except Exception as e:
        logger.error(f"Error in codebase chat: {str(e)}")
        raise