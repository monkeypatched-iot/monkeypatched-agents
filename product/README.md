# Product API
Product agent

# docker build 
sudo docker build -t monkeypatched/product-agent:latest . --no-cache

# docker run
sudo docker run  --network host -d -p 9001:9001 monkeypatched/product-agent:latest

# api docs
http://localhost:9002/docs