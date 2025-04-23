# Recipe API App

This is a **Recipe API** application built with **Python** and **Django**, designed to manage recipes and their related data. It uses **Docker** for containerization and is tested for reliability.

## Features

- **User Authentication**: Secure sign-up, login, and token-based authentication.
- **Recipe Management**: Create, read, update, and delete recipes.
- **Ingredient Management**: Manage ingredients for recipes.
- **Search and Filters**: Search recipes by name and filter by ingredients or tags.
- **API Documentation**: Easily interact with the API using built-in documentation.

## Tech Stack

- **Backend**: Python, Django, Django REST Framework
- **Database**: PostgreSQL
- **Containerization**: Docker and Docker Compose
- **Testing**: Python's `unittest` framework

## Prerequisites

- Docker and Docker Compose installed on your system.
- Python 3.9+ (if running locally without Docker).

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Tekalig/recipe_api_app.git
   cd recipe_api_app
   ```

2. Build and start the application using Docker:
   ```bash
   docker-compose up --build
   ```

3. Run migrations to set up the database:
   ```bash
   docker-compose run --rm app sh -c "python manage.py migrate"
   ```

4. Access the application locally:
   - API: [http://localhost:8000](http://localhost:8000)

## Running Tests

To run tests, use the following command:
```bash
docker-compose run --rm app sh -c "python manage.py test"
```

## Deployment

- Ensure all environment variables (e.g., `DATABASE_URL`, `SECRET_KEY`) are set properly.
- Build and deploy the Docker containers to your production environment.

## Contributing

1. Fork the repository and create your branch:
   ```bash
   git checkout -b my-feature
   ```

2. Commit your changes:
   ```bash
   git commit -m "Add my feature"
   ```

3. Push to the branch:
   ```bash
   git push origin my-feature
   ```

4. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
