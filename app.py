# -*- coding: utf-8 -*-
import google.generativeai as genai
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from datasets import load_dataset
import gradio as gr
import os
from dotenv import load_dotenv  # <- YENİ EKLENDİ

# .env dosyasını yükle
load_dotenv()

# API Key'leri .env dosyasından al
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# API Key kontrolü
if not GOOGLE_API_KEY or not HF_TOKEN:
    raise ValueError("API Key'ler bulunamadı! Lütfen .env dosyasını kontrol edin.")

os.environ['HUGGINGFACE_HUB_TOKEN'] = HF_TOKEN
genai.configure(api_key=GOOGLE_API_KEY)

# Veri setini yükle ve vektör veritabanını oluştur
def initialize_system():
    print("Sistem başlatılıyor...")
    
    # Veri setini yükle
    dataset = load_dataset("aliarda/Turkish-Poems-19K", token=HF_TOKEN)
    print(f"Veri seti yüklendi! Toplam {len(dataset['train'])} şiir bulundu.")

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
    print("FAISS veritabanı oluşturuldu!")

    # LLM ve RAG zinciri
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.8
    )

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )

    print("Sistem hazır! Şiir üretmeye hazırsınız")
    return qa_chain

# Sistemi başlat
qa_chain = initialize_system()

# Şiir üretici fonksiyon
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

    try:
        response = qa_chain.invoke({"question": prompt, "chat_history": []})
        return response["answer"].strip()
    except Exception as e:
        return f"Bir hata oluştu: {str(e)}"

# Gradio arayüzü
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
    title="Türkçe Şiir Üretici - Akbank GenAI Bootcamp",
    description="RAG tabanlı Türkçe şiir üretici. Bir tema yazın, AI şiir oluştursun!",
    theme="soft",
    allow_flagging="never"
)

# Render için özel launch
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
        share=False
    )
