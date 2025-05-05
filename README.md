# Knowledge Base
This project is a knowledge base system for ai assistant for human-ai interactive diary application.  
  
## project structure
- core
    - components
    - domain
        - entity
            knowledge.py
        - usecase
            add_producer.py
            add_consumer.py
            search.py
- infra
    litellm
- present
    - search
    - add

## Design of actions
__Add: Save diary__  
Add action is triggered when user saves diary or enter chat messages to ai assistant.  
1. Data processing from backend app
2. Presentation layer of knowledge base app
3. Trigger add producer usecase
4. Producer puts the data into queue (kafka)
5. Consumer gets the data from the queue
    a. Extract knowledge leveraging LLM
    b. Search similar knowledge by vector search <-> pgvector store
    c. Distinguish add, update, and delete actions on knowledges
    d. Do the actions

```mermaid
flowchart TD
    frontend[Frontend App]
    backend[Backend App] <-->|Save and find|database[(Postgresql-pgvector)]


    frontend -->|User saves diary/chat| backend

    backend -->|Send to KB| C[Knowledge Base App
    Presentation Layer]
    subgraph knowledge-base-producer
        C -->|Trigger| D[Add Producer]
    end


    D -->|Put data| E[(Queue - Kafka)]
    E -->|Consume data| F[Add Consumer]

    subgraph knowledge-base-consumer
        F -->|Extract knowledge - leveraging LLM| G[New knowledge]
        G -->|Search similar knowledge| database
        database -->H[All related knowledges]
        H -->|Distinguish actions: Add, Update, Delete, No-action leveraging LLM|I[Knowledge with actions]
        I -->|Save to| database
    end
```
  

__Search: Chat request__  
Search action is triggered when user enter chat messages to ai assistant
1. Data processing from backend app
2. Presentation layer of knowledge base app
3. Vector search on pgvector and retrieve top k knowledge
  
```mermaid
flowchart TD
    frontend[Frontend App]
    backend[Backend App]
    database[(Postgresql-pgvector)]


    frontend -->|User enters chat| backend

    backend -->|Search on KB| C[Knowledge Base App]

    C <-->|Vector search| database
    
    C -->|Search result|backend
```