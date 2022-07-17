#!/bin/bash

VERSION=$(python -m setuptools_scm)
TAG=${VERSION//[+]/-}
echo "Build podman image for version $VERSION with tag $TAG"
podman build --build-arg VERSION="$VERSION" --rm --pull -t "code_split:latest" -t "code_split:${TAG}" .
# podman save "code_split:${TAG}" | gzip >"dist/code_split-docker-${TAG}.tar.gz"
podman save code_split | gzip >"dist/code_split-docker-${TAG}.tar.gz"
