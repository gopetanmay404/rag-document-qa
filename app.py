# # import streamlit as st
# # import fitz
# # import numpy as np
# # from sentence_transformers import SentenceTransformer
# # from sklearn.metrics.pairwise import cosine_similarity

# # # ---------------- MODEL ----------------
# # @st.cache_resource
# # def load_model():
# #     return SentenceTransformer("all-MiniLM-L6-v2")

# # model = load_model()


# # # ---------------- PDF EXTRACTION ----------------
# # def extract_text(file_bytes):
# #     doc = fitz.open(stream=file_bytes, filetype="pdf")
# #     text = ""
# #     for page in doc:
# #         text += page.get_text("text") + "\n"
# #     return text


# # # ---------------- CHUNKING ----------------
# # def chunk_text(text):
# #     lines = text.split("\n")

# #     chunks = []
# #     current_chunk = []

# #     for line in lines:
# #         if line.strip().startswith(("1.", "2.", "3.", "4.", "Module")):
# #             if current_chunk:
# #                 chunks.append("\n".join(current_chunk))
# #                 current_chunk = []

# #         current_chunk.append(line)

# #     if current_chunk:
# #         chunks.append("\n".join(current_chunk))

# #     return chunks


# # # ---------------- EMBEDDINGS ----------------
# # def get_embeddings(chunks):
# #     return model.encode(chunks)


# # # ---------------- RETRIEVAL ----------------
# # def retrieve(question, chunks, embeddings, top_k=3):
# #     q_emb = model.encode([question])
# #     scores = cosine_similarity(q_emb, embeddings)[0]

# #     top_idx = np.argsort(scores)[-top_k:][::-1]

# #     top_chunks = [chunks[i] for i in top_idx]
# #     top_scores = [scores[i] for i in top_idx]

# #     return top_chunks, top_scores, scores


# # # ---------------- UI ----------------
# # st.set_page_config(page_title="RAG Debug Bot", layout="wide")

# # st.title("📄 PDF RAG Debug Bot")

# # uploaded_file = st.file_uploader(
# #     "Upload PDF",
# #     type=["pdf"],
# #     key="pdf_upload"
# # )

# # # session state
# # if "chunks" not in st.session_state:
# #     st.session_state.chunks = None
# #     st.session_state.embeddings = None
# #     st.session_state.text = None


# # # ---------------- PROCESS ----------------
# # if uploaded_file:
# #     file_bytes = uploaded_file.getvalue()

# #     text = extract_text(file_bytes)
# #     chunks = chunk_text(text)
# #     embeddings = get_embeddings(chunks)

# #     st.session_state.text = text
# #     st.session_state.chunks = chunks
# #     st.session_state.embeddings = embeddings

# #     st.success("PDF processed successfully!")


# # # ---------------- DEBUG SECTION ----------------
# # if st.session_state.text:

# #     st.subheader("🔍 Extracted Text (DEBUG)")
# #     st.write(st.session_state.text[:1500])

# #     st.subheader("🧩 Sample Chunks (DEBUG)")
# #     for i, c in enumerate(st.session_state.chunks[:3]):
# #         st.write(f"Chunk {i+1}")
# #         st.write(c)
# #         st.write("------")


# # # ---------------- QUESTION ----------------
# # st.subheader("Ask Question")

# # question = st.text_input("Type your question")

# # if question and st.session_state.chunks is not None:

# #     top_chunks, top_scores, all_scores = retrieve(
# #         question,
# #         st.session_state.chunks,
# #         st.session_state.embeddings
# #     )

# #     st.subheader("📌 Top Relevant Chunks")

# #     for i, c in enumerate(top_chunks):
# #         st.write(f"Score: {top_scores[i]:.4f}")
# #         st.write(c)
# #         st.write("------")

# #     st.subheader("📊 Score Preview (first 10 chunks)")

# #     st.write(all_scores[:10])


# # import streamlit as st
# # import fitz
# # import os
# # from dotenv import load_dotenv

# # from langchain_groq import ChatGroq
# # from langchain_huggingface import HuggingFaceEmbeddings
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain_community.vectorstores import FAISS
# # from langchain_core.prompts import ChatPromptTemplate

# # # ---------------- LOAD ENV ----------------
# # load_dotenv()

# # groq_api_key = os.getenv("GROQ_API_KEY")

# # if not groq_api_key:
# #     st.error("❌ GROQ_API_KEY not found in .env file")
# #     st.stop()

# # # ---------------- LLM ----------------
# # llm = ChatGroq(
# #     api_key=groq_api_key,
# #     model_name="llama-3.1-8b-instant"
# # )

# # # ---------------- EMBEDDINGS ----------------
# # embeddings = HuggingFaceEmbeddings(
# #     model_name="sentence-transformers/all-MiniLM-L6-v2"
# # )

# # # ---------------- PDF TEXT ----------------
# # def extract_text_from_pdf(file_bytes):
# #     doc = fitz.open(stream=file_bytes, filetype="pdf")
# #     text = ""
# #     for page in doc:
# #         text += page.get_text("text")
# #     return text

# # # ---------------- CHUNKING ----------------
# # def split_text(text):
# #     splitter = RecursiveCharacterTextSplitter(
# #         chunk_size=1000,
# #         chunk_overlap=200
# #     )
# #     return splitter.create_documents([text])

# # # ---------------- PROMPT ----------------
# # prompt = ChatPromptTemplate.from_template("""
# # Answer ONLY from the given context.

# # <context>
# # {context}
# # </context>

# # Question: {input}

# # Give a simple and clear answer.
# # """)

# # # ---------------- UI ----------------
# # st.set_page_config(page_title="PDF RAG (Groq)", layout="wide")
# # st.title("📄 PDF Q&A System (Groq + FAISS)")

# # uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

# # if "vectorstore" not in st.session_state:
# #     st.session_state.vectorstore = None

# # # ---------------- PROCESS PDF ----------------
# # if uploaded_file:

# #     file_bytes = uploaded_file.getvalue()

# #     with st.spinner("Processing PDF..."):
# #         text = extract_text_from_pdf(file_bytes)

# #         docs = split_text(text)

# #         st.session_state.vectorstore = FAISS.from_documents(
# #             docs,
# #             embeddings
# #         )

# #     st.success("PDF Ready 🚀")

# # # ---------------- QUESTION ----------------
# # query = st.text_input("Ask a question")

# # if query and st.session_state.vectorstore is not None:

# #     retriever = st.session_state.vectorstore.as_retriever()

# #     docs = retriever.invoke(query)

# #     context = "\n\n".join([d.page_content for d in docs])

# #     final_prompt = prompt.format(context=context, input=query)

# #     response = llm.invoke(final_prompt)

# #     st.subheader("📌 Answer")
# #     st.write(response.content)

# #     with st.expander("📊 Retrieved Chunks"):
# #         for i, d in enumerate(docs):
# #             st.write(f"Chunk {i+1}")
# #             st.write(d.page_content)
# #             st.divider()















# # import streamlit as st
# # import fitz
# # import os
# # from dotenv import load_dotenv

# # from langchain_groq import ChatGroq
# # from langchain_huggingface import HuggingFaceEmbeddings
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain_community.vectorstores import FAISS

# # # ---------------- LOAD ENV ----------------
# # load_dotenv()

# # groq_api_key = os.getenv("GROQ_API_KEY")

# # if not groq_api_key:
# #     st.error("❌ GROQ_API_KEY not found in .env file")
# #     st.stop()

# # # ---------------- LLM ----------------
# # llm = ChatGroq(
# #     api_key=groq_api_key,
# #     model_name="llama-3.1-8b-instant"
# # )

# # # ---------------- EMBEDDINGS ----------------
# # embeddings = HuggingFaceEmbeddings(
# #     model_name="sentence-transformers/all-MiniLM-L6-v2"
# # )

# # # ---------------- PDF TEXT ----------------
# # def extract_text_from_pdf(file_bytes):
# #     doc = fitz.open(stream=file_bytes, filetype="pdf")

# #     text = ""

# #     for page in doc:
# #         text += page.get_text("text")

# #     return text

# # # ---------------- CHUNKING ----------------
# # def split_text(text):

# #     splitter = RecursiveCharacterTextSplitter(
# #         chunk_size=1000,
# #         chunk_overlap=200
# #     )

# #     return splitter.create_documents([text])

# # # ---------------- UI ----------------
# # st.set_page_config(
# #     page_title="PDF RAG + Memory",
# #     layout="wide"
# # )

# # st.title("📄 PDF Q&A System (Groq + FAISS + Memory)")

# # # ---------------- SESSION STATE ----------------
# # if "vectorstore" not in st.session_state:
# #     st.session_state.vectorstore = None

# # if "chat_history" not in st.session_state:
# #     st.session_state.chat_history = []

# # # ---------------- PDF UPLOAD ----------------
# # uploaded_file = st.file_uploader(
# #     "Upload PDF",
# #     type=["pdf"]
# # )

# # # ---------------- PROCESS PDF ----------------
# # if uploaded_file:

# #     file_bytes = uploaded_file.getvalue()

# #     with st.spinner("Processing PDF..."):

# #         text = extract_text_from_pdf(file_bytes)

# #         docs = split_text(text)

# #         st.session_state.vectorstore = FAISS.from_documents(
# #             docs,
# #             embeddings
# #         )

# #     st.success("✅ PDF Ready")

# # # ---------------- QUESTION ----------------
# # query = st.text_input("Ask a question")

# # if query and st.session_state.vectorstore:

# #     retriever = st.session_state.vectorstore.as_retriever()

# #     docs = retriever.invoke(query)

# #     context = "\n\n".join(
# #         [doc.page_content for doc in docs]
# #     )

# #     # Last few messages only
# #     history = "\n".join(
# #         st.session_state.chat_history[-6:]
# #     )

# #     final_prompt = f"""
# # You are a helpful assistant.

# # Previous Conversation:
# # {history}

# # Context:
# # {context}

# # Question:
# # {query}

# # Rules:
# # 1. Answer ONLY from the context.
# # 2. Use previous conversation if helpful.
# # 3. Keep answer clear and well formatted.
# # 4. If answer is not found in context, say:
# #    "Answer not found in the document."
# # """

# #     response = llm.invoke(final_prompt)

# #     # Save Memory
# #     st.session_state.chat_history.append(
# #         f"User: {query}"
# #     )

# #     st.session_state.chat_history.append(
# #         f"Assistant: {response.content}"
# #     )

# #     # Answer
# #     st.subheader("📌 Answer")
# #     st.write(response.content)

# #     # Retrieved Chunks
# #     with st.expander("📊 Retrieved Chunks"):

# #         for i, doc in enumerate(docs):

# #             st.markdown(f"### Chunk {i+1}")

# #             st.write(doc.page_content)

# #             st.divider()

# # # ---------------- CHAT HISTORY ----------------
# # with st.expander("🧠 Memory / Chat History"):

# #     if st.session_state.chat_history:

# #         for msg in st.session_state.chat_history:
# #             st.write(msg)

# #     else:
# #         st.write("No conversation yet.")



















# # import streamlit as st
# # import fitz
# # import os
# # from dotenv import load_dotenv

# # from langchain_groq import ChatGroq
# # from langchain_huggingface import HuggingFaceEmbeddings
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain_community.vectorstores import FAISS
# # from langchain_core.prompts import ChatPromptTemplate

# # # ---------------- LOAD ENV ----------------
# # load_dotenv()

# # groq_api_key = os.getenv("GROQ_API_KEY")

# # if not groq_api_key:
# #     st.error("❌ GROQ_API_KEY not found in .env file")
# #     st.stop()

# # # ---------------- LLM ----------------
# # llm = ChatGroq(
# #     api_key=groq_api_key,
# #     model_name="llama-3.1-8b-instant"
# # )

# # # ---------------- EMBEDDINGS ----------------
# # embeddings = HuggingFaceEmbeddings(
# #     model_name="sentence-transformers/all-MiniLM-L6-v2"
# # )

# # # ---------------- PDF TEXT EXTRACTION ----------------
# # def extract_text_from_pdf(file_bytes):
# #     doc = fitz.open(stream=file_bytes, filetype="pdf")
# #     text = ""
# #     for page in doc:
# #         text += page.get_text("text")
# #     return text

# # # ---------------- CHUNKING ----------------
# # def split_text(text):
# #     splitter = RecursiveCharacterTextSplitter(
# #         chunk_size=2000,
# #         chunk_overlap=400
# #     )
# #     return splitter.create_documents([text])

# # # ---------------- PROMPT ----------------
# # prompt = ChatPromptTemplate.from_template("""
# # You are a document question-answering assistant.

# # Use ONLY the provided context.

# # Rules:
# # - Do not make up information.
# # - If the answer is not present in the context, say so.
# # - If the user asks for a summary, overview, project explanation, or brief description, combine information from multiple relevant sections.
# # - Keep the answer clear and structured.

# # <context>
# # {context}
# # </context>

# # Question:
# # {input}

# # Answer:
# # """)

# # # ---------------- UI ----------------
# # st.set_page_config(page_title="Multi-PDF RAG", layout="wide")
# # st.title("📄 Multi-PDF Q&A System (Groq + FAISS)")

# # uploaded_files = st.file_uploader(
# #     "Upload PDFs",
# #     type=["pdf"],
# #     accept_multiple_files=True
# # )

# # # ---------------- SESSION STATE ----------------
# # if "vectorstore" not in st.session_state:
# #     st.session_state.vectorstore = None

# # if "chat_history" not in st.session_state:
# #     st.session_state.chat_history = []

# # # ---------------- PROCESS PDFs ----------------
# # if uploaded_files:

# #     with st.spinner("Processing PDFs..."):

# #         all_text = ""

# #         for pdf in uploaded_files:
# #             file_bytes = pdf.getvalue()
# #             all_text += extract_text_from_pdf(file_bytes)
# #             all_text += "\n\n"

# #         docs = split_text(all_text)

# #         st.session_state.vectorstore = FAISS.from_documents(
# #             docs,
# #             embeddings
# #         )

# #     st.success("All PDFs Ready 🚀")

# # # ---------------- QUESTION INPUT ----------------
# # query = st.text_input("Ask your question")

# # # ---------------- ANSWER FLOW ----------------
# # if query and st.session_state.vectorstore is not None:

# #     docs_and_scores = (
# #         st.session_state.vectorstore
# #         .similarity_search_with_score(query, k=5)
# #         )

# #     docs = [doc for doc, score in docs_and_scores]



    

# #     final_prompt = prompt.format(context=context, input=query)

# #     response = llm.invoke(final_prompt)

# #     # -------- MEMORY --------
# #     st.session_state.chat_history.append(f"User: {query}")
# #     st.session_state.chat_history.append(f"Assistant: {response.content}")

# #     # -------- OUTPUT --------
# #     st.subheader("📌 Answer")
# #     st.write(response.content)

# #     # -------- DEBUG CHUNKS --------
    
# #     with st.expander("📊 Retrieved Chunks"):

# #     st.write(f"Retrieved {len(docs_and_scores)} chunks")

# #     for i, (doc, score) in enumerate(docs_and_scores):

# #         st.markdown(f"### Chunk {i+1}")

# #         st.write(f"Distance Score: {score:.4f}")

# #         st.write(doc.page_content[:1000])

# #         st.divider()
        

# # # ---------------- CHAT HISTORY ----------------
# # if st.session_state.chat_history:
# #     with st.expander("💬 Chat History"):
# #         for msg in st.session_state.chat_history:
# #             st.write(msg)















# # import streamlit as st
# # import fitz
# # import os
# # from dotenv import load_dotenv

# # from langchain_groq import ChatGroq
# # from langchain_huggingface import HuggingFaceEmbeddings
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain_community.vectorstores import FAISS
# # from langchain_core.prompts import ChatPromptTemplate

# # # ---------------- LOAD ENV ----------------
# # load_dotenv()

# # groq_api_key = os.getenv("GROQ_API_KEY")

# # if not groq_api_key:
# #     st.error("❌ GROQ_API_KEY not found in .env file")
# #     st.stop()

# # # ---------------- LLM ----------------
# # llm = ChatGroq(
# #     api_key=groq_api_key,
# #     model_name="llama-3.1-8b-instant"
# # )

# # # ---------------- EMBEDDINGS ----------------
# # embeddings = HuggingFaceEmbeddings(
# #     model_name="sentence-transformers/all-MiniLM-L6-v2"
# # )

# # # ---------------- PDF TEXT EXTRACTION ----------------
# # def extract_text_from_pdf(file_bytes):
# #     doc = fitz.open(stream=file_bytes, filetype="pdf")

# #     text = ""

# #     for page in doc:
# #         text += page.get_text("text")

# #     return text


# # # ---------------- CHUNKING ----------------
# # def split_text(text):

# #     splitter = RecursiveCharacterTextSplitter(
# #         chunk_size=1500,
# #         chunk_overlap=300
# #     )

# #     return splitter.create_documents([text])


# # # ---------------- PROMPT ----------------
# # prompt = ChatPromptTemplate.from_template("""
# # You are a document question-answering assistant.

# # Use ONLY the provided context.

# # Rules:
# # - Do not make up information.
# # - If the answer is not present in the context, say:
# #   "Answer not found in the document."
# # - If user asks for a summary, overview, explanation, architecture,
# #   workflow, modules, benefits, objectives, etc.,
# #   combine information from multiple retrieved chunks.
# # - Keep answers structured and clear.

# # Conversation History:
# # {history}

# # <context>
# # {context}
# # </context>

# # Question:
# # {input}

# # Answer:
# # """)


# # # ---------------- UI ----------------
# # st.set_page_config(
# #     page_title="Multi PDF RAG",
# #     layout="wide"
# # )

# # st.title("📄 Multi-PDF RAG Chatbot")


# # # ---------------- SESSION STATE ----------------
# # if "vectorstore" not in st.session_state:
# #     st.session_state.vectorstore = None

# # if "chat_history" not in st.session_state:
# #     st.session_state.chat_history = []


# # # ---------------- PDF UPLOAD ----------------
# # uploaded_files = st.file_uploader(
# #     "Upload PDF files",
# #     type=["pdf"],
# #     accept_multiple_files=True
# # )


# # # ---------------- PROCESS PDFs ----------------
# # if uploaded_files:

# #     with st.spinner("Processing PDFs..."):

# #         all_docs = []

# #         for pdf in uploaded_files:

# #             file_bytes = pdf.getvalue()

# #             text = extract_text_from_pdf(file_bytes)

# #             docs = split_text(text)

# #             # store source metadata
# #             for doc in docs:
# #                 doc.metadata["source"] = pdf.name

# #             all_docs.extend(docs)

# #         st.session_state.vectorstore = FAISS.from_documents(
# #             all_docs,
# #             embeddings
# #         )

# #     st.success(
# #         f"✅ {len(uploaded_files)} PDF(s) processed successfully"
# #     )


# # # ---------------- QUESTION ----------------
# # query = st.text_input(
# #     "Ask your question"
# # )


# # # ---------------- ANSWER FLOW ----------------
# # if query and st.session_state.vectorstore is not None:

# #     # Better Retrieval using MMR
# #     retriever = st.session_state.vectorstore.as_retriever(
# #         search_type="mmr",
# #         search_kwargs={
# #             "k": 8,
# #             "fetch_k": 20
# #         }
# #     )

# #     docs = retriever.invoke(query)

# #     context = "\n\n".join(
# #         [doc.page_content for doc in docs]
# #     )

# #     # Also retrieve scores for debugging
# #     docs_and_scores = (
# #         st.session_state.vectorstore
# #         .similarity_search_with_score(
# #             query,
# #             k=5
# #         )
# #     )

# #     history = "\n".join(
# #         st.session_state.chat_history[-8:]
# #     )

# #     final_prompt = prompt.format(
# #         history=history,
# #         context=context,
# #         input=query
# #     )

# #     response = llm.invoke(final_prompt)

# #     # ---------------- MEMORY ----------------
# #     st.session_state.chat_history.append(
# #         f"User: {query}"
# #     )

# #     st.session_state.chat_history.append(
# #         f"Assistant: {response.content}"
# #     )

# #     # ---------------- ANSWER ----------------
# #     st.subheader("📌 Answer")
# #     st.write(response.content)

# #     # ---------------- RETRIEVED CHUNKS ----------------
# #     with st.expander("📊 Retrieved Chunks + Scores"):

# #         st.write(
# #             f"Retrieved {len(docs_and_scores)} chunks"
# #         )

# #         for i, (doc, score) in enumerate(
# #             docs_and_scores
# #         ):

# #             st.markdown(
# #                 f"### Chunk {i+1}"
# #             )

# #             st.write(
# #                 f"📏 Distance Score: {score:.4f}"
# #             )

# #             st.write(
# #                 f"📄 Source: {doc.metadata.get('source', 'Unknown')}"
# #             )

# #             st.write(
# #                 doc.page_content[:1200]
# #             )

# #             st.divider()


# # # ---------------- CHAT HISTORY ----------------
# # if st.session_state.chat_history:

# #     with st.expander("💬 Chat History"):

# #         for msg in st.session_state.chat_history:
# #             st.write(msg)






# # import streamlit as st
# # import fitz
# # import os
# # import hashlib
# # from dotenv import load_dotenv

# # from langchain_groq import ChatGroq
# # from langchain_huggingface import HuggingFaceEmbeddings
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain_community.vectorstores import FAISS
# # from langchain_core.prompts import ChatPromptTemplate

# # # ── ENV ──────────────────────────────────────────────────────────────────────
# # load_dotenv()
# # groq_api_key = os.getenv("GROQ_API_KEY")
# # if not groq_api_key:
# #     st.error("❌ GROQ_API_KEY not found in .env file")
# #     st.stop()

# # # ── PAGE CONFIG ───────────────────────────────────────────────────────────────
# # st.set_page_config(page_title="Multi PDF RAG", layout="wide", page_icon="📄")
# # st.title("📄 Multi-PDF RAG Chatbot")

# # # ── SESSION STATE ─────────────────────────────────────────────────────────────
# # defaults = {
# #     "vectorstore": None,
# #     "chat_history": [],       # list of {"role": str, "content": str}
# #     "pdf_hashes": set(),      # detect re-uploads
# #     "chunk_stats": {},        # per-pdf stats for inspector
# #     "all_docs": [],           # keep chunks for inspector tab
# # }
# # for k, v in defaults.items():
# #     if k not in st.session_state:
# #         st.session_state[k] = v

# # # ── SIDEBAR: CHUNKING CONTROLS ────────────────────────────────────────────────
# # with st.sidebar:
# #     st.header("⚙️ Chunking Settings")

# #     chunk_size = st.slider(
# #         "Chunk size (chars)", 200, 3000, 1000, step=50,
# #         help="Smaller = more precise retrieval. Larger = more context per chunk."
# #     )
# #     overlap_pct = st.slider(
# #         "Overlap %", 5, 40, 20, step=5,
# #         help="Overlap as % of chunk size. 15–25% is the sweet spot."
# #     )
# #     overlap = int(chunk_size * overlap_pct / 100)
# #     st.caption(f"→ Overlap = **{overlap}** chars")

# #     k_retrieve = st.slider(
# #         "Chunks to retrieve (k)", 3, 15, 6,
# #         help="How many chunks to pull per query. More = broader context, slower."
# #     )

# #     st.divider()
# #     st.header("🤖 Model")
# #     model_name = st.selectbox(
# #         "Groq model",
# #         ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
# #     )
# #     temperature = st.slider("Temperature", 0.0, 1.0, 0.1, step=0.05)

# # # ── LLM ──────────────────────────────────────────────────────────────────────
# # @st.cache_resource
# # def get_llm(model, temp, key):
# #     return ChatGroq(api_key=key, model_name=model, temperature=temp)

# # llm = get_llm(model_name, temperature, groq_api_key)

# # # ── EMBEDDINGS ────────────────────────────────────────────────────────────────
# # @st.cache_resource
# # def get_embeddings():
# #     return HuggingFaceEmbeddings(
# #         model_name="sentence-transformers/all-MiniLM-L6-v2",
# #         model_kwargs={"device": "cpu"},
# #         encode_kwargs={"normalize_embeddings": True},
# #     )

# # embeddings = get_embeddings()

# # # ── PDF EXTRACTION ────────────────────────────────────────────────────────────
# # def extract_text(file_bytes: bytes) -> str:
# #     doc = fitz.open(stream=file_bytes, filetype="pdf")
# #     pages = []
# #     for i, page in enumerate(doc):
# #         text = page.get_text("text").strip()
# #         if text:
# #             pages.append(f"[Page {i+1}]\n{text}")
# #     return "\n\n".join(pages)

# # # ── CHUNKING ──────────────────────────────────────────────────────────────────
# # def split_text(text: str, cs: int, ov: int):
# #     splitter = RecursiveCharacterTextSplitter(
# #         chunk_size=cs,
# #         chunk_overlap=ov,
# #         separators=["\n\n", "\n", ". ", " ", ""],
# #         length_function=len,
# #     )
# #     return splitter.create_documents([text])

# # # ── PROMPT ────────────────────────────────────────────────────────────────────
# # prompt = ChatPromptTemplate.from_template("""
# # You are a precise document Q&A assistant.

# # Rules:
# # - Answer ONLY from the provided context.
# # - If the answer isn't in the context, say: "Answer not found in the document."
# # - After your answer, list which source files you used like: **Sources: file1.pdf, file2.pdf**
# # - For summaries or overviews, synthesize across all relevant chunks.
# # - Keep answers structured and concise.

# # Conversation history (last 6 turns):
# # {history}

# # <context>
# # {context}
# # </context>

# # Question: {input}

# # Answer:
# # """)

# # # ── TABS ──────────────────────────────────────────────────────────────────────
# # tab_chat, tab_inspect, tab_history = st.tabs(
# #     ["💬 Chat", "🔬 Chunk Inspector", "📜 History"]
# # )

# # # ════════════════════════════════════════════════════════════════════════════
# # # TAB 1 — CHAT
# # # ════════════════════════════════════════════════════════════════════════════
# # with tab_chat:

# #     uploaded_files = st.file_uploader(
# #         "Upload PDF files",
# #         type=["pdf"],
# #         accept_multiple_files=True,
# #         key="pdf_uploader",
# #     )

# #     if uploaded_files:
# #         # Detect new files by content hash (avoid re-embedding same files)
# #         new_files = []
# #         for pdf in uploaded_files:
# #             h = hashlib.md5(pdf.getvalue()).hexdigest()
# #             if h not in st.session_state.pdf_hashes:
# #                 new_files.append((pdf, h))

# #         if new_files:
# #             with st.spinner(f"Processing {len(new_files)} new PDF(s)…"):
# #                 new_docs = []
# #                 for pdf, h in new_files:
# #                     text = extract_text(pdf.getvalue())
# #                     docs = split_text(text, chunk_size, overlap)

# #                     char_counts = [len(d.page_content) for d in docs]
# #                     st.session_state.chunk_stats[pdf.name] = {
# #                         "n_chunks": len(docs),
# #                         "avg_chars": round(sum(char_counts) / max(len(char_counts), 1)),
# #                         "min_chars": min(char_counts),
# #                         "max_chars": max(char_counts),
# #                         "total_chars": len(text),
# #                         "chunk_size": chunk_size,
# #                         "overlap": overlap,
# #                     }

# #                     for doc in docs:
# #                         doc.metadata["source"] = pdf.name
# #                     new_docs.extend(docs)
# #                     st.session_state.all_docs.extend(docs)
# #                     st.session_state.pdf_hashes.add(h)

# #                 if st.session_state.vectorstore is None:
# #                     st.session_state.vectorstore = FAISS.from_documents(
# #                         new_docs, embeddings
# #                     )
# #                 else:
# #                     st.session_state.vectorstore.add_documents(new_docs)

# #             st.success(f"✅ {len(new_files)} PDF(s) indexed — "
# #                        f"{len(st.session_state.all_docs)} total chunks")
# #         else:
# #             st.info("These PDFs are already indexed.")

# #     # ── CHAT DISPLAY ──────────────────────────────────────────────────────────
# #     for msg in st.session_state.chat_history:
# #         with st.chat_message(msg["role"]):
# #             st.write(msg["content"])

# #     # ── INPUT ─────────────────────────────────────────────────────────────────
# #     query = st.chat_input(
# #         "Ask a question about your PDFs…",
# #         disabled=st.session_state.vectorstore is None,
# #     )

# #     if query:
# #         with st.chat_message("user"):
# #             st.write(query)

# #         retriever = st.session_state.vectorstore.as_retriever(
# #             search_type="mmr",
# #             search_kwargs={
# #                 "k": k_retrieve,
# #                 "fetch_k": k_retrieve * 5,
# #                 "lambda_mult": 0.6,  # diversity vs relevance balance
# #             },
# #         )
# #         retrieved_docs = retriever.invoke(query)

# #         # Build context with source labels

        
# #         context_parts = []

# #         for doc in retrieved_docs:
# #             text = doc.page_content.strip()

# #             if len(text) <= 50:
# #                 continue

# #             src = doc.metadata.get("source", "unknown")
# #             context_parts.append(f"[{src}]\n{text}")
# #         context = "\n\n---\n\n".join(context_parts)
# #         # History: keep last 6 turns as structured text
# #         history_text = "\n".join(
# #             f"{m['role'].capitalize()}: {m['content']}"
# #             for m in st.session_state.chat_history[-6:]
# #         )

# #         final_prompt = prompt.format(
# #             history=history_text,
# #             context=context,
# #             input=query,
# #         )

# #         with st.chat_message("assistant"):
# #             with st.spinner("Thinking…"):
# #                 response = llm.invoke(final_prompt)
# #             answer = response.content
# #             st.write(answer)

# #             with st.expander("📎 Retrieved chunks"):
# #                 for i, doc in enumerate(retrieved_docs):
# #                     src = doc.metadata.get("source", "unknown")
# #                     st.markdown(f"**Chunk {i+1}** — `{src}`")
# #                     st.caption(doc.page_content[:600] +
# #                                ("…" if len(doc.page_content) > 600 else ""))
# #                     st.divider()

# #         st.session_state.chat_history.append({"role": "user", "content": query})
# #         st.session_state.chat_history.append({"role": "assistant", "content": answer})

# #     if st.session_state.vectorstore is None:
# #         st.info("⬆️ Upload at least one PDF to start chatting.")

# # # ════════════════════════════════════════════════════════════════════════════
# # # TAB 2 — CHUNK INSPECTOR
# # # ════════════════════════════════════════════════════════════════════════════
# # with tab_inspect:
# #     st.subheader("🔬 Chunk Inspector")

# #     if not st.session_state.chunk_stats:
# #         st.info("Upload PDFs to see chunk statistics here.")
# #     else:
# #         for fname, stats in st.session_state.chunk_stats.items():
# #             with st.expander(f"📄 {fname}"):
# #                 col1, col2, col3, col4 = st.columns(4)
# #                 col1.metric("Chunks", stats["n_chunks"])
# #                 col2.metric("Avg chars", stats["avg_chars"])
# #                 col3.metric("Min chars", stats["min_chars"])
# #                 col4.metric("Max chars", stats["max_chars"])

# #                 overlap_ratio = round(
# #                     stats["overlap"] / max(stats["chunk_size"], 1) * 100
# #                 )
# #                 st.caption(
# #                     f"Settings used: chunk_size={stats['chunk_size']}, "
# #                     f"overlap={stats['overlap']} ({overlap_ratio}%), "
# #                     f"total doc chars={stats['total_chars']:,}"
# #                 )

# #                 # Quality warning
# #                 if stats["avg_chars"] < 200:
# #                     st.warning(
# #                         "⚠️ Avg chunk is very small. Consider increasing chunk size "
# #                         "— too many tiny chunks hurt retrieval quality."
# #                     )
# #                 elif stats["avg_chars"] > 1800:
# #                     st.warning(
# #                         "⚠️ Avg chunk is large. LLM gets a lot of irrelevant text "
# #                         "per chunk (haystack effect). Consider reducing chunk size."
# #                     )
# #                 else:
# #                     st.success("✅ Chunk size looks healthy for Q&A retrieval.")

# #         # Show sample chunks from selected PDF
# #         st.divider()
# #         st.subheader("Sample chunks")
# #         sources = list({
# #             d.metadata.get("source", "unknown")
# #             for d in st.session_state.all_docs
# #         })
# #         if sources:
# #             chosen_src = st.selectbox("Pick a PDF", sources)
# #             src_docs = [
# #                 d for d in st.session_state.all_docs
# #                 if d.metadata.get("source") == chosen_src
# #             ]
# #             n_show = st.slider("Chunks to preview", 1, min(10, len(src_docs)), 3)
# #             for i, doc in enumerate(src_docs[:n_show]):
# #                 st.markdown(f"**Chunk {i+1}** — {len(doc.page_content)} chars")
# #                 st.text_area(
# #                     label="",
# #                     value=doc.page_content,
# #                     height=140,
# #                     key=f"chunk_preview_{chosen_src}_{i}",
# #                     disabled=True,
# #                 )

# # # ════════════════════════════════════════════════════════════════════════════
# # # TAB 3 — HISTORY
# # # ════════════════════════════════════════════════════════════════════════════
# # with tab_history:
# #     st.subheader("💬 Conversation History")

# #     if not st.session_state.chat_history:
# #         st.info("No conversation yet.")
# #     else:
# #         for msg in st.session_state.chat_history:
# #             icon = "🧑" if msg["role"] == "user" else "🤖"
# #             st.markdown(f"**{icon} {msg['role'].capitalize()}:** {msg['content']}")
# #             st.divider()

# #         if st.button("🗑️ Clear history"):
# #             st.session_state.chat_history = []
# #             st.rerun()





# # import streamlit as st
# # import fitz
# # import os
# # import hashlib
# # from dotenv import load_dotenv

# # from langchain_groq import ChatGroq
# # from langchain_huggingface import HuggingFaceEmbeddings
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain_community.vectorstores import FAISS
# # from langchain_core.prompts import ChatPromptTemplate

# # # ── ENV ──────────────────────────────────────────────────────────────────────
# # load_dotenv()
# # groq_api_key = os.getenv("GROQ_API_KEY")
# # if not groq_api_key:
# #     st.error("❌ GROQ_API_KEY not found in .env file")
# #     st.stop()

# # # ── PAGE CONFIG ───────────────────────────────────────────────────────────────
# # st.set_page_config(page_title="Multi PDF RAG", layout="wide", page_icon="📄")
# # st.title("📄 Multi-PDF RAG Chatbot")

# # # ── SESSION STATE ─────────────────────────────────────────────────────────────
# # defaults = {
# #     "vectorstore": None,
# #     "chat_history": [],       # list of {"role": str, "content": str}
# #     "pdf_hashes": set(),      # detect re-uploads
# #     "chunk_stats": {},        # per-pdf stats for inspector
# #     "all_docs": [],           # keep chunks for inspector tab
# # }
# # for k, v in defaults.items():
# #     if k not in st.session_state:
# #         st.session_state[k] = v

# # # ── SIDEBAR: CHUNKING CONTROLS ────────────────────────────────────────────────
# # with st.sidebar:
# #     st.header("⚙️ Chunking Settings")

# #     chunk_size = st.slider(
# #         "Chunk size (chars)", 200, 3000, 1000, step=50,
# #         help="Smaller = more precise retrieval. Larger = more context per chunk."
# #     )
# #     overlap_pct = st.slider(
# #         "Overlap %", 5, 40, 20, step=5,
# #         help="Overlap as % of chunk size. 15–25% is the sweet spot."
# #     )
# #     overlap = int(chunk_size * overlap_pct / 100)
# #     st.caption(f"→ Overlap = **{overlap}** chars")

# #     k_retrieve = st.slider(
# #         "Chunks to retrieve (k)", 3, 15, 6,
# #         help="How many chunks to pull per query. More = broader context, slower."
# #     )

# #     st.divider()
# #     st.header("🤖 Model")
# #     model_name = st.selectbox(
# #         "Groq model",
# #         ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
# #     )
# #     temperature = st.slider("Temperature", 0.0, 1.0, 0.1, step=0.05)

# # # ── LLM ──────────────────────────────────────────────────────────────────────
# # @st.cache_resource
# # def get_llm(model, temp, key):
# #     return ChatGroq(api_key=key, model_name=model, temperature=temp)

# # llm = get_llm(model_name, temperature, groq_api_key)

# # # ── EMBEDDINGS ────────────────────────────────────────────────────────────────
# # @st.cache_resource
# # def get_embeddings():
# #     return HuggingFaceEmbeddings(
# #         model_name="sentence-transformers/all-MiniLM-L6-v2",
# #         model_kwargs={"device": "cpu"},
# #         encode_kwargs={"normalize_embeddings": True},
# #     )

# # embeddings = get_embeddings()

# # # ── PDF EXTRACTION ────────────────────────────────────────────────────────────
# # def extract_text(file_bytes: bytes) -> str:
# #     doc = fitz.open(stream=file_bytes, filetype="pdf")
# #     pages = []
# #     for i, page in enumerate(doc):
# #         text = page.get_text("text").strip()
# #         if text:
# #             pages.append(f"[Page {i+1}]\n{text}")
# #     return "\n\n".join(pages)

# # # ── CHUNKING ──────────────────────────────────────────────────────────────────
# # def split_text(text: str, cs: int, ov: int):
# #     splitter = RecursiveCharacterTextSplitter(
# #         chunk_size=cs,
# #         chunk_overlap=ov,
# #         separators=["\n\n", "\n", ". ", " ", ""],
# #         length_function=len,
# #     )
# #     return splitter.create_documents([text])

# # # ── PROMPT ────────────────────────────────────────────────────────────────────
# # prompt = ChatPromptTemplate.from_template("""
# # You are a precise document Q&A assistant.

# # Rules:
# # - Answer ONLY from the provided context.
# # - If the answer isn't in the context, say: "Answer not found in the document."
# # - After your answer, list which source files you used like: **Sources: file1.pdf, file2.pdf**
# # - For summaries or overviews, synthesize across all relevant chunks.
# # - Keep answers structured and concise.

# # Conversation history (last 6 turns):
# # {history}

# # <context>
# # {context}
# # </context>

# # Question: {input}

# # Answer:
# # """)

# # # ── TABS ──────────────────────────────────────────────────────────────────────
# # tab_chat, tab_inspect, tab_history = st.tabs(
# #     ["💬 Chat", "🔬 Chunk Inspector", "📜 History"]
# # )

# # # ════════════════════════════════════════════════════════════════════════════
# # # TAB 1 — CHAT
# # # ════════════════════════════════════════════════════════════════════════════
# # with tab_chat:

# #     uploaded_files = st.file_uploader(
# #         "Upload PDF files",
# #         type=["pdf"],
# #         accept_multiple_files=True,
# #         key="pdf_uploader",
# #     )

