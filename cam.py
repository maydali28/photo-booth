import sys
import pygame
import pygame.camera
import os
import time
import io
from datetime import datetime
from twython import Twython
from itertools import cycle


#@MicroDesignClub
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)


#os.putenv('SDL_VIDEODRIVER','fbcon')
#os.putenv('SDLFBDEV','/dev/fb1')
#home path
home_dir=""
#ouput imgs folder path
picture_dir = home_dir+""
#overlay folder path
overlay_dir = home_dir+""
overlays = ['girl', 'cowboy', 'top', 'pink', 'glassesnose', 'moustache', 'sunglasses', 'elvis', 'emo', 'flowers', 'mop', 'glasses']
all_overlays = cycle(overlays)

if not os.path.exists(picture_dir) :
	os.makedirs(picture_dir)
if not os.path.exists(overlay_dir):
	os.makedirs(overlay_dir)

overlay = overlays[0]


def get_overlay(overlay):
	return pygame.image.load(overlay_dir+"/"+overlay+".png")

def next_overlay():
	global overlay
    	overlay = next(all_overlays)

def currentTime():
	now = datetime.now()
	return now.strftime("%Y-%m-%d %H:%M")

def tweet(pic):
	twitter = Twython(consumer_key,consumer_secret,access_token,access_token_secret)
	message = "\#microdesignclub \#photobooth \#taking a picture"
	#for picture
	photo = open(pic,'rb')
	response = twitter.upload_media(media=photo)
	twitter.update_status(status=message,media_ids=[response['media_id']])
	#for a simple tweet
	#twitter.update_status(status=message)
	print("Tweeted: %s" % message)

def main():
	pygame.init()
	pygame.camera.init()
	screen = pygame.display.set_mode((640,480),0)
	cam_list = pygame.camera.list_cameras()
	cam = pygame.camera.Camera(cam_list[0],(640,480))
	screen1 = pygame.surface.Surface((640,480),0,screen)
	cam.start()
	pic= get_overlay(overlay)
	while True:

		screen1 = cam.get_image(screen1)
		screen.blit(screen1,(0,0))
		pos = pic.get_rect()
		pos.centerx = screen.get_rect().centerx
		pos.centery = screen.get_rect().centery
		screen.blit(pic,pos)
		pygame.display.update()

		for event in pygame.event.get():
          		if event.type == pygame.QUIT:
          			cam.stop()
          			pygame.quit()
          			sys.exit()
	  		if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					path = picture_dir +"/" +currentTime()+".jpg"
					print "key pressed"
					pygame.image.save(screen,path)
#					tweet(path)
				if event.key == pygame.K_d:
					next_overlay()
					pic = get_overlay(overlay)
if __name__ == '__main__':
	main()
