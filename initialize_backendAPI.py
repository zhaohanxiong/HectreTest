'''
This script initializes the Flask API and the SQL alchemy database
'''

# import dependencies
import os
import cv2
from datetime import datetime 
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

# UserInfo database has a one-to-many relationship with ImageDB Database, defined below
# class define the structure of the database for user info
class UserInfo(db.Model):
	
	# define tenant ID column (max 100 character string)
	user_ID = db.Column(db.String(100), primary_key=True)
	
	# define user email column (max 100 character string), 
	Email = db.Column(db.String(100), nullable=False)
	
	# create one-to-many relation, a sudo column in Image DB for the user
	image_by_user = db.relationship("ImageDB", backref="userinfo")
	
	# wrapper to print all info
	def __repr__(self):
		return ("Email = "+Email+" tenant id = "+user_ID)

# class to define the structure of the database for images info
class ImageDB(db.Model):

	# define the image ID column which is primary key
	ImageID = db.Column(db.Integer, primary_key=True)
	
	# define the path of the image to be uploaded
	ImagePath = db.Column(db.String, nullable=False)
	
	# define date time column (UTC format)
	Date = db.Column(db.DateTime(timezone=True), nullable=False)
	
	# define fruit type column (max 100 character string), may be you dont know the fruit type at first
	Type = db.Column(db.String(100))

	# define tenant ID column (max 100 character string)
	# foreign key refers to the primary key in another table, so its linked to the user info table
	TenantID = db.Column(db.String(100), db.ForeignKey(UserInfo.user_ID), nullable=False)
	
	# wrapper to print all info
	def __repr__(self):
		return ("Images(image id = "+str(ImageID)+" date = "+str(Date)+" type = "+Type+" tenant id = "+TenantID)

# create the database if it doesnt exist, if it exist, then dont overwrite
if not any([s for s in os.listdir() if s == "image_database.db"]):
	
	# create database
	db.create_all()
	
# create a folder to store images (more efficient to store images in filesystem than in SQL database)
if not any([s for s in os.listdir() if s == "image_filesystem"]):
	
	# create folder
	os.mkdir("image_filesystem")

