FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# Serveur web léger pour build Vite
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "5173"]