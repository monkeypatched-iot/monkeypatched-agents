# Customer API
Builder agent

# docker build 
sudo docker build -t monkeypatched/builder-agent:latest . --no-cache

# docker run
sudo docker run  --network host -d -p 9006:9006 monkeypatched/builder-agent:latest

# api docs
http://localhost:9006/docs
