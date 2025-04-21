## Requirements

1. **Install Docker** by following their [installation instructions for your OS](https://docs.docker.com/get-docker/). Bedrock uses Docker to start the local development database.

## Development
In your local environment, set up a python virtual env
in that environment, run

0. pip install --upgrade pip
1. pip install pip-tools
2. Add new dependencies on requirements.in
3. Compile new dependencies into requirements.txt using pip-compile

https://suyojtamrakar.medium.com/managing-your-requirements-txt-with-pip-tools-in-python-8d07d9dfa464

## Install

1. Run: `docker-compose up`
2. **Open Docker**
3. Then, **run migrations** with `alembic` in new terminal window:

```sh
docker exec -it vorian-services-api alembic upgrade head
```

That's it! You should be able to visit http://localhost:5009/health 🎉
