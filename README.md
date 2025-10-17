



# 🎭 Türkçe Şiir Üretici - RAG Tabanlı AI Asistanı

  

<div  align="center">

  

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

![LangChain](https://img.shields.io/badge/LangChain-⚡-orange)

![Gemini](https://img.shields.io/badge/Google-GeminiAI-blue)

![FAISS](https://img.shields.io/badge/VectorDB-FAISS-green)

  

**Kullanıcının girdiği temaya göre özgün Türkçe şiirler üreten yapay zeka asistanı**

  

[🌐 Web Uygulaması](#-web-uygulaması) • [🚀 Hızlı Başlangıç](#-hızlı-başlangıç) • [📊 Veri Seti](#-veri-seti) • [🏗️ Mimari](#️-mimari)

  

</div>

  

## 🎯 Proje Amacı

  

Bu proje, **Retrieval Augmented Generation (RAG)** mimarisi kullanarak, kullanıcıların belirlediği temalara uygun **orijinal Türkçe şiirler** üreten bir yapay zeka asistanıdır. Geleneksel Türk şiirinden öğrenerek yeni ve yaratıcı şiirler oluşturur.

  

---

  

## 🌟 Özellikler

  

- 🎨 **Tema Tabanlı Şiir Üretimi**: Kullanıcının girdiği her temaya uygun şiirler

- 📚 **Türk Edebiyatı Bilgisi**: 19.000+ şiirden oluşan veri seti

- 🤖 **Akıllı AI Modeli**: Google Gemini 2.5 Pro ile gelişmiş metin üretimi

- ⚡ **Hızlı Arama**: FAISS ile anında benzer şiir bulma

- 🎭 **Kafiye ve Ahenk**: Otomatik kafiye ve şiirsel yapı oluşturma

- 🌐 **Kullanıcı Dostu Arayüz**: Gradio ile modern web arayüzü

  

---

  


<div align="center">

## 🛠️ Teknolojiler

<table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%;">
  <thead style="background-color: #f8f9fa;">
    <tr>
      <th width="20%">Kategori</th>
      <th width="30%">Teknoloji</th>
      <th width="35%">Açıklama</th>
      <th width="15%">Versiyon</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>🤖 AI Model</strong></td>
      <td>Google Gemini 2.5 Pro</td>
      <td>Şiir üretimi için ana LLM</td>
      <td><code>Pro</code></td>
    </tr>
    <tr style="background-color: #f8f9fa;">
      <td><strong>🔤 Embedding</strong></td>
      <td>Multilingual MiniLM</td>
      <td>Metin vektörleştirme</td>
      <td><code>v2</code></td>
    </tr>
    <tr>
      <td><strong>🗄️ Vector DB</strong></td>
      <td>FAISS</td>
      <td>Benzerlik arama motoru</td>
      <td><code>CPU</code></td>
    </tr>
    <tr style="background-color: #f8f9fa;">
      <td><strong>⚡ Framework</strong></td>
      <td>LangChain</td>
      <td>RAG pipeline yönetimi</td>
      <td><code>0.1+</code></td>
    </tr>
    <tr>
      <td><strong>🌐 Web UI</strong></td>
      <td>Gradio</td>
      <td>Kullanıcı arayüzü</td>
      <td><code>4.0+</code></td>
    </tr>
    <tr style="background-color: #f8f9fa;">
      <td><strong>🐍 Programlama</strong></td>
      <td>Python</td>
      <td>Ana programlama dili</td>
      <td><code>3.8+</code></td>
    </tr>
    <tr>
      <td><strong>📊 Veri Seti</strong></td>
      <td>Hugging Face</td>
      <td>Türkçe şiir koleksiyonu</td>
      <td><code>19K</code></td>
    </tr>
    <tr style="background-color: #f8f9fa;">
      <td><strong>🔗 API</strong></td>
      <td>Google Generative AI</td>
      <td>Gemini API erişimi</td>
      <td><code>v1</code></td>
    </tr>
  </tbody>
</table>

</div>

  

---

  

## 📊 Veri Seti

  

### 📖 Veri Kaynağı

-  **Platform**: Hugging Face Datasets

-  **Veri Seti**: `aliarda/Turkish-Poems-19K`

-  **İçerik**: 19.026 adet Türkçe şiir

-  **Kullanım**: Projede ilk 1.000 şiir işleme alınmıştır

  

# 🚀 Hızlı Başlangıç

## 📋 Ön Koşullar
- Python 3.8+
- Google Gemini API anahtarı
- Hugging Face token

---

#### 1. Repository'yi Klonlayın
```bash
git clone https://github.com/IlgarRzayev/rag-based-project.git
cd rag-based-project
```
####  2. `.env` dosyasını oluştur ve API anahtarlarını ekle
```bash
GOOGLE_API_KEY=your_api_key
HF_TOKEN=your_huggingface_token
```

####  3. Gerekli kütüphaneleri yükleyin
```bash
pip install -r requirements.txt
```

####  4. Uygulamayı Başlatın
```bash
jupyter notebook
```
-   Açılan tarayıcıda `turkish-poem-rag.ipynb` dosyasını açın
    
-   Üst menüden **Run All** ile tüm hücreleri çalıştırın

# 📁 Proje Yapısı

```bash
rag_based_chatbot/
├── rag_based_project.ipynb      # Ana proje notebook'u
├── requirements.txt             # Bağımlılıklar
├── README.md                    # Bu dosya

```
