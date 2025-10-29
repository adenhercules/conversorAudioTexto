# API de Transcrição de Áudio com FastAPI e Faster-Whisper

Este projeto implementa uma API REST simples utilizando **FastAPI** para receber um arquivo de áudio e retornar a sua transcrição textual. A transcrição é realizada localmente usando a biblioteca de código aberto **Faster-Whisper** da SYSTRAN, uma versão otimizada do popular modelo Whisper da OpenAI, conhecida por sua velocidade e eficiência.

---

## Tecnologias Utilizadas

* **FastAPI** 
* **Faster-Whisper** 
* **Uvicorn** 
* **Python-Multipart**

---

## Pré-requisitos

Para rodar o projeto localmente, você precisará ter instalado:

1.  **Python 3.8+**
2.  **`ffmpeg`**: Uma ferramenta de linha de comando essencial para o processamento de áudio pelo `faster-whisper`.
    * **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install ffmpeg`
    * **macOS (Homebrew):** `brew install ffmpeg`
    * **Windows:** Baixe o binário e adicione ao seu PATH.

---

## Instalação e Execução

### Instalar as Dependências

Instale todas as bibliotecas Python necessárias usando `pip`:

```bash
pip install fastapi uvicorn python-multipart faster-whisper requests
```

Executar a API
Inicie o servidor localmente com Uvicorn:

```Bash
uvicorn main:app --reload
```

A API estará acessível em http://127.0.0.1:8000.

⚠️ Primeira Execução: Na primeira vez que você executar a API, o faster-whisper fará o download do modelo de IA configurado (medium por padrão), o que pode levar alguns minutos dependendo da sua conexão.

A subida de arquivos deve ser feita via método `POST` utilizando o formato `multipart/form-data`.

| Método | Caminho           | Parâmetro de Arquivo |
| :----- | :---------------- | :------------------- |
| `POST` | `/transcrever/` | `audio_file`         |

## Exemplo de Retorno Esperado (JSON)
Se o áudio enviado contiver a frase "Olá, este é um teste de API com Faster-Whisper." em português, a API retornará o seguinte objeto JSON:
```bash
{
    "filename": "seu_audio.extensao",
    "content_type": "audio/mpeg",
    "transcription": "Olá, este é um teste de API com Faster-Whisper.",
    "language": "pt"
}
```