# #     if uploaded_files:
# #         # Detect new files by content hash (avoid re-embedding same files)
# #         new_files = []
# #         for pdf in uploaded_files:
# #             h = hashlib.md5(pdf.getvalue()).hexdigest()
# #             if h not in st.session_state.pdf_hashes:
# #                 new_files.append((pdf, h))

# #         if new_files:
# #             with st.spinner(f"Processing {len(new_files)} new PDF(s)…"):
# #                 new_docs = []
# #                 for pdf, h in new_files:
# #                     text = extract_text(pdf.getvalue())
# #                     docs = split_text(text, chunk_size, overlap)

# #                     char_counts = [len(d.page_content) for d in docs]
# #                     st.session_state.chunk_stats[pdf.name] = {
# #                         "n_chunks": len(docs),
# #                         "avg_chars": round(sum(char_counts) / max(len(char_counts), 1)),
# #                         "min_chars": min(char_counts),
# #                         "max_chars": max(char_counts),
# #                         "total_chars": len(text),
# #                         "chunk_size": chunk_size,
# #                         "overlap": overlap,
# #                     }

# #                     for doc in docs:
# #                         doc.metadata["source"] = pdf.name
# #                     new_docs.extend(docs)
# #                     st.session_state.all_docs.extend(docs)
# #                     st.session_state.pdf_hashes.add(h)

# #                 if st.session_state.vectorstore is None:
# #                     st.session_state.vectorstore = FAISS.from_documents(
# #                         new_docs, embeddings
# #                     )
# #                 else:
# #                     st.session_state.vectorstore.add_documents(new_docs)

# #             st.success(f"✅ {len(new_files)} PDF(s) indexed — "
# #                        f"{len(st.session_state.all_docs)} total chunks")
# #         else:
# #             st.info("These PDFs are already indexed.")

# #     # ── CHAT DISPLAY ──────────────────────────────────────────────────────────
# #     for msg in st.session_state.chat_history:
# #         with st.chat_message(msg["role"]):
# #             st.write(msg["content"])

# #     # ── INPUT ─────────────────────────────────────────────────────────────────
# #     query = st.chat_input(
# #         "Ask a question about your PDFs…",
# #         disabled=st.session_state.vectorstore is None,
# #     )

# #     if query:
# #         with st.chat_message("user"):
# #             st.write(query)

# #         retriever = st.session_state.vectorstore.as_retriever(
# #             search_type="mmr",
# #             search_kwargs={
# #                 "k": k_retrieve,
# #                 "fetch_k": k_retrieve * 3,
# #                 "lambda_mult": 0.6,  # diversity vs relevance balance
# #             },
# #         )
# #         retrieved_docs = retriever.invoke(query)

# #         # Build context with source labels
# #         context_parts = []
# #         for doc in retrieved_docs:
# #             src = doc.metadata.get("source", "unknown")
# #             context_parts.append(f"[{src}]\n{doc.page_content}")
# #         context = "\n\n---\n\n".join(context_parts)

# #         # History: keep last 6 turns as structured text
# #         history_text = "\n".join(
# #             f"{m['role'].capitalize()}: {m['content']}"
# #             for m in st.session_state.chat_history[-6:]
# #         )

# #         final_prompt = prompt.format(
# #             history=history_text,
# #             context=context,
# #             input=query,
# #         )

# #         with st.chat_message("assistant"):
# #             with st.spinner("Thinking…"):
# #                 response = llm.invoke(final_prompt)
# #             answer = response.content
# #             st.write(answer)

# #             with st.expander("📎 Retrieved chunks"):
# #                 for i, doc in enumerate(retrieved_docs):
# #                     src = doc.metadata.get("source", "unknown")
# #                     st.markdown(f"**Chunk {i+1}** — `{src}`")
# #                     st.caption(doc.page_content[:600] +
# #                                ("…" if len(doc.page_content) > 600 else ""))
# #                     st.divider()

# #         st.session_state.chat_history.append({"role": "user", "content": query})
# #         st.session_state.chat_history.append({"role": "assistant", "content": answer})

# #     if st.session_state.vectorstore is None:
# #         st.info("⬆️ Upload at least one PDF to start chatting.")

# # # ════════════════════════════════════════════════════════════════════════════
# # # TAB 2 — CHUNK INSPECTOR
# # # ════════════════════════════════════════════════════════════════════════════
# # with tab_inspect:
# #     st.subheader("🔬 Chunk Inspector")

# #     if not st.session_state.chunk_stats:
# #         st.info("Upload PDFs to see chunk statistics here.")
# #     else:
# #         for fname, stats in st.session_state.chunk_stats.items():
# #             with st.expander(f"📄 {fname}"):
# #                 col1, col2, col3, col4 = st.columns(4)
# #                 col1.metric("Chunks", stats["n_chunks"])
# #                 col2.metric("Avg chars", stats["avg_chars"])
# #                 col3.metric("Min chars", stats["min_chars"])
# #                 col4.metric("Max chars", stats["max_chars"])

# #                 overlap_ratio = round(
# #                     stats["overlap"] / max(stats["chunk_size"], 1) * 100
# #                 )
# #                 st.caption(
# #                     f"Settings used: chunk_size={stats['chunk_size']}, "
# #                     f"overlap={stats['overlap']} ({overlap_ratio}%), "
# #                     f"total doc chars={stats['total_chars']:,}"
# #                 )

# #                 # Quality warning
# #                 if stats["avg_chars"] < 200:
# #                     st.warning(
# #                         "⚠️ Avg chunk is very small. Consider increasing chunk size "
# #                         "— too many tiny chunks hurt retrieval quality."
# #                     )
# #                 elif stats["avg_chars"] > 1800:
# #                     st.warning(
# #                         "⚠️ Avg chunk is large. LLM gets a lot of irrelevant text "
# #                         "per chunk (haystack effect). Consider reducing chunk size."
# #                     )
# #                 else:
# #                     st.success("✅ Chunk size looks healthy for Q&A retrieval.")

# #         # Show sample chunks from selected PDF
# #         st.divider()
# #         st.subheader("Sample chunks")
# #         sources = list({
# #             d.metadata.get("source", "unknown")
# #             for d in st.session_state.all_docs
# #         })
# #         if sources:
# #             chosen_src = st.selectbox("Pick a PDF", sources)
# #             src_docs = [
# #                 d for d in st.session_state.all_docs
# #                 if d.metadata.get("source") == chosen_src
# #             ]
# #             n_show = st.slider("Chunks to preview", 1, min(10, len(src_docs)), 3)
# #             for i, doc in enumerate(src_docs[:n_show]):
# #                 st.markdown(f"**Chunk {i+1}** — {len(doc.page_content)} chars")
# #                 st.text_area(
# #                     label="",
# #                     value=doc.page_content,
# #                     height=140,
# #                     key=f"chunk_preview_{chosen_src}_{i}",
# #                     disabled=True,
# #                 )

# # # ════════════════════════════════════════════════════════════════════════════
# # # TAB 3 — HISTORY
# # # ════════════════════════════════════════════════════════════════════════════
# # with tab_history:
# #     st.subheader("💬 Conversation History")

# #     if not st.session_state.chat_history:
# #         st.info("No conversation yet.")
# #     else:
# #         for msg in st.session_state.chat_history:
# #             icon = "🧑" if msg["role"] == "user" else "🤖"
# #             st.markdown(f"**{icon} {msg['role'].capitalize()}:** {msg['content']}")
# #             st.divider()

# #         if st.button("🗑️ Clear history"):
# #             st.session_state.chat_history = []
# #             st.rerun()




# # """
# # 🚀 PRODUCTION-READY STREAMLIT RAG CHATBOT
# # Secure Geo-Spatial and QR-Based Authentication Framework for Last-Mile Postal Delivery

# # IMPROVEMENTS OVER BASIC VERSION:
# # ✅ Advanced Memory Management (Buffer Window + Summary)
# # ✅ Multiple tabs for different features
# # ✅ Document statistics and quality checks
# # ✅ Configurable chunking and retrieval
# # ✅ Better error handling and logging
# # ✅ Performance metrics and timing
# # ✅ Chat history export
# # ✅ Debug mode
# # ✅ Model selection
# # ✅ Caching for speed
# # ✅ Professional UI/UX
# # """

# # import streamlit as st
# # import fitz
# # import os
# # import hashlib
# # import time
# # import json
# # from datetime import datetime
# # from typing import List, Dict, Tuple, Optional
# # from dotenv import load_dotenv

# # from langchain_groq import ChatGroq
# # from langchain_huggingface import HuggingFaceEmbeddings
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain_community.vectorstores import FAISS
# # from langchain_core.prompts import ChatPromptTemplate
# # from langchain.memory import ConversationBufferWindowMemory

# # # ════════════════════════════════════════════════════════════════════════════
# # # CONFIGURATION
# # # ════════════════════════════════════════════════════════════════════════════

# # # Load environment
# # load_dotenv()
# # GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # if not GROQ_API_KEY:
# #     st.error("❌ GROQ_API_KEY not found in .env file")
# #     st.stop()

# # # Page config
# # st.set_page_config(
# #     page_title="RAG Chatbot - Delivery System",
# #     page_icon="📦",
# #     layout="wide",
# #     initial_sidebar_state="expanded"
# # )

# # # ════════════════════════════════════════════════════════════════════════════
# # # CUSTOM STYLES
# # # ════════════════════════════════════════════════════════════════════════════

# # st.markdown("""
# # <style>
# #     .metric-box {
# #         background-color: #f0f2f6;
# #         padding: 15px;
# #         border-radius: 8px;
# #         margin: 10px 0;
# #     }
# #     .success-msg {
# #         background-color: #d4edda;
# #         padding: 12px;
# #         border-radius: 5px;
# #         color: #155724;
# #         border: 1px solid #c3e6cb;
# #         margin: 10px 0;
# #     }
# #     .warning-msg {
# #         background-color: #fff3cd;
# #         padding: 12px;
# #         border-radius: 5px;
# #         color: #856404;
# #         border: 1px solid #ffeaa7;
# #         margin: 10px 0;
# #     }
# # </style>
# # """, unsafe_allow_html=True)

# # # ════════════════════════════════════════════════════════════════════════════
# # # CACHING - LLM & EMBEDDINGS
# # # ════════════════════════════════════════════════════════════════════════════

# # @st.cache_resource
# # def get_llm(model_name: str, temperature: float):
# #     """Get LLM with caching"""
# #     return ChatGroq(
# #         api_key=GROQ_API_KEY,
# #         model_name=model_name,
# #         temperature=temperature
# #     )

# # @st.cache_resource
# # def get_embeddings():
# #     """Get embeddings with caching"""
# #     return HuggingFaceEmbeddings(
# #         # model_name="sentence-transformers/all-MiniLM-L6-v2",
# #         model_name="BAAI/bge-base-en",
# #         model_kwargs={"device": "cpu"},
# #         encode_kwargs={"normalize_embeddings": True}
# #     )

# # # ════════════════════════════════════════════════════════════════════════════
# # # ADVANCED MEMORY CLASS
# # # ════════════════════════════════════════════════════════════════════════════

# # class RAGMemory:
# #     """Advanced memory management for RAG"""
    
# #     def __init__(self, buffer_size: int = 5):
# #         self.buffer_size = buffer_size
# #         self.conversation_memory = ConversationBufferWindowMemory(
# #             k=buffer_size,
# #             memory_key="chat_history",
# #             human_prefix="User",
# #             ai_prefix="Assistant",
# #             input_key="query",
# #             output_key="response"
# #         )
# #         self.token_count = 0
# #         self.interaction_count = 0
    
# #     def add_exchange(self, query: str, response: str):
# #         """Add query-response pair"""
# #         try:
# #             self.conversation_memory.save_context(
# #                 {"query": query},
# #                 {"response": response}
# #             )
# #             self.token_count += len(query.split()) + len(response.split())
# #             self.interaction_count += 1
# #         except Exception as e:
# #             st.warning(f"Memory error: {str(e)}")
    
# #     def get_context(self) -> str:
# #         """Get conversation context"""
# #         try:
# #             return self.conversation_memory.get_buffer()
# #         except:
# #             return ""
    
# #     def get_metrics(self) -> Dict:
# #         """Get memory metrics"""
# #         return {
# #             "tokens": self.token_count,
# #             "interactions": self.interaction_count,
# #             "status": "✅ Healthy" if self.token_count < 5000 else "⚠️ High"
# #         }
    
# #     def reset(self):
# #         """Reset memory"""
# #         self.conversation_memory.clear()
# #         self.token_count = 0
# #         self.interaction_count = 0

# # # ════════════════════════════════════════════════════════════════════════════
# # # PDF PROCESSING FUNCTIONS
# # # ════════════════════════════════════════════════════════════════════════════

# # def extract_text_from_pdf(file_bytes: bytes) -> Tuple[str, int]:
# #     """Extract text from PDF with page tracking"""
# #     try:
# #         doc = fitz.open(stream=file_bytes, filetype="pdf")
# #         pages = []
# #         for i, page in enumerate(doc):
# #             text = page.get_text("text").strip()
# #             if text:
# #                 pages.append(f"[Page {i+1}]\n{text}")
# #         return "\n\n".join(pages), len(doc)
# #     except Exception as e:
# #         st.error(f"❌ PDF extraction failed: {str(e)}")
# #         return "", 0

# # def split_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List:
# #     """Split text into chunks"""
# #     try:
# #         splitter = RecursiveCharacterTextSplitter(
# #             chunk_size=chunk_size,
# #             chunk_overlap=chunk_overlap,
# #             separators=["\n\n", "\n", ". ", " ", ""],
# #             length_function=len,
# #         )
# #         return splitter.create_documents([text])
# #     except Exception as e:
# #         st.error(f"❌ Text splitting failed: {str(e)}")
# #         return []

# # # ════════════════════════════════════════════════════════════════════════════
# # # IMPROVED PROMPT TEMPLATE
# # # ════════════════════════════════════════════════════════════════════════════

# # PROMPT_TEMPLATE = ChatPromptTemplate.from_template("""
# # You are a precise and helpful document Q&A assistant.

# # CRITICAL RULES:
# # 1. Answer ONLY using the provided context
# # 2. If information is not in the context, clearly state: "This information is not found in the documents"
# # 3. For complex questions, combine information from multiple sections
# # 4. Keep responses structured and easy to read
# # 5. Cite sources using [Source Name] format

# # PREVIOUS CONVERSATION (for context continuity):
# # {memory}

# # RETRIEVED DOCUMENTS:
# # {context}

# # USER QUESTION:
# # {input}

# # RESPONSE:
# # """)

# # # ════════════════════════════════════════════════════════════════════════════
# # # SESSION STATE INITIALIZATION
# # # ════════════════════════════════════════════════════════════════════════════

# # def init_session_state():
# #     """Initialize session state variables"""
# #     if "vectorstore" not in st.session_state:
# #         st.session_state.vectorstore = None
# #     if "memory" not in st.session_state:
# #         st.session_state.memory = RAGMemory(buffer_size=5)
# #     if "chat_history" not in st.session_state:
# #         st.session_state.chat_history = []
# #     if "pdf_hashes" not in st.session_state:
# #         st.session_state.pdf_hashes = set()
# #     if "chunk_stats" not in st.session_state:
# #         st.session_state.chunk_stats = {}
# #     if "all_docs" not in st.session_state:
# #         st.session_state.all_docs = []

# # init_session_state()

# # # ════════════════════════════════════════════════════════════════════════════
# # # SIDEBAR CONFIGURATION
# # # ════════════════════════════════════════════════════════════════════════════

# # with st.sidebar:
# #     st.header("⚙️ Settings")
    
# #     # Model selection
# #     st.subheader("🤖 Model Configuration")
# #     model_choice = st.selectbox(
# #         "Select Model",
# #         ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
# #         help="8B = Fast, 70B = Better Quality"
# #     )
# #     temperature = st.slider(
# #         "Temperature",
# #         0.0, 1.0, 0.3, 0.1,
# #         help="Lower = Focused answers, Higher = Creative"
# #     )
    
# #     # Chunking parameters
# #     st.subheader("📑 Document Settings")
# #     chunk_size = st.slider(
# #         "Chunk Size (characters)",
# #         200, 2000, 1000, 100,
# #         help="Recommended: 800-1200"
# #     )
# #     overlap_pct = st.slider(
# #         "Overlap %",
# #         5, 40, 20, 5,
# #         help="Recommended: 15-25%"
# #     )
    
# #     # Retrieval parameters
# #     st.subheader("🔍 Retrieval Settings")
# #     k_retrieve = st.slider(
# #         "Number of chunks to retrieve",
# #         3, 15, 6,
# #         help="More = Broader context"
# #     )
    
# #     # Memory status
# #     st.divider()
# #     st.subheader("💾 Memory Status")
# #     metrics = st.session_state.memory.get_metrics()
# #     col1, col2 = st.columns(2)
# #     col1.metric("Tokens", metrics["tokens"])
# #     col2.metric("Queries", metrics["interactions"])
# #     st.caption(f"Status: {metrics['status']}")
    
# #     if st.button("🔄 Reset Memory", use_container_width=True):
# #         st.session_state.memory.reset()
# #         st.session_state.chat_history = []
# #         st.success("✅ Memory reset!")
# #         st.rerun()
    
# #     # Debug mode
# #     st.divider()
# #     debug_mode = st.checkbox("🐛 Debug Mode")

# # # ════════════════════════════════════════════════════════════════════════════
# # # MAIN APP LAYOUT
# # # ════════════════════════════════════════════════════════════════════════════

# # # Header
# # st.title("📦 RAG Chatbot")
# # st.markdown("*Delivery System Documentation Assistant*")

# # # Tabs
# # tab1, tab2, tab3, tab4 = st.tabs(
# #     ["💬 Chat", "📚 Documents", "📊 Insights", "📜 History"]
# # )

# # # ════════════════════════════════════════════════════════════════════════════
# # # TAB 1: CHAT
# # # ════════════════════════════════════════════════════════════════════════════

# # with tab1:
# #     st.header("Ask Questions About Your Documents")
    
# #     # PDF Upload
# #     col1, col2 = st.columns([4, 1])
# #     with col1:
# #         uploaded_files = st.file_uploader(
# #             "📤 Upload PDF files",
# #             type=["pdf"],
# #             accept_multiple_files=True,
# #             key="pdf_uploader"
# #         )
# #     with col2:
# #         if st.button("Clear All", use_container_width=True):
# #             st.session_state.vectorstore = None
# #             st.session_state.pdf_hashes = set()
# #             st.session_state.chunk_stats = {}
# #             st.session_state.all_docs = []
# #             st.success("✅ Cleared!")
# #             st.rerun()
    
# #     # Process PDFs
# #     if uploaded_files:
# #         new_files = []
# #         for pdf in uploaded_files:
# #             file_hash = hashlib.md5(pdf.getvalue()).hexdigest()
# #             if file_hash not in st.session_state.pdf_hashes:
# #                 new_files.append((pdf, file_hash))
        
# #         if new_files:
# #             progress_bar = st.progress(0)
# #             status_text = st.empty()
            
# #             for idx, (pdf, file_hash) in enumerate(new_files):
# #                 status_text.text(f"Processing {pdf.name}...")
                
# #                 try:
# #                     # Extract and process
# #                     text, num_pages = extract_text_from_pdf(pdf.getvalue())
# #                     if not text:
# #                         continue
                    
# #                     # Calculate actual overlap
# #                     overlap = int(chunk_size * overlap_pct / 100)
# #                     docs = split_text(text, chunk_size, overlap)
                    
# #                     if not docs:
# #                         continue
                    
# #                     # Statistics
# #                     char_counts = [len(d.page_content) for d in docs]
# #                     st.session_state.chunk_stats[pdf.name] = {
# #                         "chunks": len(docs),
# #                         "avg_size": round(sum(char_counts) / len(char_counts)),
# #                         "min_size": min(char_counts),
# #                         "max_size": max(char_counts),
# #                         "total_chars": len(text),
# #                         "pages": num_pages
# #                     }
                    
# #                     # Add to vectorstore
# #                     for doc in docs:
# #                         doc.metadata["source"] = pdf.name
                    
# #                     st.session_state.all_docs.extend(docs)
                    
# #                     if st.session_state.vectorstore is None:
# #                         st.session_state.vectorstore = FAISS.from_documents(
# #                             docs,
# #                             get_embeddings()
# #                         )
# #                     else:
# #                         st.session_state.vectorstore.add_documents(docs)
                    
# #                     st.session_state.pdf_hashes.add(file_hash)
                
# #                 except Exception as e:
# #                     st.error(f"❌ Error processing {pdf.name}: {str(e)}")
                
# #                 progress_bar.progress((idx + 1) / len(new_files))
            
# #             progress_bar.empty()
# #             status_text.empty()
# #             st.success(f"✅ {len(new_files)} file(s) processed!")
    
# #     st.divider()
    
# #     # Chat Interface
# #     if st.session_state.vectorstore is None:
# #         st.info("⬆️ Upload PDFs to start chatting")
    
# #     else:
# #         # Display chat history
# #         for msg in st.session_state.chat_history:
# #             with st.chat_message(msg["role"]):
# #                 st.write(msg["content"])
# #                 if "sources" in msg and msg["sources"]:
# #                     st.caption(f"📎 {', '.join(msg['sources'])}")
        
# #         # User input
# #         query = st.chat_input("Ask a question...")
        
# #         if query:
# #             with st.chat_message("user"):
# #                 st.write(query)
            
# #             with st.spinner("🤔 Analyzing..."):
# #                 try:
# #                     start_time = time.time()
                    
# #                     # Get LLM
# #                     llm = get_llm(model_choice, temperature)
                    
# #                     # Retrieve documents
# #                     retriever = st.session_state.vectorstore.as_retriever(
# #                         search_type="mmr",
# #                         search_kwargs={
# #                             "k": k_retrieve,
# #                             "fetch_k": k_retrieve * 3,
# #                             "lambda_mult": 0.6
# #                         }
# #                     )
# #                     retrieved_docs = retriever.invoke(query)
                    
# #                     # Get similarity scores
# #                     docs_with_scores = st.session_state.vectorstore.similarity_search_with_score(
# #                         query,
# #                         k=min(5, k_retrieve)
# #                     )
                    
# #                     # Build context
# #                     context_parts = []
# #                     sources = set()
# #                     for doc in retrieved_docs:
# #                         src = doc.metadata.get("source", "Unknown")
# #                         sources.add(src)
# #                         context_parts.append(f"[{src}]\n{doc.page_content}")
                    
# #                     context = "\n\n---\n\n".join(context_parts)
                    
# #                     # Get memory context
# #                     memory_context = st.session_state.memory.get_context()
                    
# #                     # Format and generate response
# #                     formatted_prompt = PROMPT_TEMPLATE.format(
# #                         memory=memory_context,
# #                         context=context,
# #                         input=query
# #                     )
                    
# #                     response = llm.invoke(formatted_prompt)
# #                     answer = response.content
                    
# #                     elapsed_time = time.time() - start_time
                    
# #                     # Update memory
# #                     st.session_state.memory.add_exchange(query, answer)
                    
# #                     # Display response
# #                     with st.chat_message("assistant"):
# #                         st.write(answer)
# #                         col1, col2, col3 = st.columns([2, 1, 1])
# #                         with col1:
# #                             st.caption(f"📎 {', '.join(sorted(sources))}")
# #                         with col2:
# #                             st.caption(f"⏱️ {elapsed_time:.2f}s")
# #                         with col3:
# #                             st.caption(f"📄 {len(retrieved_docs)} chunks")
                        
# #                         # Show retrieved chunks
# #                         with st.expander("📋 View Retrieved Chunks"):
# #                             st.write(f"Retrieved {len(docs_with_scores)} relevant chunks")
# #                             for i, (doc, score) in enumerate(docs_with_scores[:5]):
# #                                 with st.container():
# #                                     st.markdown(f"**Chunk {i+1}** (Score: {score:.4f})")
# #                                     st.caption(f"Source: {doc.metadata.get('source')}")
# #                                     st.text(doc.page_content[:400] + "...")
# #                                     st.divider()
                    
# #                     # Store in chat history
# #                     st.session_state.chat_history.append({
# #                         "role": "user",
# #                         "content": query,
# #                         "timestamp": datetime.now().isoformat()
# #                     })
# #                     st.session_state.chat_history.append({
# #                         "role": "assistant",
# #                         "content": answer,
# #                         "sources": sorted(sources),
# #                         "elapsed": elapsed_time,
# #                         "timestamp": datetime.now().isoformat()
# #                     })
                
# #                 except Exception as e:
# #                     st.error(f"❌ Error: {str(e)}")

# # # ════════════════════════════════════════════════════════════════════════════
# # # TAB 2: DOCUMENTS
# # # ════════════════════════════════════════════════════════════════════════════

# # with tab2:
# #     st.header("Document Statistics")
    
# #     if not st.session_state.chunk_stats:
# #         st.info("📄 No documents loaded yet")
# #     else:
# #         # Summary
# #         col1, col2, col3, col4 = st.columns(4)
# #         col1.metric("Files", len(st.session_state.chunk_stats))
# #         col2.metric("Total Chunks", sum(s["chunks"] for s in st.session_state.chunk_stats.values()))
# #         col3.metric("Total Pages", sum(s["pages"] for s in st.session_state.chunk_stats.values()))
# #         col4.metric("Total Size", f"{sum(s['total_chars'] for s in st.session_state.chunk_stats.values()) // 1000}KB")
        
# #         st.divider()
        
# #         # Per-document details
# #         for fname, stats in st.session_state.chunk_stats.items():
# #             with st.expander(f"📄 {fname}"):
# #                 col1, col2, col3, col4, col5 = st.columns(5)
# #                 col1.metric("Chunks", stats["chunks"])
# #                 col2.metric("Avg Size", f"{stats['avg_size']} chars")
# #                 col3.metric("Min", f"{stats['min_size']} chars")
# #                 col4.metric("Max", f"{stats['max_size']} chars")
# #                 col5.metric("Pages", stats["pages"])
                
# #                 # Quality check
# #                 avg = stats['avg_size']
# #                 if avg < 300:
# #                     st.warning("⚠️ Chunks are small")
# #                 elif avg > 1500:
# #                     st.warning("⚠️ Chunks are large")
# #                 else:
# #                     st.success("✅ Optimal chunk size")

# # # ════════════════════════════════════════════════════════════════════════════
# # # TAB 3: INSIGHTS
# # # ════════════════════════════════════════════════════════════════════════════

# # with tab3:
# #     st.header("Model Performance Insights")
    
# #     st.info("""
# #     ### Quick Health Check
# #     - **Accuracy**: How well model answers (target: >75%)
# #     - **Hallucination**: False info generated (target: <10%)
# #     - **Speed**: Response time (target: <2s)
# #     - **Memory**: Token usage (target: <700/query)
# #     """)
    
# #     # Memory health
# #     metrics = st.session_state.memory.get_metrics()
# #     col1, col2, col3 = st.columns(3)
# #     col1.metric("Total Tokens", metrics["tokens"])
# #     col2.metric("Interactions", metrics["interactions"])
# #     col3.write(f"**Status**: {metrics['status']}")
    
# #     if metrics['tokens'] > 5000:
# #         st.error("⚠️ High token usage - Consider resetting")
# #     elif metrics['tokens'] > 3000:
# #         st.warning("⚠️ Moderate usage - Monitor for long sessions")
# #     else:
# #         st.success("✅ Memory usage is optimal")

# # # ════════════════════════════════════════════════════════════════════════════
# # # TAB 4: HISTORY
# # # ════════════════════════════════════════════════════════════════════════════

# # with tab4:
# #     st.header("Conversation History")
    
# #     if not st.session_state.chat_history:
# #         st.info("💬 No conversation yet")
# #     else:
# #         # Summary
# #         user_msgs = sum(1 for m in st.session_state.chat_history if m["role"] == "user")
# #         assist_msgs = sum(1 for m in st.session_state.chat_history if m["role"] == "assistant")
        
# #         col1, col2, col3 = st.columns(3)
# #         col1.metric("User Messages", user_msgs)
# #         col2.metric("Assistant Responses", assist_msgs)
# #         col3.metric("Total Exchanges", user_msgs)
        
# #         st.divider()
        
# #         # Display history
# #         for msg in st.session_state.chat_history:
# #             with st.container():
# #                 role_icon = "🧑" if msg["role"] == "user" else "🤖"
# #                 st.markdown(f"**{role_icon} {msg['role'].upper()}**")
# #                 st.write(msg["content"][:200] + "..." if len(msg["content"]) > 200 else msg["content"])
                
# #                 if msg["role"] == "assistant" and "sources" in msg:
# #                     st.caption(f"📎 {', '.join(msg['sources'])}")
# #                 if "elapsed" in msg:
# #                     st.caption(f"⏱️ {msg['elapsed']:.2f}s")
                
# #                 st.divider()
        
# #         # Export button
# #         if st.button("📥 Export as JSON"):
# #             json_data = json.dumps(st.session_state.chat_history, indent=2, default=str)
# #             st.download_button(
# #                 "Download JSON",
# #                 json_data,
# #                 f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
# #                 "application/json"
# #             )

# # # ════════════════════════════════════════════════════════════════════════════
# # # DEBUG PANEL
# # # ════════════════════════════════════════════════════════════════════════════

# # if debug_mode:
# #     st.divider()
# #     with st.expander("🐛 Debug Information"):
# #         col1, col2 = st.columns(2)
# #         with col1:
# #             st.json({
# #                 "vectorstore": "Loaded" if st.session_state.vectorstore else "None",
# #                 "total_docs": len(st.session_state.all_docs),
# #                 "pdfs": len(st.session_state.pdf_hashes),
# #                 "history": len(st.session_state.chat_history)
# #             })
# #         with col2:
# #             st.json({
# #                 "model": model_choice,
# #                 "temperature": temperature,
# #                 "chunk_size": chunk_size,
# #                 "overlap": overlap_pct,
# #                 "k_retrieve": k_retrieve
# #             })

# # # ════════════════════════════════════════════════════════════════════════════
# # # FOOTER
# # # ════════════════════════════════════════════════════════════════════════════

# # st.divider()
# # st.markdown("""
# # <div style='text-align: center; color: #888; font-size: 12px;'>
# # ✨ Advanced RAG System with Optimized Memory Management<br>
# # 🚀 Production-Ready Implementation<br>
# # 📦 Secure Delivery Authentication Framework
# # </div>
# # """, unsafe_allow_html=True)










# # import streamlit as st
# # import fitz
# # import os
# # import hashlib
# # from datetime import datetime
# # from typing import List, Dict, Tuple
# # from dotenv import load_dotenv

# # from langchain_groq import ChatGroq
# # from langchain_huggingface import HuggingFaceEmbeddings
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain_community.vectorstores import FAISS
# # from langchain_core.prompts import ChatPromptTemplate
# # from langchain_classic.memory import (
# #     ConversationBufferWindowMemory,
# #     ConversationSummaryMemory
# # )

# # # ════════════════════════════════════════════════════════════════════════════
# # # LOAD ENV & CONFIG
# # # ════════════════════════════════════════════════════════════════════════════
# # load_dotenv()
# # groq_api_key = os.getenv("GROQ_API_KEY")

# # if not groq_api_key:
# #     st.error("❌ GROQ_API_KEY not found in .env file")
# #     st.stop()

# # # ════════════════════════════════════════════════════════════════════════════
# # # OPTIMIZED LLM & EMBEDDINGS (cached)
# # # ════════════════════════════════════════════════════════════════════════════
# # @st.cache_resource
# # def get_llm(model_name: str, temperature: float):
# #     return ChatGroq(
# #         api_key=groq_api_key,
# #         model_name=model_name,
# #         temperature=temperature
# #     )

# # @st.cache_resource
# # def get_embeddings(model_name: str):
# #     return HuggingFaceEmbeddings(
# #         model_name=model_name,
# #         model_kwargs={"device": "cpu"},
# #         encode_kwargs={"normalize_embeddings": True}
# #     )

# # # ════════════════════════════════════════════════════════════════════════════
# # # IMPROVED MEMORY MANAGEMENT
# # # ════════════════════════════════════════════════════════════════════════════
# # class OptimizedRAGMemory:
# #     """Hybrid memory system for RAG"""
    
# #     def __init__(self, llm):
# #         # Short-term: Keep last 5 exchanges for immediate context
# #         self.conversation_memory = ConversationBufferWindowMemory(
# #             k=5,
# #             memory_key="chat_history",
# #             human_prefix="User",
# #             ai_prefix="Assistant",
# #             input_key="query",
# #             output_key="response"
# #         )
        
# #         # Long-term: Summarize older conversations
# #         self.summary_memory = ConversationSummaryMemory(
# #             llm=llm,
# #             memory_key="summary"
# #         )
        
# #         # Document context: Keep last 3 retrievals
# #         self.document_memory = ConversationBufferWindowMemory(
# #             k=3,
# #             memory_key="document_context",
# #             human_prefix="Query",
# #             ai_prefix="Documents"
# #         )
        
# #         self.token_count = 0
# #         self.interaction_count = 0
    
# #     def add_exchange(self, query: str, response: str, documents: List[str]):
# #         """Add query, response, and retrieved documents to memory"""
# #         try:
# #             # Add to conversation memory
# #             self.conversation_memory.save_context(
# #                 {"query": query},
# #                 {"response": response}
# #             )
            
# #             # Add to document memory
# #             if documents:
# #                 self.document_memory.save_context(
# #                     {"query": query},
# #                     {"response": "\n---\n".join(documents[:2])}  # Keep 2 docs max
# #                 )
            
# #             # Count tokens (rough estimate)
# #             self.token_count += len(query.split()) + len(response.split())
# #             self.interaction_count += 1
            
# #             # Update summary if conversation gets long
# #             if self.interaction_count % 5 == 0 and self.token_count > 2000:
# #                 self.summary_memory.buffer = self.conversation_memory.get_buffer()
        
# #         except Exception as e:
# #             st.warning(f"⚠️ Memory save error: {str(e)}")
    
# #     def get_conversation_context(self) -> str:
# #         """Get recent conversation history"""
# #         try:
# #             return self.conversation_memory.get_buffer()
# #         except:
# #             return ""
    
# #     def get_full_context(self) -> str:
# #         """Get all available context"""
# #         contexts = []
        
# #         # Recent conversation
# #         conv = self.get_conversation_context()
# #         if conv:
# #             contexts.append(f"Recent Conversation:\n{conv}")
        
# #         # Document context
# #         try:
# #             doc_context = self.document_memory.get_buffer()
# #             if doc_context:
# #                 contexts.append(f"\nRecent Documents:\n{doc_context}")
# #         except:
# #             pass
        
# #         # Summary (if available)
# #         if self.summary_memory.buffer and self.summary_memory.buffer != "":
# #             contexts.append(f"\nConversation Summary:\n{self.summary_memory.buffer}")
        
# #         return "\n".join(contexts)
    
# #     def get_metrics(self) -> Dict:
# #         """Get memory metrics"""
# #         return {
# #             "token_count": self.token_count,
# #             "interactions": self.interaction_count,
# #             "status": "✅ Healthy" if self.token_count < 5000 else "⚠️ High"
# #         }
    
# #     def reset(self):
# #         """Reset all memory"""
# #         self.conversation_memory.clear()
# #         self.summary_memory.clear()
# #         self.document_memory.clear()
# #         self.token_count = 0
# #         self.interaction_count = 0

# # # ════════════════════════════════════════════════════════════════════════════
# # # PDF PROCESSING
# # # ════════════════════════════════════════════════════════════════════════════
# # def extract_text_from_pdf(file_bytes: bytes) -> str:
# #     """Extract text from PDF with page tracking"""
# #     doc = fitz.open(stream=file_bytes, filetype="pdf")
# #     pages = []
    
# #     for i, page in enumerate(doc):
# #         text = page.get_text("text").strip()
# #         if text:
# #             pages.append(f"[Page {i+1}]\n{text}")
    
# #     return "\n\n".join(pages)

# # def split_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200):
# #     """Split text with configurable parameters"""
# #     splitter = RecursiveCharacterTextSplitter(
# #         chunk_size=chunk_size,
# #         chunk_overlap=chunk_overlap,
# #         separators=["\n\n", "\n", ". ", " ", ""],
# #         length_function=len,
# #     )
# #     return splitter.create_documents([text])

# # # ════════════════════════════════════════════════════════════════════════════
# # # PAGE CONFIG
# # # ════════════════════════════════════════════════════════════════════════════
# # st.set_page_config(
# #     page_title="📄 Multi-PDF RAG Chatbot (Optimized)",
# #     layout="wide",
# #     initial_sidebar_state="expanded"
# # )

# # st.title("📄 Multi-PDF RAG Chatbot")
# # st.markdown("*Enhanced with Optimized Memory & Evaluation*")

# # # ════════════════════════════════════════════════════════════════════════════
# # # SIDEBAR: CONFIGURATION
# # # ════════════════════════════════════════════════════════════════════════════
# # with st.sidebar:
# #     st.header("⚙️ Configuration")
    
# #     # Memory Settings
# #     st.subheader("💾 Memory Settings")
# #     memory_window = st.slider(
# #         "Keep last N conversations",
# #         min_value=3,
# #         max_value=10,
# #         value=5,
# #         help="How many recent exchanges to keep in memory"
# #     )
    
# #     # Chunking Settings
# #     st.subheader("📑 Chunking Settings")
# #     chunk_size = st.slider(
# #         "Chunk size (chars)",
# #         min_value=200,
# #         max_value=2000,
# #         value=1000,
# #         step=100,
# #         help="Optimal: 800-1200 for most documents"
# #     )
# #     overlap_pct = st.slider(
# #         "Overlap %",
# #         min_value=5,
# #         max_value=40,
# #         value=20,
# #         step=5,
# #         help="Optimal: 15-25%"
# #     )
# #     overlap = int(chunk_size * overlap_pct / 100)
    
# #     # Retrieval Settings
# #     st.subheader("🔍 Retrieval Settings")
# #     k_retrieve = st.slider(
# #         "Chunks to retrieve",
# #         min_value=3,
# #         max_value=15,
# #         value=6,
# #         help="More chunks = broader context, slower"
# #     )
    
# #     # Model Settings
# #     st.subheader("🤖 Model Settings")
# #     model_name = st.selectbox(
# #         "Model",
# #         ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
# #     )

# #     st.subheader("🤖 Embedding Model")
# #     embedding_model = st.selectbox(
# #         "Embedding Model",
# #         [
# #             "sentence-transformers/all-MiniLM-L6-v2",
# #             "BAAI/bge-small-en-v1.5",
# #             "BAAI/bge-base-en-v1.5"
# #         ]   
# #     )

# #     temperature = st.slider(
# #         "Temperature",
# #         min_value=0.0,
# #         max_value=1.0,
# #         value=0.3,
# #         step=0.1,
# #         help="Lower = more focused, Higher = more creative"
# #     )
    
# #     # Divider
# #     st.divider()
    
