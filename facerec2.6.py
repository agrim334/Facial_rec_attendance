import face_recognition
import cv2
import argparse
import os
import sys
from PIL import Image,ImageDraw
import numpy as np
import re

def print_vid(act_frames,img_in_frames,output,frame_count,upsample = 0):
	try:
		batch_of_face_locations = face_recognition.batch_face_locations(img_in_frames,batch_size=2,number_of_times_to_upsample=upsample)

		for frame_number_in_batch, face_locations in enumerate(batch_of_face_locations):
			number_of_faces_in_frame = len(face_locations)
			frame_number = frame_count - 2 + frame_number_in_batch
			print("Found {} face(s) in frame #{}.".format(number_of_faces_in_frame, frame_number))
			pil_image = Image.fromarray(act_frames[frame_number_in_batch])
			name = "detected"

			for face_location in face_locations:
				top, right, bottom, left = face_location

				cv2.rectangle(act_frames[frame_number_in_batch], (left, top), (right, bottom), (0, 0, 255), 2)
				cv2.rectangle(act_frames[frame_number_in_batch], (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
				font = cv2.FONT_HERSHEY_DUPLEX
				cv2.putText(act_frames[frame_number_in_batch], name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

			print("Writing frame {}".format(frame_number))
			output.write(act_frames[frame_number_in_batch])
	except RuntimeError:
		print("Out of Memory. Switching to single image detection method")
		for frame_number_in_batch,img in enumerate(img_in_frames):

			frame_number = frame_count - 2 + frame_number_in_batch

			try:
				face_locations = face_recognition.face_locations(img,model = "cnn",number_of_times_to_upsample=upsample)
			except RuntimeError:
				print("Out of Memory.Switching to HOG model.")
				face_locations = face_recognition.face_locations(img,model = "hog",number_of_times_to_upsample=upsample)

			print("Found {} face(s) in frame #{}.".format(len(face_locations),frame_number))

			pil_image = Image.fromarray(img)
			name = "detected"
			for (top, right, bottom, left) in face_locations:
				cv2.rectangle(act_frames[frame_number_in_batch], (left, top), (right, bottom), (0, 0, 255), 2)

				cv2.rectangle(act_frames[frame_number_in_batch], (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
				font = cv2.FONT_HERSHEY_DUPLEX
				cv2.putText(act_frames[frame_number_in_batch], name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
	
			print("Writing frame #{}".format(frame_number))
			output.write(act_frames[frame_number_in_batch])

def print_image(in_image,in_model="hog",upsample = 0):
	image = face_recognition.load_image_file(in_image)
	try:
		face_locations = face_recognition.face_locations(image,model = in_model,number_of_times_to_upsample=upsample)
	except RuntimeError:
		print("Out of Memory.Switching to HOG model.")
		face_locations = face_recognition.face_locations(image,model = "hog",number_of_times_to_upsample=upsample)

	print("Found {} face(s) in this photograph.".format(len(face_locations)))
				
	pil_image = Image.fromarray(image)
	draw = ImageDraw.Draw(pil_image)

	for (top, right, bottom, left) in face_locations:

		draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

		text_width, text_height = draw.textsize("found")

		draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))

		draw.text((left + 6, bottom - text_height - 5), "found", fill=(255, 255, 255, 255))
		face_image = image[top:bottom, left:right]

	pil_image.show()

def print_matches_vid(act_frames,img_in_frames,output,frame_count,known_face_encodings,known_face_name,in_tolerance=float(0.6),upsample = 0):
	x = in_tolerance
	batch_of_face_locations = face_recognition.batch_face_locations(img_in_frames,batch_size=2,number_of_times_to_upsample=upsample)

	for frame_number_in_batch, face_locations in enumerate(batch_of_face_locations):

		number_of_faces_in_frame = len(face_locations)
		frame_number = frame_count - 2 + frame_number_in_batch
		print("Found {} face(s) in frame #{}.".format(number_of_faces_in_frame, frame_number))
		pil_image = Image.fromarray(act_frames[frame_number_in_batch])

		face_encodings = face_recognition.face_encodings(img_in_frames[frame_number_in_batch],known_face_locations=face_locations)
		face_names = []
		
		for face_encoding in face_encodings:

			matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=x)

			name = "Unknown"

			face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
			best_match_index = np.argmin(face_distances)

			if matches[best_match_index]:
				im = known_face_encodings[best_match_index]
				name = known_face_name[str(im)]
			face_names.append(name)

		for (top, right, bottom, left), name in zip(face_locations, face_names):
			cv2.rectangle(act_frames[frame_number_in_batch], (left, top), (right, bottom), (0, 0, 255), 2)
			cv2.rectangle(act_frames[frame_number_in_batch], (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
			font = cv2.FONT_HERSHEY_DUPLEX
			cv2.putText(act_frames[frame_number_in_batch], name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
		
		print("Writing frame {}".format(frame_number))
		output.write(act_frames[frame_number_in_batch])

def print_matches(in_image,known_face_encodings,known_face_name,in_model="hog",in_tolerance=float(0.6),upsample = 0):
	x = in_tolerance

	image = face_recognition.load_image_file(in_image)
	try:
		face_locations = face_recognition.face_locations(image,model = in_model,number_of_times_to_upsample=upsample)
	except RuntimeError:
		print("Out of Memory.Switching to HOG model.")
		face_locations = face_recognition.face_locations(image,model = "hog",number_of_times_to_upsample=upsample)
	print("Found {} face(s) in this photograph.".format(len(face_locations)))
				
	face_encodings = face_recognition.face_encodings(image,known_face_locations=face_locations)
	pil_image = Image.fromarray(image)
	draw = ImageDraw.Draw(pil_image)
	
	for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
		matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=x)

		name = "Unknown"

		face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
		best_match_index = np.argmin(face_distances)

		if matches[best_match_index]:
			im = known_face_encodings[best_match_index]
			name = known_face_name[str(im)]

		draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

		text_width, text_height = draw.textsize(name)
		draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))

		draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

	pil_image.show()

def get_encd_name_dict(known_img,in_model="hog",upsample = 0):
	images = os.listdir(known_img)
	known_face_encd = []
	known_face_name = {}
	for image in images:
		try:
			temp = face_recognition.load_image_file(known_img+image)
			try:
				inp_face_locations = face_recognition.face_locations(temp, model = in_model,number_of_times_to_upsample=upsample)
			except RuntimeError:
				print("Out of Memory.Switching to HOG model.")
				inp_face_locations = face_recognition.face_locations(temp, model = "hog",number_of_times_to_upsample=upsample)

			encd= face_recognition.face_encodings(temp, known_face_locations = inp_face_locations)[0]
			known_face_encd.append(encd)
			known_face_name[str(encd)] = image
		except:
			print("Invalid file type or path does not exist for" + image)
	return known_face_encd,known_face_name;

def main():
	face_rec_parser = argparse.ArgumentParser(description='perform facial recognition/detection in image or videos')
	face_rec_parser.add_argument('method',type=str,help='detect for face detection.recognize for face recognition')
	face_rec_parser.add_argument('input_type',type=str,help='image or video input')
	face_rec_parser.add_argument('input_folder',metavar='path',type=str,help='path for input file')
	face_rec_parser.add_argument('--known_img',action="store",metavar='path',type=str,help='folder containing faces to be recognized')
	face_rec_parser.add_argument('--model',action="store",type=str,help='enter cnn or hog. hog is faster but less accurate. cnn is more accurate and can be fast if an Nvidia GPU is available and dlib is compiled with CUDA.By default hog is used')
	face_rec_parser.add_argument('--tolerance',action="store",type=float,help='set strictness of detection. lower value means more strictness in comparison. value should be between 0 and 1. By default value is 0.6')
	face_rec_parser.add_argument('--upsample',action="store",type=int,help='default value 1. higher (integer) values make for better detection of smaller faces.Large values may cause slowdown or memory overflow')

	args = face_rec_parser.parse_args()
	if not args.method:
		print("Usage [detect | recognize] [image | video] [path of input video/image to check] [path of known images(for recognition only]") 

	elif args.method == "detect":
		if args.input_type == "image":
			if not args.input_folder:
				print("missing file")
			else:
				if args.model is not None and args.upsample is not None:
					print_image(args.input_folder,args.model,args.upsample)
				elif args.model is not None and args.upsample is None:
					print_image(args.input_folder,args.model)
				elif args.model is None and args.upsample is not None:
					print_image(args.input_folder,upsample=args.upsample)
				else:
					print_image(args.input_folder)

		elif args.input_type == "video":
			if not args.input_folder:
				print("missing file")
			else:
				input_movie = cv2.VideoCapture(args.input_folder)
				length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
				fps = input_movie.get(cv2.CAP_PROP_FPS)
				fourcc = cv2.VideoWriter_fourcc(*'MP4V')
				w = input_movie.get(cv2.CAP_PROP_FRAME_WIDTH)
				h = input_movie.get(cv2.CAP_PROP_FRAME_HEIGHT)
				output_movie = cv2.VideoWriter(args.input_folder+'detected.mp4', fourcc, fps, (int(w), int(h)))
				frame_count = 0
				frames = []
				act_frames = []

				while True:
					ret, frame = input_movie.read()
					if not ret:
						break
					frame_count += 1
					act_frames.append(frame)
					frame = frame[:, :, ::-1]
					frames.append(frame)
					if len(frames) == 2:
						if args.upsample is not None:
							print_vid(act_frames,frames,output_movie,frame_count,args.upsample)
						else:
							print_vid(act_frames,frames,output_movie,frame_count)
						frames = []
						act_frames = []

				input_movie.release()
				cv2.destroyAllWindows()

		else:
			print("Usage [detect | recognize] [image | video] [path of input video/image to check] [path of known images(for recognition only)]") 

	elif args.method == "recognize":
		if not args.known_img:
			print("missing known images folder")
		else :
			if args.input_type == "image":

				if args.model is not None and args.upsample is not None:
					known_face_encd,known_face_name = get_encd_name_dict(args.known_img,args.model,args.upsample)
				elif args.model is not None and args.upsample is None:
					known_face_encd,known_face_name = get_encd_name_dict(args.known_img,args.model)
				elif args.model is None and args.upsample is not None:
					known_face_encd,known_face_name = get_encd_name_dict(args.known_img,upsample=args.upsample)
				else:
					known_face_encd,known_face_name = get_encd_name_dict(args.known_img)

				if args.upsample is not None:
					if args.model is not None and args.tolerance is not None:
						print_matches(args.input_folder,known_face_encd,known_face_name,args.model,args.tolerance,args.upsample)
					elif args.model is not None and args.tolerance is None:
						print_matches(args.input_folder,known_face_encd,known_face_name,in_model = args.model,upsample = args.upsample)
					elif args.model is None and args.tolerance is not None:
						print_matches(args.input_folder,known_face_encd,known_face_name,in_tolerance = args.tolerance,upsample = args.upsample)
					else:
						print_matches(args.input_folder,known_face_encd,known_face_name,upsample = args.upsample)
				else:		
					if args.model is not None and args.tolerance is not None:
						print_matches(args.input_folder,known_face_encd,known_face_name,args.model,args.tolerance)
					elif args.model is not None and args.tolerance is None:
						print_matches(args.input_folder,known_face_encd,known_face_name,in_model = args.model)
					elif args.model is None and args.tolerance is not None:
						print_matches(args.input_folder,known_face_encd,known_face_name,in_tolerance = args.tolerance)
					else:
						print_matches(args.input_folder,known_face_encd,known_face_name)


			elif args.input_type == "video":
				input_movie = cv2.VideoCapture(args.input_folder)
				length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
				fps = input_movie.get(cv2.CAP_PROP_FPS)
				fourcc = cv2.VideoWriter_fourcc(*'MP4V')
				w = input_movie.get(cv2.CAP_PROP_FRAME_WIDTH)
				h = input_movie.get(cv2.CAP_PROP_FRAME_HEIGHT)
				output_movie = cv2.VideoWriter(args.input_folder+'recognized.mp4', fourcc, fps, (int(w), int(h)))

				if args.model is not None and args.upsample is not None:
					known_face_encd,known_face_name = get_encd_name_dict(args.known_img,args.model,args.upsample)
				elif args.model is not None and args.upsample is None:
					known_face_encd,known_face_name = get_encd_name_dict(args.known_img,args.model)
				elif args.model is None and args.upsample is not None:
					known_face_encd,known_face_name = get_encd_name_dict(args.known_img,upsample=args.upsample)
				else:
					known_face_encd,known_face_name = get_encd_name_dict(args.known_img)

				frame_count = 0
				frames = []
				act_frames = []

				while True:
					ret, frame = input_movie.read()
					if not ret:
						break
					frame_count += 1
					act_frames.append(frame)
					frame = frame[:, :, ::-1]
					frames.append(frame)
					if len(frames) == 2:
						if args.tolerance is not None and args.upsample is not None:
							print_matches_vid(act_frames,frames,output_movie,frame_count,known_face_encd,known_face_name,args.tolerance,args.upsample)
						elif args.tolerance is None and args.upsample is not None:
							print_matches_vid(act_frames,frames,output_movie,frame_count,known_face_encd,known_face_name,upsample=args.upsample)
						elif args.tolerance is not None and args.upsample is None:
							print_matches_vid(act_frames,frames,output_movie,frame_count,known_face_encd,known_face_name,args.tolerance)
						else:
							print_matches_vid(act_frames,frames,output_movie,frame_count,known_face_encd,known_face_name)
						frames = []
						act_frames = []

				input_movie.release()
				cv2.destroyAllWindows()
			else:
				print("Usage [detect | recognize] [image | video] [path of input video/image to check] [path of known images(for recognition only)]") 

	else:
		print("Usage [detect | recognize] [image | video] [path of input video/image to check] [path of known images(for recognition only]")

if __name__ == '__main__':
	main()