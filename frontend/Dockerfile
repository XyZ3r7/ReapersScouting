FROM node:18 AS build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend .
RUN npm run build

FROM alpine:3.18
WORKDIR /app
COPY --from=build /app/dist ./dist
