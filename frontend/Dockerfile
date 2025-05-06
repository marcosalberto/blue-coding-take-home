FROM node:20-alpine as builder

WORKDIR /app

COPY package.json .

ARG VITE_API_ADDRESS
ENV VITE_API_ADDRESS=$VITE_API_ADDRESS

RUN yarn

COPY . .

RUN yarn build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]