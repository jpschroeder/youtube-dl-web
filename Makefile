
all:
	sudo docker build -t youtube_img .
	sudo docker run -d --name youtube_cont -p 80:5000 youtube_img

clean:
	sudo docker kill youtube_cont
	sudo docker rm youtube_cont
	sudo docker rmi youtube_img
