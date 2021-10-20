# import dependencies
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
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
	def __repr(self):
		return ("Video(name = "+str(name)+" views = "+str(views)+" likes = "+str(likes))

# create a database, only do this once!!!
#db.create_all()

# define guidelines for input arguments with data type and error msg
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name",type=str,help="Error! Insert Name of Video",required=True)
video_put_args.add_argument("views",type=int,help="Error! Insert Likes on Video",required=True)
video_put_args.add_argument("likes",type=int,help="Error! Insert Views on Video",required=True)

videos = {}

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
	
	# return something
	def get(self, video_id):
	
		# abort if video id queried doesnt exist in database
		abort_if_video_id_doesnt_exist(video_id)
		return(videos[video_id])
		
	# create something
	def put(self, video_id):
	
		# skip if ID already exists
		abort_if_video_exist(video_id)
		
		# gets input argumments to insert new data
		args = video_put_args.parse_args()
	
		# add video from parsed argument into database
		videos[video_id] = args
		
		return(videos[video_id], 201)
		
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
	
