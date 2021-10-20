# import dependencies
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
# create a new app
app = Flask(__name__)

# wrap app within restful api
api = Api(app)

# configure the sql alchemy database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

# define the database
db = SQLAlchemy(app)

# define structure of database
class VideoModel(db.Model):

	# define the id column with unique keys
	id = db.Column(db.Integer, primary_key=True)

	# define name column with max 100 char, and data has to always have a name
	name = db.Column(db.String(100), nullable=False)
	
	# define two more numeric columns
	views = db.Column(db.Integer, nullable=False)
	likes = db.Column(db.Integer, nullable=False)

	# wrapper to pring all info
	def __repr__(self):
		return ("Video(name = "+str(name)+" views = "+str(views)+" likes = "+str(likes))

# create a database, only do this once!!!
#db.create_all()

# define guidelines for input arguments with data type and error msg
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name",type=str,help="Error! Insert Name of Video",required=True)
video_put_args.add_argument("views",type=int,help="Error! Insert Likes on Video",required=True)
video_put_args.add_argument("likes",type=int,help="Error! Insert Views on Video",required=True)

# define guidelines for updating data, not contrained to needing all input args
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name",type=str,help="Error! Insert Name of Video")
video_update_args.add_argument("views",type=int,help="Error! Insert Likes on Video")
video_update_args.add_argument("likes",type=int,help="Error! Insert Views on Video")

# define the data types of the class
resource_fields = {"id": fields.Integer,
				   "name": fields.String,
				   "views": fields.Integer,
				   "likes": fields.Integer
				  }

# abort criteria if queried video doesnt exist, doesnt crash program and return error message
def abort_if_video_id_doesnt_exist(video_id):
	if video_id not in videos:
		abort(404,message="Video ID is not valid")

# abort criteria if video already exists
def abort_if_video_exist(video_id):
	if video_id in videos:
		abort(409, message="Video already exists")

# create a class with inherits from resource, resource has few methods (get put delete etc)
class Video(Resource):
	
	# decorator to serialize the object into the desired dictionary, otherwise only object will be returned
	@marshal_with(resource_fields)
	
	# return something
	def get(self, video_id):
	
		# abort if video id queried doesnt exist in database
		result = VideoModel.query.filter_by(id=video_id).first()
		
		# if no result found
		if not result:
			abort(404, message="could not find video with ID")
			
		return(result)
	
	# decorator to serialize the object into the desired dictionary, otherwise only object will be returned
	@marshal_with(resource_fields)
	
	# create something
	def put(self, video_id):
		
		# take input arguments and define the class with it
		args  = video_put_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		
		# if ID already exist then abort
		if result:
			abort(409, message="Video ID taken")
		
		video = VideoModel(id=video_id, name=args["name"],views=args["views"],likes=args["likes"])
		
		# store info
		db.session.add(video) # temporarily add
		db.session.commit() # permanently add
		
		return(video, 201)
	
	# decorator to serialize the object into the desired dictionary, otherwise only object will be returned
	@marshal_with(resource_fields)
	def patch(self,video_id):
		
		# take input arguments and define the class with it
		args  = video_update_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		
		if not result:
			abort(404, message="could not find video with ID, cannot update")
		
		if args["name"]:
			result.name = args["name"]
		if args["views"]:
			result.views = args["views"]	
		if args["likes"]:
			result.likes = args["likes"]
		
		db.session.commit()
		
		return result
		
	# remove something
	def delete(self, video_id):
	
		# abort if trying to delete data that doesnt exist
		abort_if_video_id_doesnt_exist(video_id)
		del videos[video_id]
		return("",204)

api.add_resource(Video, "/video/<int:video_id>")

# start server and flask application, in debugging mode
if __name__ == "__main__":
	app.run(debug=True) # false unless in dev mode
	