# #     # Memory Status
# #     st.subheader("📊 Memory Status")
# #     if "memory" in st.session_state:
# #         metrics = st.session_state.memory.get_metrics()
# #         col1, col2 = st.columns(2)
# #         col1.metric("Tokens", metrics["token_count"])
# #         col2.metric("Interactions", metrics["interactions"])
# #         st.caption(f"Status: {metrics['status']}")
        
# #         if st.button("🔄 Reset Memory"):
# #             st.session_state.memory.reset()
# #             # st.rerun()
    
# #     # Debug Mode
# #     st.divider()
# #     st.subheader("🐛 Debug")
# #     debug_mode = st.checkbox("Enable debug info")
# # # 🔥 EMBEDDING MODEL CHANGE DETECTION (ADD HERE)
# # if "last_embedding_model" not in st.session_state:
# #     st.session_state.last_embedding_model = None

# # if st.session_state.last_embedding_model != embedding_model:
# #     st.warning("⚠️ Embedding model changed → Vectorstore will reset")

# #     st.session_state.vectorstore = None
# #     st.session_state.pdf_hashes = set()
# #     st.session_state.all_docs = []
# #     st.session_state.last_embedding_model = embedding_model
# # # ════════════════════════════════════════════════════════════════════════════
# # # SESSION STATE INITIALIZATION
# # # ════════════════════════════════════════════════════════════════════════════
# # if "vectorstore" not in st.session_state:
# #     st.session_state.vectorstore = None
# # if "pdf_hashes" not in st.session_state:
# #     st.session_state.pdf_hashes = set()
# # if "chunk_stats" not in st.session_state:
# #     st.session_state.chunk_stats = {}
# # if "all_docs" not in st.session_state:
# #     st.session_state.all_docs = []


# # # st.write("MEMORY EXISTS:", "memory" in st.session_state)
# # # st.write("WINDOW:", st.session_state.get("memory_window"))
# # # st.write("CURRENT:", memory_window)
# # # Initialize memory (with updated window size)
# # if "memory" not in st.session_state or st.session_state.get("memory_window") != memory_window:
# #     # st.write("🚨 MEMORY RECREATED")
# #     llm_for_memory = get_llm(model_name, temperature)
# #     st.session_state.memory = OptimizedRAGMemory(llm_for_memory)
# #     st.session_state.memory_window = memory_window

# # # ════════════════════════════════════════════════════════════════════════════
# # # TABS: CHAT, DOCUMENTS, EVALUATION, SETTINGS
# # # ════════════════════════════════════════════════════════════════════════════
# # tab_chat, tab_documents, tab_evaluation, tab_debug = st.tabs(
# #     ["💬 Chat", "📚 Documents", "📊 Evaluation", "🔧 Debug"]
# # )

# # # ════════════════════════════════════════════════════════════════════════════
# # # TAB 1: CHAT
# # # ════════════════════════════════════════════════════════════════════════════
# # with tab_chat:
    
# #     # PDF Upload Section
# #     uploaded_files = st.file_uploader(
# #         "📤 Upload PDF files",
# #         type=["pdf"],
# #         accept_multiple_files=True,
# #         key="pdf_uploader",
# #     )
    
# #     if uploaded_files:
# #         # Process new files only
# #         new_files = []
# #         for pdf in uploaded_files:
# #             h = hashlib.md5(pdf.getvalue()).hexdigest()
# #             if h not in st.session_state.pdf_hashes:
# #                 new_files.append((pdf, h))
        
# #         if new_files:
# #             progress_bar = st.progress(0)
# #             for idx, (pdf, h) in enumerate(new_files):
# #                 with st.spinner(f"Processing {pdf.name}..."):
# #                     text = extract_text_from_pdf(pdf.getvalue())
# #                     docs = split_text(text, chunk_size, overlap)
                    
# #                     # Track stats
# #                     char_counts = [len(d.page_content) for d in docs]
# #                     st.session_state.chunk_stats[pdf.name] = {
# #                         "n_chunks": len(docs),
# #                         "avg_chars": round(sum(char_counts) / max(len(char_counts), 1)),
# #                         "total_chars": len(text),
# #                     }
                    
# #                     # Add metadata
# #                     for doc in docs:
# #                         doc.metadata["source"] = pdf.name
# #                     st.session_state.all_docs.extend(docs)
                    
# #                     # Create/update vectorstore
# #                     if st.session_state.vectorstore is None:
# #                         st.session_state.vectorstore = FAISS.from_documents(
# #                             docs, get_embeddings(embedding_model)
# #                         )
# #                     else:
# #                         st.session_state.vectorstore.add_documents(docs)
                    
# #                     st.session_state.pdf_hashes.add(h)
                
# #                 progress_bar.progress((idx + 1) / len(new_files))
            
# #             st.success(f"✅ {len(new_files)} PDF(s) indexed")
    
# #     # Chat Interface
# #     if st.session_state.vectorstore is not None:
        
# #         # Display chat history
# #         for msg in st.session_state.get("chat_history", []):
# #             with st.chat_message(msg["role"]):
# #                 st.write(msg["content"])
# #                 if "sources" in msg:
# #                     st.caption(f"📎 {', '.join(msg['sources'])}")
        
# #         # User input
# #         query = st.chat_input("Ask a question about your documents...")
        
# #         if query:
# #             # Display user message
# #             with st.chat_message("user"):
# #                 st.write(query)
            
# #             # Generate response
# #             with st.spinner("🤔 Thinking..."):
# #                 llm = get_llm(model_name, temperature)
                
# #                 # Retrieve documents
# #                 retriever = st.session_state.vectorstore.as_retriever(
# #                     search_type="mmr",
# #                     search_kwargs={
# #                         "k": k_retrieve,
# #                         "fetch_k": k_retrieve * 3,
# #                         "lambda_mult": 0.6,
# #                     },
# #                 )
# #                 retrieved_docs = retriever.invoke(query)
                
# #                 # Build context
# #                 context_parts = []
# #                 sources = set()
# #                 for doc in retrieved_docs:
# #                     src = doc.metadata.get("source", "unknown")
# #                     sources.add(src)
# #                     context_parts.append(f"[{src}]\n{doc.page_content}")
                
# #                 context = "\n\n---\n\n".join(context_parts)
                
# #                 # Get conversation context
# #                 conv_context = st.session_state.memory.get_conversation_context()
                
# #                 # Enhanced prompt with memory
# #                 prompt = ChatPromptTemplate.from_template("""
# # You are a precise document Q&A assistant.

# # PREVIOUS CONTEXT:
# # {conversation_context}

# # RETRIEVED DOCUMENTS:
# # {context}

# # USER QUESTION:
# # {input}

# # INSTRUCTIONS:
# # - Answer ONLY from the provided documents
# # - Cite sources using [SourceName]
# # - If information not found, say clearly: "This information is not found in the documents"
# # - Be concise and structured
# # - Reference previous context when relevant
# # """)
                
# #                 formatted_prompt = prompt.format(
# #                     conversation_context=conv_context,
# #                     context=context,
# #                     input=query
# #                 )
                
# #                 # Generate response
# #                 response = llm.invoke(formatted_prompt)
# #                 answer = response.content
                
# #                 st.write("🔥 Before:", st.session_state.memory.get_metrics())
# #                 # Update memory
# #                 st.session_state.memory.add_exchange(
# #                     query,
# #                     answer,
# #                     [doc.page_content[:200] for doc in retrieved_docs[:3]]
# #                 )
# #                 st.session_state._force_refresh = True
# #                 st.write("🔥 after:", st.session_state.memory.get_metrics())
# #                 # Display response
# #                 with st.chat_message("assistant"):
# #                     st.write(answer)
# #                     st.caption(f"📎 Sources: {', '.join(sorted(sources))}")
                    
# #                     # Show retrieved chunks in expander
# #                     with st.expander("📑 Retrieved Chunks"):
# #                         for i, doc in enumerate(retrieved_docs[:3]):
# #                             st.markdown(f"**Chunk {i+1}** - `{doc.metadata.get('source')}`")
# #                             st.text(doc.page_content[:300] + "...")
# #                             st.divider()
                
# #                 # Update chat history
# #                 if "chat_history" not in st.session_state:
# #                     st.session_state.chat_history = []
                
# #                 st.session_state.chat_history.append({
# #                     "role": "user",
# #                     "content": query
# #                 })
# #                 st.session_state.chat_history.append({
# #                     "role": "assistant",
# #                     "content": answer,
# #                     "sources": sorted(sources)
# #                 })

# #                 # st.rerun()
# #     else:
# #         st.info("⬆️ Upload PDF files to start chatting")

# # # ════════════════════════════════════════════════════════════════════════════
# # # TAB 2: DOCUMENTS
# # # ════════════════════════════════════════════════════════════════════════════
# # with tab_documents:
# #     if st.session_state.chunk_stats:
# #         st.subheader("📊 Document Statistics")
        
# #         col1, col2, col3 = st.columns(3)
# #         col1.metric("Files Loaded", len(st.session_state.chunk_stats))
# #         col2.metric("Total Chunks", sum(s["n_chunks"] for s in st.session_state.chunk_stats.values()))
# #         col3.metric("Total Size", f"{sum(s['total_chars'] for s in st.session_state.chunk_stats.values()):,} chars")
        
# #         st.divider()
        
# #         for fname, stats in st.session_state.chunk_stats.items():
# #             with st.expander(f"📄 {fname}"):
# #                 col1, col2, col3, col4 = st.columns(4)
# #                 col1.metric("Chunks", stats["n_chunks"])
# #                 col2.metric("Avg Size", f"{stats['avg_chars']} chars")
# #                 col3.metric("Total Size", f"{stats['total_chars']:,} chars")
                
# #                 # Quality check
# #                 if stats['avg_chars'] < 300:
# #                     st.warning("⚠️ Chunks are small. Increasing size may improve context.")
# #                 elif stats['avg_chars'] > 1500:
# #                     st.warning("⚠️ Chunks are large. Decreasing size may improve precision.")
# #                 else:
# #                     st.success("✅ Chunk size is optimal")
    
# #     else:
# #         st.info("No documents loaded yet")

# # # ════════════════════════════════════════════════════════════════════════════
# # # TAB 3: EVALUATION
# # # ════════════════════════════════════════════════════════════════════════════
# # with tab_evaluation:
# #     st.subheader("📊 Model Evaluation")
    
# #     st.info("""
# #     This tab shows information about evaluating your RAG model.
    
# #     To evaluate your model:
# #     1. Run the `rag_evaluation_framework.py` file
# #     2. It will test 12 questions from the PDF
# #     3. Generate a health report
# #     """)
    
# #     # Show test questions
# #     st.subheader("Test Questions Available:")
# #     st.write("""
# #     - **Easy** (3 questions): Basic system overview
# #     - **Medium** (6 questions): Architecture and features
# #     - **Hard** (3 questions): Technical implementation
    
# #     Run evaluation to check:
# #     ✓ Overall accuracy (target: >75%)
# #     ✓ Hallucination rate (target: <10%)
# #     ✓ Performance by category
# #     """)
    
# #     # Memory health check
# #     memory = st.session_state.get("memory", None)
# #     if memory:
# #         st.subheader("💾 Memory Health")
# #         metrics =memory.get_metrics()
        
# #         col1, col2, col3 = st.columns(3)
# #         col1.metric("Token Count", metrics["token_count"])
# #         col2.metric("Interactions", metrics["interactions"])
# #         col3.write(f"Status: {metrics['status']}")
        
# #         # Health warnings
# #         if metrics['token_count'] > 5000:
# #             st.warning("⚠️ High token usage - consider using smaller context window")
# #         elif metrics['token_count'] > 3000:
# #             st.info("ℹ️ Moderate token usage - monitor for long sessions")
# #         else:
# #             st.success("✅ Memory usage is optimal")

# # # ════════════════════════════════════════════════════════════════════════════
# # # TAB 4: DEBUG
# # # ════════════════════════════════════════════════════════════════════════════
# # with tab_debug:
# #     if debug_mode or st.checkbox("Show debug info"):
# #         st.subheader("🐛 Debug Information")
        
# #         # Memory content
# #         if "memory" in st.session_state:
# #             st.subheader("📝 Memory Content")
            
# #             conv = st.session_state.memory.get_conversation_context()
# #             if conv:
# #                 st.text_area(
# #                     "Recent Conversation Memory:",
# #                     value=conv,
# #                     height=200,
# #                     disabled=True
# #                 )
            
# #             # Session state
# #             st.subheader("📦 Session State")
# #             st.json({
# #                 "vectorstore": "Loaded" if st.session_state.vectorstore else "None",
# #                 "pdfs_loaded": len(st.session_state.pdf_hashes),
# #                 "total_chunks": len(st.session_state.all_docs),
# #                 "chat_history": len(st.session_state.get("chat_history", [])),
# #                 "memory_metrics": st.session_state.memory.get_metrics()
# #             })

# # # ════════════════════════════════════════════════════════════════════════════
# # # FOOTER
# # # ════════════════════════════════════════════════════════════════════════════
# # st.divider()
# # st.markdown("""
# # <div style='text-align: center; color: #888; font-size: 12px;'>
# #     ✨ Enhanced with Optimized Memory (ConversationBufferWindow + ConversationSummary)
# #     <br>
# #     📊 Ready for evaluation with rag_evaluation_framework.py
# # </div>
# # """, unsafe_allow_html=True)









# this is need to b checked a bit...

# import streamlit as st
# import fitz
# import os
# import hashlib
# import time
# from typing import List, Tuple, Optional
# from dotenv import load_dotenv

# from langchain_groq import ChatGroq
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory

# from rag_evaluation_framework import RAGEvaluator, score_to_label, health_to_label

# # ════════════════════════════════════════════════════════
# # SETUP
# # ════════════════════════════════════════════════════════

# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# FAISS_INDEX_PATH = "./faiss_index"

# if not GROQ_API_KEY:
#     st.error("❌ GROQ_API_KEY not found in .env file")
#     st.stop()

# st.set_page_config(
#     page_title="RAG Chatbot",
#     page_icon="📦",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ════════════════════════════════════════════════════════
# # MEMORY CLASS
# # ════════════════════════════════════════════════════════

# class DualRAGMemory:
#     """Buffer memory + summary memory, both injected into prompt."""

#     def __init__(self, buffer_size: int = 5, llm=None):
#         self.buffer_size = buffer_size
#         self.buffer = ConversationBufferWindowMemory(
#             k=buffer_size,
#             memory_key="chat_history",
#             human_prefix="User",
#             ai_prefix="Assistant",
#             input_key="query",
#             output_key="response"
#         )
#         self.summary_memory = None
#         self.token_count = 0
#         self.interaction_count = 0
#         if llm:
#             try:
#                 self.summary_memory = ConversationSummaryMemory(
#                     llm=llm,
#                     memory_key="summary",
#                     human_prefix="User",
#                     ai_prefix="Assistant",
#                     input_key="query",
#                     output_key="response"
#                 )
#             except Exception:
#                 self.summary_memory = None

#     def add_exchange(self, query: str, response: str):
#         try:
#             self.buffer.save_context({"query": query}, {"response": response})
#             if self.summary_memory:
#                 self.summary_memory.save_context({"query": query}, {"response": response})
#             self.token_count += len(query.split()) + len(response.split())
#             self.interaction_count += 1
#         except Exception:
#             pass

#     def get_recent(self) -> str:
#         try:
#             return self.buffer.buffer or ""
#         except Exception:
#             return ""

#     def get_summary(self) -> str:
#         try:
#             if self.summary_memory:
#                 return self.summary_memory.buffer or ""
#         except Exception:
#             pass
#         return ""

#     def get_status(self) -> str:
#         return "✅ Healthy" if self.token_count < 5000 else "⚠️ High"

#     def reset(self):
#         self.buffer.clear()
#         if self.summary_memory:
#             try:
#                 self.summary_memory.clear()
#             except Exception:
#                 pass
#         self.token_count = 0
#         self.interaction_count = 0

# # ════════════════════════════════════════════════════════
# # CACHED RESOURCES
# # ════════════════════════════════════════════════════════

# @st.cache_resource
# def get_llm(model_name: str, temperature: float):
#     return ChatGroq(api_key=GROQ_API_KEY, model_name=model_name, temperature=temperature)

# @st.cache_resource
# def get_embeddings(model_name: str = "BAAI/bge-base-en-v1.5"):
#     return HuggingFaceEmbeddings(
#         model_name=model_name,
#         model_kwargs={"device": "cpu"},
#         encode_kwargs={"normalize_embeddings": True}
#     )

# # ════════════════════════════════════════════════════════
# # PDF PROCESSING
# # ════════════════════════════════════════════════════════

# def extract_text_from_pdf(file_bytes: bytes, filename: str) -> Tuple[List, int]:
#     """Extract text with page-level metadata."""
#     try:
#         doc = fitz.open(stream=file_bytes, filetype="pdf")
#         page_docs = []
#         for i, page in enumerate(doc):
#             text = page.get_text("text").strip()
#             if text:
#                 page_docs.append({"text": text, "page": i + 1, "source": filename})
#         return page_docs, len(doc)
#     except Exception as e:
#         st.error(f"❌ PDF error: {e}")
#         return [], 0

# def split_text_with_pages(page_docs: list, chunk_size: int = 1000, overlap: int = 200):
#     """Split with page metadata preserved per chunk."""
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=overlap,
#         separators=["\n\n", "\n", ". ", " ", ""]
#     )
#     all_chunks = []
#     for page_doc in page_docs:
#         chunks = splitter.create_documents([page_doc["text"]])
#         for chunk in chunks:
#             chunk.metadata["source"] = page_doc["source"]
#             chunk.metadata["page"] = page_doc["page"]
#         all_chunks.extend(chunks)
#     return all_chunks

# # ════════════════════════════════════════════════════════
# # ADAPTIVE RETRIEVAL
# # ════════════════════════════════════════════════════════

# COMPLEX_KEYWORDS = [
#     "compare", "difference", "explain", "analyze", "how does", "why does",
#     "summarize", "describe", "elaborate", "relationship", "architecture",
#     "workflow", "process", "mechanism", "contrast", "evaluate", "assess"
# ]

# def get_adaptive_k(query: str, base_k: int) -> int:
#     """Return fewer chunks for simple queries, more for complex ones."""
#     q = query.lower()
#     is_complex = len(query.split()) > 12 or any(kw in q for kw in COMPLEX_KEYWORDS)
#     return base_k if is_complex else max(3, base_k // 2)

# # ════════════════════════════════════════════════════════
# # FAISS PERSISTENCE
# # ════════════════════════════════════════════════════════

# def save_faiss(vectorstore, embedding_model: str):
#     """Persist FAISS index and record which embedding model built it."""
#     try:
#         vectorstore.save_local(FAISS_INDEX_PATH)
#         with open(f"{FAISS_INDEX_PATH}/embedding_model.txt", "w") as f:
#             f.write(embedding_model)
#     except Exception as e:
#         st.warning(f"⚠️ Could not save FAISS index: {e}")

# def load_faiss(embeddings, embedding_model: str) -> Optional[object]:
#     """Load persisted FAISS index if embedding model matches."""
#     model_file = f"{FAISS_INDEX_PATH}/embedding_model.txt"
#     index_file = f"{FAISS_INDEX_PATH}/index.faiss"
#     if not (os.path.exists(index_file) and os.path.exists(model_file)):
#         return None
#     try:
#         saved_model = open(model_file).read().strip()
#         if saved_model != embedding_model:
#             return None  # Model mismatch — must rebuild
#         return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
#     except Exception:
#         return None

# # ════════════════════════════════════════════════════════
# # PROMPT
# # ════════════════════════════════════════════════════════

# SYSTEM_PROMPT = ChatPromptTemplate.from_template("""You are a strict document-based question answering assistant.

# CONVERSATION SUMMARY (for context):
# {conversation_summary}

# RECENT EXCHANGES:
# {recent_history}

# RETRIEVED DOCUMENTS:
# {context}

# QUESTION:
# {input}

# INSTRUCTIONS:
# 1. Answer ONLY using information explicitly present in the retrieved documents above.
# 2. Do NOT use prior knowledge, training data, or external information.
# 3. Do NOT speculate, guess, or invent details not in the documents.
# 4. If partially supported: provide only the supported part, then state "The remaining information is not available in the provided documents."
# 5. If not supported at all: respond ONLY "This information is not available in the provided documents."
# 6. Cite sources using: [filename | Page N] after every factual claim.
# 7. Keep answers concise and accurate.
# 8. Prefer accuracy over completeness.

# FINAL ANSWER:""")

# # ════════════════════════════════════════════════════════
# # SESSION STATE
# # ════════════════════════════════════════════════════════

# EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"

# def init_session():
#     defaults = {
#         "vectorstore": None,
#         "chat_history": [],
#         "pdf_hashes": set(),
#         "chunk_info": {},
#         "last_processed_query": None,
#         "eval_results": None,
#         "interaction_log": [],   # Stores {question, answer, retrieved_docs} for eval
#         "faiss_loaded": False,
#     }
#     for k, v in defaults.items():
#         if k not in st.session_state:
#             st.session_state[k] = v

# init_session()

# # ════════════════════════════════════════════════════════
# # SIDEBAR
# # ════════════════════════════════════════════════════════

# with st.sidebar:
#     st.header("⚙️ Configuration")

#     st.subheader("🤖 Model Settings")
#     model_choice = st.selectbox(
#         "LLM Model",
#         ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
#         help="8B = Fast, 70B = Better Quality"
#     )
#     temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)

#     st.subheader("📑 Document Settings")
#     chunk_size = st.slider("Chunk Size", 200, 2000, 1000, 100)
#     overlap_pct = st.slider("Overlap %", 5, 40, 20, 5)

#     st.subheader("🔍 Retrieval")
#     k_retrieve = st.slider("Chunks to Retrieve", 3, 15, 6)

#     st.subheader("💾 Memory")
#     memory_window = st.slider("Memory Window (exchanges)", 2, 10, 5)

#     # Initialize or update memory if window size changes
#     if "memory" not in st.session_state:
#         llm_for_memory = get_llm(model_choice, temperature)
#         st.session_state.memory = DualRAGMemory(buffer_size=memory_window, llm=llm_for_memory)
#     elif st.session_state.memory.buffer_size != memory_window:
#         old = st.session_state.memory
#         llm_for_memory = get_llm(model_choice, temperature)
#         st.session_state.memory = DualRAGMemory(buffer_size=memory_window, llm=llm_for_memory)
#         st.session_state.memory.token_count = old.token_count
#         st.session_state.memory.interaction_count = old.interaction_count

#     st.caption(f"Status: {st.session_state.memory.get_status()}")
#     st.caption(f"Tokens: {st.session_state.memory.token_count}")
#     st.caption(f"Exchanges: {st.session_state.memory.interaction_count}")

#     if st.button("🔄 Reset All", use_container_width=True):
#         st.session_state.memory.reset()
#         st.session_state.chat_history = []
#         st.session_state.last_processed_query = None
#         st.session_state.eval_results = None
#         st.session_state.interaction_log = []
#         st.success("✅ Reset complete!")
#         st.rerun()

# # ════════════════════════════════════════════════════════
# # LOAD FAISS ON STARTUP (once per session)
# # ════════════════════════════════════════════════════════

# if not st.session_state.faiss_loaded and st.session_state.vectorstore is None:
#     embeddings = get_embeddings(EMBEDDING_MODEL)
#     loaded = load_faiss(embeddings, EMBEDDING_MODEL)
#     if loaded:
#         st.session_state.vectorstore = loaded
#         st.sidebar.success("📂 FAISS index loaded from disk")
#     st.session_state.faiss_loaded = True

# # ════════════════════════════════════════════════════════
# # MAIN LAYOUT
# # ════════════════════════════════════════════════════════

# st.title("📦 RAG Chatbot")
# st.markdown("*Delivery System Documentation Assistant*")

# tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📚 Documents", "📜 History", "📊 Evaluation"])

# # ════════════════════════════════════════════════════════
# # TAB 1: CHAT
# # ════════════════════════════════════════════════════════

# with tab1:
#     col1, col2 = st.columns([4, 1])
#     with col1:
#         uploaded_files = st.file_uploader("📤 Upload PDF", type=["pdf"], accept_multiple_files=True)
#     with col2:
#         if st.button("Clear Docs", use_container_width=True):
#             st.session_state.vectorstore = None
#             st.session_state.pdf_hashes = set()
#             st.session_state.chunk_info = {}
#             st.success("✅ Cleared!")
#             st.rerun()

#     # PDF Processing
#     if uploaded_files:
#         new_files = [
#             (pdf, hashlib.md5(pdf.getvalue()).hexdigest())
#             for pdf in uploaded_files
#             if hashlib.md5(pdf.getvalue()).hexdigest() not in st.session_state.pdf_hashes
#         ]

#         if new_files:
#             progress_bar = st.progress(0)
#             status_text = st.empty()
#             embeddings = get_embeddings(EMBEDDING_MODEL)

#             for idx, (pdf, file_hash) in enumerate(new_files):
#                 status_text.text(f"📄 Processing: {pdf.name}")
#                 try:
#                     page_docs, num_pages = extract_text_from_pdf(pdf.getvalue(), pdf.name)
#                     if not page_docs:
#                         st.warning(f"⚠️ No text in {pdf.name}")
#                         continue

#                     overlap = int(chunk_size * overlap_pct / 100)
#                     docs = split_text_with_pages(page_docs, chunk_size, overlap)

#                     if not docs:
#                         st.warning(f"⚠️ Could not split {pdf.name}")
#                         continue

#                     char_counts = [len(d.page_content) for d in docs]
#                     st.session_state.chunk_info[pdf.name] = {
#                         "chunks": len(docs),
#                         "avg_size": round(sum(char_counts) / len(char_counts)),
#                         "pages": num_pages,
#                         "total_chars": sum(char_counts)
#                     }

#                     status_text.text(f"🔍 Indexing: {pdf.name}")
#                     if st.session_state.vectorstore is None:
#                         st.session_state.vectorstore = FAISS.from_documents(docs, embeddings)
#                     else:
#                         st.session_state.vectorstore.add_documents(docs)

#                     st.session_state.pdf_hashes.add(file_hash)
#                 except Exception as e:
#                     st.error(f"❌ Error processing {pdf.name}: {e}")

#                 progress_bar.progress((idx + 1) / len(new_files))

#             # Persist FAISS to disk
#             if st.session_state.vectorstore:
#                 save_faiss(st.session_state.vectorstore, EMBEDDING_MODEL)

#             progress_bar.empty()
#             status_text.empty()
#             st.success(f"✅ Loaded {len(new_files)} PDF(s)!")

#     st.divider()

#     # Chat Interface
#     if st.session_state.vectorstore is None:
#         st.info("⬆️ Upload a PDF to start chatting")
#     else:
#         # Render existing history
#         for msg in st.session_state.chat_history:
#             with st.chat_message(msg["role"]):
#                 st.write(msg["content"])
#                 if "time" in msg:
#                     st.caption(f"⏱️ {msg['time']:.2f}s")

#         query = st.chat_input("Ask a question about your documents...")

#         if query and query != st.session_state.last_processed_query:
#             st.session_state.last_processed_query = query

#             with st.chat_message("user"):
#                 st.write(query)

#             with st.spinner("🤔 Analyzing..."):
#                 try:
#                     start_time = time.time()
#                     llm = get_llm(model_choice, temperature)
#                     embeddings = get_embeddings(EMBEDDING_MODEL)

#                     # Adaptive k
#                     adaptive_k = get_adaptive_k(query, k_retrieve)

#                     retriever = st.session_state.vectorstore.as_retriever(
#                         search_type="mmr",
#                         search_kwargs={
#                             "k": adaptive_k,
#                             "fetch_k": adaptive_k * 3,
#                             "lambda_mult": 0.6
#                         }
#                     )
#                     retrieved_docs = retriever.invoke(query)

#                     # Build context with page citations
#                     context_parts = []
#                     sources = []
#                     for doc in retrieved_docs:
#                         src = doc.metadata.get("source", "Unknown")
#                         page = doc.metadata.get("page", "")
#                         citation = f"{src} | Page {page}" if page else src
#                         if citation not in sources:
#                             sources.append(citation)
#                         context_parts.append(f"[{citation}]\n{doc.page_content}")

#                     context = "\n\n---\n\n".join(context_parts)
#                     recent_history = st.session_state.memory.get_recent()
#                     conversation_summary = st.session_state.memory.get_summary()

#                     formatted_prompt = SYSTEM_PROMPT.format(
#                         conversation_summary=conversation_summary or "No prior summary.",
#                         recent_history=recent_history or "No recent exchanges.",
#                         context=context,
#                         input=query
#                     )

#                     response = llm.invoke(formatted_prompt)
#                     answer = response.content
#                     elapsed = time.time() - start_time

#                     # Update memory (guarded — only once per query)
#                     st.session_state.memory.add_exchange(query, answer)

#                     # Log for evaluation
#                     st.session_state.interaction_log.append({
#                         "question": query,
#                         "answer": answer,
#                         "retrieved_docs": retrieved_docs
#                     })
#                     # Keep only last 10
#                     st.session_state.interaction_log = st.session_state.interaction_log[-10:]

#                     # Display response
#                     with st.chat_message("assistant"):
#                         st.write(answer)
#                         col1, col2, col3 = st.columns([3, 1, 1])
#                         with col1:
#                             st.caption(f"📎 {' · '.join(sources[:3])}")
#                         with col2:
#                             st.caption(f"⏱️ {elapsed:.2f}s")
#                         with col3:
#                             st.caption(f"📄 {len(retrieved_docs)} chunks (k={adaptive_k})")

#                         with st.expander("📋 Retrieved Chunks"):
#                             for i, doc in enumerate(retrieved_docs[:6]):
#                                 src = doc.metadata.get("source", "Unknown")
#                                 page = doc.metadata.get("page", "")
#                                 st.markdown(f"**Chunk {i+1}** — `{src}` | Page {page}")
#                                 st.text(doc.page_content[:400] + ("..." if len(doc.page_content) > 400 else ""))
#                                 st.divider()

#                     # Store in history
#                     st.session_state.chat_history.append({"role": "user", "content": query})
#                     st.session_state.chat_history.append({
#                         "role": "assistant",
#                         "content": answer,
#                         "time": elapsed
#                     })

#                 except Exception as e:
#                     st.error(f"❌ Error: {e}")

# # ════════════════════════════════════════════════════════
# # TAB 2: DOCUMENTS
# # ════════════════════════════════════════════════════════

# with tab2:
#     st.header("📚 Document Information")

#     if not st.session_state.chunk_info:
#         st.info("No documents loaded yet")
#     else:
#         col1, col2, col3, col4 = st.columns(4)
#         col1.metric("Files", len(st.session_state.chunk_info))
#         col2.metric("Total Chunks", sum(v["chunks"] for v in st.session_state.chunk_info.values()))
#         col3.metric("Total Pages", sum(v["pages"] for v in st.session_state.chunk_info.values()))
#         col4.metric("Total Size", f"{sum(v['total_chars'] for v in st.session_state.chunk_info.values()) // 1000}KB")

#         st.divider()
#         for fname, info in st.session_state.chunk_info.items():
#             with st.expander(f"📄 {fname}"):
#                 c1, c2, c3, c4 = st.columns(4)
#                 c1.metric("Chunks", info["chunks"])
#                 c2.metric("Avg Size", f"{info['avg_size']} chars")
#                 c3.metric("Total Size", f"{info['total_chars']:,} chars")
#                 c4.metric("Pages", info["pages"])
#                 avg = info["avg_size"]
#                 if avg < 300:
#                     st.warning("⚠️ Chunks are small — consider increasing chunk size")
#                 elif avg > 1500:
#                     st.warning("⚠️ Chunks are large — consider reducing chunk size")
#                 else:
#                     st.success("✅ Optimal chunk size")

# # ════════════════════════════════════════════════════════
# # TAB 3: HISTORY
# # ════════════════════════════════════════════════════════

# with tab3:
#     st.header("📜 Chat History")

#     if not st.session_state.chat_history:
#         st.info("No conversation yet")
#     else:
#         user_msgs = [m for m in st.session_state.chat_history if m["role"] == "user"]
#         asst_msgs = [m for m in st.session_state.chat_history if m["role"] == "assistant"]
#         col1, col2 = st.columns(2)
#         col1.metric("User Messages", len(user_msgs))
#         col2.metric("Responses", len(asst_msgs))

#         st.divider()
#         for msg in st.session_state.chat_history:
#             icon = "🧑" if msg["role"] == "user" else "🤖"
#             st.write(f"**{icon} {msg['role'].upper()}**")
#             content = msg["content"]
#             st.write(content[:300] + ("..." if len(content) > 300 else content[300:]))
#             if "time" in msg:
#                 st.caption(f"⏱️ {msg['time']:.2f}s")
#             st.divider()

# # ════════════════════════════════════════════════════════
# # TAB 4: LIVE EVALUATION
# # ════════════════════════════════════════════════════════

# with tab4:
#     st.header("📊 Live RAG Evaluation Dashboard")
#     st.markdown("Evaluate recent interactions using the existing LLM. Scores are based on retrieval quality, faithfulness, and hallucination risk.")

#     interaction_count = len(st.session_state.interaction_log)

#     if interaction_count == 0:
#         st.info("💬 Ask at least one question in the Chat tab before running evaluation.")
#     else:
#         st.write(f"**{interaction_count}** interaction(s) available for evaluation.")

#         n_to_eval = st.slider(
#             "Number of recent interactions to evaluate",
#             min_value=1,
#             max_value=max(1, interaction_count),
#             value=min(3, interaction_count)
#         )

#         if st.button("🔍 Run Evaluation", type="primary", use_container_width=True):
#             with st.spinner("🤔 Evaluating interactions... (this makes 1 LLM call per interaction)"):
#                 try:
#                     llm = get_llm(model_choice, temperature)
#                     evaluator = RAGEvaluator(llm=llm)

#                     recent = st.session_state.interaction_log[-n_to_eval:]
#                     batch_result = evaluator.evaluate_batch(recent)
#                     batch_result["_n_eval"] = n_to_eval  # Store slice size with results
#                     st.session_state.eval_results = batch_result
#                 except Exception as e:
#                     st.error(f"❌ Evaluation failed: {e}")

#         # Display results
#         if st.session_state.eval_results:
#             res = st.session_state.eval_results

#             if res.get("error") and res.get("count", 0) == 0:
#                 st.error(f"Evaluation error: {res['error']}")
#             else:
#                 st.divider()
#                 st.subheader("📈 Aggregate Scores")

#                 # Overall health — large display
#                 health = res["overall_health"]
#                 health_label = health_to_label(health)
#                 st.metric("🏥 Overall Health Score", f"{health}/100", delta=health_label)
#                 st.progress(health / 100)

#                 st.divider()

#                 # 4 score columns
#                 c1, c2, c3, c4 = st.columns(4)

#                 rq = res["retrieval_quality"]
#                 cc = res["context_coverage"]
#                 sg = res["source_grounding"]
#                 hr = res["hallucination_risk"]
#                 fs = res["faithfulness_score"]

#                 with c1:
#                     st.metric("🔍 Retrieval Quality", f"{rq}/10")
#                     st.caption(score_to_label(rq))
#                     st.progress(rq / 10)

#                 with c2:
#                     st.metric("📖 Context Coverage", f"{cc}/10")
#                     st.caption(score_to_label(cc))
#                     st.progress(cc / 10)

#                 with c3:
#                     st.metric("📌 Faithfulness Score", f"{fs}/100")
#                     st.caption(score_to_label(sg))
#                     st.progress(fs / 100)

#                 with c4:
#                     st.metric("⚠️ Hallucination Risk", f"{hr}/10")
#                     st.caption(score_to_label(hr, invert=True))
#                     st.progress(hr / 10)

#                 st.divider()

#                 # Per-interaction breakdown
#                 if res.get("results"):
#                     st.subheader("🔎 Per-Interaction Breakdown")
#                     _n = res.get("_n_eval", len(res["results"]))
#                     recent = st.session_state.interaction_log[-_n:]

#                     for i, (interaction, r) in enumerate(zip(recent, res["results"])):
#                         q_preview = interaction["question"][:80] + ("..." if len(interaction["question"]) > 80 else "")
#                         status = "✅" if r.get("error") is None else "❌"
#                         with st.expander(f"{status} Interaction {i+1}: {q_preview}"):
#                             if r.get("error"):
#                                 st.warning(f"Evaluation error: {r['error']}")
#                             else:
#                                 ic1, ic2, ic3, ic4 = st.columns(4)
#                                 ic1.metric("Retrieval", f"{r['retrieval_quality']}/10")
#                                 ic2.metric("Coverage", f"{r['context_coverage']}/10")
#                                 ic3.metric("Grounding", f"{r['source_grounding']}/10")
#                                 ic4.metric("Hallucination", f"{r['hallucination_risk']}/10")
#                                 st.caption(f"💬 **Reasoning:** {r.get('reasoning', 'N/A')}")

# # ════════════════════════════════════════════════════════
# # FOOTER
# # ════════════════════════════════════════════════════════

# st.divider()
# st.markdown("""
# <div style='text-align: center; color: #888; font-size: 12px;'>
# ✨ Production-Ready RAG System &nbsp;|&nbsp;
# 📦 bge-base-en embeddings &nbsp;|&nbsp;
# 🚀 FAISS + Groq + Dual Memory + Live Evaluation
# </div>
# """, unsafe_allow_html=True)














# import streamlit as st
# import fitz
# import os
# import hashlib
# import time
# from typing import List, Tuple, Optional
# from dotenv import load_dotenv

# from langchain_groq import ChatGroq
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory

# from rag_evaluation_framework import RAGEvaluator, score_to_label, health_to_label

# # ════════════════════════════════════════════════════════
# # SETUP
# # ════════════════════════════════════════════════════════

# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# FAISS_INDEX_PATH = "./faiss_index"

# if not GROQ_API_KEY:
#     st.error("❌ GROQ_API_KEY not found in .env file")
#     st.stop()

# st.set_page_config(
#     page_title="RAG Chatbot",
#     page_icon="📦",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ════════════════════════════════════════════════════════
# # MEMORY CLASS
# # ════════════════════════════════════════════════════════

# class DualRAGMemory:
#     """Buffer memory + summary memory, both injected into prompt."""

#     def __init__(self, buffer_size: int = 5, llm=None):
#         self.buffer_size = buffer_size
#         self.buffer = ConversationBufferWindowMemory(
#             k=buffer_size,
#             memory_key="chat_history",
#             human_prefix="User",
#             ai_prefix="Assistant",
#             input_key="query",
#             output_key="response"
#         )
#         self.summary_memory = None
#         self.token_count = 0
#         self.interaction_count = 0
#         if llm:
#             try:
#                 self.summary_memory = ConversationSummaryMemory(
#                     llm=llm,
#                     memory_key="summary",
#                     human_prefix="User",
#                     ai_prefix="Assistant",
#                     input_key="query",
#                     output_key="response"
#                 )
#             except Exception:
#                 self.summary_memory = None

