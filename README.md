# Clarke Energia - SPA de Fornecedores de Energia

Um desafio técnico que implementa uma SPA (Single Page Application) para escolha de fornecedores de energia renovável, com suporte a GD (Geração Distribuída) e Mercado Livre.

## Tecnologias

- Frontend em React com TypeScript
- Backend em Python com FastAPI
- GraphQL para comunicação entre frontend e backend
- Banco de dados PostgreSQL
- Docker e Docker Compose para containerização
- Biblioteca de Estilo Tailwind CSS

### Inicialização do projeto

```bash
# Inicie os containers
docker-compose up -d

# Acesse a aplicação
# Frontend: http://localhost:5173
# GraphQL: http://localhost:8000/graphql
# Health Check: http://localhost:8000/health
```

## Testes

### Backend
```bash
cd back-end
pytest
```

### Frontend
```bash
cd front-end
npm run test
```


## Dados de Teste

A aplicação vem com dados fictícios pré-carregados no banco de dados:
- 10 estados brasileiros com tarifas base realistas
- 6 fornecedores fictícios com diferentes soluções
- Múltiplas combinações de fornecedores por estado e solução

## Live URL

[Go Live](https://clarke-spa.onrender.com)