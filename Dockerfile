# Use uma imagem base do Python
FROM python:3.10-slim

# Instalar dependências do sistema (pkg-config e MariaDB/MySQL client)
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos para o contêiner
COPY . .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Defina a variável de ambiente FLASK_APP
ENV FLASK_APP=run.py

# Exponha a porta
EXPOSE 5000

# Comando para iniciar o Flask
CMD ["flask", "run", "--host=0.0.0.0"]