#     def add_exchange(self, query: str, response: str):
#         try:
#             self.buffer.save_context({"query": query}, {"response": response})
#             if self.summary_memory:
#                 self.summary_memory.save_context({"query": query}, {"response": response})
#             self.token_count += len(query.split()) + len(response.split())
#             self.interaction_count += 1
#         except Exception:
#             pass

#     def get_recent(self) -> str:
#         try:
#             return self.buffer.buffer or ""
#         except Exception:
#             return ""

#     def get_summary(self) -> str:
#         try:
#             if self.summary_memory:
#                 return self.summary_memory.buffer or ""
#         except Exception:
#             pass
#         return ""

#     def get_status(self) -> str:
#         return "✅ Healthy" if self.token_count < 5000 else "⚠️ High"

#     def reset(self):
#         self.buffer.clear()
#         if self.summary_memory:
#             try:
#                 self.summary_memory.clear()
#             except Exception:
#                 pass
#         self.token_count = 0
#         self.interaction_count = 0

# # ════════════════════════════════════════════════════════
# # CACHED RESOURCES
# # ════════════════════════════════════════════════════════

# @st.cache_resource
# def get_llm(model_name: str, temperature: float):
#     return ChatGroq(api_key=GROQ_API_KEY, model_name=model_name, temperature=temperature)

# @st.cache_resource
# def get_embeddings(model_name: str = "BAAI/bge-base-en-v1.5"):
#     return HuggingFaceEmbeddings(
#         model_name=model_name,
#         model_kwargs={"device": "cpu"},
#         encode_kwargs={"normalize_embeddings": True}
#     )

# # ════════════════════════════════════════════════════════
# # PDF PROCESSING
# # ════════════════════════════════════════════════════════

# def extract_text_from_pdf(file_bytes: bytes, filename: str) -> Tuple[List, int]:
#     """Extract text with page-level metadata."""
#     try:
#         doc = fitz.open(stream=file_bytes, filetype="pdf")
#         page_docs = []
#         for i, page in enumerate(doc):
#             text = page.get_text("text").strip()
#             if text:
#                 page_docs.append({"text": text, "page": i + 1, "source": filename})
#         return page_docs, len(doc)
#     except Exception as e:
#         st.error(f"❌ PDF error: {e}")
#         return [], 0

# def split_text_with_pages(page_docs: list, chunk_size: int = 1000, overlap: int = 200):
#     """Split with page metadata preserved per chunk."""
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=overlap,
#         separators=["\n\n", "\n", ". ", " ", ""]
#     )
#     all_chunks = []
#     for page_doc in page_docs:
#         chunks = splitter.create_documents([page_doc["text"]])
#         for chunk in chunks:
#             chunk.metadata["source"] = page_doc["source"]
#             chunk.metadata["page"] = page_doc["page"]
#         all_chunks.extend(chunks)
#     return all_chunks

# # ════════════════════════════════════════════════════════
# # ADAPTIVE RETRIEVAL
# # ════════════════════════════════════════════════════════

# COMPLEX_KEYWORDS = [
#     "compare", "difference", "explain", "analyze", "how does", "why does",
#     "summarize", "describe", "elaborate", "relationship", "architecture",
#     "workflow", "process", "mechanism", "contrast", "evaluate", "assess"
# ]

# def get_adaptive_k(query: str, base_k: int) -> int:
#     """Return fewer chunks for simple queries, more for complex ones."""
#     q = query.lower()
#     is_complex = len(query.split()) > 12 or any(kw in q for kw in COMPLEX_KEYWORDS)
#     return base_k if is_complex else max(3, base_k // 2)

# # ════════════════════════════════════════════════════════
# # FAISS PERSISTENCE
# # ════════════════════════════════════════════════════════

# def save_faiss(vectorstore, embedding_model: str):
#     """Persist FAISS index and record which embedding model built it."""
#     try:
#         vectorstore.save_local(FAISS_INDEX_PATH)
#         with open(f"{FAISS_INDEX_PATH}/embedding_model.txt", "w") as f:
#             f.write(embedding_model)
#     except Exception as e:
#         st.warning(f"⚠️ Could not save FAISS index: {e}")

# def load_faiss(embeddings, embedding_model: str) -> Optional[object]:
#     """Load persisted FAISS index if embedding model matches."""
#     model_file = f"{FAISS_INDEX_PATH}/embedding_model.txt"
#     index_file = f"{FAISS_INDEX_PATH}/index.faiss"
#     if not (os.path.exists(index_file) and os.path.exists(model_file)):
#         return None
#     try:
#         saved_model = open(model_file).read().strip()
#         if saved_model != embedding_model:
#             return None  # Model mismatch — must rebuild
#         return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
#     except Exception:
#         return None

# # ════════════════════════════════════════════════════════
# # PROMPT
# # ════════════════════════════════════════════════════════

# SYSTEM_PROMPT = ChatPromptTemplate.from_template("""You are a strict document-based question answering assistant.

# CONVERSATION SUMMARY (for context):
# {conversation_summary}

# RECENT EXCHANGES:
# {recent_history}

# RETRIEVED DOCUMENTS:
# {context}

# QUESTION:
# {input}

# INSTRUCTIONS:
# 1. Answer ONLY using information explicitly present in the retrieved documents above.
# 2. Do NOT use prior knowledge, training data, or external information.
# 3. Do NOT speculate, guess, or invent details not in the documents.
# 4. If partially supported: provide only the supported part, then state "The remaining information is not available in the provided documents."
# 5. If not supported at all: respond ONLY "This information is not available in the provided documents."
# 6. Cite sources using: [filename | Page N] after every factual claim.
# 7. Keep answers concise and accurate.
# 8. Prefer accuracy over completeness.

# FINAL ANSWER:""")

# # ════════════════════════════════════════════════════════
# # SESSION STATE
# # ════════════════════════════════════════════════════════

# EMBEDDING_MODELS = {
#     "BGE Base (Recommended)": "BAAI/bge-base-en-v1.5",
#     "MiniLM L6 (Fastest)": "sentence-transformers/all-MiniLM-L6-v2",
#     "MPNet Base (Highest Quality)": "sentence-transformers/all-mpnet-base-v2",
# }

# def init_session():
#     defaults = {
#         "vectorstore": None,
#         "chat_history": [],
#         "pdf_hashes": set(),
#         "chunk_info": {},
#         "last_processed_query": None,
#         "eval_results": None,
#         "interaction_log": [],   # Stores {question, answer, retrieved_docs} for eval
#         "faiss_loaded": False,
#     }
#     for k, v in defaults.items():
#         if k not in st.session_state:
#             st.session_state[k] = v

# init_session()

# # ════════════════════════════════════════════════════════
# # SIDEBAR
# # ════════════════════════════════════════════════════════

# with st.sidebar:
#     st.header("⚙️ Configuration")

#     st.subheader("🤖 Model Settings")
#     model_choice = st.selectbox(
#         "LLM Model",
#         ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
#         help="8B = Fast, 70B = Better Quality"
#     )
#     temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)

#     st.subheader("🧠 Embedding Model")
#     embedding_label = st.selectbox(
#         "Embedding Model",
#         list(EMBEDDING_MODELS.keys()),
#         help="BGE Base = best balance | MiniLM = fastest | MPNet = highest quality"
#     )
#     EMBEDDING_MODEL = EMBEDDING_MODELS[embedding_label]
#     # Warn if model changed while vectorstore exists
#     if st.session_state.get("active_embedding_model") and \
#        st.session_state.active_embedding_model != EMBEDDING_MODEL and \
#        st.session_state.vectorstore is not None:
#         st.warning("⚠️ Embedding model changed! Clear documents and re-upload to rebuild the index.")

#     st.subheader("📑 Document Settings")
#     chunk_size = st.slider("Chunk Size", 200, 2000, 1000, 100)
#     overlap_pct = st.slider("Overlap %", 5, 40, 20, 5)
#     # Track active embedding model in session state
#     st.session_state.active_embedding_model = EMBEDDING_MODEL

#     st.subheader("🔍 Retrieval")
#     k_retrieve = st.slider("Chunks to Retrieve", 3, 15, 6)

#     st.subheader("💾 Memory")
#     memory_window = st.slider("Memory Window (exchanges)", 2, 10, 5)

#     # Initialize or update memory if window size changes
#     if "memory" not in st.session_state:
#         llm_for_memory = get_llm(model_choice, temperature)
#         st.session_state.memory = DualRAGMemory(buffer_size=memory_window, llm=llm_for_memory)
#     elif st.session_state.memory.buffer_size != memory_window:
#         old = st.session_state.memory
#         llm_for_memory = get_llm(model_choice, temperature)
#         st.session_state.memory = DualRAGMemory(buffer_size=memory_window, llm=llm_for_memory)
#         st.session_state.memory.token_count = old.token_count
#         st.session_state.memory.interaction_count = old.interaction_count

#     st.caption(f"Status: {st.session_state.memory.get_status()}")
#     st.caption(f"Tokens: {st.session_state.memory.token_count}")
#     st.caption(f"Exchanges: {st.session_state.memory.interaction_count}")

#     if st.button("🔄 Reset All", use_container_width=True):
#         st.session_state.memory.reset()
#         st.session_state.chat_history = []
#         st.session_state.last_processed_query = None
#         st.session_state.eval_results = None
#         st.session_state.interaction_log = []
#         st.success("✅ Reset complete!")
#         st.rerun()

# # ════════════════════════════════════════════════════════
# # LOAD FAISS ON STARTUP (once per session)
# # ════════════════════════════════════════════════════════

# if not st.session_state.faiss_loaded and st.session_state.vectorstore is None:
#     embeddings = get_embeddings(EMBEDDING_MODEL)
#     loaded = load_faiss(embeddings, EMBEDDING_MODEL)
#     if loaded:
#         st.session_state.vectorstore = loaded
#         st.sidebar.success("📂 FAISS index loaded from disk")
#     st.session_state.faiss_loaded = True

# # ════════════════════════════════════════════════════════
# # MAIN LAYOUT
# # ════════════════════════════════════════════════════════

# st.title("📦 RAG Chatbot")
# st.markdown("*Delivery System Documentation Assistant*")

# tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📚 Documents", "📜 History", "📊 Evaluation"])

# # ════════════════════════════════════════════════════════
# # TAB 1: CHAT
# # ════════════════════════════════════════════════════════

# with tab1:
#     col1, col2 = st.columns([4, 1])
#     with col1:
#         uploaded_files = st.file_uploader("📤 Upload PDF", type=["pdf"], accept_multiple_files=True)
#     with col2:
#         if st.button("Clear Docs", use_container_width=True):
#             st.session_state.vectorstore = None
#             st.session_state.pdf_hashes = set()
#             st.session_state.chunk_info = {}
#             st.success("✅ Cleared!")
#             st.rerun()

#     # PDF Processing
#     if uploaded_files:
#         new_files = [
#             (pdf, hashlib.md5(pdf.getvalue()).hexdigest())
#             for pdf in uploaded_files
#             if hashlib.md5(pdf.getvalue()).hexdigest() not in st.session_state.pdf_hashes
#         ]

#         if new_files:
#             progress_bar = st.progress(0)
#             status_text = st.empty()
#             embeddings = get_embeddings(EMBEDDING_MODEL)

#             for idx, (pdf, file_hash) in enumerate(new_files):
#                 status_text.text(f"📄 Processing: {pdf.name}")
#                 try:
#                     page_docs, num_pages = extract_text_from_pdf(pdf.getvalue(), pdf.name)
#                     if not page_docs:
#                         st.warning(f"⚠️ No text in {pdf.name}")
#                         continue

#                     overlap = int(chunk_size * overlap_pct / 100)
#                     docs = split_text_with_pages(page_docs, chunk_size, overlap)

#                     if not docs:
#                         st.warning(f"⚠️ Could not split {pdf.name}")
#                         continue

#                     char_counts = [len(d.page_content) for d in docs]
#                     st.session_state.chunk_info[pdf.name] = {
#                         "chunks": len(docs),
#                         "avg_size": round(sum(char_counts) / len(char_counts)),
#                         "pages": num_pages,
#                         "total_chars": sum(char_counts)
#                     }

#                     status_text.text(f"🔍 Indexing: {pdf.name}")
#                     if st.session_state.vectorstore is None:
#                         st.session_state.vectorstore = FAISS.from_documents(docs, embeddings)
#                     else:
#                         st.session_state.vectorstore.add_documents(docs)

#                     st.session_state.pdf_hashes.add(file_hash)
#                 except Exception as e:
#                     st.error(f"❌ Error processing {pdf.name}: {e}")

#                 progress_bar.progress((idx + 1) / len(new_files))

#             # Persist FAISS to disk
#             if st.session_state.vectorstore:
#                 save_faiss(st.session_state.vectorstore, EMBEDDING_MODEL)

#             progress_bar.empty()
#             status_text.empty()
#             st.success(f"✅ Loaded {len(new_files)} PDF(s)!")

#     st.divider()

#     # Chat Interface
#     if st.session_state.vectorstore is None:
#         st.info("⬆️ Upload a PDF to start chatting")
#     else:
#         # Render existing history
#         for msg in st.session_state.chat_history:
#             with st.chat_message(msg["role"]):
#                 st.write(msg["content"])
#                 if "time" in msg:
#                     st.caption(f"⏱️ {msg['time']:.2f}s")

#         query = st.chat_input("Ask a question about your documents...")

#         if query and query != st.session_state.last_processed_query:
#             st.session_state.last_processed_query = query

#             with st.chat_message("user"):
#                 st.write(query)

#             with st.spinner("🤔 Analyzing..."):
#                 try:
#                     start_time = time.time()
#                     llm = get_llm(model_choice, temperature)
#                     embeddings = get_embeddings(EMBEDDING_MODEL)

#                     # Adaptive k
#                     adaptive_k = get_adaptive_k(query, k_retrieve)

#                     retriever = st.session_state.vectorstore.as_retriever(
#                         search_type="mmr",
#                         search_kwargs={
#                             "k": adaptive_k,
#                             "fetch_k": adaptive_k * 3,
#                             "lambda_mult": 0.6
#                         }
#                     )
#                     retrieved_docs = retriever.invoke(query)

#                     # Build context with page citations
#                     context_parts = []
#                     sources = []
#                     for doc in retrieved_docs:
#                         src = doc.metadata.get("source", "Unknown")
#                         page = doc.metadata.get("page", "")
#                         citation = f"{src} | Page {page}" if page else src
#                         if citation not in sources:
#                             sources.append(citation)
#                         context_parts.append(f"[{citation}]\n{doc.page_content}")

#                     context = "\n\n---\n\n".join(context_parts)
#                     recent_history = st.session_state.memory.get_recent()
#                     conversation_summary = st.session_state.memory.get_summary()

#                     formatted_prompt = SYSTEM_PROMPT.format(
#                         conversation_summary=conversation_summary or "No prior summary.",
#                         recent_history=recent_history or "No recent exchanges.",
#                         context=context,
#                         input=query
#                     )

#                     response = llm.invoke(formatted_prompt)
#                     answer = response.content
#                     elapsed = time.time() - start_time

#                     # Update memory (guarded — only once per query)
#                     st.session_state.memory.add_exchange(query, answer)

#                     # Log for evaluation
#                     st.session_state.interaction_log.append({
#                         "question": query,
#                         "answer": answer,
#                         "retrieved_docs": retrieved_docs
#                     })
#                     # Keep only last 10
#                     st.session_state.interaction_log = st.session_state.interaction_log[-10:]

#                     # Display response
#                     with st.chat_message("assistant"):
#                         st.write(answer)
#                         col1, col2, col3 = st.columns([3, 1, 1])
#                         with col1:
#                             st.caption(f"📎 {' · '.join(sources[:3])}")
#                         with col2:
#                             st.caption(f"⏱️ {elapsed:.2f}s")
#                         with col3:
#                             st.caption(f"📄 {len(retrieved_docs)} chunks (k={adaptive_k})")

#                         with st.expander("📋 Retrieved Chunks"):
#                             for i, doc in enumerate(retrieved_docs[:6]):
#                                 src = doc.metadata.get("source", "Unknown")
#                                 page = doc.metadata.get("page", "")
#                                 st.markdown(f"**Chunk {i+1}** — `{src}` | Page {page}")
#                                 st.text(doc.page_content[:400] + ("..." if len(doc.page_content) > 400 else ""))
#                                 st.divider()

#                     # Store in history
#                     st.session_state.chat_history.append({"role": "user", "content": query})
#                     st.session_state.chat_history.append({
#                         "role": "assistant",
#                         "content": answer,
#                         "time": elapsed
#                     })

#                 except Exception as e:
#                     st.error(f"❌ Error: {e}")

# # ════════════════════════════════════════════════════════
# # TAB 2: DOCUMENTS
# # ════════════════════════════════════════════════════════

# with tab2:
#     st.header("📚 Document Information")

#     if not st.session_state.chunk_info:
#         st.info("No documents loaded yet")
#     else:
#         col1, col2, col3, col4 = st.columns(4)
#         col1.metric("Files", len(st.session_state.chunk_info))
#         col2.metric("Total Chunks", sum(v["chunks"] for v in st.session_state.chunk_info.values()))
#         col3.metric("Total Pages", sum(v["pages"] for v in st.session_state.chunk_info.values()))
#         col4.metric("Total Size", f"{sum(v['total_chars'] for v in st.session_state.chunk_info.values()) // 1000}KB")

#         st.divider()
#         for fname, info in st.session_state.chunk_info.items():
#             with st.expander(f"📄 {fname}"):
#                 c1, c2, c3, c4 = st.columns(4)
#                 c1.metric("Chunks", info["chunks"])
#                 c2.metric("Avg Size", f"{info['avg_size']} chars")
#                 c3.metric("Total Size", f"{info['total_chars']:,} chars")
#                 c4.metric("Pages", info["pages"])
#                 avg = info["avg_size"]
#                 if avg < 300:
#                     st.warning("⚠️ Chunks are small — consider increasing chunk size")
#                 elif avg > 1500:
#                     st.warning("⚠️ Chunks are large — consider reducing chunk size")
#                 else:
#                     st.success("✅ Optimal chunk size")

# # ════════════════════════════════════════════════════════
# # TAB 3: HISTORY
# # ════════════════════════════════════════════════════════

# with tab3:
#     st.header("📜 Chat History")

#     if not st.session_state.chat_history:
#         st.info("No conversation yet")
#     else:
#         user_msgs = [m for m in st.session_state.chat_history if m["role"] == "user"]
#         asst_msgs = [m for m in st.session_state.chat_history if m["role"] == "assistant"]
#         col1, col2 = st.columns(2)
#         col1.metric("User Messages", len(user_msgs))
#         col2.metric("Responses", len(asst_msgs))

#         st.divider()
#         for msg in st.session_state.chat_history:
#             icon = "🧑" if msg["role"] == "user" else "🤖"
#             st.write(f"**{icon} {msg['role'].upper()}**")
#             content = msg["content"]
#             st.write(content[:300] + ("..." if len(content) > 300 else content[300:]))
#             if "time" in msg:
#                 st.caption(f"⏱️ {msg['time']:.2f}s")
#             st.divider()

# # ════════════════════════════════════════════════════════
# # TAB 4: LIVE EVALUATION
# # ════════════════════════════════════════════════════════

# with tab4:
#     st.header("📊 Live RAG Evaluation Dashboard")
#     st.markdown("Evaluate recent interactions using the existing LLM. Scores are based on retrieval quality, faithfulness, and hallucination risk.")

#     interaction_count = len(st.session_state.interaction_log)

#     if interaction_count == 0:
#         st.info("💬 Ask at least one question in the Chat tab first — the evaluation button will activate once you have interactions to score.")

#     # Always show slider + button — disabled when no interactions
#     n_to_eval = st.slider(
#         "Number of recent interactions to evaluate",
#         min_value=1,
#         max_value=max(1, interaction_count) if interaction_count > 0 else 1,
#         value=min(3, interaction_count) if interaction_count > 0 else 1,
#         disabled=(interaction_count == 0)
#     )

#     if interaction_count > 0:
#         st.write(f"**{interaction_count}** interaction(s) available for evaluation.")

#     run_eval = st.button(
#         "🔍 Run Evaluation",
#         type="primary",
#         use_container_width=True,
#         disabled=(interaction_count == 0),
#         help="Ask questions in the Chat tab first to enable evaluation."
#     )

#     if run_eval and interaction_count > 0:
#         with st.spinner("🤔 Evaluating... (1 LLM call per interaction)"):
#             try:
#                 llm = get_llm(model_choice, temperature)
#                 evaluator = RAGEvaluator(llm=llm)
#                 recent = st.session_state.interaction_log[-n_to_eval:]
#                 batch_result = evaluator.evaluate_batch(recent)
#                 batch_result["_n_eval"] = n_to_eval
#                 st.session_state.eval_results = batch_result
#             except Exception as e:
#                 st.error(f"❌ Evaluation failed: {e}")

#     # Display results — always shown if available (persists across reruns)
#     if st.session_state.eval_results:
#         res = st.session_state.eval_results

#         if res.get("error") and res.get("count", 0) == 0:
#             st.error(f"Evaluation error: {res['error']}")
#         else:
#             st.divider()
#             st.subheader("📈 Aggregate Scores")

#             health = res["overall_health"]
#             health_label = health_to_label(health)
#             st.metric("🏥 Overall Health Score", f"{health}/100", delta=health_label)
#             st.progress(health / 100)

#             st.divider()

#             c1, c2, c3, c4 = st.columns(4)
#             rq = res["retrieval_quality"]
#             cc = res["context_coverage"]
#             sg = res["source_grounding"]
#             hr = res["hallucination_risk"]
#             fs = res["faithfulness_score"]

#             with c1:
#                 st.metric("🔍 Retrieval Quality", f"{rq}/10")
#                 st.caption(score_to_label(rq))
#                 st.progress(rq / 10)

#             with c2:
#                 st.metric("📖 Context Coverage", f"{cc}/10")
#                 st.caption(score_to_label(cc))
#                 st.progress(cc / 10)

#             with c3:
#                 st.metric("📌 Faithfulness Score", f"{fs}/100")
#                 st.caption(score_to_label(sg))
#                 st.progress(fs / 100)

#             with c4:
#                 st.metric("⚠️ Hallucination Risk", f"{hr}/10")
#                 st.caption(score_to_label(hr, invert=True))
#                 st.progress(hr / 10)

#             st.divider()

#             if res.get("results"):
#                 st.subheader("🔎 Per-Interaction Breakdown")
#                 _n = res.get("_n_eval", len(res["results"]))
#                 recent_log = st.session_state.interaction_log[-_n:]

#                 for i, (interaction, r) in enumerate(zip(recent_log, res["results"])):
#                     q_preview = interaction["question"][:80] + ("..." if len(interaction["question"]) > 80 else "")
#                     status = "✅" if r.get("error") is None else "❌"
#                     with st.expander(f"{status} Interaction {i+1}: {q_preview}"):
#                         if r.get("error"):
#                             st.warning(f"Evaluation error: {r['error']}")
#                         else:
#                             ic1, ic2, ic3, ic4 = st.columns(4)
#                             ic1.metric("Retrieval", f"{r['retrieval_quality']}/10")
#                             ic2.metric("Coverage", f"{r['context_coverage']}/10")
#                             ic3.metric("Grounding", f"{r['source_grounding']}/10")
#                             ic4.metric("Hallucination", f"{r['hallucination_risk']}/10")
#                             st.caption(f"💬 **Reasoning:** {r.get('reasoning', 'N/A')}")

# # ════════════════════════════════════════════════════════
# # FOOTER
# # ════════════════════════════════════════════════════════

# st.divider()
# st.markdown("""
# <div style='text-align: center; color: #888; font-size: 12px;'>
# ✨ Production-Ready RAG System &nbsp;|&nbsp;
# 📦 bge-base-en embeddings &nbsp;|&nbsp;
# 🚀 FAISS + Groq + Dual Memory + Live Evaluation
# </div>
# """, unsafe_allow_html=True)





# import streamlit as st
# import fitz
# import os
# import hashlib
# import time
# from typing import List, Tuple, Optional
# from dotenv import load_dotenv

# from langchain_groq import ChatGroq
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.documents import Document
# from langgraph.graph import StateGraph, END
# from typing_extensions import TypedDict

# from rag_evaluation_framework import RAGEvaluator, score_to_label, health_to_label

# # ════════════════════════════════════════════════════════
# # SETUP
# # ════════════════════════════════════════════════════════

# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# FAISS_INDEX_PATH = "./faiss_index"

# if not GROQ_API_KEY:
#     st.error("❌ GROQ_API_KEY not found in .env file")
#     st.stop()

# st.set_page_config(
#     page_title="RAG Chatbot",
#     page_icon="📦",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ════════════════════════════════════════════════════════
# # MEMORY CLASS
# # ════════════════════════════════════════════════════════

# class DualRAGMemory:
#     """
#     Simple dual memory: sliding window buffer + periodic LLM summary.
#     No LangChain memory classes needed — fully version-safe.
#     """

#     def __init__(self, buffer_size: int = 5, llm=None):
#         self.buffer_size = buffer_size
#         self.llm = llm
#         self._exchanges: List[dict] = []   # [{"q": ..., "a": ...}]
#         self._summary: str = ""
#         self.token_count = 0
#         self.interaction_count = 0

#     def add_exchange(self, query: str, response: str):
#         """Add a Q&A exchange; trim buffer to window size; refresh summary every 5 turns."""
#         self._exchanges.append({"q": query, "a": response})
#         # Keep only last N exchanges in the sliding window
#         if len(self._exchanges) > self.buffer_size:
#             self._exchanges = self._exchanges[-self.buffer_size:]
#         self.token_count += len(query.split()) + len(response.split())
#         self.interaction_count += 1
#         # Refresh summary every 5 interactions if LLM available
#         if self.llm and self.interaction_count % 5 == 0:
#             self._refresh_summary()

#     def _refresh_summary(self):
#         """Ask the LLM to summarise the full conversation so far."""
#         try:
#             history_text = self.get_recent()
#             if not history_text.strip():
#                 return
#             prompt = (
#                 "Summarise this conversation in 2-3 sentences, preserving key facts:\n\n"
#                 + history_text
#             )
#             result = self.llm.invoke(prompt)
#             self._summary = result.content.strip()
#         except Exception:
#             pass  # Silent fail — summary is optional

#     def get_recent(self) -> str:
#         """Return recent exchanges as formatted text."""
#         if not self._exchanges:
#             return ""
#         lines = []
#         for ex in self._exchanges:
#             lines.append(f"User: {ex['q']}")
#             lines.append(f"Assistant: {ex['a']}")
#         return "\n".join(lines)

#     def get_summary(self) -> str:
#         """Return the current conversation summary."""
#         return self._summary

#     def get_status(self) -> str:
#         return "✅ Healthy" if self.token_count < 5000 else "⚠️ High"

#     def reset(self):
#         self._exchanges = []
#         self._summary = ""
#         self.token_count = 0
#         self.interaction_count = 0

# # ════════════════════════════════════════════════════════
# # CACHED RESOURCES
# # ════════════════════════════════════════════════════════

# @st.cache_resource
# def get_llm(model_name: str, temperature: float):
#     return ChatGroq(api_key=GROQ_API_KEY, model_name=model_name, temperature=temperature)

# @st.cache_resource
# def get_embeddings(model_name: str = "BAAI/bge-base-en-v1.5"):
#     return HuggingFaceEmbeddings(
#         model_name=model_name,
#         model_kwargs={"device": "cpu"},
#         encode_kwargs={"normalize_embeddings": True}
#     )

# # ════════════════════════════════════════════════════════
# # PDF PROCESSING
# # ════════════════════════════════════════════════════════

# def extract_text_from_pdf(file_bytes: bytes, filename: str) -> Tuple[List, int]:
#     """Extract text with page-level metadata."""
#     try:
#         doc = fitz.open(stream=file_bytes, filetype="pdf")
#         page_docs = []
#         for i, page in enumerate(doc):
#             text = page.get_text("text").strip()
#             if text:
#                 page_docs.append({"text": text, "page": i + 1, "source": filename})
#         return page_docs, len(doc)
#     except Exception as e:
#         st.error(f"❌ PDF error: {e}")
#         return [], 0

# def split_text_with_pages(page_docs: list, chunk_size: int = 1000, overlap: int = 200):
#     """Split with page metadata preserved per chunk."""
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=overlap,
#         separators=["\n\n", "\n", ". ", " ", ""]
#     )
#     all_chunks = []
#     for page_doc in page_docs:
#         chunks = splitter.create_documents([page_doc["text"]])
#         for chunk in chunks:
#             chunk.metadata["source"] = page_doc["source"]
#             chunk.metadata["page"] = page_doc["page"]
#         all_chunks.extend(chunks)
#     return all_chunks

# # ════════════════════════════════════════════════════════
# # ADAPTIVE RETRIEVAL
# # ════════════════════════════════════════════════════════

# COMPLEX_KEYWORDS = [
#     "compare", "difference", "explain", "analyze", "how does", "why does",
#     "summarize", "describe", "elaborate", "relationship", "architecture",
#     "workflow", "process", "mechanism", "contrast", "evaluate", "assess"
# ]

# def get_adaptive_k(query: str, base_k: int) -> int:
#     """Return fewer chunks for simple queries, more for complex ones."""
#     q = query.lower()
#     is_complex = len(query.split()) > 12 or any(kw in q for kw in COMPLEX_KEYWORDS)
#     return base_k if is_complex else max(3, base_k // 2)

# # ════════════════════════════════════════════════════════
# # FAISS PERSISTENCE
# # ════════════════════════════════════════════════════════

# def save_faiss(vectorstore, embedding_model: str):
#     """Persist FAISS index and record which embedding model built it."""
#     try:
#         vectorstore.save_local(FAISS_INDEX_PATH)
#         with open(f"{FAISS_INDEX_PATH}/embedding_model.txt", "w") as f:
#             f.write(embedding_model)
#     except Exception as e:
#         st.warning(f"⚠️ Could not save FAISS index: {e}")

# def load_faiss(embeddings, embedding_model: str) -> Optional[object]:
#     """Load persisted FAISS index if embedding model matches."""
#     model_file = f"{FAISS_INDEX_PATH}/embedding_model.txt"
#     index_file = f"{FAISS_INDEX_PATH}/index.faiss"
#     if not (os.path.exists(index_file) and os.path.exists(model_file)):
#         return None
#     try:
#         saved_model = open(model_file).read().strip()
#         if saved_model != embedding_model:
#             return None  # Model mismatch — must rebuild
#         return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
#     except Exception:
#         return None

# # ════════════════════════════════════════════════════════
# # PROMPT
# # ════════════════════════════════════════════════════════

# SYSTEM_PROMPT = ChatPromptTemplate.from_template("""You are a strict document-based question answering assistant.

# CONVERSATION SUMMARY (for context):
# {conversation_summary}

# RECENT EXCHANGES:
# {recent_history}

# RETRIEVED DOCUMENTS:
# {context}

# QUESTION:
# {input}

# INSTRUCTIONS:
# 1. Answer ONLY using information explicitly present in the retrieved documents above.
# 2. Do NOT use prior knowledge, training data, or external information.
# 3. Do NOT speculate, guess, or invent details not in the documents.
# 4. If partially supported: provide only the supported part, then state "The remaining information is not available in the provided documents."
# 5. If not supported at all: respond ONLY "This information is not available in the provided documents."
# 6. Cite sources using: [filename | Page N] after every factual claim.
# 7. Keep answers concise and accurate.
# 8. Prefer accuracy over completeness.

# FINAL ANSWER:""")

# # ════════════════════════════════════════════════════════
# # LANGGRAPH — AGENTIC RAG STATE & NODES
# # ════════════════════════════════════════════════════════

# class RAGState(TypedDict):
#     """Typed state passed through the LangGraph RAG pipeline."""
#     query: str
#     documents: List[Document]
#     answer: str
#     sources: List[str]
#     retrieval_attempts: int
#     document_grade: str          # "relevant" | "not_relevant"
#     conversation_summary: str
#     recent_history: str
#     adaptive_k: int
#     vectorstore: object
#     llm: object


# GRADE_PROMPT = """You are a document relevance grader.

# Question: {question}

# Retrieved document excerpt:
# {document}

# Does this document contain information useful for answering the question?
# Respond ONLY with JSON: {{"score": "relevant"}} or {{"score": "not_relevant"}}"""

# REWRITE_PROMPT = """You are a query rewriter for a RAG system.
# The original query failed to retrieve useful documents. Rewrite it to be more specific.

# Original query: {question}

# Rewritten query (output ONLY the new query, nothing else):"""


# def node_retrieve(state: RAGState) -> RAGState:
#     """Retrieve documents using MMR with adaptive k."""
#     retriever = state["vectorstore"].as_retriever(
#         search_type="mmr",
#         search_kwargs={
#             "k": state["adaptive_k"],
#             "fetch_k": state["adaptive_k"] * 3,
#             "lambda_mult": 0.6
#         }
#     )
#     docs = retriever.invoke(state["query"])
#     return {**state, "documents": docs, "retrieval_attempts": state["retrieval_attempts"] + 1}


# def node_grade_documents(state: RAGState) -> RAGState:
#     """LLM grades whether retrieved docs are relevant to the query."""
#     llm = state["llm"]
#     question = state["query"]
#     docs = state["documents"]

#     if not docs:
#         return {**state, "document_grade": "not_relevant"}

#     relevant_count = 0
#     for doc in docs[:4]:  # Grade first 4 docs for speed
#         try:
#             prompt = GRADE_PROMPT.format(
#                 question=question,
#                 document=doc.page_content[:600]
#             )
#             result = llm.invoke(prompt)
#             raw = result.content.strip()
#             import json, re
#             raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
#             grade = json.loads(raw)
#             if grade.get("score") == "relevant":
#                 relevant_count += 1
#         except Exception:
#             relevant_count += 1  # Assume relevant on parse failure

#     grade = "relevant" if relevant_count >= 1 else "not_relevant"
#     return {**state, "document_grade": grade}


# def node_transform_query(state: RAGState) -> RAGState:
#     """Rewrite the query when retrieved docs are not relevant."""
#     try:
#         prompt = REWRITE_PROMPT.format(question=state["query"])
#         result = state["llm"].invoke(prompt)
#         new_query = result.content.strip()
#     except Exception:
#         new_query = state["query"]  # Fallback to original
#     return {**state, "query": new_query}


# def node_generate(state: RAGState) -> RAGState:
#     """Generate the final answer from retrieved documents."""
#     docs = state["documents"]
#     context_parts = []
#     sources = []
#     for doc in docs:
#         src = doc.metadata.get("source", "Unknown")
#         page = doc.metadata.get("page", "")
#         citation = f"{src} | Page {page}" if page else src
#         if citation not in sources:
#             sources.append(citation)
#         context_parts.append(f"[{citation}]\n{doc.page_content}")

#     context = "\n\n---\n\n".join(context_parts) if context_parts else "No documents retrieved."

#     formatted_prompt = SYSTEM_PROMPT.format(
#         conversation_summary=state["conversation_summary"] or "No prior summary.",
#         recent_history=state["recent_history"] or "No recent exchanges.",
#         context=context,
#         input=state["query"]
#     )
#     response = state["llm"].invoke(formatted_prompt)
#     return {**state, "answer": response.content, "sources": sources}


# def should_retry(state: RAGState) -> str:
#     """Conditional edge: retry with rewritten query or go straight to generate."""
#     if state["document_grade"] == "relevant":
#         return "generate"
#     if state["retrieval_attempts"] < 2:
#         return "transform_query"   # Rewrite and retry once
#     return "generate"              # Give up retrying, generate with what we have


# def build_rag_graph() -> StateGraph:
#     """Compile the LangGraph agentic RAG pipeline."""
#     graph = StateGraph(RAGState)
#     graph.add_node("retrieve", node_retrieve)
#     graph.add_node("grade_documents", node_grade_documents)
#     graph.add_node("transform_query", node_transform_query)
#     graph.add_node("generate", node_generate)

#     graph.set_entry_point("retrieve")
#     graph.add_edge("retrieve", "grade_documents")
#     graph.add_conditional_edges(
#         "grade_documents",
#         should_retry,
#         {"generate": "generate", "transform_query": "transform_query"}
#     )
#     graph.add_edge("transform_query", "retrieve")
#     graph.add_edge("generate", END)
#     return graph.compile()


# # Compile once at module level (cached between reruns via Streamlit)
# @st.cache_resource
# def get_rag_graph():
#     return build_rag_graph()

# # ════════════════════════════════════════════════════════
# # SESSION STATE
# # ════════════════════════════════════════════════════════

# EMBEDDING_MODELS = {
#     "BGE Base (Recommended)": "BAAI/bge-base-en-v1.5",
#     "MiniLM L6 (Fastest)": "sentence-transformers/all-MiniLM-L6-v2",
#     "MPNet Base (Highest Quality)": "sentence-transformers/all-mpnet-base-v2",
# }

# def init_session():
#     defaults = {
#         "vectorstore": None,
#         "chat_history": [],
#         "pdf_hashes": set(),
#         "chunk_info": {},
#         "last_processed_query": None,
#         "eval_results": None,
#         "interaction_log": [],   # Stores {question, answer, retrieved_docs} for eval
#         "faiss_loaded": False,
#     }
#     for k, v in defaults.items():
#         if k not in st.session_state:
#             st.session_state[k] = v

# init_session()

# # ════════════════════════════════════════════════════════
# # SIDEBAR
# # ════════════════════════════════════════════════════════

# with st.sidebar:
#     st.header("⚙️ Configuration")

#     st.subheader("🤖 Model Settings")
#     model_choice = st.selectbox(
#         "LLM Model",
#         ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
#         help="8B = Fast, 70B = Better Quality"
#     )
#     temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)

#     st.subheader("🧠 Embedding Model")
#     embedding_label = st.selectbox(
#         "Embedding Model",
#         list(EMBEDDING_MODELS.keys()),
#         help="BGE Base = best balance | MiniLM = fastest | MPNet = highest quality"
#     )
#     EMBEDDING_MODEL = EMBEDDING_MODELS[embedding_label]
#     # Warn if model changed while vectorstore exists
#     if st.session_state.get("active_embedding_model") and \
#        st.session_state.active_embedding_model != EMBEDDING_MODEL and \
#        st.session_state.vectorstore is not None:
#         st.warning("⚠️ Embedding model changed! Clear documents and re-upload to rebuild the index.")

#     st.subheader("📑 Document Settings")
#     chunk_size = st.slider("Chunk Size", 200, 2000, 1000, 100)
#     overlap_pct = st.slider("Overlap %", 5, 40, 20, 5)
#     # Track active embedding model in session state
#     st.session_state.active_embedding_model = EMBEDDING_MODEL

