sudo chown -R $(whoami) ~/.docker

# Build
docker build -t omnistudy/ai:dev -f ./docker/Dockerfile.dev .
# Run
docker run -dp 5001:5001 --name ai omnistudy/ai:dev