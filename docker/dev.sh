# sudo chown -R $(whoami) ~/.docker

# Build
docker build --no-cache -t omnistudy/ai:dev -f ./docker/Dockerfile.dev .
# Run
docker run -dp 5001:5001 --name ai --network omninet -v `pwd`:/app omnistudy/ai:dev