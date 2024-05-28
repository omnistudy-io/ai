sudo chown -R $(whoami) ~/.docker

# Build
docker build -t omnistudy/ai:prod -f ./docker/Dockerfile.prod .
# Run
docker run -dp 80:80 --name ai omnistudy/ai:prod