#     st.subheader("🔍 Retrieval")
#     k_retrieve = st.slider("Chunks to Retrieve", 3, 15, 6)

#     st.subheader("💾 Memory")
#     memory_window = st.slider("Memory Window (exchanges)", 2, 10, 5)

#     # Initialize or update memory if window size changes
#     if "memory" not in st.session_state:
#         llm_for_memory = get_llm(model_choice, temperature)
#         st.session_state.memory = DualRAGMemory(buffer_size=memory_window, llm=llm_for_memory)
#     elif st.session_state.memory.buffer_size != memory_window:
#         old = st.session_state.memory
#         llm_for_memory = get_llm(model_choice, temperature)
#         st.session_state.memory = DualRAGMemory(buffer_size=memory_window, llm=llm_for_memory)
#         st.session_state.memory.token_count = old.token_count
#         st.session_state.memory.interaction_count = old.interaction_count

#     st.caption(f"Status: {st.session_state.memory.get_status()}")
#     st.caption(f"Tokens: {st.session_state.memory.token_count}")
#     st.caption(f"Exchanges: {st.session_state.memory.interaction_count}")

#     if st.button("🔄 Reset All", use_container_width=True):
#         st.session_state.memory.reset()
#         st.session_state.chat_history = []
#         st.session_state.last_processed_query = None
#         st.session_state.eval_results = None
#         st.session_state.interaction_log = []
#         st.success("✅ Reset complete!")
#         st.rerun()

# # ════════════════════════════════════════════════════════
# # LOAD FAISS ON STARTUP (once per session)
# # ════════════════════════════════════════════════════════

# if not st.session_state.faiss_loaded and st.session_state.vectorstore is None:
#     embeddings = get_embeddings(EMBEDDING_MODEL)
#     loaded = load_faiss(embeddings, EMBEDDING_MODEL)
#     if loaded:
#         st.session_state.vectorstore = loaded
#         st.sidebar.success("📂 FAISS index loaded from disk")
#     st.session_state.faiss_loaded = True

# # ════════════════════════════════════════════════════════
# # MAIN LAYOUT
# # ════════════════════════════════════════════════════════

# st.title("📦 RAG Chatbot")
# st.markdown("*Delivery System Documentation Assistant*")

# tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📚 Documents", "📜 History", "📊 Evaluation"])

# # ════════════════════════════════════════════════════════
# # TAB 1: CHAT
# # ════════════════════════════════════════════════════════

# with tab1:
#     col1, col2 = st.columns([4, 1])
#     with col1:
#         uploaded_files = st.file_uploader("📤 Upload PDF", type=["pdf"], accept_multiple_files=True)
#     with col2:
#         if st.button("Clear Docs", use_container_width=True):
#             st.session_state.vectorstore = None
#             st.session_state.pdf_hashes = set()
#             st.session_state.chunk_info = {}
#             st.success("✅ Cleared!")
#             st.rerun()

#     # PDF Processing
#     if uploaded_files:
#         new_files = [
#             (pdf, hashlib.md5(pdf.getvalue()).hexdigest())
#             for pdf in uploaded_files
#             if hashlib.md5(pdf.getvalue()).hexdigest() not in st.session_state.pdf_hashes
#         ]

#         if new_files:
#             progress_bar = st.progress(0)
#             status_text = st.empty()
#             embeddings = get_embeddings(EMBEDDING_MODEL)

#             for idx, (pdf, file_hash) in enumerate(new_files):
#                 status_text.text(f"📄 Processing: {pdf.name}")
#                 try:
#                     page_docs, num_pages = extract_text_from_pdf(pdf.getvalue(), pdf.name)
#                     if not page_docs:
#                         st.warning(f"⚠️ No text in {pdf.name}")
#                         continue

#                     overlap = int(chunk_size * overlap_pct / 100)
#                     docs = split_text_with_pages(page_docs, chunk_size, overlap)

#                     if not docs:
#                         st.warning(f"⚠️ Could not split {pdf.name}")
#                         continue

#                     char_counts = [len(d.page_content) for d in docs]
#                     st.session_state.chunk_info[pdf.name] = {
#                         "chunks": len(docs),
#                         "avg_size": round(sum(char_counts) / len(char_counts)),
#                         "pages": num_pages,
#                         "total_chars": sum(char_counts)
#                     }

#                     status_text.text(f"🔍 Indexing: {pdf.name}")
#                     if st.session_state.vectorstore is None:
#                         st.session_state.vectorstore = FAISS.from_documents(docs, embeddings)
#                     else:
#                         st.session_state.vectorstore.add_documents(docs)

#                     st.session_state.pdf_hashes.add(file_hash)
#                 except Exception as e:
#                     st.error(f"❌ Error processing {pdf.name}: {e}")

#                 progress_bar.progress((idx + 1) / len(new_files))

#             # Persist FAISS to disk
#             if st.session_state.vectorstore:
#                 save_faiss(st.session_state.vectorstore, EMBEDDING_MODEL)

#             progress_bar.empty()
#             status_text.empty()
#             st.success(f"✅ Loaded {len(new_files)} PDF(s)!")

#     st.divider()

#     # Chat Interface
#     if st.session_state.vectorstore is None:
#         st.info("⬆️ Upload a PDF to start chatting")
#     else:
#         # Render existing history
#         for msg in st.session_state.chat_history:
#             with st.chat_message(msg["role"]):
#                 st.write(msg["content"])
#                 if "time" in msg:
#                     st.caption(f"⏱️ {msg['time']:.2f}s")

#         query = st.chat_input("Ask a question about your documents...")

#         if query and query != st.session_state.last_processed_query:
#             st.session_state.last_processed_query = query

#             with st.chat_message("user"):
#                 st.write(query)

#             with st.spinner("🤔 Analyzing..."):
#                 try:
#                     start_time = time.time()
#                     llm = get_llm(model_choice, temperature)
#                     adaptive_k = get_adaptive_k(query, k_retrieve)

#                     # ── LangGraph agentic RAG pipeline ──
#                     rag_graph = get_rag_graph()
#                     initial_state: RAGState = {
#                         "query": query,
#                         "documents": [],
#                         "answer": "",
#                         "sources": [],
#                         "retrieval_attempts": 0,
#                         "document_grade": "",
#                         "conversation_summary": st.session_state.memory.get_summary(),
#                         "recent_history": st.session_state.memory.get_recent(),
#                         "adaptive_k": adaptive_k,
#                         "vectorstore": st.session_state.vectorstore,
#                         "llm": llm,
#                     }
#                     final_state = rag_graph.invoke(initial_state)

#                     answer = final_state["answer"]
#                     retrieved_docs = final_state["documents"]
#                     sources = final_state["sources"]
#                     retries = final_state["retrieval_attempts"] - 1  # attempts beyond first
#                     doc_grade = final_state["document_grade"]
#                     elapsed = time.time() - start_time

#                     # Update memory
#                     st.session_state.memory.add_exchange(query, answer)

#                     # Log for evaluation
#                     st.session_state.interaction_log.append({
#                         "question": query,
#                         "answer": answer,
#                         "retrieved_docs": retrieved_docs
#                     })
#                     st.session_state.interaction_log = st.session_state.interaction_log[-10:]

#                     # Display response
#                     with st.chat_message("assistant"):
#                         st.write(answer)
#                         col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
#                         with col1:
#                             st.caption(f"📎 {' · '.join(sources[:3])}")
#                         with col2:
#                             st.caption(f"⏱️ {elapsed:.2f}s")
#                         with col3:
#                             st.caption(f"📄 {len(retrieved_docs)} chunks")
#                         with col4:
#                             grade_icon = "🟢" if doc_grade == "relevant" else "🟡"
#                             retry_txt = f" (retry ×{retries})" if retries > 0 else ""
#                             st.caption(f"{grade_icon} {doc_grade}{retry_txt}")

#                         with st.expander("📋 Retrieved Chunks"):
#                             for i, doc in enumerate(retrieved_docs[:6]):
#                                 src = doc.metadata.get("source", "Unknown")
#                                 page = doc.metadata.get("page", "")
#                                 st.markdown(f"**Chunk {i+1}** — `{src}` | Page {page}")
#                                 st.text(doc.page_content[:400] + ("..." if len(doc.page_content) > 400 else ""))
#                                 st.divider()

#                     # Store in history
#                     st.session_state.chat_history.append({"role": "user", "content": query})
#                     st.session_state.chat_history.append({
#                         "role": "assistant",
#                         "content": answer,
#                         "time": elapsed
#                     })

#                 except Exception as e:
#                     st.error(f"❌ Error: {e}")

# # ════════════════════════════════════════════════════════
# # TAB 2: DOCUMENTS
# # ════════════════════════════════════════════════════════

# with tab2:
#     st.header("📚 Document Information")

#     if not st.session_state.chunk_info:
#         st.info("No documents loaded yet")
#     else:
#         col1, col2, col3, col4 = st.columns(4)
#         col1.metric("Files", len(st.session_state.chunk_info))
#         col2.metric("Total Chunks", sum(v["chunks"] for v in st.session_state.chunk_info.values()))
#         col3.metric("Total Pages", sum(v["pages"] for v in st.session_state.chunk_info.values()))
#         col4.metric("Total Size", f"{sum(v['total_chars'] for v in st.session_state.chunk_info.values()) // 1000}KB")

#         st.divider()
#         for fname, info in st.session_state.chunk_info.items():
#             with st.expander(f"📄 {fname}"):
#                 c1, c2, c3, c4 = st.columns(4)
#                 c1.metric("Chunks", info["chunks"])
#                 c2.metric("Avg Size", f"{info['avg_size']} chars")
#                 c3.metric("Total Size", f"{info['total_chars']:,} chars")
#                 c4.metric("Pages", info["pages"])
#                 avg = info["avg_size"]
#                 if avg < 300:
#                     st.warning("⚠️ Chunks are small — consider increasing chunk size")
#                 elif avg > 1500:
#                     st.warning("⚠️ Chunks are large — consider reducing chunk size")
#                 else:
#                     st.success("✅ Optimal chunk size")

# # ════════════════════════════════════════════════════════
# # TAB 3: HISTORY
# # ════════════════════════════════════════════════════════

# with tab3:
#     st.header("📜 Chat History")

#     if not st.session_state.chat_history:
#         st.info("No conversation yet")
#     else:
#         user_msgs = [m for m in st.session_state.chat_history if m["role"] == "user"]
#         asst_msgs = [m for m in st.session_state.chat_history if m["role"] == "assistant"]
#         col1, col2 = st.columns(2)
#         col1.metric("User Messages", len(user_msgs))
#         col2.metric("Responses", len(asst_msgs))

#         st.divider()
#         for msg in st.session_state.chat_history:
#             icon = "🧑" if msg["role"] == "user" else "🤖"
#             st.write(f"**{icon} {msg['role'].upper()}**")
#             content = msg["content"]
#             st.write(content[:300] + ("..." if len(content) > 300 else content[300:]))
#             if "time" in msg:
#                 st.caption(f"⏱️ {msg['time']:.2f}s")
#             st.divider()

# # ════════════════════════════════════════════════════════
# # TAB 4: LIVE EVALUATION
# # ════════════════════════════════════════════════════════

# with tab4:
#     st.header("📊 Live RAG Evaluation Dashboard")
#     st.markdown("Evaluate recent interactions using the existing LLM. Scores are based on retrieval quality, faithfulness, and hallucination risk.")

#     interaction_count = len(st.session_state.interaction_log)

#     if interaction_count == 0:
#         st.info("💬 Ask at least one question in the Chat tab first — the evaluation button will activate once you have interactions to score.")

#     # Always show slider + button — disabled when no interactions
#     n_to_eval = st.slider(
#         "Number of recent interactions to evaluate",
#         min_value=1,
#         max_value=max(2, interaction_count),   # Always >= 2 to avoid min==max crash
#         value=max(1, min(3, interaction_count)),
#         disabled=(interaction_count == 0)
#     )

#     if interaction_count > 0:
#         st.write(f"**{interaction_count}** interaction(s) available for evaluation.")

#     run_eval = st.button(
#         "🔍 Run Evaluation",
#         type="primary",
#         use_container_width=True,
#         disabled=(interaction_count == 0),
#         help="Ask questions in the Chat tab first to enable evaluation."
#     )

#     if run_eval and interaction_count > 0:
#         with st.spinner("🤔 Evaluating... (1 LLM call per interaction)"):
#             try:
#                 llm = get_llm(model_choice, temperature)
#                 evaluator = RAGEvaluator(llm=llm)
#                 recent = st.session_state.interaction_log[-n_to_eval:]
#                 batch_result = evaluator.evaluate_batch(recent)
#                 batch_result["_n_eval"] = n_to_eval
#                 st.session_state.eval_results = batch_result
#             except Exception as e:
#                 st.error(f"❌ Evaluation failed: {e}")

#     # Display results — always shown if available (persists across reruns)
#     if st.session_state.eval_results:
#         res = st.session_state.eval_results

#         if res.get("error") and res.get("count", 0) == 0:
#             st.error(f"Evaluation error: {res['error']}")
#         else:
#             st.divider()
#             st.subheader("📈 Aggregate Scores")

#             health = res["overall_health"]
#             health_label = health_to_label(health)
#             st.metric("🏥 Overall Health Score", f"{health}/100", delta=health_label)
#             st.progress(health / 100)

#             st.divider()

#             c1, c2, c3, c4 = st.columns(4)
#             rq = res["retrieval_quality"]
#             cc = res["context_coverage"]
#             sg = res["source_grounding"]
#             hr = res["hallucination_risk"]
#             fs = res["faithfulness_score"]

#             with c1:
#                 st.metric("🔍 Retrieval Quality", f"{rq}/10")
#                 st.caption(score_to_label(rq))
#                 st.progress(rq / 10)

#             with c2:
#                 st.metric("📖 Context Coverage", f"{cc}/10")
#                 st.caption(score_to_label(cc))
#                 st.progress(cc / 10)

#             with c3:
#                 st.metric("📌 Faithfulness Score", f"{fs}/100")
#                 st.caption(score_to_label(sg))
#                 st.progress(fs / 100)

#             with c4:
#                 st.metric("⚠️ Hallucination Risk", f"{hr}/10")
#                 st.caption(score_to_label(hr, invert=True))
#                 st.progress(hr / 10)

#             st.divider()

#             if res.get("results"):
#                 st.subheader("🔎 Per-Interaction Breakdown")
#                 _n = res.get("_n_eval", len(res["results"]))
#                 recent_log = st.session_state.interaction_log[-_n:]

#                 for i, (interaction, r) in enumerate(zip(recent_log, res["results"])):
#                     q_preview = interaction["question"][:80] + ("..." if len(interaction["question"]) > 80 else "")
#                     status = "✅" if r.get("error") is None else "❌"
#                     with st.expander(f"{status} Interaction {i+1}: {q_preview}"):
#                         if r.get("error"):
#                             st.warning(f"Evaluation error: {r['error']}")
#                         else:
#                             ic1, ic2, ic3, ic4 = st.columns(4)
#                             ic1.metric("Retrieval", f"{r['retrieval_quality']}/10")
#                             ic2.metric("Coverage", f"{r['context_coverage']}/10")
#                             ic3.metric("Grounding", f"{r['source_grounding']}/10")
#                             ic4.metric("Hallucination", f"{r['hallucination_risk']}/10")
#                             st.caption(f"💬 **Reasoning:** {r.get('reasoning', 'N/A')}")

# # ════════════════════════════════════════════════════════
# # FOOTER
# # ════════════════════════════════════════════════════════

# st.divider()
# st.markdown("""
# <div style='text-align: center; color: #888; font-size: 12px;'>
# ✨ Production-Ready RAG System &nbsp;|&nbsp;
# 📦 bge-base-en embeddings &nbsp;|&nbsp;
# 🚀 FAISS + Groq + Dual Memory + Live Evaluation
# </div>
# """, unsafe_allow_html=True)


























# import streamlit as st
# import fitz
# import os
# import hashlib
# import time
# import json
# import re
# import math
# import pickle
# from typing import List, Tuple, Optional, Dict
# from dotenv import load_dotenv

# from langchain_groq import ChatGroq
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.documents import Document
# from langgraph.graph import StateGraph, END
# from typing_extensions import TypedDict

# from rag_evaluation_framework import RAGEvaluator, score_to_label, health_to_label

# # ════════════════════════════════════════════════════════
# # SETUP
# # ════════════════════════════════════════════════════════

# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# FAISS_INDEX_PATH = "./faiss_index"

# if not GROQ_API_KEY:
#     st.error("❌ GROQ_API_KEY not found in .env file")
#     st.stop()

# st.set_page_config(
#     page_title="RAG Chatbot",
#     page_icon="📦",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ════════════════════════════════════════════════════════
# # MEMORY CLASS
# # ════════════════════════════════════════════════════════

# class DualRAGMemory:
#     """
#     Simple dual memory: sliding window buffer + periodic LLM summary.
#     No LangChain memory classes needed — fully version-safe.
#     """

#     def __init__(self, buffer_size: int = 5, llm=None):
#         self.buffer_size = buffer_size
#         self.llm = llm
#         self._exchanges: List[dict] = []   # [{"q": ..., "a": ...}]
#         self._summary: str = ""
#         self.token_count = 0
#         self.interaction_count = 0

#     def add_exchange(self, query: str, response: str):
#         """Add exchange; trim buffer; progressively update summary every turn."""
#         self._exchanges.append({"q": query, "a": response})
#         if len(self._exchanges) > self.buffer_size:
#             self._exchanges = self._exchanges[-self.buffer_size:]
#         self.token_count += len(query.split()) + len(response.split())
#         self.interaction_count += 1
#         if self.llm:
#             self._progressive_summary(query, response)

#     def _progressive_summary(self, new_q: str, new_a: str):
#         """
#         Progressive summarisation: compress(prev_summary + new_exchange).
#         Never loses prior context — each update compounds on the last.
#         """
#         try:
#             prev = self._summary or "No prior summary."
#             prompt = (
#                 "You are maintaining a running conversation summary.\n\n"
#                 f"PREVIOUS SUMMARY:\n{prev}\n\n"
#                 f"NEW EXCHANGE:\nUser: {new_q}\nAssistant: {new_a}\n\n"
#                 "Update the summary to include the new exchange. "
#                 "Keep it under 5 sentences. Preserve ALL important facts from the previous summary. "
#                 "Output ONLY the updated summary, nothing else."
#             )
#             result = self.llm.invoke(prompt)
#             self._summary = result.content.strip()
#         except Exception:
#             pass  # Silent fail — summary is optional

#     def get_recent(self) -> str:
#         """Return recent exchanges as formatted text."""
#         if not self._exchanges:
#             return ""
#         lines = []
#         for ex in self._exchanges:
#             lines.append(f"User: {ex['q']}")
#             lines.append(f"Assistant: {ex['a']}")
#         return "\n".join(lines)

#     def get_summary(self) -> str:
#         """Return the current conversation summary."""
#         return self._summary

#     def get_status(self) -> str:
#         return "✅ Healthy" if self.token_count < 5000 else "⚠️ High"

#     def reset(self):
#         self._exchanges = []
#         self._summary = ""
#         self.token_count = 0
#         self.interaction_count = 0

# # ════════════════════════════════════════════════════════
# # CACHED RESOURCES
# # ════════════════════════════════════════════════════════

# @st.cache_resource
# def get_llm(model_name: str, temperature: float):
#     return ChatGroq(api_key=GROQ_API_KEY, model_name=model_name, temperature=temperature)

# @st.cache_resource
# def get_embeddings(model_name: str = "BAAI/bge-base-en-v1.5"):
#     return HuggingFaceEmbeddings(
#         model_name=model_name,
#         model_kwargs={"device": "cpu"},
#         encode_kwargs={"normalize_embeddings": True}
#     )

# # ════════════════════════════════════════════════════════
# # PDF PROCESSING
# # ════════════════════════════════════════════════════════

# def extract_text_from_pdf(file_bytes: bytes, filename: str) -> Tuple[List, int]:
#     """Extract text with page-level metadata."""
#     try:
#         doc = fitz.open(stream=file_bytes, filetype="pdf")
#         page_docs = []
#         for i, page in enumerate(doc):
#             text = page.get_text("text").strip()
#             if text:
#                 page_docs.append({"text": text, "page": i + 1, "source": filename})
#         return page_docs, len(doc)
#     except Exception as e:
#         st.error(f"❌ PDF error: {e}")
#         return [], 0

# # Header patterns for technical PDFs (markdown headers, numbered sections, ALL-CAPS titles)
# _HEADER_RE = re.compile(
#     r"^(#{1,3}\s.{3,}|[A-Z][A-Z0-9 ]{5,50}$|\d+\.\d*\s+[A-Z].{4,}|Chapter\s+\d+|SECTION\s+\d+)",
#     re.MULTILINE
# )

# def _detect_section(text: str) -> str:
#     """Return the first header found in text, or empty string."""
#     m = _HEADER_RE.search(text)
#     return m.group(0).strip()[:80] if m else ""

# def split_text_with_pages(page_docs: list, chunk_size: int = 1000, overlap: int = 200):
#     """
#     Header-aware chunking: detects section headings and annotates each chunk
#     with its section. Falls back to RecursiveCharacterTextSplitter boundaries.
#     Reason chosen over SemanticChunker: no heavy NLP dependency, preserves
#     document hierarchy, fast, deterministic for technical PDFs.
#     """
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=overlap,
#         separators=["\n\n", "\n", ". ", " ", ""]
#     )
#     all_chunks = []
#     for page_doc in page_docs:
#         text   = page_doc["text"]
#         source = page_doc["source"]
#         page   = page_doc["page"]
#         section = _detect_section(text)
#         chunks = splitter.create_documents([text])
#         for chunk in chunks:
#             chunk.metadata["source"]  = source
#             chunk.metadata["page"]    = page
#             if section:
#                 chunk.metadata["section"] = section
#         all_chunks.extend(chunks)
#     return all_chunks

# # ════════════════════════════════════════════════════════
# # ADAPTIVE RETRIEVAL
# # ════════════════════════════════════════════════════════

# COMPLEX_KEYWORDS = [
#     "compare", "difference", "explain", "analyze", "how does", "why does",
#     "summarize", "describe", "elaborate", "relationship", "architecture",
#     "workflow", "process", "mechanism", "contrast", "evaluate", "assess"
# ]

# def get_adaptive_k(query: str, base_k: int) -> int:
#     """Return fewer chunks for simple queries, more for complex ones."""
#     q = query.lower()
#     is_complex = len(query.split()) > 12 or any(kw in q for kw in COMPLEX_KEYWORDS)
#     return base_k if is_complex else max(3, base_k // 2)

# # ════════════════════════════════════════════════════════
# # FAISS PERSISTENCE
# # ════════════════════════════════════════════════════════

# def save_faiss(vectorstore, embedding_model: str):
#     """Persist FAISS index and record which embedding model built it."""
#     try:
#         vectorstore.save_local(FAISS_INDEX_PATH)
#         with open(f"{FAISS_INDEX_PATH}/embedding_model.txt", "w") as f:
#             f.write(embedding_model)
#     except Exception as e:
#         st.warning(f"⚠️ Could not save FAISS index: {e}")

# def load_faiss(embeddings, embedding_model: str) -> Optional[object]:
#     """Load persisted FAISS index if embedding model matches."""
#     model_file = f"{FAISS_INDEX_PATH}/embedding_model.txt"
#     index_file = f"{FAISS_INDEX_PATH}/index.faiss"
#     if not (os.path.exists(index_file) and os.path.exists(model_file)):
#         return None
#     try:
#         saved_model = open(model_file).read().strip()
#         if saved_model != embedding_model:
#             return None  # Model mismatch — must rebuild
#         return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
#     except Exception:
#         return None

# # ════════════════════════════════════════════════════════
# # BM25 — SPARSE RETRIEVAL
# # ════════════════════════════════════════════════════════

# BM25_PATH = f"{FAISS_INDEX_PATH}/bm25.pkl"

# def build_bm25(docs: List) -> Tuple[object, List]:
#     """Build BM25 index from a flat list of Document objects."""
#     from rank_bm25 import BM25Okapi
#     tokenized = [d.page_content.lower().split() for d in docs]
#     return BM25Okapi(tokenized), docs

# def save_bm25(bm25_obj, corpus: List):
#     """Persist BM25 index and corpus to disk alongside FAISS."""
#     try:
#         os.makedirs(FAISS_INDEX_PATH, exist_ok=True)
#         with open(BM25_PATH, "wb") as f:
#             pickle.dump({"bm25": bm25_obj, "corpus": corpus}, f)
#     except Exception as e:
#         st.warning(f"⚠️ BM25 save failed: {e}")

# def load_bm25() -> Tuple[Optional[object], Optional[List]]:
#     """Reload persisted BM25 index from disk."""
#     if not os.path.exists(BM25_PATH):
#         return None, None
#     try:
#         with open(BM25_PATH, "rb") as f:
#             data = pickle.load(f)
#         return data["bm25"], data["corpus"]
#     except Exception:
#         return None, None

# def hybrid_retrieve(query: str, vectorstore, bm25_obj, bm25_corpus: List,
#                     k: int, bm25_weight: float = 0.3) -> List:
#     """
#     Merge dense FAISS results with sparse BM25 results.
#     bm25_weight controls how many of the k slots go to BM25.
#     """
#     n_bm25 = max(1, round(k * bm25_weight))
#     n_dense = max(1, k - n_bm25)

#     # Dense retrieval
#     dense_docs = vectorstore.similarity_search(query, k=n_dense * 2)

#     # Sparse BM25 retrieval
#     bm25_docs: List = []
#     if bm25_obj and bm25_corpus:
#         tokens = query.lower().split()
#         scores = bm25_obj.get_scores(tokens)
#         top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:n_bm25 * 2]
#         bm25_docs = [bm25_corpus[i] for i in top_idx if scores[i] > 0]

#     # Merge, deduplicate by first 80 chars of content
#     seen: set = set()
#     merged: List = []
#     for doc in dense_docs[:n_dense] + bm25_docs[:n_bm25]:
#         key = doc.page_content[:80]
#         if key not in seen:
#             seen.add(key)
#             merged.append(doc)
#     return merged[:k]

# # ════════════════════════════════════════════════════════
# # PROMPT
# # ════════════════════════════════════════════════════════

# SYSTEM_PROMPT = ChatPromptTemplate.from_template("""You are a strict document-based question answering assistant.

# CONVERSATION SUMMARY (for context):
# {conversation_summary}

# RECENT EXCHANGES:
# {recent_history}

# RETRIEVED DOCUMENTS:
# {context}

# QUESTION:
# {input}

# INSTRUCTIONS:
# 1. Answer ONLY using information explicitly present in the retrieved documents above.
# 2. Do NOT use prior knowledge, training data, or external information.
# 3. Do NOT speculate, guess, or invent details not in the documents.
# 4. If partially supported: provide only the supported part, then state "The remaining information is not available in the provided documents."
# 5. If not supported at all: respond ONLY "This information is not available in the provided documents."
# 6. Cite sources using: [filename | Page N] after every factual claim.
# 7. Keep answers concise and accurate.
# 8. Prefer accuracy over completeness.

# FINAL ANSWER:""")

# # ════════════════════════════════════════════════════════
# # LANGGRAPH — AGENTIC RAG STATE & NODES
# # ════════════════════════════════════════════════════════

# class RAGState(TypedDict):
#     """Typed state passed through the LangGraph RAG pipeline."""
#     query: str
#     original_query: str
#     documents: List[Document]
#     answer: str
#     sources: List[str]
#     retrieval_attempts: int
#     document_grade: str          # "relevant" | "not_relevant"
#     conversation_summary: str
#     recent_history: str
#     adaptive_k: int
#     vectorstore: object
#     bm25_index: object
#     bm25_corpus: List
#     bm25_weight: float
#     llm: object
#     rewrite_log: List
#     confidence: Dict
#     use_reranker: bool
#     reranker: object


# # ── Prompts for grading and rewriting ────────────────────

# BATCH_GRADE_PROMPT = """You are a document relevance grader for a RAG system.

# Question: {question}

# Below are {n} retrieved document excerpts. For each, decide if it contains information useful for answering the question.

# {documents}

# Respond ONLY with a JSON array — one entry per document, in order:
# [{{"id": 1, "score": "relevant"}}, {{"id": 2, "score": "not_relevant"}}, ...]
# All {n} documents must appear. No extra text."""

# REWRITE_PROMPT = """You are a query rewriter for a RAG system.
# The original query failed to retrieve useful documents. Rewrite it to be clearer and more specific, preserving the original intent.

# Original query: {question}

# Rewritten query (output ONLY the rewritten query, nothing else):"""


# # ── Confidence scoring (no LLM calls) ────────────────────

# def compute_confidence(docs: List, answer: str) -> Dict:
#     """Lightweight confidence signals from retrieved docs and answer text."""
#     if not docs or not answer:
#         return {"retrieval": 0.0, "grounding": 0.0}
#     # Retrieval confidence: proxy via doc count (6 docs = max)
#     retrieval_conf = round(min(1.0, len(docs) / 6), 2)
#     # Grounding confidence: keyword overlap between context and answer
#     stop = {"the", "a", "an", "is", "are", "was", "were", "in", "on",
#             "at", "to", "for", "of", "and", "or", "not", "it", "this", "that"}
#     ctx_words: set = set()
#     for d in docs:
#         ctx_words.update(w.lower() for w in d.page_content.split())
#     ans_words = {w.lower() for w in answer.split()} - stop
#     grounding = round(len(ans_words & ctx_words) / max(len(ans_words), 1), 2)
#     return {"retrieval": retrieval_conf, "grounding": min(1.0, grounding)}


# # ── Optional Cross-Encoder reranker ──────────────────────

# @st.cache_resource
# def get_reranker(model_name: str = "BAAI/bge-reranker-base"):
#     from sentence_transformers import CrossEncoder
#     return CrossEncoder(model_name)

# def rerank_docs(reranker, query: str, docs: List, top_k: int = 5) -> List:
#     """Score all candidates with CrossEncoder, return top_k."""
#     if not docs:
#         return docs
#     pairs = [(query, d.page_content[:512]) for d in docs]
#     scores = reranker.predict(pairs)
#     ranked = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)
#     return [d for _, d in ranked[:top_k]]


# def node_retrieve(state: RAGState) -> RAGState:
#     """Hybrid BM25 + FAISS retrieval with optional CrossEncoder reranking."""
#     query = state["query"]
#     k = state["adaptive_k"]

#     # Retrieve more candidates when reranker is active
#     fetch_k = 15 if state.get("use_reranker") else k

#     docs = hybrid_retrieve(
#         query=query,
#         vectorstore=state["vectorstore"],
#         bm25_obj=state.get("bm25_index"),
#         bm25_corpus=state.get("bm25_corpus") or [],
#         k=fetch_k,
#         bm25_weight=state.get("bm25_weight", 0.3),
#     )

#     # Optional reranking: score 15 candidates, keep top 5
#     if state.get("use_reranker") and state.get("reranker") and docs:
#         docs = rerank_docs(state["reranker"], query, docs, top_k=min(5, k))

#     return {**state, "documents": docs, "retrieval_attempts": state["retrieval_attempts"] + 1}


# def node_grade_documents(state: RAGState) -> RAGState:
#     """
#     Batch-grade all retrieved docs in ONE LLM call (was N separate calls).
#     Never marks docs as relevant on parse failure — conservative by default.
#     """
#     docs = state["documents"]
#     if not docs:
#         return {**state, "document_grade": "not_relevant"}

#     # Build batch prompt
#     doc_block = ""
#     for i, doc in enumerate(docs[:6]):
#         section = doc.metadata.get("section", "")
#         sec_note = f" [{section}]" if section else ""
#         doc_block += f"[Document {i+1}{sec_note}]:\n{doc.page_content[:400]}\n\n"

#     prompt = BATCH_GRADE_PROMPT.format(
#         question=state["query"],
#         n=min(len(docs), 6),
#         documents=doc_block.strip()
#     )

#     try:
#         result = state["llm"].invoke(prompt)
#         raw = result.content.strip()
#         raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
#         grades = json.loads(raw)
#         relevant_count = sum(1 for g in grades if isinstance(g, dict) and g.get("score") == "relevant")
#         grade = "relevant" if relevant_count >= 1 else "not_relevant"
#     except Exception:
#         # Conservative: mark not_relevant on any parse failure
#         grade = "not_relevant"

#     return {**state, "document_grade": grade}


# def node_transform_query(state: RAGState) -> RAGState:
#     """Rewrite query with semantic similarity guard to prevent drift."""
#     original = state["query"]
#     rewrite_log = list(state.get("rewrite_log") or [])
#     try:
#         prompt = REWRITE_PROMPT.format(question=original)
#         result = state["llm"].invoke(prompt)
#         new_query = result.content.strip()

#         # Semantic guard: word-overlap proxy. If >85% same words, skip rewrite.
#         orig_words = set(original.lower().split())
#         new_words  = set(new_query.lower().split())
#         overlap = len(orig_words & new_words) / max(len(orig_words), 1)
#         if overlap > 0.85:
#             new_query = original  # Rewrite too similar — no benefit

#     except Exception:
#         new_query = original

#     rewrite_log.append({"original": original, "rewritten": new_query})
#     return {**state, "query": new_query, "rewrite_log": rewrite_log}


# def node_generate(state: RAGState) -> RAGState:
#     """Generate answer; compute confidence scores from retrieved docs."""
#     docs = state["documents"]
#     context_parts, sources = [], []
#     for doc in docs:
#         src  = doc.metadata.get("source", "Unknown")
#         page = doc.metadata.get("page", "")
#         sect = doc.metadata.get("section", "")
#         citation = f"{src} | Page {page}" + (f" · {sect}" if sect else "") if page else src
#         if citation not in sources:
#             sources.append(citation)
#         context_parts.append(f"[{citation}]\n{doc.page_content}")

#     context = "\n\n---\n\n".join(context_parts) if context_parts else "No documents retrieved."
#     formatted = SYSTEM_PROMPT.format(
#         conversation_summary=state["conversation_summary"] or "No prior summary.",
#         recent_history=state["recent_history"] or "No recent exchanges.",
#         context=context,
#         input=state["query"]
#     )
#     response = state["llm"].invoke(formatted)
#     answer = response.content
#     confidence = compute_confidence(docs, answer)
#     return {**state, "answer": answer, "sources": sources, "confidence": confidence}


# def should_retry(state: RAGState) -> str:
#     """Conditional edge: retry with rewritten query or go straight to generate."""
#     if state["document_grade"] == "relevant":
#         return "generate"
#     if state["retrieval_attempts"] < 2:
#         return "transform_query"   # Rewrite and retry once
#     return "generate"              # Give up retrying, generate with what we have


# def build_rag_graph() -> StateGraph:
#     """Compile the LangGraph agentic RAG pipeline."""
#     graph = StateGraph(RAGState)
#     graph.add_node("retrieve", node_retrieve)
#     graph.add_node("grade_documents", node_grade_documents)
#     graph.add_node("transform_query", node_transform_query)
#     graph.add_node("generate", node_generate)

#     graph.set_entry_point("retrieve")
#     graph.add_edge("retrieve", "grade_documents")
#     graph.add_conditional_edges(
#         "grade_documents",
#         should_retry,
#         {"generate": "generate", "transform_query": "transform_query"}
#     )
#     graph.add_edge("transform_query", "retrieve")
#     graph.add_edge("generate", END)
#     return graph.compile()


# # Compile once at module level (cached between reruns via Streamlit)
# @st.cache_resource
# def get_rag_graph():
#     return build_rag_graph()

# # ════════════════════════════════════════════════════════
# # SESSION STATE
# # ════════════════════════════════════════════════════════

# EMBEDDING_MODELS = {
#     "BGE Base (Recommended)": "BAAI/bge-base-en-v1.5",
#     "MiniLM L6 (Fastest)": "sentence-transformers/all-MiniLM-L6-v2",
#     "MPNet Base (Highest Quality)": "sentence-transformers/all-mpnet-base-v2",
# }

# def init_session():
#     defaults = {
#         "vectorstore": None,
#         "bm25_index": None,
#         "bm25_corpus": [],
#         "chat_history": [],
#         "pdf_hashes": set(),
#         "chunk_info": {},
#         "ingestion_timings": {},   # {filename: {extract, chunk, embed, index, save}}
#         "last_processed_query": None,
#         "eval_results": None,
#         "interaction_log": [],
#         "faiss_loaded": False,
#     }
#     for k, v in defaults.items():
#         if k not in st.session_state:
#             st.session_state[k] = v

# init_session()

# # ════════════════════════════════════════════════════════
# # SIDEBAR
# # ════════════════════════════════════════════════════════

# with st.sidebar:
#     st.header("⚙️ Configuration")

#     st.subheader("🤖 LLM Model")
#     model_choice = st.selectbox(
#         "LLM Model",
#         ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
#         help="8B = Fast, 70B = Better Quality"
#     )
#     temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)

#     st.subheader("🧠 Embedding Model")
#     embedding_label = st.selectbox(
#         "Embedding Model",
#         list(EMBEDDING_MODELS.keys()),
#         help="BGE Base = best balance | MiniLM = fastest | MPNet = highest quality"
#     )
#     EMBEDDING_MODEL = EMBEDDING_MODELS[embedding_label]
#     if st.session_state.get("active_embedding_model") and \
#        st.session_state.active_embedding_model != EMBEDDING_MODEL and \
#        st.session_state.vectorstore is not None:
#         st.warning("⚠️ Embedding model changed! Clear docs and re-upload.")

#     st.subheader("📑 Document Settings")
#     chunk_size  = st.slider("Chunk Size", 200, 2000, 1000, 100)
#     overlap_pct = st.slider("Overlap %", 5, 40, 20, 5)
#     st.session_state.active_embedding_model = EMBEDDING_MODEL

#     st.subheader("🔍 Retrieval")
#     k_retrieve  = st.slider("Chunks to Retrieve", 3, 15, 6)
#     bm25_weight = st.slider("BM25 Weight", 0.0, 1.0, 0.3, 0.05,
#                              help="0 = pure FAISS | 1 = pure BM25 | 0.3 = recommended")

#     st.subheader("🎯 Reranker (P2)")
#     use_reranker = st.toggle("Enable Cross-Encoder Reranker", value=False,
#                               help="BAAI/bge-reranker-base. Retrieves 15 candidates → keeps top 5. Adds ~0.5–1s latency.")
#     if use_reranker:
#         st.caption("Fetches 15 candidates, reranks, returns top 5")

