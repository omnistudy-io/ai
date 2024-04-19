sudo chown -R $(whoami) ~/.docker

# Build
docker build -t omnistudy/ai:staging -f ./docker/Dockerfile.staging .
# Run
docker run -dp 80:80 --name ai omnistudy/ai:staging