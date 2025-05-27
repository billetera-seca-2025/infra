# infra

## Folder Structure
```
├── infra/
│   └── ...
├── billetera-seca/
│   └── ...
├── api-fake/
│   └── ...
└── billetera-seca-web-app/
    └── ...
```

## Running the Environment with Docker Compose

### Production Environment
To run the production environment using Docker Compose, use the following command:

```bash
docker-compose --profile prod up --build --force-recreate
```

This command executes all the services required for production. **Important**: After running this command, ensure that all services have started and are fully ready before interacting with the application. Docker will handle service dependencies, but some services, like the database, may take a few moments to become healthy. You can monitor the logs to confirm their readiness.

---

### Test Environment
To run the test environment, use the following command:

```bash
docker-compose -f docker-compose.yml -f docker-compose.test.yml --profile test up --build --force-recreate
```

This command starts the test environment with the necessary services and configurations. It integrates with the additional `docker-compose.test.yml` file, where test-specific settings are defined. For example:

- The database (`db`) always starts empty, ensuring a clean slate for testing.
- The `DDL_AUTO` property for the API is set to `create-drop`, ensuring that tables are created at the start and dropped when the services stop.

All application endpoints and services will be functional in the test environment, mirroring the production setup but tailored for testing purposes.