# define guidelines for put arguments with data type and error msg
image_put_args = reqparse.RequestParser()
image_put_args.add_argument("ImageID",type=int,help="Error! Insert ImageID",required=True)
image_put_args.add_argument("ImagePath",type=str,help="Error! Insert image path")
image_put_args.add_argument("Date",type=lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'),help="Error! Insert Date",required=True)
image_put_args.add_argument("Type",type=str,help="Error! Insert Fruit Type",required=True)
image_put_args.add_argument("Email",type=str,help="Error! Insert User Email",required=True)
image_put_args.add_argument("TenantID",type=str,help="Error! Insert TenantID",required=True)

# define guidelines for updating database, not all fields are required, only primary key (ImageID)
image_update_args = reqparse.RequestParser()
image_update_args.add_argument("ImageID",type=int,help="Error! Insert ImageID",required=True)
image_update_args.add_argument("ImagePath",type=str)
image_update_args.add_argument("Date",type=lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
image_update_args.add_argument("Type",type=str)
image_update_args.add_argument("Email",type=str)
image_update_args.add_argument("TenantID",type=str)

# define the data types of the class
resource_fields = {"ImageID": fields.Integer, # unique ID of image
				   "ImagePath": fields.String, # path of image to be uploaded
				   "Date": fields.DateTime(dt_format='iso8601'), # time and date of image acquired
				   "Type": fields.String, # type of fruit in image
				   "TenantID": fields.String # ID of user uploading image
				  }

# create a class with inherits from resource, resource has few methods (get put delete etc)
class ImageInfo(Resource):
	
	# decorator to serialize the object into the desired dictionary, otherwise only object will be returned
	@marshal_with(resource_fields)
	
	# return something from database given the image ID
	def get(self, image_id):
	
		# query images by ID, get first sample
		result = ImageDB.query.filter_by(ImageID=image_id).first()
		
		# if no result found
		if not result:
			abort(404, message="Error! could not find image with id")
		
		# return output data row
		return(result)
	
	# decorator to serialize the object into the desired dictionary, otherwise only object will be returned
	@marshal_with(resource_fields)
	
	# create new entry into database
	def put(self, image_id):
		
		# take input arguments and define the class with it
		args = image_put_args.parse_args()
		
		# check if image ID already exists
		result = ImageDB.query.filter_by(ImageID=image_id).first()
		
		# if image ID already exist then abort
		if result:
			abort(409, message="Error! image id already taken")
		
		# check if user id exists, if not, we can insert it into user table
		result = UserInfo.query.filter_by(user_ID=args["TenantID"]).first()
		
		if result:
			user = result # reuse user if already exists in database
		else:
			user = UserInfo(user_ID=args["TenantID"],Email=args["Email"])
			
		# save info
		db.session.add(user) # temporarily add
		db.session.commit() # permanently add
		
		# define objects
		image = ImageDB(ImageID=image_id,ImagePath=args["ImagePath"],Date=args["Date"],Type=args["Type"],TenantID=args["TenantID"],userinfo=user)

		# save info
		db.session.add(image) # temporarily add
		db.session.commit() # permanently add
		
		# read the file into memory given path
		# not sure if open-cv can be used like this in this in this framework?
		image_file = cv2.imread(args["ImagePath"],cv2.IMREAD_GRAYSCALE) # made it black and white so you can see its a different image
		
		# save the image into the filesystem created above, pad name with zeros
		cv2.imwrite("image_filesystem/"+"{0:04}".format(image_id)+" - new_image.png",image_file)

		# return image with success
		return(image, 201)
	
	# decorator to serialize the object into the desired dictionary, otherwise only object will be returned
	@marshal_with(resource_fields)
	
	# edit an existing entry in a database
	def patch(self, image_id):
		
		# take input arguments and define the class with it
		args  = image_update_args.parse_args()
		result = ImageDB.query.filter_by(ImageID=image_id).first()
		
		# if such ID doesnt exist
		if not result:
			abort(404, message="Error! could not find image with that ID, cannot update")
		
		# make individual changes (not a very clean way to do it, can be improved in future)
		# dont make changes to primary key
		if args["ImagePath"]:
			result.ImagePath = args["ImagePath"]
		if args["Date"]:
			result.Date = args["Date"]	
		if args["Type"]:
			result.Type = args["Type"]
		if args["TenantID"]:
			result.TenantID = args["TenantID"]
		
		# save changes
		db.session.commit()
		
		# return filtered result
		return(result)
	
	# decorator to serialize the object into the desired dictionary, otherwise only object will be returned
	@marshal_with(resource_fields)
	
	# remove entry from database
	def delete(self, image_id):
	
		# take input arguments and define the class with it
		result = ImageDB.query.filter_by(ImageID=image_id).first()
		
		# if such ID doesnt exist
		if not result:
			abort(404, message="Error! could not find image with that ID, cannot delete")
		
		# remove entry
		ImageDB.query.filter_by(ImageID=image_id).delete()
		
		# save changes
		db.session.commit()
		
		# return success message
		return("successfully delete entry image id = "+str(image_id))

'''
# set up connections to upload images (this part doesnt work, I didnt have enough time for this)
# 	this part reads image from some user interface (could be html site upload) and stores it into the
# 	database as defined above. For this to work, I would need to define another data structure inside the
# 	class, and also know more about the exact connection being made
#	
# 	but I believe this shouldnt be a good way as storing images in SQL databases is inefficient
@app.route("/")
def index():
	return(render_template("upload_image_into_this_app"))
	
@app.route("/upload")
def upload():
	file = request.files["inputFile"]
	
	newFile = FileContents(name=file.filename, data=file.read())
	db.session.add(newFile)
	db.session.commit()
	
'''

# Add class to API
api.add_resource(ImageInfo, "/image/<int:image_id>")

# start server and flask application
if __name__ == "__main__":

	app.run(debug=True) # run testing in debugging mode, choose False if deploying