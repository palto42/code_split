# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

ARG VERSION

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY dist /app

# Upgrdae pip but ignore "running as root" warning
RUN pip install --upgrade pip 2>/dev/null
# Install app with dependencies
RUN python -m pip install /app/code_split-${VERSION}.tar.gz

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 1000 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["code_split"]
