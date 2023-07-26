# BudgetCars
Welcome to the repository for used car recommender engine bootstrapped [cookiecutter fullstack template](https://github.com/tiangolo/full-stack-fastapi-postgresql) using Vue.js on the frontend and python fastapi on backend with postgres as a database.

## Requirements
* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.
  - poetry can be installed by following commands (more info [here](https://github.com/python-poetry/install.python-poetry.org)):
    - windows (powershell)
    ```
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
    ```
    - osx/linux
    ```
    curl -sSL https://install.python-poetry.org | python3 -
    ```

## Startup
The app can be run locally by following these steps:
- clone the repository to you local machine
- make sure that you have [Docker](https://www.docker.com/) installed and it's up and running on you machine
- navigate to the root directory of the repository
- run the following command (there's bunch of dependecies to be downloaded so feel free to go for a coffee or any other beverage of you choice, it will take a while)
```bash
docker-compose up -d
```
- after that you will have couple of http://localhost urls:
  - http://localhost/docs → OpenAPI documentation for all the available endpoints
  - http://localhost/dashboard → dashboard with/for users
  
## Frontend
- there's basic frontend that can be used as an administration portal (http://localhost/dashboard)
- the frontend project is created in Vue.js and ideally would be expanded to implement all the frontend details
- I have prepared [this basic figma design](https://www.figma.com/file/3sVnZe22gEffAhPuIQ6OZe/BudgetCars?type=design&node-id=0%3A1&mode=design&t=eZecsRbZSBfPBksa-1) for a showcase how the interactive website could look like
- suggested features:
  - users can login and like cars which will be base for the recommendation
  - actions like view and like will be recorded so the engine provides the most personalised recommendations
  - chat with sales rep/customer support to help with choosing car (can be chatbot)
  - advanced filtering options (color, number of seats, fuel type,…)
  - car comparison
  - sharing of the cars on social media/email
  - interactive visualizations and charts to display statistical insights about the available cars, such as the distribution of prices, mileage, or popularity of different makes and models.
  - **Instant Notifications:** Set up real-time notifications for users, such as price drop alerts or newly added listings that match their saved searches.
  - **Accessibility Features:** Implement accessibility features to ensure that users with disabilities can access and use the recommender engine effectively.
  - **Multilingual Support:** Provide support for multiple languages to cater to users from diverse regions.
  - **User Reviews and Ratings:** Include user reviews and ratings for listed cars, providing valuable feedback and transparency to potential buyers.

## Backend
- backend is using fastapi for exposing rest api endpoints
- full list of endpoints can be seen here http://localhost/docs
- the database for storing all the information is postgres
- on top of that there are 3 components that are prepared for the future use:
  - celery → prepared for async task processing such as data processing, model training etc.
  - rabbit → message broker for receiving and passing tasks to celery
  - flower → prepared for monitoring the celery and the status of tasks
- everything is wrapped in docker containers
- pytest is used as a testing framework and tool for understanding the test coverage (it's not 100% for the sake of time)
- login and user/s endpoints have a certain level of authorization/authentication but for the remaining endpoints I kept it without it for the sake of POC

## Data Engineering
- for the data engineering part there's a showcase of how the module for data pipeline could look like [this](backend/app/data_processing/car_data_pipeline.py)
- additionally, the data could be uploaded to the postgres (to already existing table or create new table specific for data pipeline)
- basic exploratory data analysis is [here](backend/app/data_processing/car_data_utils.py)
- very basic content filtering used to show similar cars is [here](backend/app/app/core/filtering_utils.py)
- part of the docker setup are jupyter notebooks (check [AdditionalProjectInfo](AdditionalProjectInfo.md) for more info)

## DevOps/Infrastructure
- the whole fullstack app is wrapped in dockers
- part of the docker compose is running the tests
- The whole stack can be deployed e.g. using docker swarm as described in the [AdditionalProjectInfo](AdditionalProjectInfo.md)
- network is handled by Traefik
- there is a setup for dev, stage and prod env as well as local development

### Ideas for some monitoring and observability:
- logging → add some basic logging to both
  - backend:
      - HTTP Requests and Responses
      - Errors and Exceptions
      - Database Queries
      - Authentication and Authorization Events
      - Business Events (preferences, searches, recommendations)
      - Performance Metrics (CPU and memory usage)
  - frontend:
      - User Interactions
      - Network Requests
      - Errors and Exceptions
      - Performance Metrics
      - Browser and Device Information
      - User Authentication and Session Events
- centralised logging → e.g. Elasticsearch or Kibana
- error tracking → sentry or rollbar for real-time error reports
- alerting → rules for critical metrics and events … send messages to slack if certain threshold breached
- dashboards → grafana




NOTE: Other additional info about the project and the setup can be found in [AdditionalProjectInfo](AdditionalProjectInfo.md)