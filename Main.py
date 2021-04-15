import os
import requests
import sqlite3

# path to the \Movies.txt file on Desktop 
desktopLocation = os.path.join(os.getcwd(), 'movies.txt')

apiKey = '8f0d9811'
URL = 'http://www.omdbapi.com/?apikey=' + apiKey

# DataBase handling
connection = sqlite3.connect('movies.db')
cursor = connection.cursor()
cursor.execute("""CREATE TABLE movies(
                title text, type text, genre text, actors text, language text, director text,
                country text, awards text, boxoffice text, imdbID text, rating text, votes text,
                year text, writer text, runtime text, production text, plot text) """)
connection.commit()

class Movie:

	def __init__(self, movie):
		self.title = movie['Title'] if movie['Title'] else 'Unknown'
		self._type = movie['Type'] if movie['Type'] else 'Unknown'
		self.genre = movie['Genre'] if movie['Genre'] else 'Unknown'
		self.actors = movie['Actors'] if movie['Actors'] else 'Unknown'
		self.language = movie['Language'] if movie['Language'] else 'Unknown'
		self.director = movie['Director'] if movie['Director'] else 'Unknown'
		self.country = movie['Country'] if movie['Country'] else 'Unknown'
		self.awards = movie['Awards'] if movie['Awards'] else 'Unknown'
		self.boxoffice = movie['BoxOffice'] if movie['BoxOffice'] else 'Unknown'
		self.id = movie['imdbID'] if movie['imdbID'] else 'Unknown'
		self.rating = movie['imdbRating'] if movie['imdbRating'] else 'Unknown'
		self.votes = movie['imdbVotes'] if movie['imdbVotes'] else 'Unknown'
		self.year = movie['Year'] if movie['Year'] else 'Unknown'
		self.writer = movie['Writer'] if movie['Writer'] else 'Unknown'
		self.runtime = movie['Runtime'] if movie['Runtime'] else 'Unknown'
		self.production = movie['Production'] if movie['Production'] else 'Unknown'
		self.plot = movie['Plot'] if movie['Plot'] else 'Unknown'

	# Check if the movie satisfies users conditions
	def checkMe(self, genre, rating):
		if rating and (float(rating) > float(self.rating)):
			return True
		if genre and (self.genre.strip() in genre.strip()):
			return True
		return False

	# Write informations about movie into .txt file
	def saveMe(self, location):
		with open(location, 'a') as f:
			for attribute, value in self.__dict__.items():
				f.write(f'{attribute}: {value} \n')
			f.write('-'*200 + '\n')


def getMyMovies(titles):
	results = []
	
	for titlee in titles:
		cursor.execute(f"SELECT * FROM movies WHERE title = '{titlee}'")
		queryResults = cursor.fetchall()
		
		if queryResults: # Check if the movie exist in DataBase
			for qr in queryResults:
				movie ={'Title':qr[0],'Type':qr[1],'Genre':qr[2],'Actors':qr[3],'Language':qr[4],'Director':qr[5],
						'Country':qr[6],'Awards':qr[7],'BoxOffice':qr[8],'imdbID':qr[9],'imdbRating':qr[10],
						'imdbVotes':qr[11],'Year':qr[12],'Writer':qr[13],'Runtime':qr[14],'Production':qr[15],'Plot':qr[16]
						}
		else:	
			params = {
    				't': titlee,
    				'type':'movie',
    				'y':'',
    				'plot':'full'
					}
			movie = requests.get( URL, params=params).json()
			cursor.execute("""INSERT INTO movies VALUES (:Title,:Type,:Genre,:Actors,:Language,:Director,:Country,:Awards,
							  :BoxOffice,:imdbID,:imdbRating,:imdbVotes,:Year,:Writer,:Runtime,:Production,:Plot)""",movie)
			connection.commit()
		
		results.append(Movie(movie))
	return results

def getAndFilterMyMovies(title, genre= '', rating= ''):
	movies = getMyMovies(title)
	results = [movie for movie in movies if movie.checkMe(genre, rating)]
	return results

def main():
	while True:

		title = input('Titles (Separate titles with ,):').split(',')
		genre = input('Genre (optional):')
		rating = input('Rating (optional):')

		movies = getAndFilterMyMovies(title, genre, rating) if (genre!='' or rating!='') else getMyMovies(title)

		fileLocation = input('Path to .txt file for storing info about movies (Default: Desktop/Movies.txt):')
		fileLocation = fileLocation if (fileLocation and '.txt' in fileLocation) else desktopLocation

		for movie in movies:
			movie.saveMe(fileLocation)

		if 'y' in input('Exit application ? (y/n)').lower():
			connection.close()
			break


if __name__ == '__main__':

	main()
	



