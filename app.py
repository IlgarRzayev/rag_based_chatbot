# -*- coding: utf-8 -*-

import google.generativeai as genai
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from datasets import load_dataset
import gradio as gr
import os

# Ortam değişkenlerinden al
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# Eğer ortam değişkeni bulunmazsa kullanıcıdan al
if not GOOGLE_API_KEY:
    GOOGLE_API_KEY = input("Lütfen Google Gemini API anahtarınızı girin: ").strip()

if not HF_TOKEN:
    HF_TOKEN = input("Lütfen Hugging Face token’ınızı girin: ").strip()

# Ortam değişkenlerine yeniden kaydet (bazı kütüphaneler buna ihtiyaç duyar)
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["HUGGINGFACE_HUB_TOKEN"] = HF_TOKEN



# Dataset'i private token ile yükle
dataset = load_dataset("aliarda/Turkish-Poems-19K")
print(f"Veri seti yüklendi! Toplam {len(dataset['train'])} şiir bulundu.")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable bulunamadı!")

genai.configure(api_key=GOOGLE_API_KEY)

poems = [
    item["siir_metni"].strip()
    for item in dataset["train"]
    if item["siir_metni"] and isinstance(item["siir_metni"], str) and item["siir_metni"].strip()
]
poems = poems[:1000]
print(f"{len(poems)} şiir işleme alındı.")

# Embedding ve vektör veritabanı
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)

docs = []
for p in poems:
    if p and isinstance(p, str) and p.strip():
        docs.extend(text_splitter.create_documents([p.strip()]))

vectorstore = FAISS.from_documents(docs, embeddings)
print("✅ FAISS veritabanı oluşturuldu!")

# RAG mantığı: ChatGoogleGenerativeAI + FAISS retriever
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.8
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# .chains kullanmadan QA fonksiyonu oluştur
def qa_chain(question, chat_history=[]):
    docs = retriever.invoke(question)
    context = "\n\n".join([d.page_content for d in docs])
    prompt_text = f"Soru: {question}\n\nBağlam:\n{context}\n\nCevap:"
    response = llm.invoke(prompt_text)
    return response


print("Sistem hazır! Şiir üretmeye hazırsınız")

# Gradio arayüzü
def siir_uretici(tema):
    prompt = f"""Türkçe, sanatsal ve kafiyeli bir şiir yaz.
    Şiir şu temaya uygun olmalı: '{tema}'.
    Veri tabanındaki Türkçe şiirlerin tarzından esinlen:
    Şiir özellikleri:
    - Her dize kısa olsun (4–8 kelime arası)
    - Son kelimelerde kafiye uyumu bulunsun
    - Gerekirse iç uyak (iç kafiye) da kullanılabilir
    - Akıcı, duygusal ve imgelerle dolu olsun
    - Doğa ve insan temaları kullanılabilir
    - Sadece şiiri yaz, açıklama yapma.
    """

    response = qa_chain(prompt, chat_history=[])
    return response.content.strip()


demo = gr.Interface(
    fn=siir_uretici,
    inputs=gr.Textbox(
        label="🎭 Şiir Teması",
        placeholder="Örnek: Ayrılık, doğa, aşk...",
        lines=1
    ),
    outputs=gr.Textbox(
        label="Üretilen Şiir",
        lines=10,
        max_lines=20
    ),
    title="Türkçe Şiir Üretici",
    theme="soft",
    allow_flagging="never"
)

if __name__ == "__main__":
    demo.launch()
