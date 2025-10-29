# /Dockerfile

# 1. Use uma imagem base do Python
FROM python:3.11-slim

# 2. Instale o FFMPEG (dependência do Whisper)
# Esta é a principal razão de usarmos o Docker
RUN apt-get update && apt-get install -y ffmpeg

# 3. Configure o diretório de trabalho
WORKDIR /app

# 4. Copie o arquivo de requisitos e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copie todo o seu código (main.py, transcriber_service.py, etc.)
COPY . .

# 6. Exponha a porta que a aplicação vai rodar
# O Render Free usa a porta 10000. Vamos usá-la.
EXPOSE 10000

# 7. Comando para iniciar a aplicação
# Usamos Gunicorn para produção (ele gerencia o Uvicorn)
# --timeout 120: Aumenta o tempo limite para 120s (o padrão de 30s é muito baixo para o whisper)
# --bind 0.0.0.0:10000: Escuta na porta 10000
CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:10000", "--timeout", "120"]