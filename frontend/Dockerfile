FROM node:lts-alpine3.21  AS base

WORKDIR /app/

COPY \
  ./components.json \
  ./eslint.config.js \
  ./jsconfig.json \
  ./package*.json \
  ./postcss.config.js \
  ./tailwind.config.js \
  ./vite.config.js \
  ./


FROM base AS dev

RUN npm install

COPY . .

CMD ["npm", "run", "dev"]


FROM base AS prod

# RUN npm ci --omit=dev
RUN npm ci

COPY . .

CMD ["npm", "run", "build"]
