# cz-year-calendar

construction of docker container:<br>
wget https://raw.githubusercontent.com/mcjobo/cz-year-calendar/master/docker/dockerfile<br>
create image:<br>
sudo docker build -t cz-year-calendar .<br>
run container:<br>
#sudo docker run --name cz-year-calendar-instance -p 6080:6080 -i -t cz-year-calendar
sudo docker run --name cz-year-calendar-instance -p 6080:6080 -i -t cz-year-calendar
sudo docker run --name cz-year-calendar-instance -d -t cz-year-calendar

command to collapse all files into one
vulcanize --inline-scripts --inline-css --strip-comments index2.html > ../build/index2.build.html