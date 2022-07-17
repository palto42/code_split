# For more information, please refer to https://aka.ms/vscode-docker-python
FROM docker.io/python:3.10-slim

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

# No need to create a non-root user inside the container because podmand runs rootless.

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
ENTRYPOINT ["code_split"]
# CMD ["--help"]