#     st.subheader("💾 Memory")
#     memory_window = st.slider("Memory Window (exchanges)", 2, 10, 5)
#     if "memory" not in st.session_state:
#         st.session_state.memory = DualRAGMemory(buffer_size=memory_window,
#                                                 llm=get_llm(model_choice, temperature))
#     elif st.session_state.memory.buffer_size != memory_window:
#         old = st.session_state.memory
#         st.session_state.memory = DualRAGMemory(buffer_size=memory_window,
#                                                 llm=get_llm(model_choice, temperature))
#         st.session_state.memory.token_count      = old.token_count
#         st.session_state.memory.interaction_count = old.interaction_count
#         st.session_state.memory._summary          = old._summary

#     st.caption(f"Status: {st.session_state.memory.get_status()}")
#     st.caption(f"Tokens ≈ {st.session_state.memory.token_count} | Exchanges: {st.session_state.memory.interaction_count}")
#     if st.session_state.memory._summary:
#         with st.expander("📝 Memory Summary"):
#             st.write(st.session_state.memory._summary)

#     if st.button("🔄 Reset All", use_container_width=True):
#         st.session_state.memory.reset()
#         st.session_state.chat_history = []
#         st.session_state.last_processed_query = None
#         st.session_state.eval_results = None
#         st.session_state.interaction_log = []
#         st.success("✅ Reset complete!")
#         st.rerun()

# # ════════════════════════════════════════════════════════
# # LOAD FAISS ON STARTUP (once per session)
# # ════════════════════════════════════════════════════════

# if not st.session_state.faiss_loaded and st.session_state.vectorstore is None:
#     embeddings = get_embeddings(EMBEDDING_MODEL)
#     loaded = load_faiss(embeddings, EMBEDDING_MODEL)
#     if loaded:
#         st.session_state.vectorstore = loaded
#         # Also reload BM25 index from disk
#         bm25_obj, bm25_corpus = load_bm25()
#         if bm25_obj:
#             st.session_state.bm25_index  = bm25_obj
#             st.session_state.bm25_corpus = bm25_corpus
#             st.sidebar.success("📂 FAISS + BM25 loaded from disk")
#         else:
#             st.sidebar.success("📂 FAISS index loaded from disk")
#     st.session_state.faiss_loaded = True

# # ════════════════════════════════════════════════════════
# # MAIN LAYOUT
# # ════════════════════════════════════════════════════════

# st.title("📦 RAG Chatbot")
# st.markdown("*Delivery System Documentation Assistant*")

# tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📚 Documents", "📜 History", "📊 Evaluation"])

# # ════════════════════════════════════════════════════════
# # TAB 1: CHAT
# # ════════════════════════════════════════════════════════

# with tab1:
#     col1, col2 = st.columns([4, 1])
#     with col1:
#         uploaded_files = st.file_uploader("📤 Upload PDF", type=["pdf"], accept_multiple_files=True)
#     with col2:
#         if st.button("Clear Docs", use_container_width=True):
#             st.session_state.vectorstore   = None
#             st.session_state.bm25_index    = None
#             st.session_state.bm25_corpus   = []
#             st.session_state.pdf_hashes    = set()
#             st.session_state.chunk_info    = {}
#             st.session_state.ingestion_timings = {}
#             st.success("✅ Cleared!")
#             st.rerun()

#     # PDF Processing
#     if uploaded_files:
#         new_files = [
#             (pdf, hashlib.md5(pdf.getvalue()).hexdigest())
#             for pdf in uploaded_files
#             if hashlib.md5(pdf.getvalue()).hexdigest() not in st.session_state.pdf_hashes
#         ]

#         if new_files:
#             progress_bar = st.progress(0)
#             status_text  = st.empty()
#             timing_placeholder = st.empty()
#             embeddings = get_embeddings(EMBEDDING_MODEL)
#             all_new_docs: List = []

#             for idx, (pdf, file_hash) in enumerate(new_files):
#                 timings: Dict = {}
#                 status_text.text(f"📄 Processing: {pdf.name}")
#                 try:
#                     # ─ Step 1: PDF extraction ─────────────────────────
#                     t0 = time.time()
#                     page_docs, num_pages = extract_text_from_pdf(pdf.getvalue(), pdf.name)
#                     timings["extract"] = round(time.time() - t0, 2)
#                     if not page_docs:
#                         st.warning(f"⚠️ No text in {pdf.name}")
#                         continue

#                     # ─ Step 2: Chunking ─────────────────────────────
#                     t0 = time.time()
#                     overlap = int(chunk_size * overlap_pct / 100)
#                     docs = split_text_with_pages(page_docs, chunk_size, overlap)
#                     timings["chunk"] = round(time.time() - t0, 2)
#                     if not docs:
#                         st.warning(f"⚠️ Could not split {pdf.name}")
#                         continue

#                     char_counts = [len(d.page_content) for d in docs]
#                     st.session_state.chunk_info[pdf.name] = {
#                         "chunks": len(docs), "avg_size": round(sum(char_counts)/len(char_counts)),
#                         "pages": num_pages, "total_chars": sum(char_counts)
#                     }

#                     # ─ Step 3: Embedding + FAISS indexing ───────────────
#                     status_text.text(f"🔍 Embedding: {pdf.name} ({len(docs)} chunks)")
#                     t0 = time.time()
#                     if st.session_state.vectorstore is None:
#                         st.session_state.vectorstore = FAISS.from_documents(docs, embeddings)
#                     else:
#                         st.session_state.vectorstore.add_documents(docs)
#                     timings["embed_index"] = round(time.time() - t0, 2)

#                     all_new_docs.extend(docs)
#                     st.session_state.pdf_hashes.add(file_hash)
#                     st.session_state.ingestion_timings[pdf.name] = timings

#                 except Exception as e:
#                     st.error(f"❌ Error processing {pdf.name}: {e}")

#                 progress_bar.progress((idx + 1) / len(new_files))

#             # ─ Step 4: Persist FAISS + build & save BM25 ───────
#             if st.session_state.vectorstore:
#                 status_text.text("💾 Saving indexes...")
#                 t0 = time.time()
#                 save_faiss(st.session_state.vectorstore, EMBEDDING_MODEL)
#                 save_t = round(time.time() - t0, 2)

#                 # Rebuild BM25 from all indexed docs (incremental: add new docs to corpus)
#                 t0 = time.time()
#                 existing_corpus = st.session_state.bm25_corpus or []
#                 merged_corpus = existing_corpus + all_new_docs
#                 bm25_obj, bm25_corpus = build_bm25(merged_corpus)
#                 st.session_state.bm25_index  = bm25_obj
#                 st.session_state.bm25_corpus = bm25_corpus
#                 save_bm25(bm25_obj, bm25_corpus)
#                 bm25_t = round(time.time() - t0, 2)

#             progress_bar.empty()
#             status_text.empty()
#             st.success(f"✅ Loaded {len(new_files)} PDF(s)! | FAISS save: {save_t}s | BM25 build: {bm25_t}s")

#     st.divider()

#     # Chat Interface
#     if st.session_state.vectorstore is None:
#         st.info("⬆️ Upload a PDF to start chatting")
#     else:
#         # Render existing history
#         for msg in st.session_state.chat_history:
#             with st.chat_message(msg["role"]):
#                 st.write(msg["content"])
#                 if "time" in msg:
#                     st.caption(f"⏱️ {msg['time']:.2f}s")

#         query = st.chat_input("Ask a question about your documents...")

#         if query and query != st.session_state.last_processed_query:
#             st.session_state.last_processed_query = query

#             with st.chat_message("user"):
#                 st.write(query)

#             with st.spinner("🤔 Analyzing..."):
#                 try:
#                     start_time = time.time()
#                     llm = get_llm(model_choice, temperature)
#                     adaptive_k = get_adaptive_k(query, k_retrieve)

#                     # Load reranker only if toggled on
#                     reranker_obj = get_reranker() if use_reranker else None

#                     rag_graph = get_rag_graph()
#                     initial_state: RAGState = {
#                         "query":                query,
#                         "original_query":       query,
#                         "documents":            [],
#                         "answer":               "",
#                         "sources":              [],
#                         "retrieval_attempts":   0,
#                         "document_grade":       "",
#                         "conversation_summary": st.session_state.memory.get_summary(),
#                         "recent_history":       st.session_state.memory.get_recent(),
#                         "adaptive_k":           adaptive_k,
#                         "vectorstore":          st.session_state.vectorstore,
#                         "bm25_index":           st.session_state.bm25_index,
#                         "bm25_corpus":          st.session_state.bm25_corpus,
#                         "bm25_weight":          bm25_weight,
#                         "llm":                  llm,
#                         "rewrite_log":          [],
#                         "confidence":           {},
#                         "use_reranker":         use_reranker,
#                         "reranker":             reranker_obj,
#                     }
#                     final_state = rag_graph.invoke(initial_state)

#                     answer        = final_state["answer"]
#                     retrieved_docs = final_state["documents"]
#                     sources       = final_state["sources"]
#                     retries       = final_state["retrieval_attempts"] - 1
#                     doc_grade     = final_state["document_grade"]
#                     confidence    = final_state.get("confidence", {})
#                     rewrite_log   = final_state.get("rewrite_log", [])
#                     elapsed       = time.time() - start_time

#                     st.session_state.memory.add_exchange(query, answer)
#                     st.session_state.interaction_log.append({
#                         "question": query, "answer": answer, "retrieved_docs": retrieved_docs
#                     })
#                     st.session_state.interaction_log = st.session_state.interaction_log[-10:]

#                     with st.chat_message("assistant"):
#                         st.write(answer)

#                         # ─ Status bar: grade | retries | time | chunks
#                         c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
#                         with c1:
#                             st.caption(f"📎 {' · '.join(sources[:2])}")
#                         with c2:
#                             grade_icon = "🟢" if doc_grade == "relevant" else "🟡"
#                             retry_txt  = f" (×{retries} retry)" if retries > 0 else ""
#                             st.caption(f"{grade_icon} {doc_grade}{retry_txt}")
#                         with c3:
#                             st.caption(f"⏱️ {elapsed:.2f}s")
#                         with c4:
#                             st.caption(f"📄 {len(retrieved_docs)} chunks")

#                         # ─ Confidence scores
#                         if confidence:
#                             rc = confidence.get("retrieval", 0)
#                             gc = confidence.get("grounding", 0)
#                             cf1, cf2 = st.columns(2)
#                             cf1.metric("📊 Retrieval Conf.", f"{rc:.0%}")
#                             cf2.metric("📌 Grounding Conf.", f"{gc:.0%}")

#                         # ─ Query rewrite log
#                         if rewrite_log and rewrite_log[0]["original"] != rewrite_log[0]["rewritten"]:
#                             with st.expander("🔄 Query was rewritten"):
#                                 for entry in rewrite_log:
#                                     st.markdown(f"**Original:** {entry['original']}")
#                                     st.markdown(f"**Rewritten:** {entry['rewritten']}")

#                         # ─ Retrieved chunks
#                         with st.expander("📋 Retrieved Chunks"):
#                             for i, doc in enumerate(retrieved_docs[:6]):
#                                 src  = doc.metadata.get("source", "Unknown")
#                                 page = doc.metadata.get("page", "")
#                                 sect = doc.metadata.get("section", "")
#                                 header = f"**Chunk {i+1}** — `{src}` | Page {page}"
#                                 if sect:
#                                     header += f" | *{sect}*"
#                                 st.markdown(header)
#                                 st.text(doc.page_content[:400] + ("..." if len(doc.page_content) > 400 else ""))
#                                 st.divider()

#                     st.session_state.chat_history.append({"role": "user", "content": query})
#                     st.session_state.chat_history.append({"role": "assistant", "content": answer, "time": elapsed})

#                 except Exception as e:
#                     st.error(f"❌ Error: {e}")

# # ════════════════════════════════════════════════════════
# # TAB 2: DOCUMENTS
# # ════════════════════════════════════════════════════════

# with tab2:
#     st.header("📚 Document Information")

#     if not st.session_state.chunk_info:
#         st.info("No documents loaded yet")
#     else:
#         col1, col2, col3, col4 = st.columns(4)
#         col1.metric("Files", len(st.session_state.chunk_info))
#         col2.metric("Total Chunks", sum(v["chunks"] for v in st.session_state.chunk_info.values()))
#         col3.metric("Total Pages", sum(v["pages"] for v in st.session_state.chunk_info.values()))
#         col4.metric("Total Size", f"{sum(v['total_chars'] for v in st.session_state.chunk_info.values()) // 1000}KB")

#         st.divider()
#         for fname, info in st.session_state.chunk_info.items():
#             with st.expander(f"📄 {fname}"):
#                 c1, c2, c3, c4 = st.columns(4)
#                 c1.metric("Chunks", info["chunks"])
#                 c2.metric("Avg Size", f"{info['avg_size']} chars")
#                 c3.metric("Total Size", f"{info['total_chars']:,} chars")
#                 c4.metric("Pages", info["pages"])
#                 avg = info["avg_size"]
#                 if avg < 300:
#                     st.warning("⚠️ Chunks are small — consider increasing chunk size")
#                 elif avg > 1500:
#                     st.warning("⚠️ Chunks are large — consider reducing chunk size")
#                 else:
#                     st.success("✅ Optimal chunk size")

#                 # Ingestion timing breakdown
#                 timings = st.session_state.ingestion_timings.get(fname, {})
#                 if timings:
#                     st.caption("**⏱️ Ingestion Timing:**")
#                     tc1, tc2, tc3 = st.columns(3)
#                     tc1.metric("PDF Extract", f"{timings.get('extract', '-')}s")
#                     tc2.metric("Chunking",    f"{timings.get('chunk', '-')}s")
#                     tc3.metric("Embed+Index", f"{timings.get('embed_index', '-')}s")
#                     total = sum(v for v in timings.values() if isinstance(v, (int, float)))
#                     st.caption(f"Total ingestion: **{total:.2f}s** | "
#                                f"Throughput: **{round(info['chunks']/max(timings.get('embed_index',1),0.01))} chunks/s**")

# # ════════════════════════════════════════════════════════
# # TAB 3: HISTORY
# # ════════════════════════════════════════════════════════

# with tab3:
#     st.header("📜 Chat History")

#     if not st.session_state.chat_history:
#         st.info("No conversation yet")
#     else:
#         user_msgs = [m for m in st.session_state.chat_history if m["role"] == "user"]
#         asst_msgs = [m for m in st.session_state.chat_history if m["role"] == "assistant"]
#         col1, col2 = st.columns(2)
#         col1.metric("User Messages", len(user_msgs))
#         col2.metric("Responses", len(asst_msgs))

#         st.divider()
#         for msg in st.session_state.chat_history:
#             icon = "🧑" if msg["role"] == "user" else "🤖"
#             st.write(f"**{icon} {msg['role'].upper()}**")
#             content = msg["content"]
#             st.write(content[:300] + ("..." if len(content) > 300 else content[300:]))
#             if "time" in msg:
#                 st.caption(f"⏱️ {msg['time']:.2f}s")
#             st.divider()

# # ════════════════════════════════════════════════════════
# # TAB 4: LIVE EVALUATION
# # ════════════════════════════════════════════════════════

# with tab4:
#     st.header("📊 Live RAG Evaluation Dashboard")
#     st.markdown("Evaluate recent interactions using the existing LLM. Scores are based on retrieval quality, faithfulness, and hallucination risk.")

#     interaction_count = len(st.session_state.interaction_log)

#     if interaction_count == 0:
#         st.info("💬 Ask at least one question in the Chat tab first — the evaluation button will activate once you have interactions to score.")

#     # Always show slider + button — disabled when no interactions
#     n_to_eval = st.slider(
#         "Number of recent interactions to evaluate",
#         min_value=1,
#         max_value=max(2, interaction_count),   # Always >= 2 to avoid min==max crash
#         value=max(1, min(3, interaction_count)),
#         disabled=(interaction_count == 0)
#     )

#     if interaction_count > 0:
#         st.write(f"**{interaction_count}** interaction(s) available for evaluation.")

#     run_eval = st.button(
#         "🔍 Run Evaluation",
#         type="primary",
#         use_container_width=True,
#         disabled=(interaction_count == 0),
#         help="Ask questions in the Chat tab first to enable evaluation."
#     )

#     if run_eval and interaction_count > 0:
#         with st.spinner("🤔 Evaluating... (1 LLM call per interaction)"):
#             try:
#                 llm = get_llm(model_choice, temperature)
#                 evaluator = RAGEvaluator(llm=llm)
#                 recent = st.session_state.interaction_log[-n_to_eval:]
#                 batch_result = evaluator.evaluate_batch(recent)
#                 batch_result["_n_eval"] = n_to_eval
#                 st.session_state.eval_results = batch_result
#             except Exception as e:
#                 st.error(f"❌ Evaluation failed: {e}")

#     # Display results — always shown if available (persists across reruns)
#     if st.session_state.eval_results:
#         res = st.session_state.eval_results

#         if res.get("error") and res.get("count", 0) == 0:
#             st.error(f"Evaluation error: {res['error']}")
#         else:
#             st.divider()
#             st.subheader("📈 Aggregate Scores")

#             health = res["overall_health"]
#             health_label = health_to_label(health)
#             st.metric("🏥 Overall Health Score", f"{health}/100", delta=health_label)
#             st.progress(health / 100)

#             st.divider()

#             c1, c2, c3, c4 = st.columns(4)
#             rq = res["retrieval_quality"]
#             cc = res["context_coverage"]
#             sg = res["source_grounding"]
#             hr = res["hallucination_risk"]
#             fs = res["faithfulness_score"]

#             with c1:
#                 st.metric("🔍 Retrieval Quality", f"{rq}/10")
#                 st.caption(score_to_label(rq))
#                 st.progress(rq / 10)

#             with c2:
#                 st.metric("📖 Context Coverage", f"{cc}/10")
#                 st.caption(score_to_label(cc))
#                 st.progress(cc / 10)

#             with c3:
#                 st.metric("📌 Faithfulness Score", f"{fs}/100")
#                 st.caption(score_to_label(sg))
#                 st.progress(fs / 100)

#             with c4:
#                 st.metric("⚠️ Hallucination Risk", f"{hr}/10")
#                 st.caption(score_to_label(hr, invert=True))
#                 st.progress(hr / 10)

#             st.divider()

#             if res.get("results"):
#                 st.subheader("🔎 Per-Interaction Breakdown")
#                 _n = res.get("_n_eval", len(res["results"]))
#                 recent_log = st.session_state.interaction_log[-_n:]

#                 for i, (interaction, r) in enumerate(zip(recent_log, res["results"])):
#                     q_preview = interaction["question"][:80] + ("..." if len(interaction["question"]) > 80 else "")
#                     status = "✅" if r.get("error") is None else "❌"
#                     with st.expander(f"{status} Interaction {i+1}: {q_preview}"):
#                         if r.get("error"):
#                             st.warning(f"Evaluation error: {r['error']}")
#                         else:
#                             ic1, ic2, ic3, ic4 = st.columns(4)
#                             ic1.metric("Retrieval", f"{r['retrieval_quality']}/10")
#                             ic2.metric("Coverage", f"{r['context_coverage']}/10")
#                             ic3.metric("Grounding", f"{r['source_grounding']}/10")
#                             ic4.metric("Hallucination", f"{r['hallucination_risk']}/10")
#                             st.caption(f"💬 **Reasoning:** {r.get('reasoning', 'N/A')}")

# # ════════════════════════════════════════════════════════
# # FOOTER
# # ════════════════════════════════════════════════════════

# st.divider()
# st.markdown("""
# <div style='text-align: center; color: #888; font-size: 12px;'>
# ✨ Production-Ready RAG System &nbsp;|&nbsp;
# 📦 bge-base-en embeddings &nbsp;|&nbsp;
# 🚀 FAISS + Groq + Dual Memory + Live Evaluation
# </div>
# """, unsafe_allow_html=True)























# import streamlit as st
# import fitz
# import os
# import hashlib
# import time
# import json
# import re
# import math
# import pickle
# import logging
# from typing import List, Tuple, Optional, Dict
# from dotenv import load_dotenv

# from langchain_groq import ChatGroq
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.documents import Document
# from langgraph.graph import StateGraph, END
# from typing_extensions import TypedDict

# from rag_evaluation_framework import RAGEvaluator, score_to_label, health_to_label

# # ════════════════════════════════════════════════════════
# # SETUP
# # ════════════════════════════════════════════════════════

# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# FAISS_INDEX_PATH = "./faiss_index"

# # ── Structured logger (writes to stdout; redirect to file via shell if needed) ──
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S"
# )
# logger = logging.getLogger("rag_app")

# if not GROQ_API_KEY:
#     st.error("❌ GROQ_API_KEY not found in .env file")
#     logger.critical("GROQ_API_KEY missing — app cannot start")
#     st.stop()

# st.set_page_config(
#     page_title="RAG Chatbot",
#     page_icon="📦",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ════════════════════════════════════════════════════════
# # MEMORY CLASS
# # ════════════════════════════════════════════════════════

# class DualRAGMemory:
#     """
#     Simple dual memory: sliding window buffer + periodic LLM summary.
#     No LangChain memory classes needed — fully version-safe.
#     """

#     def __init__(self, buffer_size: int = 5, llm=None):
#         self.buffer_size = buffer_size
#         self.llm = llm
#         self._exchanges: List[dict] = []   # [{"q": ..., "a": ...}]
#         self._summary: str = ""
#         self.token_count = 0
#         self.interaction_count = 0

#     def add_exchange(self, query: str, response: str):
#         """Add exchange; trim buffer; progressively update summary every turn."""
#         self._exchanges.append({"q": query, "a": response})
#         if len(self._exchanges) > self.buffer_size:
#             self._exchanges = self._exchanges[-self.buffer_size:]
#         self.token_count += len(query.split()) + len(response.split())
#         self.interaction_count += 1
#         if self.llm:
#             self._progressive_summary(query, response)

#     def _progressive_summary(self, new_q: str, new_a: str):
#         """
#         Progressive summarisation: compress(prev_summary + new_exchange).
#         Never loses prior context — each update compounds on the last.
#         """
#         try:
#             prev = self._summary or "No prior summary."
#             prompt = (
#                 "You are maintaining a running conversation summary.\n\n"
#                 f"PREVIOUS SUMMARY:\n{prev}\n\n"
#                 f"NEW EXCHANGE:\nUser: {new_q}\nAssistant: {new_a}\n\n"
#                 "Update the summary to include the new exchange. "
#                 "Keep it under 5 sentences. Preserve ALL important facts from the previous summary. "
#                 "Output ONLY the updated summary, nothing else."
#             )
#             result = self.llm.invoke(prompt)
#             self._summary = result.content.strip()
#         except Exception:
#             pass  # Silent fail — summary is optional

#     def get_recent(self) -> str:
#         """Return recent exchanges as formatted text."""
#         if not self._exchanges:
#             return ""
#         lines = []
#         for ex in self._exchanges:
#             lines.append(f"User: {ex['q']}")
#             lines.append(f"Assistant: {ex['a']}")
#         return "\n".join(lines)

#     def get_summary(self) -> str:
#         """Return the current conversation summary."""
#         return self._summary

#     def get_status(self) -> str:
#         return "✅ Healthy" if self.token_count < 5000 else "⚠️ High"

#     def reset(self):
#         self._exchanges = []
#         self._summary = ""
#         self.token_count = 0
#         self.interaction_count = 0

# # ════════════════════════════════════════════════════════
# # CACHED RESOURCES
# # ════════════════════════════════════════════════════════

# @st.cache_resource
# def get_llm(model_name: str, temperature: float):
#     return ChatGroq(api_key=GROQ_API_KEY, model_name=model_name, temperature=temperature)

# @st.cache_resource
# def get_embeddings(model_name: str = "BAAI/bge-base-en-v1.5"):
#     return HuggingFaceEmbeddings(
#         model_name=model_name,
#         model_kwargs={"device": "cpu"},
#         encode_kwargs={"normalize_embeddings": True}
#     )

# # ════════════════════════════════════════════════════════
# # PDF PROCESSING
# # ════════════════════════════════════════════════════════

# def extract_text_from_pdf(file_bytes: bytes, filename: str) -> Tuple[List, int]:
#     """
#     Extract text with page-level metadata.
#     Fallback: if full-document extraction fails, retries page-by-page
#     so a single corrupt page does not drop the entire PDF.
#     """
#     try:
#         doc = fitz.open(stream=file_bytes, filetype="pdf")
#         page_docs = []
#         failed_pages = []
#         for i, page in enumerate(doc):
#             try:
#                 text = page.get_text("text").strip()
#                 if text:
#                     page_docs.append({"text": text, "page": i + 1, "source": filename})
#             except Exception as page_err:
#                 failed_pages.append(i + 1)
#                 logger.warning("PDF page extraction failed | file=%s page=%d error=%s",
#                                filename, i + 1, page_err)
#         if failed_pages:
#             st.warning(f"⚠️ {filename}: {len(failed_pages)} page(s) skipped (corrupt/unreadable): {failed_pages[:5]}")
#         logger.info("PDF extracted | file=%s pages_ok=%d pages_failed=%d",
#                     filename, len(page_docs), len(failed_pages))
#         return page_docs, len(doc)
#     except Exception as e:
#         logger.error("PDF open failed | file=%s error=%s", filename, e)
#         st.error(f"❌ PDF error ({filename}): {e}")
#         return [], 0

# # Header patterns for technical PDFs (markdown headers, numbered sections, ALL-CAPS titles)
# _HEADER_RE = re.compile(
#     r"^(#{1,3}\s.{3,}|[A-Z][A-Z0-9 ]{5,50}$|\d+\.\d*\s+[A-Z].{4,}|Chapter\s+\d+|SECTION\s+\d+)",
#     re.MULTILINE
# )

# def _detect_section(text: str) -> str:
#     """Return the first header found in text, or empty string."""
#     m = _HEADER_RE.search(text)
#     return m.group(0).strip()[:80] if m else ""

# def split_text_with_pages(page_docs: list, chunk_size: int = 1000, overlap: int = 200):
#     """
#     Header-aware chunking: detects section headings and annotates each chunk
#     with its section. Falls back to RecursiveCharacterTextSplitter boundaries.
#     Reason chosen over SemanticChunker: no heavy NLP dependency, preserves
#     document hierarchy, fast, deterministic for technical PDFs.
#     """
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=overlap,
#         separators=["\n\n", "\n", ". ", " ", ""]
#     )
#     all_chunks = []
#     for page_doc in page_docs:
#         text   = page_doc["text"]
#         source = page_doc["source"]
#         page   = page_doc["page"]
#         section = _detect_section(text)
#         chunks = splitter.create_documents([text])
#         for chunk in chunks:
#             chunk.metadata["source"]  = source
#             chunk.metadata["page"]    = page
#             if section:
#                 chunk.metadata["section"] = section
#         all_chunks.extend(chunks)
#     return all_chunks

# # ════════════════════════════════════════════════════════
# # ADAPTIVE RETRIEVAL
# # ════════════════════════════════════════════════════════

# COMPLEX_KEYWORDS = [
#     "compare", "difference", "explain", "analyze", "how does", "why does",
#     "summarize", "describe", "elaborate", "relationship", "architecture",
#     "workflow", "process", "mechanism", "contrast", "evaluate", "assess"
# ]

# def get_adaptive_k(query: str, base_k: int) -> int:
#     """Return fewer chunks for simple queries, more for complex ones."""
#     q = query.lower()
#     is_complex = len(query.split()) > 12 or any(kw in q for kw in COMPLEX_KEYWORDS)
#     return base_k if is_complex else max(3, base_k // 2)

# # ════════════════════════════════════════════════════════
# # FAISS PERSISTENCE
# # ════════════════════════════════════════════════════════

# def save_faiss(vectorstore, embedding_model: str):
#     """Persist FAISS index and record which embedding model built it."""
#     try:
#         vectorstore.save_local(FAISS_INDEX_PATH)
#         with open(f"{FAISS_INDEX_PATH}/embedding_model.txt", "w") as f:
#             f.write(embedding_model)
#     except Exception as e:
#         st.warning(f"⚠️ Could not save FAISS index: {e}")

# def load_faiss(embeddings, embedding_model: str) -> Optional[object]:
#     """Load persisted FAISS index if embedding model matches."""
#     model_file = f"{FAISS_INDEX_PATH}/embedding_model.txt"
#     index_file = f"{FAISS_INDEX_PATH}/index.faiss"
#     if not (os.path.exists(index_file) and os.path.exists(model_file)):
#         return None
#     try:
#         saved_model = open(model_file).read().strip()
#         if saved_model != embedding_model:
#             return None  # Model mismatch — must rebuild
#         return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
#     except Exception:
#         return None

# # ════════════════════════════════════════════════════════
# # BM25 — SPARSE RETRIEVAL
# # ════════════════════════════════════════════════════════

# BM25_PATH = f"{FAISS_INDEX_PATH}/bm25.pkl"

# def build_bm25(docs: List) -> Tuple[object, List]:
#     """Build BM25 index from a flat list of Document objects."""
#     from rank_bm25 import BM25Okapi
#     tokenized = [d.page_content.lower().split() for d in docs]
#     return BM25Okapi(tokenized), docs

# def save_bm25(bm25_obj, corpus: List):
#     """Persist BM25 index and corpus to disk alongside FAISS."""
#     try:
#         os.makedirs(FAISS_INDEX_PATH, exist_ok=True)
#         with open(BM25_PATH, "wb") as f:
#             pickle.dump({"bm25": bm25_obj, "corpus": corpus}, f)
#     except Exception as e:
#         st.warning(f"⚠️ BM25 save failed: {e}")

# def load_bm25() -> Tuple[Optional[object], Optional[List]]:
#     """Reload persisted BM25 index from disk."""
#     if not os.path.exists(BM25_PATH):
#         return None, None
#     try:
#         with open(BM25_PATH, "rb") as f:
#             data = pickle.load(f)
#         return data["bm25"], data["corpus"]
#     except Exception:
#         return None, None

# def hybrid_retrieve(query: str, vectorstore, bm25_obj, bm25_corpus: List,
#                     k: int, bm25_weight: float = 0.3) -> List:
#     """
#     Merge dense FAISS results with sparse BM25 results.
#     bm25_weight controls how many of the k slots go to BM25.
#     """
#     n_bm25 = max(1, round(k * bm25_weight))
#     n_dense = max(1, k - n_bm25)

#     # Dense retrieval
#     dense_docs = vectorstore.similarity_search(query, k=n_dense * 2)

#     # Sparse BM25 retrieval
#     bm25_docs: List = []
#     if bm25_obj and bm25_corpus:
#         tokens = query.lower().split()
#         scores = bm25_obj.get_scores(tokens)
#         top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:n_bm25 * 2]
#         bm25_docs = [bm25_corpus[i] for i in top_idx if scores[i] > 0]

#     # Merge, deduplicate by first 80 chars of content
#     seen: set = set()
#     merged: List = []
#     for doc in dense_docs[:n_dense] + bm25_docs[:n_bm25]:
#         key = doc.page_content[:80]
#         if key not in seen:
#             seen.add(key)
#             merged.append(doc)
#     return merged[:k]

# # ════════════════════════════════════════════════════════
# # PROMPT
# # ════════════════════════════════════════════════════════

# SYSTEM_PROMPT = ChatPromptTemplate.from_template("""You are a strict document-based question answering assistant.

# CONVERSATION SUMMARY (for context):
# {conversation_summary}

# RECENT EXCHANGES:
# {recent_history}

# RETRIEVED DOCUMENTS:
# {context}

# QUESTION:
# {input}

# INSTRUCTIONS:
# 1. Answer ONLY using information explicitly present in the retrieved documents above.
# 2. Do NOT use prior knowledge, training data, or external information.
# 3. Do NOT speculate, guess, or invent details not in the documents.
# 4. If partially supported: provide only the supported part, then state "The remaining information is not available in the provided documents."
# 5. If not supported at all: respond ONLY "This information is not available in the provided documents."
# 6. Cite sources using: [filename | Page N] after every factual claim.
# 7. Keep answers concise and accurate.
# 8. Prefer accuracy over completeness.

# FINAL ANSWER:""")

# # ════════════════════════════════════════════════════════
# # LANGGRAPH — AGENTIC RAG STATE & NODES
# # ════════════════════════════════════════════════════════

# class RAGState(TypedDict):
#     """Typed state passed through the LangGraph RAG pipeline."""
#     query: str
#     original_query: str
#     documents: List[Document]
#     answer: str
#     sources: List[str]
#     retrieval_attempts: int
#     document_grade: str          # "relevant" | "not_relevant"
#     retrieval_method: str        # "hybrid" | "faiss-only" | "hybrid+reranked"
#     conversation_summary: str
#     recent_history: str
#     adaptive_k: int
#     vectorstore: object
#     bm25_index: object
#     bm25_corpus: List
#     bm25_weight: float
#     llm: object
#     rewrite_log: List
#     confidence: Dict
#     use_reranker: bool
#     reranker: object


# # ── Prompts for grading and rewriting ────────────────────

# BATCH_GRADE_PROMPT = """You are a document relevance grader for a RAG system.

# Question: {question}

# Below are {n} retrieved document excerpts. For each, decide if it contains information useful for answering the question.

# {documents}

# Respond ONLY with a JSON array — one entry per document, in order:
# [{{"id": 1, "score": "relevant"}}, {{"id": 2, "score": "not_relevant"}}, ...]
# All {n} documents must appear. No extra text."""

# REWRITE_PROMPT = """You are a query rewriter for a RAG system.
# The original query failed to retrieve useful documents. Rewrite it to be clearer and more specific, preserving the original intent.

# Original query: {question}

# Rewritten query (output ONLY the rewritten query, nothing else):"""


# # ── Confidence scoring (no LLM calls) ────────────────────

# def compute_confidence(docs: List, answer: str) -> Dict:
#     """Lightweight confidence signals from retrieved docs and answer text."""
#     if not docs or not answer:
#         return {"retrieval": 0.0, "grounding": 0.0}
#     # Retrieval confidence: proxy via doc count (6 docs = max)
#     retrieval_conf = round(min(1.0, len(docs) / 6), 2)
#     # Grounding confidence: keyword overlap between context and answer
#     stop = {"the", "a", "an", "is", "are", "was", "were", "in", "on",
#             "at", "to", "for", "of", "and", "or", "not", "it", "this", "that"}
#     ctx_words: set = set()
#     for d in docs:
#         ctx_words.update(w.lower() for w in d.page_content.split())
#     ans_words = {w.lower() for w in answer.split()} - stop
#     grounding = round(len(ans_words & ctx_words) / max(len(ans_words), 1), 2)
#     return {"retrieval": retrieval_conf, "grounding": min(1.0, grounding)}


# # ── Optional Cross-Encoder reranker ──────────────────────

# @st.cache_resource
# def get_reranker(model_name: str = "BAAI/bge-reranker-base"):
#     from sentence_transformers import CrossEncoder
#     return CrossEncoder(model_name)

# def rerank_docs(reranker, query: str, docs: List, top_k: int = 5) -> List:
#     """Score all candidates with CrossEncoder, return top_k."""
#     if not docs:
#         return docs
#     pairs = [(query, d.page_content[:512]) for d in docs]
#     scores = reranker.predict(pairs)
#     ranked = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)
#     return [d for _, d in ranked[:top_k]]


# def node_retrieve(state: RAGState) -> RAGState:
#     """Hybrid BM25 + FAISS retrieval with optional CrossEncoder reranking."""
#     query  = state["query"]
#     k      = state["adaptive_k"]
#     has_bm25 = bool(state.get("bm25_index") and state.get("bm25_corpus"))

#     fetch_k = 15 if state.get("use_reranker") else k

#     docs = hybrid_retrieve(
#         query=query,
#         vectorstore=state["vectorstore"],
#         bm25_obj=state.get("bm25_index"),
#         bm25_corpus=state.get("bm25_corpus") or [],
#         k=fetch_k,
#         bm25_weight=state.get("bm25_weight", 0.3),
#     )

#     method = "hybrid" if has_bm25 else "faiss-only"

#     # Optional reranking
#     if state.get("use_reranker") and state.get("reranker") and docs:
#         docs   = rerank_docs(state["reranker"], query, docs, top_k=min(5, k))
#         method = "hybrid+reranked"

#     logger.info("retrieval | query=%r attempt=%d method=%s docs=%d",
#                 query[:60], state["retrieval_attempts"] + 1, method, len(docs))

#     return {**state, "documents": docs,
#             "retrieval_attempts": state["retrieval_attempts"] + 1,
#             "retrieval_method": method}


# def node_grade_documents(state: RAGState) -> RAGState:
#     """
#     Batch-grade all retrieved docs in ONE LLM call (was N separate calls).
#     Never marks docs as relevant on parse failure — conservative by default.
#     """
#     docs = state["documents"]
#     if not docs:
#         logger.info("grading | query=%r result=not_relevant (no docs)", state["query"][:60])
#         return {**state, "document_grade": "not_relevant"}

#     doc_block = ""
#     for i, doc in enumerate(docs[:6]):
#         section  = doc.metadata.get("section", "")
#         sec_note = f" [{section}]" if section else ""
#         doc_block += f"[Document {i+1}{sec_note}]:\n{doc.page_content[:400]}\n\n"

#     prompt = BATCH_GRADE_PROMPT.format(
#         question=state["query"],
#         n=min(len(docs), 6),
#         documents=doc_block.strip()
#     )

#     try:
#         result = state["llm"].invoke(prompt)
#         raw = result.content.strip()
#         raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
#         grades = json.loads(raw)
#         relevant_count = sum(1 for g in grades if isinstance(g, dict) and g.get("score") == "relevant")
#         grade = "relevant" if relevant_count >= 1 else "not_relevant"
#     except Exception as exc:
#         grade = "not_relevant"   # Conservative on parse failure
#         logger.warning("grading parse failed | query=%r error=%s", state["query"][:60], exc)

#     logger.info("grading | query=%r result=%s", state["query"][:60], grade)
#     return {**state, "document_grade": grade}


# def node_transform_query(state: RAGState) -> RAGState:
#     """Rewrite query with semantic similarity guard to prevent drift."""
#     original   = state["query"]
#     rewrite_log = list(state.get("rewrite_log") or [])
#     try:
#         prompt = REWRITE_PROMPT.format(question=original)
#         result = state["llm"].invoke(prompt)
#         new_query = result.content.strip()

#         orig_words = set(original.lower().split())
#         new_words  = set(new_query.lower().split())
#         overlap    = len(orig_words & new_words) / max(len(orig_words), 1)
#         if overlap > 0.85:
#             new_query = original   # Rewrite too similar — skip
#     except Exception as exc:
#         new_query = original
#         logger.warning("query rewrite failed | error=%s", exc)

#     rewrite_log.append({"original": original, "rewritten": new_query})
#     logger.info("query_rewrite | original=%r rewritten=%r", original[:60], new_query[:60])
#     return {**state, "query": new_query, "rewrite_log": rewrite_log}


