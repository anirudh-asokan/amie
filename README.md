# How to Run Amie To-Do App

This guide will walk you through the steps required to get the app up and running on your local machine using Docker.

## Prerequisites
Before you continue, ensure you have the following installed on your system:
- [Git](https://git-scm.com/downloads)
- [Docker](https://docs.docker.com/get-docker/)

## Steps

1. ### Clone the Repository
   Open your terminal and run the following command to clone the repository:
   
   ```sh
   git clone https://github.com/anirudh-asokan/amie.git
   ```
   
   Navigate to the cloned repository by running:
   
   ```sh
   cd amie
   ```

2. ### Build Docker
   Build the Docker containers using Docker Compose. Run the following command:
   
   ```sh
   docker-compose build
   ```

3. ### Run Docker Containers
   Start the Docker containers using Docker Compose. Run the following command:
   
   ```sh
   docker-compose up
   ```
   
   This command starts the Docker containers in the foreground. To start them in the background, use the `-d` flag like this:
   
   ```sh
   docker-compose up -d
   ```

4. ### Access the Application
   Open your web browser and go to the following URL to access the frontend of the Amie To-Do App:
   
   ```
   http://localhost:8080/index.html
   ```

You should now have the Amie To-Do App running on your local machine.