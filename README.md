# Knowledge Base
This project is a graph-db based knowledge-base system.
This code extract and update knowledge leveraging llm with producer-consumer architecture.

## project structure
- app
  - add_consumer - entry point of `add_consumer` app
  - api - entry point of `api` app
- core
  - component: implemtation of port
  - entity
  - port: interface connecting outside and inside of core logic
  - prompt
  - service: combining ports, implements detail logic
  - usecase: business logic
- infra

## Design of actions
```mermaid
flowchart TD
  kafka[(Kafka Queue)]
  neo4j[(Graph DB)]

  subgraph api-application
    add_api[POST /v1/knowledge]
    search_api[GET /v1/knowledge]

    subgraph search-usecase
      ss1[extract vertices]
      ss2[search existing edges]

      ss1 --> ss2
    end

    search_api -->|execute| search-usecase
  end

  add_api --> |produce|kafka
  search-usecase --> |actions in each step|neo4j

  subgraph add-consumer
    consumer[consumer]

    subgraph add-usecase
      as1[extract vertices]
      as2[extract edges]
      as3[search existing edges]
      as4[check and delete existing edges]
      as5[check and add new edges]

      as1 --> as2
      as2 --> as3
      as3 --> as4
      as4 --> as5
    end

    consumer --> |execute|add-usecase
  end

  consumer --> |consume|kafka
  add-usecase --> |actions in each step|neo4j
```
