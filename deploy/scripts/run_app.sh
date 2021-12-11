docker run -ti --rm -v $(pwd)/src:/app -v /tmp:/tmp \
  -e MAX_WORKERS=1 \
  -p 80:80  knn-api:latest
