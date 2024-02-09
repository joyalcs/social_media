FROM node:18-alpine as BUILD_IMAGE

WORKDIR /frontend

COPY package.json  ./
COPY package-lock.json ./

RUN npm install

COPY . .
