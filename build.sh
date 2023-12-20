#!/bin/bash
tag=$(awk 'NR==1 {print $1}' Changelog.md | sed 's/_//g')
echo "tagging the build with: $tag"
docker build . -t skanai.azurecr.io/prototypes/askskan:$tag
docker push  skanai.azurecr.io/prototypes/askskan:$tag
