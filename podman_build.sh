#!/bin/bash

show_help() {
    echo "Build container image for 'code_split'"
    echo "Usage:"
    echo "    -h          Display this help message"
    echo "    -v VERSION  Tag new container image with VERSION (default: derive from git tag)"
    echo "    -l          Add tag 'latest' to the image"
    echo "    -s          Save container image to file"
}

while getopts "v:lsh" opt; do
    case ${opt} in
    h)
        show_help
        exit 0
        ;;
    v)
        VERSION="$OPTARG"
        ;;
    l)
        LATEST=("-t" "code_split:latest")
        INFO=" and 'latest'"
        ;;
    s)
        SAVE=1
        ;;
    \?)
        echo "Invalid Option: -$OPTARG" 1>&2
        show_help
        exit 1
        ;;
    :)
        echo "Invalid Option: -$OPTARG requires an argument" 1>&2
        exit 1
        ;;
    esac
done
shift $((OPTIND - 1))

if [ ! "$VERSION" ]; then
    VERSION=$(python -m setuptools_scm)
fi
# Replace invalid tag char '+' with '-' (in case of git post-commit tags)
TAG=${VERSION//[+]/-}
echo "Build podman image for version $VERSION with tag '${TAG}'${INFO}"
podman build --build-arg VERSION="$VERSION" --rm --pull ${LATEST[*]} -t "code_split:${TAG}" .
# podman save "code_split:${TAG}" | gzip >"dist/code_split-docker-${TAG}.tar.gz"
if [ "$SAVE" ]; then
    echo "Saving new image to 'dist/code_split-docker-${TAG}.tar.gz'"
    podman save code_split | gzip >"dist/code_split-docker-${TAG}.tar.gz"
fi
