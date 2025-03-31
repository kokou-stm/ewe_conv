# Utilise une image Python légère
FROM python:3.9-slim

# Définit le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Copie le fichier de dépendances dans le conteneur
COPY requirements.txt ./

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie le contenu de l'application dans le conteneur
COPY . .

# Expose le port utilisé par l'application
EXPOSE 80

# Commande pour démarrer le serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
