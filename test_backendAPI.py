"""
performs unit test demo on the python app
"""



# arrange
# act
# assert



# import pytest library
import pytest

# import all dependencies and functions/classes from script we want to test
from initialize_backendAPI import *

# define objects for each class using sample inputs, use decorator to avoid repeating code
@pytest.fixture
def correct_db():

	# input some values which we know "should" work but we want to test
	user_sample = UserInfo(user_ID="1A",Email="abc@gmail.com")
	image_sample = ImageDB(ImageID=1,ImagePath="temp",Date="2021-10-1 14:01:30",Type="Apple",TenantID="1A",userinfo=user_sample)

	return user_sample, image_sample

# define objects for each class using wrong inputs, also use decorator
@pytest.fixture
def incorrect_db():

	# input values where we know are wrong
	user_sample = UserInfo(user_ID=1,Email="abc@gmail.com")
	image_sample = ImageDB(ImageID="1",ImagePath=123,Date="2021-10 14:01",Type="toothbrush",TenantID=1,userinfo=user_sample)

	return user_sample, image_sample



# define a predetermined set of fruits
@pytest.fixture
def fruit_we_know():
	return(["Apple","Orange","Kiwifruit","Lemon","Cherry"])

# test the fruit is within the predetermined set
def test_fruit(correct_db,fruit_we_know):
	assert any(correct_db[1].Type in f for f in fruit_we_know)
	
# perform same test as above except use wrong data
# this test should fail, so to pass we use "not"
def test_wrong_fruit(incorrect_db,fruit_we_know):
	assert not any(incorrect_db[1].Type in f for f in fruit_we_know)



# test the correct data types are passed through
def test_input_types(correct_db):
	assert type(correct_db[1].ImageID) is int and type(correct_db[1].ImagePath) is str and type(correct_db[0].user_ID) is str
	
# perform same test as above except use wrong data
# this test should fail, so to pass we use "not"
def test_wrong_input_types(incorrect_db):
	assert not (type(incorrect_db[1].ImageID) is int or type(incorrect_db[1].ImagePath) is str or type(incorrect_db[0].user_ID) is str)



# test the correct date format
def test_correct_date(correct_db):
	try:
		assert datetime.strptime(correct_db[1].Date, "%Y-%m-%d %H:%M:%S")
	except ValueError:
		assert False

# same as above but incorrect date format is inputted
def test_wrong_date(incorrect_db):
	try:
		assert datetime.strptime(incorrect_db[1].Date, "%Y-%m-%d %H:%M:%S")
	except ValueError:
		assert True



# test the ImageInfo class to get from database (put/path/delete require active session)
def test_get():
	
	# define object
	db_access = ImageInfo()
	
	assert isinstance(db_access.get(1),dict) # check if dictionary is return
	assert len(db_access.get(1)) == 5 # should only have 5 columns
	