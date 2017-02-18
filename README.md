# cz-year-calendar

construction of docker container:<br>
wget https://raw.githubusercontent.com/mcjobo/cz-year-calendar/master/docker/dockerfile<br>
create image:<br>
sudo docker build -t cz-year-calendar .<br>
run container:<br>
sudo docker run --name cz-year-calendar-instance -p 8080:8080 -i -t cz-year-calendar