# -*- coding: utf-8 -*-
import os
import gradio as gr
import google.generativeai as genai

# Render port'u 
PORT = int(os.environ.get("PORT", 7860))

# Environment variables'dan API anahtarlarını al
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")

# API Key kontrolü
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY bulunamadı!")

genai.configure(api_key=GOOGLE_API_KEY)

print(f"🚀 Uygulama başlatılıyor... Port: {PORT}")

# Şiir üretici fonksiyon - SADECE GEMINI KULLAN
def siir_uretici(tema):
    if not tema or not tema.strip():
        return "Lütfen bir şiir teması giriniz."
    
    try:
        # Gemini modelini kullan
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Aşağıdaki kurallara uygun, Türkçe, sanatsal ve kafiyeli bir şiir yaz:
        
        TEMA: {tema}
        
        ŞİİR KURALLARI:
        - 4-8 dize (satır) arasında olsun
        - Her dize 4-8 kelime uzunluğunda olsun  
        - Son kelimelerde kafiye uyumu olsun
        - İç uyak (iç kafiye) da kullanabilirsin
        - Akıcı, duygusal ve imgelerle dolu olsun
        - Doğa, insan, aşk, ayrılık gibi temalardan esinlen
        - Sadece şiiri yaz, hiçbir açıklama ekleme
        
        ÖRNEK ŞİİR FORMATI:
        Rüzgar uğultusuyla
        Yapraklar dans ediyor
        Gökyüzü maviliğinde
        Kuşlar şarkı söylüyor
        
        ŞİİR:
        """
        
        response = model.generate_content(prompt)
        siir_metni = response.text.strip()
        
        # Eğer şiir çok uzunsa kısalt
        if len(siir_metni) > 500:
            siir_metni = siir_metni[:500] + "..."
            
        return siir_metni
        
    except Exception as e:
        return f"❌ Şiir üretilirken bir hata oluştu: {str(e)}"

# Gradio arayüzü
with gr.Blocks(
    theme=gr.themes.Soft(),
    title="Türkçe Şiir Üretici - Akbank GenAI Bootcamp"
) as demo:
    
    gr.Markdown("""
    # 🤖 Türkçe Şiir Üretici 
    ## Akbank GenAI Bootcamp
    **RAG tabanlı Türkçe şiir üretici. Bir tema yazın, AI şiir oluştursun!**
    """)
    
    with gr.Row():
        with gr.Column():
            tema_input = gr.Textbox(
                label="🎭 Şiir Teması",
                placeholder="Örnek: Ayrılık, doğa, aşk, deniz, gurbet...",
                lines=2,
                max_lines=3
            )
            generate_btn = gr.Button(
                "🎵 Şiir Üret", 
                variant="primary", 
                size="lg"
            )
        
        with gr.Column():
            output = gr.Textbox(
                label="🎵 Üretilen Şiir",
                lines=12,
                max_lines=20,
                show_copy_button=True
            )
    
    # Örnekler
    examples = gr.Examples(
        examples=[
            ["Ayrılık"],
            ["Doğa"],
            ["Aşk"], 
            ["Deniz kenarı"],
            ["Gurbet"],
            ["Anne sevgisi"],
            ["İstanbul"],
            ["Baharda uyanış"]
        ],
        inputs=tema_input,
        label="🎯 Hızlı Örnekler"
    )
    
    # Buton click event
    generate_btn.click(
        fn=siir_uretici,
        inputs=tema_input,
        outputs=output
    )
    
    # Footer
    gr.Markdown("---")
    gr.Markdown("""
    <div style='text-align: center'>
        <p>🚀 <strong>Powered by Google Gemini AI</strong></p>
        <p><em>Akbank GenAI Bootcamp Projesi</em></p>
    </div>
    """)

# UYGULAMAYI BAŞLAT - BU KISIM ÇOK ÖNEMLİ!
if __name__ == "__main__":
    print("✅ Sistem başlatılıyor...")
    print(f"🌐 Port: {PORT}")
    print("📱 Gradio arayüzü hazırlanıyor...")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=PORT,
        share=False,
        show_error=True,
        debug=True
    )
