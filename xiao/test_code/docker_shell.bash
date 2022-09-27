docker build -f ./logistics/Dockerfile -t bee/logistics:latest .

docker run -itd --env=_ZK_HOSTS=zookeeper --env=_APP_NAME=bee --env=_APP_ENV=dev --env=_DEBUG=1 --network=bee-dev --name=bee_logistics --hostname=logistics bee/logistics
