'''
'''

# import dependencies
import os
import datetime
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# create a new app
app = Flask(__name__)

# wrap app within RESTful api
api = Api(app)

# configure the sql alchemy database, just store it in relative directory for now
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///image_database.db"

# initialize the database
db = SQLAlchemy(app)

# class to define the structure of the database
class ImageDB(db.Model):

	# define the image ID column which is primary key
	ImageID = db.Column(db.Integer, primary_key=True)

	# define date time column (UTC format)
	Date = db.Column(db.DateTime(timezone=True), nullable=False)
	
	# define fruit type column (max 100 character string)
	Type = db.Column(db.String(100), nullable=False)
	
	# define user email column (max 100 character string)
	Email = db.Column(db.String(100), nullable=False)
	
	# define tenant ID column (max 100 character string)
	TenantID = db.Column(db.String(100), nullable=False)
	
	# wrapper to print all info
	def __repr__(self):
		return ("Images(image id = "+str(ImageID)+" date = "+str(Date)+" type = "+Type+" email = "+Email+" tenant id = "+TenantID)

# create the database if it doesnt exist, if it exist, then dont overwrite
if not any([s for s in os.listdir() if s == "image_database"]):
	
	# create database
	db.create_all()

# define guidelines for put arguments with data type and error msg
image_put_args = reqparse.RequestParser()
image_put_args.add_argument("ImageID",type=int,help="Error! Insert ImageID",required=True)
image_put_args.add_argument("Date",type=datetime.datetime,help="Error! Insert Date",required=True)
image_put_args.add_argument("Type",type=str,help="Error! Insert Fruit Type",required=True)
image_put_args.add_argument("Email",type=str,help="Error! Insert User Email",required=True)
image_put_args.add_argument("TenantID",type=str,help="Error! Insert TenantID",required=True)

# define guidelines for updating database, not all fields are required, only primary key (ImageID)
image_update_args = reqparse.RequestParser()
image_update_args.add_argument("ImageID",type=int,help="Error! Insert Name of Video",required=True)
image_update_args.add_argument("Date",type=datetime.datetime)
image_update_args.add_argument("Type",type=str)
image_update_args.add_argument("Email",type=str)
image_update_args.add_argument("TenantID",type=str)

# define the data types of the class
resource_fields = {"ImageID": fields.Integer,
				   "Date": fields.DateTime,
				   "Type": fields.String,
				   "Email": fields.String,
				   "TenantID": fields.String
				  }

# create a class with inherits from resource, resource has few methods (get put delete etc)
class Image(Resource):
	
	# decorator to serialize the object into the desired dictionary, otherwise only object will be returned
	@marshal_with(resource_fields)
	
	# return something
	def get(self, ImageID):
	
		# query images by ID, get first sample
		result = ImageDB.query.filter_by(id=ImageID).first()
		
		# if no result found
		if not result:
			abort(404, message="Error! could not find image with id")
			
		return(result)
	
	# decorator to serialize the object into the desired dictionary, otherwise only object will be returned
	@marshal_with(resource_fields)
	
	# create something
	def put(self, ImageID):
		
		# take input arguments and define the class with it
		args = image_put_args.parse_args()
		result = ImageDB.query.filter_by(id=ImageID).first()
		
		# if ID already exist then abort
		if result:
			abort(409, message="Error! image id already taken")
		
		image = ImageDB(id=ImageID, name=args["name"],views=args["views"],likes=args["likes"])
		
		# store info
		db.session.add(image) # temporarily add
		db.session.commit() # permanently add
		
		# return image with success
		return(image, 201)
	
	# decorator to serialize the object into the desired dictionary, otherwise only object will be returned
	@marshal_with(resource_fields)
	def patch(self,ImageID):
		
		# take input arguments and define the class with it
		args  = image_update_args.parse_args()
		result = ImageDB.query.filter_by(id=ImageID).first()
		
		# if such ID doesnt exist
		if not result:
			abort(404, message="Error! could not find image with that ID, cannot update")
		
		# make individual changes (not a very clean way to do it, can be improved in future)
		if args["ImageID"]:
			result.name = args["ImageID"]
		if args["Date"]:
			result.views = args["Date"]	
		if args["Type"]:
			result.likes = args["Type"]
		if args["Email"]:
			result.likes = args["Email"]
		if args["TenantID"]:
			result.likes = args["TenantID"]
		
		# add changes
		db.session.commit()
		
		# return filtered result
		return result
	
	# remove something
###########	def delete(self, ImageID):
	
		# abort if trying to delete data that doesnt exist
		abort_if_video_id_doesnt_exist(ImageID)
		del images[ImageID]
		return("",204)

# Add class to API
api.add_resource(Image, "/image/<int:ImageID>")

# start server and flask application
if __name__ == "__main__":

	app.run(debug=True) # run testing in debugging mode