# def node_generate(state: RAGState) -> RAGState:
#     """Generate answer; compute confidence scores from retrieved docs."""
#     docs = state["documents"]
#     context_parts, sources = [], []
#     for doc in docs:
#         src  = doc.metadata.get("source", "Unknown")
#         page = doc.metadata.get("page", "")
#         sect = doc.metadata.get("section", "")
#         citation = f"{src} | Page {page}" + (f" · {sect}" if sect else "") if page else src
#         if citation not in sources:
#             sources.append(citation)
#         context_parts.append(f"[{citation}]\n{doc.page_content}")

#     context  = "\n\n---\n\n".join(context_parts) if context_parts else "No documents retrieved."
#     formatted = SYSTEM_PROMPT.format(
#         conversation_summary=state["conversation_summary"] or "No prior summary.",
#         recent_history=state["recent_history"] or "No recent exchanges.",
#         context=context,
#         input=state["query"]
#     )
#     response   = state["llm"].invoke(formatted)
#     answer     = response.content
#     confidence = compute_confidence(docs, answer)

#     logger.info("generation | query=%r docs_used=%d sources=%d grounding=%.2f",
#                 state["query"][:60], len(docs), len(sources),
#                 confidence.get("grounding", 0))

#     return {**state, "answer": answer, "sources": sources, "confidence": confidence}


# def should_retry(state: RAGState) -> str:
#     """Conditional edge: retry with rewritten query or go straight to generate."""
#     if state["document_grade"] == "relevant":
#         return "generate"
#     if state["retrieval_attempts"] < 2:
#         return "transform_query"   # Rewrite and retry once
#     return "generate"              # Give up retrying, generate with what we have


# def build_rag_graph() -> StateGraph:
#     """Compile the LangGraph agentic RAG pipeline."""
#     graph = StateGraph(RAGState)
#     graph.add_node("retrieve", node_retrieve)
#     graph.add_node("grade_documents", node_grade_documents)
#     graph.add_node("transform_query", node_transform_query)
#     graph.add_node("generate", node_generate)

#     graph.set_entry_point("retrieve")
#     graph.add_edge("retrieve", "grade_documents")
#     graph.add_conditional_edges(
#         "grade_documents",
#         should_retry,
#         {"generate": "generate", "transform_query": "transform_query"}
#     )
#     graph.add_edge("transform_query", "retrieve")
#     graph.add_edge("generate", END)
#     return graph.compile()


# # Compile once at module level (cached between reruns via Streamlit)
# @st.cache_resource
# def get_rag_graph():
#     return build_rag_graph()

# # ════════════════════════════════════════════════════════
# # SESSION STATE
# # ════════════════════════════════════════════════════════

# EMBEDDING_MODELS = {
#     "BGE Base (Recommended)": "BAAI/bge-base-en-v1.5",
#     "MiniLM L6 (Fastest)": "sentence-transformers/all-MiniLM-L6-v2",
#     "MPNet Base (Highest Quality)": "sentence-transformers/all-mpnet-base-v2",
# }

# def init_session():
#     defaults = {
#         "vectorstore": None,
#         "bm25_index": None,
#         "bm25_corpus": [],
#         "chat_history": [],
#         "pdf_hashes": set(),
#         "chunk_info": {},
#         "ingestion_timings": {},
#         "last_processed_query": None,
#         "eval_results": None,
#         "interaction_log": [],
#         "query_log": [],            # [{query, rewritten, method, attempts, elapsed}]
#         "faiss_loaded": False,
#     }
#     for k, v in defaults.items():
#         if k not in st.session_state:
#             st.session_state[k] = v

# init_session()

# # ════════════════════════════════════════════════════════
# # SIDEBAR
# # ════════════════════════════════════════════════════════

# with st.sidebar:
#     st.header("⚙️ Configuration")

#     st.subheader("🤖 LLM Model")
#     model_choice = st.selectbox(
#         "LLM Model",
#         ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
#         help="8B = Fast, 70B = Better Quality"
#     )
#     temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)

#     st.subheader("🧠 Embedding Model")
#     embedding_label = st.selectbox(
#         "Embedding Model",
#         list(EMBEDDING_MODELS.keys()),
#         help="BGE Base = best balance | MiniLM = fastest | MPNet = highest quality"
#     )
#     EMBEDDING_MODEL = EMBEDDING_MODELS[embedding_label]
#     if st.session_state.get("active_embedding_model") and \
#        st.session_state.active_embedding_model != EMBEDDING_MODEL and \
#        st.session_state.vectorstore is not None:
#         st.warning("⚠️ Embedding model changed! Clear docs and re-upload.")

#     st.subheader("📑 Document Settings")
#     chunk_size  = st.slider("Chunk Size", 200, 2000, 1000, 100)
#     overlap_pct = st.slider("Overlap %", 5, 40, 20, 5)
#     st.session_state.active_embedding_model = EMBEDDING_MODEL

#     st.subheader("🔍 Retrieval")
#     k_retrieve  = st.slider("Chunks to Retrieve", 3, 15, 6)
#     bm25_weight = st.slider("BM25 Weight", 0.0, 1.0, 0.3, 0.05,
#                              help="0 = pure FAISS | 1 = pure BM25 | 0.3 = recommended")

#     st.subheader("🎯 Reranker (P2)")
#     use_reranker = st.toggle("Enable Cross-Encoder Reranker", value=False,
#                               help="BAAI/bge-reranker-base. Retrieves 15 candidates → keeps top 5. Adds ~0.5–1s latency.")
#     if use_reranker:
#         st.caption("Fetches 15 candidates, reranks, returns top 5")

#     st.subheader("💾 Memory")
#     memory_window = st.slider("Memory Window (exchanges)", 2, 10, 5)
#     if "memory" not in st.session_state:
#         st.session_state.memory = DualRAGMemory(buffer_size=memory_window,
#                                                 llm=get_llm(model_choice, temperature))
#     elif st.session_state.memory.buffer_size != memory_window:
#         old = st.session_state.memory
#         st.session_state.memory = DualRAGMemory(buffer_size=memory_window,
#                                                 llm=get_llm(model_choice, temperature))
#         st.session_state.memory.token_count      = old.token_count
#         st.session_state.memory.interaction_count = old.interaction_count
#         st.session_state.memory._summary          = old._summary

#     st.caption(f"Status: {st.session_state.memory.get_status()}")
#     st.caption(f"Tokens ≈ {st.session_state.memory.token_count} | Exchanges: {st.session_state.memory.interaction_count}")
#     if st.session_state.memory._summary:
#         with st.expander("📝 Memory Summary"):
#             st.write(st.session_state.memory._summary)

#     if st.button("🔄 Reset All", use_container_width=True):
#         st.session_state.memory.reset()
#         st.session_state.chat_history = []
#         st.session_state.last_processed_query = None
#         st.session_state.eval_results = None
#         st.session_state.interaction_log = []
#         st.success("✅ Reset complete!")
#         st.rerun()

# # ════════════════════════════════════════════════════════
# # LOAD FAISS ON STARTUP (once per session)
# # ════════════════════════════════════════════════════════

# if not st.session_state.faiss_loaded and st.session_state.vectorstore is None:
#     embeddings = get_embeddings(EMBEDDING_MODEL)
#     loaded = load_faiss(embeddings, EMBEDDING_MODEL)
#     if loaded:
#         st.session_state.vectorstore = loaded
#         # Also reload BM25 index from disk
#         bm25_obj, bm25_corpus = load_bm25()
#         if bm25_obj:
#             st.session_state.bm25_index  = bm25_obj
#             st.session_state.bm25_corpus = bm25_corpus
#             st.sidebar.success("📂 FAISS + BM25 loaded from disk")
#         else:
#             st.sidebar.success("📂 FAISS index loaded from disk")
#     st.session_state.faiss_loaded = True

# # ════════════════════════════════════════════════════════
# # MAIN LAYOUT
# # ════════════════════════════════════════════════════════

# st.title("📦 RAG Chatbot")
# st.markdown("*Delivery System Documentation Assistant*")

# tab1, tab2, tab3, tab4, tab5 = st.tabs([
#     "💬 Chat", "📚 Documents", "📜 History", "📊 Evaluation", "🔧 Debug"
# ])

# # ════════════════════════════════════════════════════════
# # TAB 1: CHAT
# # ════════════════════════════════════════════════════════

# with tab1:
#     col1, col2 = st.columns([4, 1])
#     with col1:
#         uploaded_files = st.file_uploader("📤 Upload PDF", type=["pdf"], accept_multiple_files=True)
#     with col2:
#         if st.button("Clear Docs", use_container_width=True):
#             st.session_state.vectorstore   = None
#             st.session_state.bm25_index    = None
#             st.session_state.bm25_corpus   = []
#             st.session_state.pdf_hashes    = set()
#             st.session_state.chunk_info    = {}
#             st.session_state.ingestion_timings = {}
#             st.success("✅ Cleared!")
#             st.rerun()

#     # PDF Processing
#     if uploaded_files:
#         new_files = [
#             (pdf, hashlib.md5(pdf.getvalue()).hexdigest())
#             for pdf in uploaded_files
#             if hashlib.md5(pdf.getvalue()).hexdigest() not in st.session_state.pdf_hashes
#         ]

#         if new_files:
#             progress_bar = st.progress(0)
#             status_text  = st.empty()
#             timing_placeholder = st.empty()
#             embeddings = get_embeddings(EMBEDDING_MODEL)
#             all_new_docs: List = []

#             for idx, (pdf, file_hash) in enumerate(new_files):
#                 timings: Dict = {}
#                 status_text.text(f"📄 Processing: {pdf.name}")
#                 try:
#                     # ─ Step 1: PDF extraction ─────────────────────────
#                     t0 = time.time()
#                     page_docs, num_pages = extract_text_from_pdf(pdf.getvalue(), pdf.name)
#                     timings["extract"] = round(time.time() - t0, 2)
#                     if not page_docs:
#                         st.warning(f"⚠️ No text in {pdf.name}")
#                         continue

#                     # ─ Step 2: Chunking ─────────────────────────────
#                     t0 = time.time()
#                     overlap = int(chunk_size * overlap_pct / 100)
#                     docs = split_text_with_pages(page_docs, chunk_size, overlap)
#                     timings["chunk"] = round(time.time() - t0, 2)
#                     if not docs:
#                         st.warning(f"⚠️ Could not split {pdf.name}")
#                         continue

#                     char_counts = [len(d.page_content) for d in docs]
#                     st.session_state.chunk_info[pdf.name] = {
#                         "chunks": len(docs), "avg_size": round(sum(char_counts)/len(char_counts)),
#                         "pages": num_pages, "total_chars": sum(char_counts)
#                     }

#                     # ─ Step 3: Embedding + FAISS indexing ───────────────
#                     status_text.text(f"🔍 Embedding: {pdf.name} ({len(docs)} chunks)")
#                     t0 = time.time()
#                     if st.session_state.vectorstore is None:
#                         st.session_state.vectorstore = FAISS.from_documents(docs, embeddings)
#                     else:
#                         st.session_state.vectorstore.add_documents(docs)
#                     timings["embed_index"] = round(time.time() - t0, 2)

#                     all_new_docs.extend(docs)
#                     st.session_state.pdf_hashes.add(file_hash)
#                     st.session_state.ingestion_timings[pdf.name] = timings

#                 except Exception as e:
#                     st.error(f"❌ Error processing {pdf.name}: {e}")

#                 progress_bar.progress((idx + 1) / len(new_files))

#             # ─ Step 4: Persist FAISS + build & save BM25 ───────
#             if st.session_state.vectorstore:
#                 status_text.text("💾 Saving indexes...")
#                 t0 = time.time()
#                 save_faiss(st.session_state.vectorstore, EMBEDDING_MODEL)
#                 save_t = round(time.time() - t0, 2)

#                 t0 = time.time()
#                 existing_corpus = st.session_state.bm25_corpus or []
#                 merged_corpus = existing_corpus + all_new_docs
#                 bm25_obj, bm25_corpus = build_bm25(merged_corpus)
#                 st.session_state.bm25_index  = bm25_obj
#                 st.session_state.bm25_corpus = bm25_corpus
#                 save_bm25(bm25_obj, bm25_corpus)
#                 bm25_t = round(time.time() - t0, 2)
#                 logger.info("upload | files=%d faiss_save=%.2fs bm25_build=%.2fs",
#                             len(new_files), save_t, bm25_t)

#             progress_bar.empty()
#             status_text.empty()
#             st.success(f"✅ Loaded {len(new_files)} PDF(s)! | FAISS save: {save_t}s | BM25 build: {bm25_t}s")

#     st.divider()

#     # Chat Interface
#     if st.session_state.vectorstore is None:
#         st.info("⬆️ Upload a PDF to start chatting")
#     else:
#         # Render existing history
#         for msg in st.session_state.chat_history:
#             with st.chat_message(msg["role"]):
#                 st.write(msg["content"])
#                 if "time" in msg:
#                     st.caption(f"⏱️ {msg['time']:.2f}s")

#         query = st.chat_input("Ask a question about your documents...")

#         if query and query != st.session_state.last_processed_query:
#             st.session_state.last_processed_query = query

#             with st.chat_message("user"):
#                 st.write(query)

#             with st.spinner("🤔 Analyzing..."):
#                 try:
#                     start_time = time.time()
#                     llm = get_llm(model_choice, temperature)
#                     adaptive_k = get_adaptive_k(query, k_retrieve)

#                     # Load reranker only if toggled on
#                     reranker_obj = get_reranker() if use_reranker else None

#                     rag_graph = get_rag_graph()
#                     initial_state: RAGState = {
#                         "query":                query,
#                         "original_query":       query,
#                         "documents":            [],
#                         "answer":               "",
#                         "sources":              [],
#                         "retrieval_attempts":   0,
#                         "document_grade":       "",
#                         "retrieval_method":     "",
#                         "conversation_summary": st.session_state.memory.get_summary(),
#                         "recent_history":       st.session_state.memory.get_recent(),
#                         "adaptive_k":           adaptive_k,
#                         "vectorstore":          st.session_state.vectorstore,
#                         "bm25_index":           st.session_state.bm25_index,
#                         "bm25_corpus":          st.session_state.bm25_corpus,
#                         "bm25_weight":          bm25_weight,
#                         "llm":                  llm,
#                         "rewrite_log":          [],
#                         "confidence":           {},
#                         "use_reranker":         use_reranker,
#                         "reranker":             reranker_obj,
#                     }
#                     final_state = rag_graph.invoke(initial_state)

#                     answer         = final_state["answer"]
#                     retrieved_docs  = final_state["documents"]
#                     sources        = final_state["sources"]
#                     retries        = final_state["retrieval_attempts"] - 1
#                     doc_grade      = final_state["document_grade"]
#                     ret_method     = final_state.get("retrieval_method", "faiss-only")
#                     confidence     = final_state.get("confidence", {})
#                     rewrite_log    = final_state.get("rewrite_log", [])
#                     elapsed        = time.time() - start_time

#                     # Append to query analytics log
#                     st.session_state.query_log.append({
#                         "query":       query,
#                         "rewritten":   rewrite_log[-1]["rewritten"] if rewrite_log else query,
#                         "method":      ret_method,
#                         "attempts":    final_state["retrieval_attempts"],
#                         "grade":       doc_grade,
#                         "elapsed":     round(elapsed, 2),
#                         "chunks":      len(retrieved_docs),
#                     })
#                     st.session_state.query_log = st.session_state.query_log[-20:]

#                     st.session_state.memory.add_exchange(query, answer)
#                     st.session_state.interaction_log.append({
#                         "question": query, "answer": answer, "retrieved_docs": retrieved_docs
#                     })
#                     st.session_state.interaction_log = st.session_state.interaction_log[-10:]

#                     with st.chat_message("assistant"):
#                         st.write(answer)

#                         # ─ Status bar: grade | method | time | chunks
#                         c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1])
#                         with c1:
#                             st.caption(f"📎 {' · '.join(sources[:2])}")
#                         with c2:
#                             grade_icon = "🟢" if doc_grade == "relevant" else "🟡"
#                             retry_txt  = f" (×{retries})" if retries > 0 else ""
#                             st.caption(f"{grade_icon} {doc_grade}{retry_txt}")
#                         with c3:
#                             # Retrieval method badge
#                             method_icons = {"hybrid": "🔀", "faiss-only": "📊", "hybrid+reranked": "⭐"}
#                             m_icon = method_icons.get(ret_method, "📊")
#                             st.caption(f"{m_icon} {ret_method}")
#                         with c4:
#                             st.caption(f"⏱️ {elapsed:.2f}s")
#                         with c5:
#                             st.caption(f"📄 {len(retrieved_docs)} chunks")

#                         # ─ Confidence scores
#                         if confidence:
#                             rc = confidence.get("retrieval", 0)
#                             gc = confidence.get("grounding", 0)
#                             cf1, cf2 = st.columns(2)
#                             cf1.metric("📊 Retrieval Conf.", f"{rc:.0%}")
#                             cf2.metric("📌 Grounding Conf.", f"{gc:.0%}")

#                         # ─ Query rewrite log
#                         if rewrite_log and rewrite_log[0]["original"] != rewrite_log[0]["rewritten"]:
#                             with st.expander("🔄 Query was rewritten"):
#                                 for entry in rewrite_log:
#                                     st.markdown(f"**Original:** {entry['original']}")
#                                     st.markdown(f"**Rewritten:** {entry['rewritten']}")

#                         # ─ Retrieved chunks
#                         with st.expander("📋 Retrieved Chunks"):
#                             for i, doc in enumerate(retrieved_docs[:6]):
#                                 src  = doc.metadata.get("source", "Unknown")
#                                 page = doc.metadata.get("page", "")
#                                 sect = doc.metadata.get("section", "")
#                                 header = f"**Chunk {i+1}** — `{src}` | Page {page}"
#                                 if sect:
#                                     header += f" | *{sect}*"
#                                 st.markdown(header)
#                                 st.text(doc.page_content[:400] + ("..." if len(doc.page_content) > 400 else ""))
#                                 st.divider()

#                     st.session_state.chat_history.append({"role": "user", "content": query})
#                     st.session_state.chat_history.append({"role": "assistant", "content": answer, "time": elapsed})

#                 except Exception as e:
#                     st.error(f"❌ Error: {e}")

# # ════════════════════════════════════════════════════════
# # TAB 2: DOCUMENTS
# # ════════════════════════════════════════════════════════

# with tab2:
#     st.header("📚 Document Information")

#     if not st.session_state.chunk_info:
#         st.info("No documents loaded yet")
#     else:
#         col1, col2, col3, col4 = st.columns(4)
#         col1.metric("Files", len(st.session_state.chunk_info))
#         col2.metric("Total Chunks", sum(v["chunks"] for v in st.session_state.chunk_info.values()))
#         col3.metric("Total Pages", sum(v["pages"] for v in st.session_state.chunk_info.values()))
#         col4.metric("Total Size", f"{sum(v['total_chars'] for v in st.session_state.chunk_info.values()) // 1000}KB")

#         st.divider()
#         for fname, info in st.session_state.chunk_info.items():
#             with st.expander(f"📄 {fname}"):
#                 c1, c2, c3, c4 = st.columns(4)
#                 c1.metric("Chunks", info["chunks"])
#                 c2.metric("Avg Size", f"{info['avg_size']} chars")
#                 c3.metric("Total Size", f"{info['total_chars']:,} chars")
#                 c4.metric("Pages", info["pages"])
#                 avg = info["avg_size"]
#                 if avg < 300:
#                     st.warning("⚠️ Chunks are small — consider increasing chunk size")
#                 elif avg > 1500:
#                     st.warning("⚠️ Chunks are large — consider reducing chunk size")
#                 else:
#                     st.success("✅ Optimal chunk size")

#                 # Ingestion timing breakdown
#                 timings = st.session_state.ingestion_timings.get(fname, {})
#                 if timings:
#                     st.caption("**⏱️ Ingestion Timing:**")
#                     tc1, tc2, tc3 = st.columns(3)
#                     tc1.metric("PDF Extract", f"{timings.get('extract', '-')}s")
#                     tc2.metric("Chunking",    f"{timings.get('chunk', '-')}s")
#                     tc3.metric("Embed+Index", f"{timings.get('embed_index', '-')}s")
#                     total = sum(v for v in timings.values() if isinstance(v, (int, float)))
#                     st.caption(f"Total ingestion: **{total:.2f}s** | "
#                                f"Throughput: **{round(info['chunks']/max(timings.get('embed_index',1),0.01))} chunks/s**")

# # ════════════════════════════════════════════════════════
# # TAB 3: HISTORY
# # ════════════════════════════════════════════════════════

# with tab3:
#     st.header("📜 Chat History")

#     if not st.session_state.chat_history:
#         st.info("No conversation yet")
#     else:
#         user_msgs = [m for m in st.session_state.chat_history if m["role"] == "user"]
#         asst_msgs = [m for m in st.session_state.chat_history if m["role"] == "assistant"]
#         col1, col2 = st.columns(2)
#         col1.metric("User Messages", len(user_msgs))
#         col2.metric("Responses", len(asst_msgs))

#         st.divider()
#         for msg in st.session_state.chat_history:
#             icon = "🧑" if msg["role"] == "user" else "🤖"
#             st.write(f"**{icon} {msg['role'].upper()}**")
#             content = msg["content"]
#             st.write(content[:300] + ("..." if len(content) > 300 else content[300:]))
#             if "time" in msg:
#                 st.caption(f"⏱️ {msg['time']:.2f}s")
#             st.divider()

# # ════════════════════════════════════════════════════════
# # TAB 4: LIVE EVALUATION
# # ════════════════════════════════════════════════════════

# with tab4:
#     st.header("📊 Live RAG Evaluation Dashboard")
#     st.markdown("Evaluate recent interactions using the existing LLM. Scores are based on retrieval quality, faithfulness, and hallucination risk.")

#     interaction_count = len(st.session_state.interaction_log)

#     if interaction_count == 0:
#         st.info("💬 Ask at least one question in the Chat tab first — the evaluation button will activate once you have interactions to score.")

#     # Always show slider + button — disabled when no interactions
#     n_to_eval = st.slider(
#         "Number of recent interactions to evaluate",
#         min_value=1,
#         max_value=max(2, interaction_count),   # Always >= 2 to avoid min==max crash
#         value=max(1, min(3, interaction_count)),
#         disabled=(interaction_count == 0)
#     )

#     if interaction_count > 0:
#         st.write(f"**{interaction_count}** interaction(s) available for evaluation.")

#     run_eval = st.button(
#         "🔍 Run Evaluation",
#         type="primary",
#         use_container_width=True,
#         disabled=(interaction_count == 0),
#         help="Ask questions in the Chat tab first to enable evaluation."
#     )

#     if run_eval and interaction_count > 0:
#         with st.spinner("🤔 Evaluating... (1 LLM call per interaction)"):
#             try:
#                 llm = get_llm(model_choice, temperature)
#                 evaluator = RAGEvaluator(llm=llm)
#                 recent = st.session_state.interaction_log[-n_to_eval:]
#                 batch_result = evaluator.evaluate_batch(recent)
#                 batch_result["_n_eval"] = n_to_eval
#                 st.session_state.eval_results = batch_result
#             except Exception as e:
#                 st.error(f"❌ Evaluation failed: {e}")

#     # Display results — always shown if available (persists across reruns)
#     if st.session_state.eval_results:
#         res = st.session_state.eval_results

#         if res.get("error") and res.get("count", 0) == 0:
#             st.error(f"Evaluation error: {res['error']}")
#         else:
#             st.divider()
#             st.subheader("📈 Aggregate Scores")

#             health = res["overall_health"]
#             health_label = health_to_label(health)
#             st.metric("🏥 Overall Health Score", f"{health}/100", delta=health_label)
#             st.progress(health / 100)

#             st.divider()

#             c1, c2, c3, c4 = st.columns(4)
#             rq = res["retrieval_quality"]
#             cc = res["context_coverage"]
#             sg = res["source_grounding"]
#             hr = res["hallucination_risk"]
#             fs = res["faithfulness_score"]

#             with c1:
#                 st.metric("🔍 Retrieval Quality", f"{rq}/10")
#                 st.caption(score_to_label(rq))
#                 st.progress(rq / 10)

#             with c2:
#                 st.metric("📖 Context Coverage", f"{cc}/10")
#                 st.caption(score_to_label(cc))
#                 st.progress(cc / 10)

#             with c3:
#                 st.metric("📌 Faithfulness Score", f"{fs}/100")
#                 st.caption(score_to_label(sg))
#                 st.progress(fs / 100)

#             with c4:
#                 st.metric("⚠️ Hallucination Risk", f"{hr}/10")
#                 st.caption(score_to_label(hr, invert=True))
#                 st.progress(hr / 10)

#             st.divider()

#             if res.get("results"):
#                 st.subheader("🔎 Per-Interaction Breakdown")
#                 _n = res.get("_n_eval", len(res["results"]))
#                 recent_log = st.session_state.interaction_log[-_n:]

#                 for i, (interaction, r) in enumerate(zip(recent_log, res["results"])):
#                     q_preview = interaction["question"][:80] + ("..." if len(interaction["question"]) > 80 else "")
#                     status = "✅" if r.get("error") is None else "❌"
#                     with st.expander(f"{status} Interaction {i+1}: {q_preview}"):
#                         if r.get("error"):
#                             st.warning(f"Evaluation error: {r['error']}")
#                         else:
#                             ic1, ic2, ic3, ic4 = st.columns(4)
#                             ic1.metric("Retrieval", f"{r['retrieval_quality']}/10")
#                             ic2.metric("Coverage", f"{r['context_coverage']}/10")
#                             ic3.metric("Grounding", f"{r['source_grounding']}/10")
#                             ic4.metric("Hallucination", f"{r['hallucination_risk']}/10")
#                             st.caption(f"💬 **Reasoning:** {r.get('reasoning', 'N/A')}")

# # ════════════════════════════════════════════════════════
# # TAB 5: DEBUG — QUERY ANALYTICS
# # ════════════════════════════════════════════════════════

# with tab5:
#     st.header("🔧 Debug — Query Analytics")
#     st.markdown("Real-time view of every query processed this session.")

#     qlog = st.session_state.query_log
#     if not qlog:
#         st.info("No queries yet. Ask a question in the Chat tab.")
#     else:
#         # Aggregate summary
#         avg_elapsed = round(sum(q["elapsed"] for q in qlog) / len(qlog), 2)
#         hybrid_count = sum(1 for q in qlog if "hybrid" in q.get("method", ""))
#         rewrite_count = sum(1 for q in qlog if q.get("query") != q.get("rewritten"))
#         relevant_count = sum(1 for q in qlog if q.get("grade") == "relevant")

#         m1, m2, m3, m4 = st.columns(4)
#         m1.metric("Total Queries", len(qlog))
#         m2.metric("Avg Latency", f"{avg_elapsed}s")
#         m3.metric("Hybrid Retrievals", f"{hybrid_count}/{len(qlog)}")
#         m4.metric("Queries Rewritten", rewrite_count)

#         st.divider()
#         st.subheader("📋 Per-Query Log (last 20)")
#         for i, q in enumerate(reversed(qlog)):
#             rewritten = q.get("rewritten", q["query"])
#             was_rewritten = rewritten != q["query"]
#             grade_icon = "🟢" if q.get("grade") == "relevant" else "🟡"
#             method_icon = {"hybrid": "🔀", "faiss-only": "📊", "hybrid+reranked": "⭐"}.get(q.get("method",""), "📊")
#             label = f"#{len(qlog)-i} {grade_icon} {q['query'][:60]}"
#             with st.expander(label):
#                 col_a, col_b, col_c = st.columns(3)
#                 col_a.metric("Latency", f"{q['elapsed']}s")
#                 col_b.metric("Retrieval", f"{method_icon} {q.get('method','?')}")
#                 col_c.metric("Chunks Found", q.get("chunks", "?"))

#                 st.markdown(f"**Original query:** {q['query']}")
#                 if was_rewritten:
#                     st.markdown(f"**🔄 Rewritten to:** {rewritten}")
#                 st.markdown(f"**Grade:** {grade_icon} `{q.get('grade', '?')}` | "
#                             f"**Attempts:** {q.get('attempts', 1)}")

#     st.divider()
#     st.subheader("🖥️ System Info")
#     si1, si2, si3 = st.columns(3)
#     si1.metric("Indexed Docs", len(st.session_state.pdf_hashes))
#     si2.metric("BM25 Corpus", len(st.session_state.bm25_corpus))
#     si3.metric("Memory Exchanges", st.session_state.memory.interaction_count if "memory" in st.session_state else 0)

#     bm25_status = "✅ Loaded" if st.session_state.bm25_index else "❌ Not built"
#     faiss_status = "✅ Loaded" if st.session_state.vectorstore else "❌ Not loaded"
#     st.markdown(f"**FAISS:** {faiss_status} | **BM25:** {bm25_status} | "
#                 f"**FAISS path:** `{FAISS_INDEX_PATH}`")

# # ════════════════════════════════════════════════════════
# # FOOTER
# # ════════════════════════════════════════════════════════

# st.divider()
# st.markdown("""
# <div style='text-align: center; color: #888; font-size: 12px;'>
# ✨ Production RAG v2 &nbsp;|&nbsp;
# 🔀 Hybrid BM25+FAISS &nbsp;|&nbsp;
# 🧠 Progressive Memory &nbsp;|&nbsp;
# 🚀 LangGraph + Groq + Live Evaluation
# </div>
# """, unsafe_allow_html=True)













import uuid




import streamlit as st
import fitz
import os
import hashlib
import time
import json
import re
import math
import pickle
import logging
from typing import List, Tuple, Optional, Dict
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict

from rag_evaluation_framework import RAGEvaluator, score_to_label, health_to_label



import shutil
def delete_session_storage():
    if os.path.exists(SESSION_DIR):
        shutil.rmtree(SESSION_DIR, ignore_errors=True)


        

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

BASE_DIR = "./storage"
SESSION_DIR = os.path.join(BASE_DIR, st.session_state.session_id)
os.makedirs(SESSION_DIR, exist_ok=True)


# ════════════════════════════════════════════════════════
# SETUP
# ════════════════════════════════════════════════════════

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
# FAISS_INDEX_PATH = "./faiss_index"         #----------------------------------------------------------
FAISS_INDEX_PATH = os.path.join(SESSION_DIR, "faiss_index")

# ── Structured logger (writes to stdout; redirect to file via shell if needed) ──
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("rag_app")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found in .env file")
    logger.critical("GROQ_API_KEY missing — app cannot start")
    st.stop()

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ════════════════════════════════════════════════════════
# MEMORY CLASS
# ════════════════════════════════════════════════════════

class DualRAGMemory:
    """
    Simple dual memory: sliding window buffer + periodic LLM summary.
    No LangChain memory classes needed — fully version-safe.
    """

    def __init__(self, buffer_size: int = 5, llm=None):
        self.buffer_size = buffer_size
        self.llm = llm
        self._exchanges: List[dict] = []   # [{"q": ..., "a": ...}]
        self._summary: str = ""
        self.token_count = 0
        self.interaction_count = 0

    def add_exchange(self, query: str, response: str):
        """Add exchange; trim buffer; progressively update summary every turn."""
        self._exchanges.append({"q": query, "a": response})
        if len(self._exchanges) > self.buffer_size:
            self._exchanges = self._exchanges[-self.buffer_size:]
        self.token_count += len(query.split()) + len(response.split())
        self.interaction_count += 1
        if self.llm:
            self._progressive_summary(query, response)

    def _progressive_summary(self, new_q: str, new_a: str):
        """
        Progressive summarisation: compress(prev_summary + new_exchange).
        Never loses prior context — each update compounds on the last.
        """
        try:
            prev = self._summary or "No prior summary."
            prompt = (
                "You are maintaining a running conversation summary.\n\n"
                f"PREVIOUS SUMMARY:\n{prev}\n\n"
                f"NEW EXCHANGE:\nUser: {new_q}\nAssistant: {new_a}\n\n"
                "Update the summary to include the new exchange. "
                "Keep it under 5 sentences. Preserve ALL important facts from the previous summary. "
                "Output ONLY the updated summary, nothing else."
            )
            result = self.llm.invoke(prompt)
            self._summary = result.content.strip()
        except Exception:
            pass  # Silent fail — summary is optional

    def get_recent(self) -> str:
        """Return recent exchanges as formatted text."""
        if not self._exchanges:
            return ""
        lines = []
        for ex in self._exchanges:
            lines.append(f"User: {ex['q']}")
            lines.append(f"Assistant: {ex['a']}")
        return "\n".join(lines)

    def get_summary(self) -> str:
        """Return the current conversation summary."""
        return self._summary

    def get_status(self) -> str:
        return "✅ Healthy" if self.token_count < 5000 else "⚠️ High"

    def reset(self):
        self._exchanges = []
        self._summary = ""
        self.token_count = 0
        self.interaction_count = 0

# ════════════════════════════════════════════════════════
# CACHED RESOURCES
# ════════════════════════════════════════════════════════

@st.cache_resource
def get_llm(model_name: str, temperature: float):
    return ChatGroq(api_key=GROQ_API_KEY, model_name=model_name, temperature=temperature)

@st.cache_resource
def get_embeddings(model_name: str = "BAAI/bge-base-en-v1.5"):
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

# ════════════════════════════════════════════════════════
# PDF PROCESSING
# ════════════════════════════════════════════════════════

def extract_text_from_pdf(file_bytes: bytes, filename: str) -> Tuple[List, int]:
    """
    Extract text with page-level metadata.
    Fallback: if full-document extraction fails, retries page-by-page
    so a single corrupt page does not drop the entire PDF.
    """
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        page_docs = []
        failed_pages = []
        for i, page in enumerate(doc):
            try:
                text = page.get_text("text").strip()
                if text:
                    page_docs.append({"text": text, "page": i + 1, "source": filename})
            except Exception as page_err:
                failed_pages.append(i + 1)
                logger.warning("PDF page extraction failed | file=%s page=%d error=%s",
                               filename, i + 1, page_err)
        if failed_pages:
            st.warning(f"⚠️ {filename}: {len(failed_pages)} page(s) skipped (corrupt/unreadable): {failed_pages[:5]}")
        logger.info("PDF extracted | file=%s pages_ok=%d pages_failed=%d",
                    filename, len(page_docs), len(failed_pages))
        return page_docs, len(doc)
    except Exception as e:
        logger.error("PDF open failed | file=%s error=%s", filename, e)
        st.error(f"❌ PDF error ({filename}): {e}")
        return [], 0

# Header patterns for technical PDFs (markdown headers, numbered sections, ALL-CAPS titles)
_HEADER_RE = re.compile(
    r"^(#{1,3}\s.{3,}|[A-Z][A-Z0-9 ]{5,50}$|\d+\.\d*\s+[A-Z].{4,}|Chapter\s+\d+|SECTION\s+\d+)",
    re.MULTILINE
)

def _detect_section(text: str) -> str:
    """Return the first header found in text, or empty string."""
    m = _HEADER_RE.search(text)
    return m.group(0).strip()[:80] if m else ""

def split_text_with_pages(page_docs: list, chunk_size: int = 1000, overlap: int = 200):
    """
    Header-aware chunking: detects section headings and annotates each chunk
    with its section. Falls back to RecursiveCharacterTextSplitter boundaries.
    Reason chosen over SemanticChunker: no heavy NLP dependency, preserves
    document hierarchy, fast, deterministic for technical PDFs.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    all_chunks = []
    for page_doc in page_docs:
        text   = page_doc["text"]
        source = page_doc["source"]
        page   = page_doc["page"]
        section = _detect_section(text)
        chunks = splitter.create_documents([text])
        for chunk in chunks:
            chunk.metadata["source"]  = source
            chunk.metadata["page"]    = page
            if section:
                chunk.metadata["section"] = section
        all_chunks.extend(chunks)
    return all_chunks

# ════════════════════════════════════════════════════════
# ADAPTIVE RETRIEVAL
# ════════════════════════════════════════════════════════

COMPLEX_KEYWORDS = [
    "compare", "difference", "explain", "analyze", "how does", "why does",
    "summarize", "describe", "elaborate", "relationship", "architecture",
    "workflow", "process", "mechanism", "contrast", "evaluate", "assess"
]

# Queries asking for people, lists, or enumerations also need deep retrieval
_LIST_KEYWORDS = [
    # Enumeration triggers
    "who", "list", "all", "every", "each", "enumerate",
    "names", "people", "entities",

    # Category/type queries
    "types", "categories", "kinds", "examples", "instances",

    # Component queries
    "components", "elements", "parts", "modules", "sections",
    "features", "properties", "attributes", "characteristics",

    # Process/step queries
    "steps", "stages", "phases", "methods", "techniques", "approaches",

    # People queries
    "members", "authors", "contributors", "participants", "team",

    # Pros/Cons
    "advantages", "disadvantages", "benefits", "drawbacks",
    "pros", "cons", "limitations", "challenges",

    # Requirements
    "requirements", "criteria", "conditions", "rules",
]


def get_adaptive_k(query: str, base_k: int) -> int:
    """
    Return retrieval depth based on query complexity.
    People / list queries get full base_k to maximise recall of name mentions.
    Simple factual queries still get at least ceil(base_k * 0.75) chunks.
    """
    q = query.lower()
    is_complex = len(query.split()) > 12 or any(kw in q for kw in COMPLEX_KEYWORDS)
    is_list_query = any(kw in q for kw in _LIST_KEYWORDS)
    if is_complex or is_list_query:
        return base_k          # Full depth for complex / list queries
    return max(6, round(base_k * 0.75))  # At least 6 chunks for any query

# ════════════════════════════════════════════════════════
# FAISS PERSISTENCE
# ════════════════════════════════════════════════════════

def save_faiss(vectorstore, embedding_model: str):
    """Persist FAISS index and record which embedding model built it."""
    try:
        vectorstore.save_local(FAISS_INDEX_PATH)
        with open(f"{FAISS_INDEX_PATH}/embedding_model.txt", "w") as f:
            f.write(embedding_model)
    except Exception as e:
        st.warning(f"⚠️ Could not save FAISS index: {e}")

def load_faiss(embeddings, embedding_model: str) -> Optional[object]:
    print("🔥 LOAD_F CALLED")                                             # ------------------------
    """Load persisted FAISS index if embedding model matches."""
    model_file = f"{FAISS_INDEX_PATH}/embedding_model.txt"
    index_file = f"{FAISS_INDEX_PATH}/index.faiss"
    if not (os.path.exists(index_file) and os.path.exists(model_file)):
        return None
    try:
        saved_model = open(model_file).read().strip()
        if saved_model != embedding_model:
            return None  # Model mismatch — must rebuild
        return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    except Exception:
        return None

# ════════════════════════════════════════════════════════
# BM25 — SPARSE RETRIEVAL
# ════════════════════════════════════════════════════════

# BM25_PATH = f"{FAISS_INDEX_PATH}/bm25.pkl"
BM25_PATH = os.path.join(SESSION_DIR, "bm25.pkl")

def build_bm25(docs: List) -> Tuple[object, List]:
    """Build BM25 index from a flat list of Document objects."""
    from rank_bm25 import BM25Okapi
    tokenized = [d.page_content.lower().split() for d in docs]
    return BM25Okapi(tokenized), docs

def save_bm25(bm25_obj, corpus: List):
    """Persist BM25 index and corpus to disk alongside FAISS."""
    try:
        os.makedirs(FAISS_INDEX_PATH, exist_ok=True)
        with open(BM25_PATH, "wb") as f:
            pickle.dump({"bm25": bm25_obj, "corpus": corpus}, f)
    except Exception as e:
        st.warning(f"⚠️ BM25 save failed: {e}")

def load_bm25() -> Tuple[Optional[object], Optional[List]]:
    print("🔥 LOAD_BM25 CALLED")                       #------------------------------------------------
    """Reload persisted BM25 index from disk."""
    if not os.path.exists(BM25_PATH):
        return None, None
    try:
        with open(BM25_PATH, "rb") as f:
            data = pickle.load(f)
        return data["bm25"], data["corpus"]
    except Exception:
        return None, None

def hybrid_retrieve(query: str, vectorstore, bm25_obj, bm25_corpus: List,
                    k: int, bm25_weight: float = 0.3) -> List:
    """
    Merge dense FAISS results with sparse BM25 results.
    bm25_weight controls how many of the k slots go to BM25.
    """
    n_bm25 = max(1, round(k * bm25_weight))
    n_dense = max(1, k - n_bm25)

    # Dense retrieval
    dense_docs = vectorstore.similarity_search(query, k=n_dense * 2)

    # Sparse BM25 retrieval
    bm25_docs: List = []
    if bm25_obj and bm25_corpus:
        tokens = query.lower().split()
        scores = bm25_obj.get_scores(tokens)
        top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:n_bm25 * 2]
        bm25_docs = [bm25_corpus[i] for i in top_idx if scores[i] > 0]

    # Merge, deduplicate by first 80 chars of content
    seen: set = set()
    merged: List = []
    for doc in dense_docs[:n_dense] + bm25_docs[:n_bm25]:
        key = doc.page_content[:80]
        if key not in seen:
            seen.add(key)
            merged.append(doc)
    return merged[:k]

# ════════════════════════════════════════════════════════
# PROMPT
# ════════════════════════════════════════════════════════

SYSTEM_PROMPT = ChatPromptTemplate.from_template("""You are a careful and thorough document-based question answering assistant.

