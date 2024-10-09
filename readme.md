# Random Users List

This project consists of a full-stack application with a PostgreSQL database, a Python backend, and a frontend (likely React or Vue.js).

## Prerequisites

Before you begin, ensure you have the following installed:
- Docker
- Docker Compose

## Getting Started

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <project-directory>
   ```

2. Create a `.env` file in the root directory with the following variables:
   ```
   DB_NAME=<your-db-name>
   DB_USER=<your-db-user>
   DB_PASSWORD=<your-db-password>
   DB_PORT=5432
   OPENAI_API_KEY=<your-openai-api-key>
   ```

3. Build and start the containers:
   ```
   docker-compose up --build
   ```

4. The application should now be running:
   - Backend: http://localhost:8000
   - Frontend: http://localhost:3000
   - Database: PostgreSQL running on the default port (5432)

## Project Structure

- `backend/`: Contains the Python backend code
- `frontend/`: Contains the frontend code
- `docker-compose.yml`: Defines the multi-container Docker application

## Services

### Database (PostgreSQL)
- Image: postgres:13
- Environment variables: POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD

### Backend
- Built from `./backend` directory
- Runs Django migrations and starts the development server
- Environment variables: DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, OPENAI_API_KEY

### Frontend
- Built from `./frontend` directory
- Environment variables: VITE_API_URL

## Networks

All services are connected to the `app_network` bridge network.

## Volumes

- `postgres_data`: Persistent volume for PostgreSQL data

## Development

To make changes to the project:
1. Backend: Modify files in the `./backend` directory
2. Frontend: Modify files in the `./frontend` directory
3. Database: Connect to the PostgreSQL instance using the credentials in the `.env` file

Remember to rebuild the containers if you make changes to the Dockerfiles or add new dependencies:
```
docker-compose up --build
```

## Troubleshooting

If you encounter any issues, try the following:
1. Ensure all required environment variables are set in the `.env` file
2. Check the Docker logs for each service:
   ```
   docker-compose logs <service-name>
   ```
3. Verify that all services are running:
   ```
   docker-compose ps
   ```

For more detailed information, refer to the documentation in the backend and frontend directories.