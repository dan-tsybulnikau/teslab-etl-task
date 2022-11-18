<!-- Table of Contents -->
# Table of Contents

- [Table of Contents](#table-of-contents)
  - [About the Project](#about-the-project)
  - [Task description](#task-description)
  - [Solution description](#solution-description)
    - [Tech Stack](#tech-stack)
    - [Environment requirements](#environment-requirements)
    - [Build process](#build-process)
    - [App usage](#app-usage)
    - [REST API](#rest-api)
    - [Test case](#test-case)
  

<!-- About the Project -->
## About the Project
Test task on backend integration


## Task description
1. Develop API integration of currency info (https://www.cbr.ru/development/SXML/)
   1.1. Data is collected in one day offset
   1.2. Currencies - RUB, USD, EUR
2. Create database schema and tables for storing data in Postgres
3. Set up everyday routine on receiving actual data
4. Allow to perform one-time call to receive and store data on specified date
5. Perform types validation before writing to database skipping dupclicated records
6. Create API to receive data fro database on specified date
7. Use Authorization: Bearer 

<!-- TechStack -->
## Solution description
Programming language - Python
Project provides endpoints to collect currency data from CBR API to the Postgres database (either manually for today/desired date or periodically every day at 00:00)
and perform selections from given database for currency rates on desired date
About the Solution

To solve this task:
1. Created FastAPI service
2. Created two endpoints - /refresh and /currency_rate
3. Builded Docker image
4. Created development environment in Yandex Cloud
5. Created refresh scheduled function to perform everyday updates
6. Created API Gateway to perform orchestration between service endpoints

### Tech Stack

<details>
  <summary>Server</summary>
  <ul>
    <li><a href="https://fastapi.tiangolo.com/">FastAPI</a></li>
    <li><a href="https://pydantic-docs.helpmanual.io/">Pydantic</a></li>
    <li><a href="https://www.sqlalchemy.org/">SQLAlchemy</a></li>
    <li><a href="https://cloud.yandex.com/en/">Yandex Cloud</a></li>
    <li><a href="https://www.postgresql.org/">Postgres</a></li>
    <li><a href="https://www.docker.com/">Docker</a></li>
  </ul>
</details>


<!-- Features -->
### Environment requirements
In order to start app locally, next steps are required:
1. Create .env file
2. Populate it with actual data (template is in .env.local)
    - CBR_URL - path to parsed currency API
    - DB_URI - in form protocol://user:password@database_host:database_port/database_name (i.e., postgresql+psycopg2://postgres:postgres@localhost:5432/postgres)
    - CHECKED_CURRENCY - currency string codes in form of list of string codes (['RUB', 'EUR', 'USD'])
    - SECRET - secret key used for jwt decoding while validating Bearer token (i.e., secret)

3. If local instance of Postgres DB is started. add also
    - POSTGRES_USER - database user
    - POSTGRES_PASSWORD - database password
4. Installed Docker/Docker Compose are required
5. Yandex cloud account is required
6. Yandex CLI required

### Build process
Local run
```bash
docker-compose up
```

Cloud deploy
1. Navigate to https://console.cloud.yandex.ru and log in
2. Go to "All services" -> "Service accounts" -> "Create service account"
3. In pop up type service name (i.e. yandex-api), press "Add role" and select next roles: "container-registry.images.pusher", "functions.functionInvoker"
4. Copy service account "ID"
5. Go to "All services" -> "Managed Service for PostgreSQL" -> "Create cluster"
6. After cluster is alive, click on it, go to "Databases" -> "Add", enter database name and press "Add"
7. After created, press three dot sign -> "Connect" -> "Python"  and copy host, port, dbname, and format them into connection URL to POstgres DB (as in [Environment requirements](#environment-requirements) (option 2))
8. Login to Docker  (https://cloud.yandex.com/en/docs/container-registry/operations/authentication)
9. Go to "All services" -> "Container registry" -> "Create registry" and add name
10. After registry is created, copy its ID
11. Open local terminal and go to project directory
12. Login into Yandex registry
```bash
docker login --username oauth --password <YOUR_YANDEX_OATH_TOKEN> cr.yandex
```
13. Build FastAPI service
```bash
docker build -t yandex_api -f ./docker/Dockerfile .
```
14. Optionally, add tag 
```bash
docker tag yandex_api cr.yandex/<YOUR_REGISTRY_ID>/yandex_api:latest
```
15. Push image inside registry
```bash
docker push cr.yandex/<YOUR_REGISTRY_ID>/yandex_api
```
16. Go to "All services" -> "Serverless Containers" -> "Create container" and add name
17. After creating select recently pushed image in "Image URL"
18. Add environment variables from [Environment requirements](#environment-requirements) (option 2) to "Environment variables"
19. Select "Service account" that was created earlier and press "Create revision"
20. Copy container "Link to invoke" and "ID"
21. Go to "All services" -> "API gateway" -> "Create API gateway"
22. Add name and paste next lines to "Specification" with data copied before under "path" option
```bash

paths:
  /docs:
    get:
      x-yc-apigateway-integration:
        type: serverless_containers
        container_id: <CONTAINER_ID>
        service_account_id: <SERVICE_ACCOUNT_ID>
      operationId: docs
      responses:
        '200':
          content:
            application/json:
              schema: {}
          description: Successful Response
      summary: Docs
  /openapi.json:
    get:
      x-yc-apigateway-integration:
        type: serverless_containers
        container_id: <CONTAINER_ID>
        service_account_id: <SERVICE_ACCOUNT_ID>
      operationId: openapi
      responses:
        '200':
          content:
            application/json:
              schema: {}
          description: Successful Response
      summary: OpenAPI
  /refresh:
    get:
      x-yc-apigateway-integration:
        type: serverless_containers
        container_id: <CONTAINER_ID>
        service_account_id: <SERVICE_ACCOUNT_ID>
      operationId: refresh_refresh_get
      parameters:
      - explode: true
        in: query
        name: date
        required: false
        schema:
          title: Date
          type: string
        style: form
      responses:
        '200':
          content:
            application/json:
              schema: {}
          description: Successful Response
        '422':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
          description: Validation Error
      summary: Refresh
  /currency_rate:
    get:
      x-yc-apigateway-integration:
        type: serverless_containers
        container_id: <CONTAINER_ID>
        service_account_id: <SERVICE_ACCOUNT_ID>
      operationId: get_currency_records_currency_rate_get
      parameters:
      - explode: true
        in: query
        name: date
        required: true
        schema:
          pattern: '[\d]{2}/[\d]{2}/[\d]{4}'
          title: Date
          type: string
        style: form
      responses:
        '200':
          content:
            application/json:
              schema: {}
          description: Successful Response
        '422':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
          description: Validation Error
      summary: Get Currency Records
components:
  schemas:
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          title: Detail
          type: array
      title: HTTPValidationError
      type: object
    ValidationError:
      properties:
        msg:
          title: Message
          type: string
        loc:
          items:
            anyOf:
            - type: string
            - type: integer
          title: Location
          type: array
        type:
          title: Error Type
          type: string
      required:
      - loc
      - msg
      - type
      title: ValidationError
      type: object
  securitySchemes:
    bearerAuth:
      bearerFormat: JWT
      scheme: bearer
      type: http
```
23. Go to "All services" -> "Cloud Functions" -> "Create Function"
24. Add function name and press "Create"
25. Inside editor select "Python", press "Continue"
26. Press "Create file" (if "index.py") does not exist and paste code from local yandex_function.py, add "Environment variables":
        - SERVICE_URL - <API_GATEWAY_LINK_TO_INVOKE>
        - TOKEN - <TOKEN_FROM_ENV_FILE>
27. Press "Create revision" and go to "Triggers" -> "Create trigger"
28. Enter trigger name, paste "0 0 ? * * *" to Cron expression, select created function in "Function" field, select created service account name in "Service account" and press "Create trigger"
### App usage
1. Daily update of exchange rate
2. Update of exchange rate on particular date
3. Retrieve data of exchange rate of desired date

### REST API
To see docs and try requesting something go to
https://app.swaggerhub.com/apis/dan-tsybulnikau/yandex-api/1.0.1 


### Test case
Link - https://d5dq55s9sem32osrt5l9.apigw.yandexcloud.net/refresh
Test token - eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJwYXNzd29yZCI6Imhhc2hlZF9wYXNzd29yZCJ9.AIuCQISVEYooLDbYhqMH9Z4JvWvvHfz-N7JyWRgYFzI