CONVERSATION SUMMARY (for context):
{conversation_summary}

RECENT EXCHANGES:
{recent_history}

RETRIEVED DOCUMENTS:
{context}

QUESTION:
{input}

CRITICAL INSTRUCTIONS — READ CAREFULLY BEFORE ANSWERING:

1. ALWAYS search the retrieved documents thoroughly before concluding anything is unavailable.
2. Names, people, authors, students, members, contributors, candidates, team members, guides, supervisors,
   acknowledgements, group members, and participants may appear anywhere in the documents — in title pages,
   acknowledgement sections, author lists, or body text. Search ALL retrieved chunks for these.
3. If any relevant name, entity, fact, term, concept, date, or figure appears in the retrieved documents,
   you MUST include it in your answer. Do NOT omit found information.
4. NEVER say "This information is not available" when names, entities, or relevant facts ARE present
   in the retrieved context — even partially. Use what is found.
5. If information is PARTIALLY available: provide the supported part completely, then note what is missing.
6. ONLY respond with "This information is not available in the provided documents" when you have
   confirmed that zero supporting evidence exists across all retrieved chunks.
7. Answer using ONLY information from the retrieved documents. Do not use outside knowledge.
8. Do NOT speculate or invent details not present in the documents.
9. Cite sources using: [filename | Page N] after every factual claim.
10. Be thorough — completeness is important when names or lists are requested.

FINAL ANSWER:""")

# ════════════════════════════════════════════════════════
# LANGGRAPH — AGENTIC RAG STATE & NODES
# ════════════════════════════════════════════════════════

class RAGState(TypedDict):
    """Typed state passed through the LangGraph RAG pipeline."""
    query: str
    original_query: str
    documents: List[Document]
    answer: str
    sources: List[str]
    retrieval_attempts: int
    document_grade: str          # "relevant" | "not_relevant"
    retrieval_method: str        # "hybrid" | "faiss-only" | "hybrid+reranked"
    conversation_summary: str
    recent_history: str
    adaptive_k: int
    vectorstore: object
    bm25_index: object
    bm25_corpus: List
    bm25_weight: float
    llm: object
    rewrite_log: List
    confidence: Dict
    use_reranker: bool
    reranker: object


# ── Prompts for grading and rewriting ────────────────────

BATCH_GRADE_PROMPT = """You are a document relevance grader for a RAG system.

Question: {question}

Below are {n} retrieved document excerpts. For each, decide if it contains information useful for answering the question.

{documents}

Respond ONLY with a JSON array — one entry per document, in order:
[{{"id": 1, "score": "relevant"}}, {{"id": 2, "score": "not_relevant"}}, ...]
All {n} documents must appear. No extra text."""

REWRITE_PROMPT = """You are a query expansion assistant for a RAG system.
The original query failed to retrieve useful documents. Your task is to EXPAND the query using synonyms
and related terms — do NOT replace the original meaning or rephrase completely.

Rules:
- Keep the core subject and intent of the original query intact.
- Add synonyms and related vocabulary that might appear in academic reports or technical documents.
- For people-related queries (members, authors, students, etc.) expand with terms like:
  authors, contributors, students, candidates, team members, group members, participants, researchers.
- For role-related queries (supervisor, guide, mentor) expand with: advisor, faculty, professor, mentor.
- For project queries expand with: project, system, application, module, deliverable.
- Output a single expanded query on one line. Do NOT output multiple queries or bullet points.
- Output ONLY the expanded query, nothing else.

Original query: {question}

Expanded query (one line only):"""


# ── Confidence scoring (no LLM calls) ────────────────────

def compute_confidence(docs: List, answer: str) -> Dict:
    """
    Improved confidence scoring:
    - Retrieval confidence: normalised against a target of 4 docs (not 6) so
      returning 4-8 docs already gives high confidence.
    - Grounding confidence: weighted overlap with a length bonus to avoid
      penalising short, precise answers.
    """
    if not docs or not answer:
        return {"retrieval": 0.0, "grounding": 0.0}

    # Retrieval confidence — 4 docs = 100 %; scale gracefully above that
    retrieval_conf = round(min(1.0, len(docs) / 4), 2)

    # Grounding confidence — keyword overlap between context and answer
    stop = {"the", "a", "an", "is", "are", "was", "were", "in", "on",
            "at", "to", "for", "of", "and", "or", "not", "it", "this", "that",
            "be", "been", "by", "with", "as", "from", "its", "also", "have",
            "has", "had", "which", "that", "their", "they", "all", "one"}
    ctx_words: set = set()
    for d in docs:
        ctx_words.update(w.lower().strip(".,;:'\"") for w in d.page_content.split())
    ans_words = {w.lower().strip(".,;:'\"") for w in answer.split()} - stop
    ans_words = {w for w in ans_words if len(w) > 2}   # drop tiny words

    if not ans_words:
        return {"retrieval": retrieval_conf, "grounding": retrieval_conf}

    overlap = len(ans_words & ctx_words) / len(ans_words)
    # Boost for answers that are short (precise) — they should not be penalised
    length_bonus = min(0.15, 5 / max(len(ans_words), 1))
    grounding = round(min(1.0, overlap + length_bonus), 2)
    return {"retrieval": retrieval_conf, "grounding": grounding}


# ── Optional Cross-Encoder reranker ──────────────────────

@st.cache_resource
def get_reranker(model_name: str = "BAAI/bge-reranker-base"):
    from sentence_transformers import CrossEncoder
    return CrossEncoder(model_name)

def rerank_docs(reranker, query: str, docs: List, top_k: int = 5) -> List:
    """Score all candidates with CrossEncoder, return top_k."""
    if not docs:
        return docs
    pairs = [(query, d.page_content[:512]) for d in docs]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)
    return [d for _, d in ranked[:top_k]]


def node_retrieve(state: RAGState) -> RAGState:
    """Hybrid BM25 + FAISS retrieval with optional CrossEncoder reranking."""
    query  = state["query"]
    k      = state["adaptive_k"]
    has_bm25 = bool(state.get("bm25_index") and state.get("bm25_corpus"))

    fetch_k = 15 if state.get("use_reranker") else k

    docs = hybrid_retrieve(
        query=query,
        vectorstore=state["vectorstore"],
        bm25_obj=state.get("bm25_index"),
        bm25_corpus=state.get("bm25_corpus") or [],
        k=fetch_k,
        bm25_weight=state.get("bm25_weight", 0.3),
    )

    method = "hybrid" if has_bm25 else "faiss-only"

    # Optional reranking
    if state.get("use_reranker") and state.get("reranker") and docs:
        docs   = rerank_docs(state["reranker"], query, docs, top_k=min(5, k))
        method = "hybrid+reranked"

    logger.info("retrieval | query=%r attempt=%d method=%s docs=%d",
                query[:60], state["retrieval_attempts"] + 1, method, len(docs))

    return {**state, "documents": docs,
            "retrieval_attempts": state["retrieval_attempts"] + 1,
            "retrieval_method": method}


def node_grade_documents(state: RAGState) -> RAGState:
    """
    Batch-grade all retrieved docs in ONE LLM call (was N separate calls).
    Never marks docs as relevant on parse failure — conservative by default.
    """
    docs = state["documents"]
    if not docs:
        logger.info("grading | query=%r result=not_relevant (no docs)", state["query"][:60])
        return {**state, "document_grade": "not_relevant"}

    doc_block = ""
    for i, doc in enumerate(docs[:6]):
        section  = doc.metadata.get("section", "")
        sec_note = f" [{section}]" if section else ""
        doc_block += f"[Document {i+1}{sec_note}]:\n{doc.page_content[:400]}\n\n"

    prompt = BATCH_GRADE_PROMPT.format(
        question=state["query"],
        n=min(len(docs), 6),
        documents=doc_block.strip()
    )

    try:
        result = state["llm"].invoke(prompt)
        raw = result.content.strip()
        raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
        grades = json.loads(raw)
        relevant_count = sum(1 for g in grades if isinstance(g, dict) and g.get("score") == "relevant")
        grade = "relevant" if relevant_count >= 1 else "not_relevant"
    except Exception as exc:
        grade = "not_relevant"   # Conservative on parse failure
        logger.warning("grading parse failed | query=%r error=%s", state["query"][:60], exc)

    logger.info("grading | query=%r result=%s", state["query"][:60], grade)
    return {**state, "document_grade": grade}


def node_transform_query(state: RAGState) -> RAGState:
    """Rewrite query with semantic similarity guard to prevent drift."""
    original   = state["query"]
    rewrite_log = list(state.get("rewrite_log") or [])
    try:
        prompt = REWRITE_PROMPT.format(question=original)
        result = state["llm"].invoke(prompt)
        new_query = result.content.strip()

        orig_words = set(original.lower().split())
        new_words  = set(new_query.lower().split())
        overlap    = len(orig_words & new_words) / max(len(orig_words), 1)
        if overlap > 0.85:
            new_query = original   # Rewrite too similar — skip
    except Exception as exc:
        new_query = original
        logger.warning("query rewrite failed | error=%s", exc)

    rewrite_log.append({"original": original, "rewritten": new_query})
    logger.info("query_rewrite | original=%r rewritten=%r", original[:60], new_query[:60])
    return {**state, "query": new_query, "rewrite_log": rewrite_log}


def node_generate(state: RAGState) -> RAGState:
    """Generate answer; compute confidence scores from retrieved docs."""
    docs = state["documents"]
    context_parts, sources = [], []
    for doc in docs:
        src  = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "")
        sect = doc.metadata.get("section", "")
        citation = f"{src} | Page {page}" + (f" · {sect}" if sect else "") if page else src
        if citation not in sources:
            sources.append(citation)
        context_parts.append(f"[{citation}]\n{doc.page_content}")

    context  = "\n\n---\n\n".join(context_parts) if context_parts else "No documents retrieved."
    formatted = SYSTEM_PROMPT.format(
        conversation_summary=state["conversation_summary"] or "No prior summary.",
        recent_history=state["recent_history"] or "No recent exchanges.",
        context=context,
        input=state["query"]
    )
    response   = state["llm"].invoke(formatted)
    answer     = response.content
    confidence = compute_confidence(docs, answer)

    logger.info("generation | query=%r docs_used=%d sources=%d grounding=%.2f",
                state["query"][:60], len(docs), len(sources),
                confidence.get("grounding", 0))

    return {**state, "answer": answer, "sources": sources, "confidence": confidence}


def should_retry(state: RAGState) -> str:
    """Conditional edge: retry with rewritten query or go straight to generate."""
    if state["document_grade"] == "relevant":
        return "generate"
    if state["retrieval_attempts"] < 2:
        return "transform_query"   # Rewrite and retry once
    return "generate"              # Give up retrying, generate with what we have


def build_rag_graph() -> StateGraph:
    """Compile the LangGraph agentic RAG pipeline."""
    graph = StateGraph(RAGState)
    graph.add_node("retrieve", node_retrieve)
    graph.add_node("grade_documents", node_grade_documents)
    graph.add_node("transform_query", node_transform_query)
    graph.add_node("generate", node_generate)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "grade_documents")
    graph.add_conditional_edges(
        "grade_documents",
        should_retry,
        {"generate": "generate", "transform_query": "transform_query"}
    )
    graph.add_edge("transform_query", "retrieve")
    graph.add_edge("generate", END)
    return graph.compile()


# Compile once at module level (cached between reruns via Streamlit)
@st.cache_resource
def get_rag_graph():
    return build_rag_graph()

# ════════════════════════════════════════════════════════
# SESSION STATE
# ════════════════════════════════════════════════════════

EMBEDDING_MODELS = {
    "BGE Base (Recommended)": "BAAI/bge-base-en-v1.5",
    "MiniLM L6 (Fastest)": "sentence-transformers/all-MiniLM-L6-v2",
    "MPNet Base (Highest Quality)": "sentence-transformers/all-mpnet-base-v2",
}

def init_session():
    defaults = {
        "vectorstore": None,
        "bm25_index": None,
        "bm25_corpus": [],
        "chat_history": [],
        "pdf_hashes": set(),
        "chunk_info": {},
        "ingestion_timings": {},
        "last_processed_query": None,
        "eval_results": None,
        "interaction_log": [],
        "query_log": [],            # [{query, rewritten, method, attempts, elapsed}]
        "faiss_loaded": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════

with st.sidebar:
    # st.write("FAISS FULL PATH:", os.path.abspath(FAISS_INDEX_PATH))            #-----------------------------------
    st.header("⚙️ Configuration")

    st.subheader("🤖 LLM Model")
    model_choice = st.selectbox(
        "LLM Model",
        ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
        help="8B = Fast, 70B = Better Quality"
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)

    st.subheader("🧠 Embedding Model")
    embedding_label = st.selectbox(
        "Embedding Model",
        list(EMBEDDING_MODELS.keys()),
        help="BGE Base = best balance | MiniLM = fastest | MPNet = highest quality"
    )
    EMBEDDING_MODEL = EMBEDDING_MODELS[embedding_label]
    if st.session_state.get("active_embedding_model") and \
       st.session_state.active_embedding_model != EMBEDDING_MODEL and \
       st.session_state.vectorstore is not None:
        st.warning("⚠️ Embedding model changed! Clear docs and re-upload.")

    st.subheader("📑 Document Settings")
    chunk_size  = st.slider("Chunk Size", 200, 2000, 1000, 100)
    overlap_pct = st.slider("Overlap %", 5, 40, 20, 5)
    st.session_state.active_embedding_model = EMBEDDING_MODEL

    st.subheader("🔍 Retrieval")
    k_retrieve  = st.slider("Chunks to Retrieve", 3, 15, 8)
    bm25_weight = st.slider("BM25 Weight", 0.0, 1.0, 0.3, 0.05,
                             help="0 = pure FAISS | 1 = pure BM25 | 0.3 = recommended")

    st.subheader("🎯 Reranker (P2)")
    use_reranker = st.toggle("Enable Cross-Encoder Reranker", value=False,
                              help="BAAI/bge-reranker-base. Retrieves 15 candidates → keeps top 5. Adds ~0.5–1s latency.")
    if use_reranker:
        st.caption("Fetches 15 candidates, reranks, returns top 5")

    st.subheader("💾 Memory")
    memory_window = st.slider("Memory Window (exchanges)", 2, 10, 5)
    if "memory" not in st.session_state:
        st.session_state.memory = DualRAGMemory(buffer_size=memory_window,
                                                llm=get_llm(model_choice, temperature))
    elif st.session_state.memory.buffer_size != memory_window:
        old = st.session_state.memory
        st.session_state.memory = DualRAGMemory(buffer_size=memory_window,
                                                llm=get_llm(model_choice, temperature))
        st.session_state.memory.token_count      = old.token_count
        st.session_state.memory.interaction_count = old.interaction_count
        st.session_state.memory._summary          = old._summary

    st.caption(f"Status: {st.session_state.memory.get_status()}")
    st.caption(f"Tokens ≈ {st.session_state.memory.token_count} | Exchanges: {st.session_state.memory.interaction_count}")
    if st.session_state.memory._summary:
        with st.expander("📝 Memory Summary"):
            st.write(st.session_state.memory._summary)

    if st.button("🔄 Reset All", use_container_width=True):
        st.session_state.memory.reset()
        st.session_state.chat_history = []
        st.session_state.last_processed_query = None
        st.session_state.eval_results = None
        st.session_state.interaction_log = []
        delete_session_storage()                               #-------------------------------------->
        st.success("✅ Reset complete + storage cleared")
        st.rerun()

# ════════════════════════════════════════════════════════
# LOAD FAISS ON STARTUP (once per session)
# ════════════════════════════════════════════════════════

if not st.session_state.faiss_loaded and st.session_state.vectorstore is None:
    # pass
    embeddings = get_embeddings(EMBEDDING_MODEL)
    loaded = load_faiss(embeddings, EMBEDDING_MODEL)        
    if loaded:
        st.session_state.vectorstore = loaded
        # Also reload BM25 index from disk
        bm25_obj, bm25_corpus = load_bm25()         
        if bm25_obj:
            st.session_state.bm25_index  = bm25_obj
            st.session_state.bm25_corpus = bm25_corpus
            st.sidebar.success("📂 FAISS + BM25 loaded from disk")
        else:
            st.sidebar.success("📂 FAISS index loaded from disk")
    st.session_state.faiss_loaded = True

# ════════════════════════════════════════════════════════
# MAIN LAYOUT
# ════════════════════════════════════════════════════════

st.title("📄 Enterprise Document Intelligence")
st.markdown("Agentic RAG with LangGraph, FAISS, BM25 and Memory")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 Chat", "📚 Documents", "📜 History", "📊 Evaluation", "🔧 Debug"
])

# ════════════════════════════════════════════════════════
# TAB 1: CHAT
# ════════════════════════════════════════════════════════

with tab1:
    col1, col2 = st.columns([4, 1])
    with col1:
        uploaded_files = st.file_uploader("📤 Upload PDF", type=["pdf"], accept_multiple_files=True)
    with col2:
        if st.button("Clear Docs", use_container_width=True):
            st.session_state.vectorstore   = None
            st.session_state.bm25_index    = None
            st.session_state.bm25_corpus   = []
            st.session_state.pdf_hashes    = set()
            st.session_state.chunk_info    = {}
            st.session_state.ingestion_timings = {}
            delete_session_storage()                        #------------------------------------------>
            st.success("✅ Cleared!")
            st.rerun()

    # PDF Processing
    if uploaded_files:
        new_files = [
            (pdf, hashlib.md5(pdf.getvalue()).hexdigest())
            for pdf in uploaded_files
            if hashlib.md5(pdf.getvalue()).hexdigest() not in st.session_state.pdf_hashes
        ]

        if new_files:
            progress_bar = st.progress(0)
            status_text  = st.empty()
            timing_placeholder = st.empty()
            embeddings = get_embeddings(EMBEDDING_MODEL)
            all_new_docs: List = []

            for idx, (pdf, file_hash) in enumerate(new_files):
                timings: Dict = {}
                status_text.text(f"📄 Processing: {pdf.name}")
                try:
                    # ─ Step 1: PDF extraction ─────────────────────────
                    t0 = time.time()
                    page_docs, num_pages = extract_text_from_pdf(pdf.getvalue(), pdf.name)
                    timings["extract"] = round(time.time() - t0, 2)
                    if not page_docs:
                        st.warning(f"⚠️ No text in {pdf.name}")
                        continue

                    # ─ Step 2: Chunking ─────────────────────────────
                    t0 = time.time()
                    overlap = int(chunk_size * overlap_pct / 100)
                    docs = split_text_with_pages(page_docs, chunk_size, overlap)
                    timings["chunk"] = round(time.time() - t0, 2)
                    if not docs:
                        st.warning(f"⚠️ Could not split {pdf.name}")
                        continue

                    char_counts = [len(d.page_content) for d in docs]
                    st.session_state.chunk_info[pdf.name] = {
                        "chunks": len(docs), "avg_size": round(sum(char_counts)/len(char_counts)),
                        "pages": num_pages, "total_chars": sum(char_counts)
                    }

                    # ─ Step 3: Embedding + FAISS indexing ───────────────
                    status_text.text(f"🔍 Embedding: {pdf.name} ({len(docs)} chunks)")
                    t0 = time.time()
                    if st.session_state.vectorstore is None:
                        st.session_state.vectorstore = FAISS.from_documents(docs, embeddings)
                    else:
                        st.session_state.vectorstore.add_documents(docs)
                    timings["embed_index"] = round(time.time() - t0, 2)

                    all_new_docs.extend(docs)
                    st.session_state.pdf_hashes.add(file_hash)
                    st.session_state.ingestion_timings[pdf.name] = timings

                except Exception as e:
                    st.error(f"❌ Error processing {pdf.name}: {e}")

                progress_bar.progress((idx + 1) / len(new_files))

            # ─ Step 4: Persist FAISS + build & save BM25 ───────
            if st.session_state.vectorstore:
                status_text.text("💾 Saving indexes...")
                t0 = time.time()
                save_faiss(st.session_state.vectorstore, EMBEDDING_MODEL)      #---------------------------------
                save_t = round(time.time() - t0, 2)

                t0 = time.time()
                existing_corpus = st.session_state.bm25_corpus or []
                merged_corpus = existing_corpus + all_new_docs
                bm25_obj, bm25_corpus = build_bm25(merged_corpus)
                st.session_state.bm25_index  = bm25_obj
                st.session_state.bm25_corpus = bm25_corpus
                save_bm25(bm25_obj, bm25_corpus)                         #---------------------------------
                bm25_t = round(time.time() - t0, 2)
                logger.info("upload | files=%d faiss_save=%.2fs bm25_build=%.2fs",
                            len(new_files), save_t, bm25_t)

            progress_bar.empty()
            status_text.empty()
            st.success(f"✅ Loaded {len(new_files)} PDF(s)! | FAISS save: {save_t}s | BM25 build: {bm25_t}s")

    st.divider()

    # Chat Interface
    if st.session_state.vectorstore is None:
        st.info("⬆️ Upload a PDF to start chatting")
    else:
        # Render existing history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                if "time" in msg:
                    st.caption(f"⏱️ {msg['time']:.2f}s")

        query = st.chat_input("Ask a question about your documents...")

        if query and query != st.session_state.last_processed_query:
            st.session_state.last_processed_query = query

            with st.chat_message("user"):
                st.write(query)

            with st.spinner("🤔 Analyzing..."):
                try:
                    start_time = time.time()
                    llm = get_llm(model_choice, temperature)
                    adaptive_k = get_adaptive_k(query, k_retrieve)

                    # Load reranker only if toggled on
                    reranker_obj = get_reranker() if use_reranker else None

                    rag_graph = get_rag_graph()
                    initial_state: RAGState = {
                        "query":                query,
                        "original_query":       query,
                        "documents":            [],
                        "answer":               "",
                        "sources":              [],
                        "retrieval_attempts":   0,
                        "document_grade":       "",
                        "retrieval_method":     "",
                        "conversation_summary": st.session_state.memory.get_summary(),
                        "recent_history":       st.session_state.memory.get_recent(),
                        "adaptive_k":           adaptive_k,
                        "vectorstore":          st.session_state.vectorstore,
                        "bm25_index":           st.session_state.bm25_index,
                        "bm25_corpus":          st.session_state.bm25_corpus,
                        "bm25_weight":          bm25_weight,
                        "llm":                  llm,
                        "rewrite_log":          [],
                        "confidence":           {},
                        "use_reranker":         use_reranker,
                        "reranker":             reranker_obj,
                    }
                    final_state = rag_graph.invoke(initial_state)

                    answer         = final_state["answer"]
                    retrieved_docs  = final_state["documents"]
                    sources        = final_state["sources"]
                    retries        = final_state["retrieval_attempts"] - 1
                    doc_grade      = final_state["document_grade"]
                    ret_method     = final_state.get("retrieval_method", "faiss-only")
                    confidence     = final_state.get("confidence", {})
                    rewrite_log    = final_state.get("rewrite_log", [])
                    elapsed        = time.time() - start_time

                    # Append to query analytics log
                    st.session_state.query_log.append({
                        "query":       query,
                        "rewritten":   rewrite_log[-1]["rewritten"] if rewrite_log else query,
                        "method":      ret_method,
                        "attempts":    final_state["retrieval_attempts"],
                        "grade":       doc_grade,
                        "elapsed":     round(elapsed, 2),
                        "chunks":      len(retrieved_docs),
                    })
                    st.session_state.query_log = st.session_state.query_log[-20:]

                    st.session_state.memory.add_exchange(query, answer)
                    st.session_state.interaction_log.append({
                        "question": query, "answer": answer, "retrieved_docs": retrieved_docs
                    })
                    st.session_state.interaction_log = st.session_state.interaction_log[-10:]

                    with st.chat_message("assistant"):
                        st.write(answer)

                        # ─ Status bar: grade | method | time | chunks
                        c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1])
                        with c1:
                            st.caption(f"📎 {' · '.join(sources[:2])}")
                        with c2:
                            grade_icon = "🟢" if doc_grade == "relevant" else "🟡"
                            retry_txt  = f" (×{retries})" if retries > 0 else ""
                            st.caption(f"{grade_icon} {doc_grade}{retry_txt}")
                        with c3:
                            # Retrieval method badge
                            method_icons = {"hybrid": "🔀", "faiss-only": "📊", "hybrid+reranked": "⭐"}
                            m_icon = method_icons.get(ret_method, "📊")
                            st.caption(f"{m_icon} {ret_method}")
                        with c4:
                            st.caption(f"⏱️ {elapsed:.2f}s")
                        with c5:
                            st.caption(f"📄 {len(retrieved_docs)} chunks")

                        # ─ Confidence scores
                        if confidence:
                            rc = confidence.get("retrieval", 0)
                            gc = confidence.get("grounding", 0)
                            cf1, cf2 = st.columns(2)
                            cf1.metric("📊 Retrieval Conf.", f"{rc:.0%}")
                            cf2.metric("📌 Grounding Conf.", f"{gc:.0%}")

                        # ─ Query rewrite log
                        if rewrite_log and rewrite_log[0]["original"] != rewrite_log[0]["rewritten"]:
                            with st.expander("🔄 Query was rewritten"):
                                for entry in rewrite_log:
                                    st.markdown(f"**Original:** {entry['original']}")
                                    st.markdown(f"**Rewritten:** {entry['rewritten']}")

                        # ─ Retrieved chunks
                        with st.expander("📋 Retrieved Chunks"):
                            for i, doc in enumerate(retrieved_docs[:6]):
                                src  = doc.metadata.get("source", "Unknown")
                                page = doc.metadata.get("page", "")
                                sect = doc.metadata.get("section", "")
                                header = f"**Chunk {i+1}** — `{src}` | Page {page}"
                                if sect:
                                    header += f" | *{sect}*"
                                st.markdown(header)
                                st.text(doc.page_content[:400] + ("..." if len(doc.page_content) > 400 else ""))
                                st.divider()

                    st.session_state.chat_history.append({"role": "user", "content": query})
                    st.session_state.chat_history.append({"role": "assistant", "content": answer, "time": elapsed})

                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ════════════════════════════════════════════════════════
# TAB 2: DOCUMENTS
# ════════════════════════════════════════════════════════

with tab2:
    st.header("📚 Document Information")

    if not st.session_state.chunk_info:
        st.info("No documents loaded yet")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Files", len(st.session_state.chunk_info))
        col2.metric("Total Chunks", sum(v["chunks"] for v in st.session_state.chunk_info.values()))
        col3.metric("Total Pages", sum(v["pages"] for v in st.session_state.chunk_info.values()))
        col4.metric("Total Size", f"{sum(v['total_chars'] for v in st.session_state.chunk_info.values()) // 1000}KB")

        st.divider()
        for fname, info in st.session_state.chunk_info.items():
            with st.expander(f"📄 {fname}"):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Chunks", info["chunks"])
                c2.metric("Avg Size", f"{info['avg_size']} chars")
                c3.metric("Total Size", f"{info['total_chars']:,} chars")
                c4.metric("Pages", info["pages"])
                avg = info["avg_size"]
                if avg < 300:
                    st.warning("⚠️ Chunks are small — consider increasing chunk size")
                elif avg > 1500:
                    st.warning("⚠️ Chunks are large — consider reducing chunk size")
                else:
                    st.success("✅ Optimal chunk size")

                # Ingestion timing breakdown
                timings = st.session_state.ingestion_timings.get(fname, {})
                if timings:
                    st.caption("**⏱️ Ingestion Timing:**")
                    tc1, tc2, tc3 = st.columns(3)
                    tc1.metric("PDF Extract", f"{timings.get('extract', '-')}s")
                    tc2.metric("Chunking",    f"{timings.get('chunk', '-')}s")
                    tc3.metric("Embed+Index", f"{timings.get('embed_index', '-')}s")
                    total = sum(v for v in timings.values() if isinstance(v, (int, float)))
                    st.caption(f"Total ingestion: **{total:.2f}s** | "
                               f"Throughput: **{round(info['chunks']/max(timings.get('embed_index',1),0.01))} chunks/s**")

# ════════════════════════════════════════════════════════
# TAB 3: HISTORY
# ════════════════════════════════════════════════════════

with tab3:
    st.header("📜 Chat History")

    if not st.session_state.chat_history:
        st.info("No conversation yet")
    else:
        user_msgs = [m for m in st.session_state.chat_history if m["role"] == "user"]
        asst_msgs = [m for m in st.session_state.chat_history if m["role"] == "assistant"]
        col1, col2 = st.columns(2)
        col1.metric("User Messages", len(user_msgs))
        col2.metric("Responses", len(asst_msgs))

        st.divider()
        for msg in st.session_state.chat_history:
            icon = "🧑" if msg["role"] == "user" else "🤖"
            st.write(f"**{icon} {msg['role'].upper()}**")
            content = msg["content"]
            st.write(content[:300] + ("..." if len(content) > 300 else content[300:]))
            if "time" in msg:
                st.caption(f"⏱️ {msg['time']:.2f}s")
            st.divider()

# ════════════════════════════════════════════════════════
# TAB 4: LIVE EVALUATION
# ════════════════════════════════════════════════════════

with tab4:
    st.header("📊 Live RAG Evaluation Dashboard")
    st.markdown("Evaluate recent interactions using the existing LLM. Scores are based on retrieval quality, faithfulness, and hallucination risk.")

    interaction_count = len(st.session_state.interaction_log)

    if interaction_count == 0:
        st.info("💬 Ask at least one question in the Chat tab first — the evaluation button will activate once you have interactions to score.")

    # Always show slider + button — disabled when no interactions
    n_to_eval = st.slider(
        "Number of recent interactions to evaluate",
        min_value=1,
        max_value=max(2, interaction_count),   # Always >= 2 to avoid min==max crash
        value=max(1, min(3, interaction_count)),
        disabled=(interaction_count == 0)
    )

    if interaction_count > 0:
        st.write(f"**{interaction_count}** interaction(s) available for evaluation.")

    run_eval = st.button(
        "🔍 Run Evaluation",
        type="primary",
        use_container_width=True,
        disabled=(interaction_count == 0),
        help="Ask questions in the Chat tab first to enable evaluation."
    )

    if run_eval and interaction_count > 0:
        with st.spinner("🤔 Evaluating... (1 LLM call per interaction)"):
            try:
                llm = get_llm(model_choice, temperature)
                evaluator = RAGEvaluator(llm=llm)
                recent = st.session_state.interaction_log[-n_to_eval:]
                batch_result = evaluator.evaluate_batch(recent)
                batch_result["_n_eval"] = n_to_eval
                st.session_state.eval_results = batch_result
            except Exception as e:
                st.error(f"❌ Evaluation failed: {e}")

    # Display results — always shown if available (persists across reruns)
    if st.session_state.eval_results:
        res = st.session_state.eval_results

        if res.get("error") and res.get("count", 0) == 0:
            st.error(f"Evaluation error: {res['error']}")
        else:
            st.divider()
            st.subheader("📈 Aggregate Scores")

            health = res["overall_health"]
            health_label = health_to_label(health)
            st.metric("🏥 Overall Health Score", f"{health}/100", delta=health_label)
            st.progress(health / 100)

            st.divider()

            c1, c2, c3, c4 = st.columns(4)
            rq = res["retrieval_quality"]
            cc = res["context_coverage"]
            sg = res["source_grounding"]
            hr = res["hallucination_risk"]
            fs = res["faithfulness_score"]

            with c1:
                st.metric("🔍 Retrieval Quality", f"{rq}/10")
                st.caption(score_to_label(rq))
                st.progress(rq / 10)

            with c2:
                st.metric("📖 Context Coverage", f"{cc}/10")
                st.caption(score_to_label(cc))
                st.progress(cc / 10)

            with c3:
                st.metric("📌 Faithfulness Score", f"{fs}/100")
                st.caption(score_to_label(sg))
                st.progress(fs / 100)

            with c4:
                st.metric("⚠️ Hallucination Risk", f"{hr}/10")
                st.caption(score_to_label(hr, invert=True))
                st.progress(hr / 10)

            st.divider()

            if res.get("results"):
                st.subheader("🔎 Per-Interaction Breakdown")
                _n = res.get("_n_eval", len(res["results"]))
                recent_log = st.session_state.interaction_log[-_n:]

                for i, (interaction, r) in enumerate(zip(recent_log, res["results"])):
                    q_preview = interaction["question"][:80] + ("..." if len(interaction["question"]) > 80 else "")
                    status = "✅" if r.get("error") is None else "❌"
                    with st.expander(f"{status} Interaction {i+1}: {q_preview}"):
                        if r.get("error"):
                            st.warning(f"Evaluation error: {r['error']}")
                        else:
                            ic1, ic2, ic3, ic4 = st.columns(4)
                            ic1.metric("Retrieval", f"{r['retrieval_quality']}/10")
                            ic2.metric("Coverage", f"{r['context_coverage']}/10")
                            ic3.metric("Grounding", f"{r['source_grounding']}/10")
                            ic4.metric("Hallucination", f"{r['hallucination_risk']}/10")
                            st.caption(f"💬 **Reasoning:** {r.get('reasoning', 'N/A')}")

# ════════════════════════════════════════════════════════
# TAB 5: DEBUG — QUERY ANALYTICS
# ════════════════════════════════════════════════════════

with tab5:
    st.header("🔧 Debug — Query Analytics")
    st.markdown("Real-time view of every query processed this session.")

    qlog = st.session_state.query_log
    if not qlog:
        st.info("No queries yet. Ask a question in the Chat tab.")
    else:
        # Aggregate summary
        avg_elapsed = round(sum(q["elapsed"] for q in qlog) / len(qlog), 2)
        hybrid_count = sum(1 for q in qlog if "hybrid" in q.get("method", ""))
        rewrite_count = sum(1 for q in qlog if q.get("query") != q.get("rewritten"))
        relevant_count = sum(1 for q in qlog if q.get("grade") == "relevant")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Queries", len(qlog))
        m2.metric("Avg Latency", f"{avg_elapsed}s")
        m3.metric("Hybrid Retrievals", f"{hybrid_count}/{len(qlog)}")
        m4.metric("Queries Rewritten", rewrite_count)

        st.divider()
        st.subheader("📋 Per-Query Log (last 20)")
        for i, q in enumerate(reversed(qlog)):
            rewritten = q.get("rewritten", q["query"])
            was_rewritten = rewritten != q["query"]
            grade_icon = "🟢" if q.get("grade") == "relevant" else "🟡"
            method_icon = {"hybrid": "🔀", "faiss-only": "📊", "hybrid+reranked": "⭐"}.get(q.get("method",""), "📊")
            label = f"#{len(qlog)-i} {grade_icon} {q['query'][:60]}"
            with st.expander(label):
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Latency", f"{q['elapsed']}s")
                col_b.metric("Retrieval", f"{method_icon} {q.get('method','?')}")
                col_c.metric("Chunks Found", q.get("chunks", "?"))

                st.markdown(f"**Original query:** {q['query']}")
                if was_rewritten:
                    st.markdown(f"**🔄 Rewritten to:** {rewritten}")
                st.markdown(f"**Grade:** {grade_icon} `{q.get('grade', '?')}` | "
                            f"**Attempts:** {q.get('attempts', 1)}")

    st.divider()
    st.subheader("🖥️ System Info")
    si1, si2, si3 = st.columns(3)
    si1.metric("Indexed Docs", len(st.session_state.pdf_hashes))
    si2.metric("BM25 Corpus", len(st.session_state.bm25_corpus))
    si3.metric("Memory Exchanges", st.session_state.memory.interaction_count if "memory" in st.session_state else 0)

    bm25_status = "✅ Loaded" if st.session_state.bm25_index else "❌ Not built"
    faiss_status = "✅ Loaded" if st.session_state.vectorstore else "❌ Not loaded"
    # st.markdown(f"**FAISS:** {faiss_status} | **BM25:** {bm25_status} | "
    #             f"**FAISS path:** `{FAISS_INDEX_PATH}`")
    st.markdown(f"""**FAISS:** {faiss_status} | **BM25:** {bm25_status}  
                🔒 Storage: Session-based isolated index
                """)

# ════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════

st.divider()
st.markdown("""
<div style='text-align: center; color: #888; font-size: 12px;'>
Made by Tanmay 🖤 <br>
🔀 Hybrid Retrieval (FAISS + BM25) |
🧠 Conversational Memory |
🚀 LangGraph + Groq
</div>
""", unsafe_allow_html=True)