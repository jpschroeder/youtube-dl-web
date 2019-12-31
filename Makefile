
all:
	sudo docker build -t youtube_img .
	sudo docker run -d --name youtube_cont -p 127.0.0.1:8081:5000 --restart unless-stopped youtube_img

clean:
	sudo docker kill youtube_cont
	sudo docker rm youtube_cont
	sudo docker rmi youtube_img
