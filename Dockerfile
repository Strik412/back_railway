# Imagen base
FROM node:18-alpine

# Crear directorio
WORKDIR /app

# Copiar archivos y dependencias
COPY package*.json ./
RUN npm install

COPY . .

# Exponer puerto
EXPOSE 3000

# Comando de inicio
CMD ["npm", "start"]
