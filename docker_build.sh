#!/bin/bash

VERSION=$(python -m setuptools_scm)
TAG=${VERSION//[+]/-}
echo "Build docker image for version $VERSION with tag $TAG"
docker build --build-arg VERSION="$VERSION" --rm --pull -f Dockerfile -t "code_split:latest" -t "code_split:${TAG}" .
echo "Save image to ./dist/code_split-docker-${TAG}.tar"
docker save "code_split:${TAG}" | gzip >"dist/code_split-docker-${TAG}.tar.gz"
