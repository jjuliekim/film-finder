DROP DATABASE IF EXISTS `film-finder`;
CREATE DATABASE `film-finder`;
SHOW DATABASES;
USE `film-finder`;

DROP TABLE IF EXISTS UserProfiles;
CREATE TABLE UserProfiles(
    userID    INT PRIMARY KEY,
    firstName VARCHAR(50),
    lastName  VARCHAR(50),
    gender    CHAR(1),
    DOB  DATE,
    forKids BOOLEAN,
    forTeens BOOLEAN,
    forAdults BOOLEAN
);

DROP TABLE IF EXISTS Employees;
CREATE TABLE Employees(
    empID INT PRIMARY KEY,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    role VARCHAR(100)
);

DROP TABLE IF EXISTS Requests;
CREATE TABLE Requests(
    requestID INT PRIMARY KEY,
    message MEDIUMTEXT NOT NULL,
    timestamp DATETIME,
    status VARCHAR(50),
    userID INT,
    empID INT,
    FOREIGN KEY (userID) REFERENCES UserProfiles(userID),
    FOREIGN KEY (empID) REFERENCES Employees(empID)
);

DROP TABLE IF EXISTS EmpUserProfiles;
CREATE TABLE EmpUserProfiles(
    empID INT,
    userID INT,

    PRIMARY KEY (empID, userID),
    FOREIGN KEY (empID) REFERENCES Employees(empID),
    FOREIGN KEY (userID) REFERENCES UserProfiles(userID)
);

DROP TABLE IF EXISTS Messages;
CREATE TABLE Messages(
    msgID INT PRIMARY KEY,
    content TEXT,
    sender INT,
    FOREIGN KEY (sender) REFERENCES Employees(empID)
);

DROP TABLE IF EXISTS MessageReceived;
CREATE TABLE MessageReceived(
    msgID INT,
    receiver INT,
    PRIMARY KEY (msgID, receiver),
    FOREIGN KEY (msgID) REFERENCES Messages(msgID),
    FOREIGN KEY (receiver) REFERENCES Employees(empID)
);

DROP TABLE IF EXISTS Tasks;
CREATE TABLE Tasks(
    taskID           INT PRIMARY KEY AUTO_INCREMENT,
    createdAt        DATETIME,
    completedAt      DATETIME,
    description TEXT NOT NULL,
    empID INT,
    FOREIGN KEY (empID) REFERENCES Employees(empID)
);

DROP TABLE IF EXISTS FilteredSearches;
CREATE TABLE FilteredSearches(
    searchID INT PRIMARY KEY,
    filterRules TEXT,
    annotations TEXT,
    createdAt DATETIME,
    annotatorID INT,
    FOREIGN KEY (annotatorID) REFERENCES Employees(empID)
);

DROP TABLE IF EXISTS SavedSearches;
CREATE TABLE SavedSearches(
    searchID INT,
    empID INT,
    FOREIGN KEY (searchID) REFERENCES FilteredSearches(searchID),
    FOREIGN KEY (empID) REFERENCES Employees(empID)
);

DROP TABLE IF EXISTS AppVersions;
CREATE TABLE AppVersions(
    versionID INT PRIMARY KEY,
    createdAt TIMESTAMP,
    publishedAt TIMESTAMP,
    description TEXT,
    empID INT,
    FOREIGN KEY (empID) REFERENCES Employees(empID)
);

DROP TABLE IF EXISTS Movies;
CREATE TABLE Movies(
    movieID INT PRIMARY KEY,
    yearReleased INT, 
    duration INT,
    title VARCHAR(255)
);

DROP TABLE IF EXISTS Reviews;
CREATE TABLE Reviews(
    reviewID INT PRIMARY KEY AUTO_INCREMENT,
    userID INT, -- FK from UserProfiles
    movieID INT, -- FK from Movies
    reviewText VARCHAR(255),
    publishedDate DATETIME,
    starRating INT, -- stores values 1-5
    FOREIGN KEY (userID) REFERENCES UserProfiles(userID),
    FOREIGN KEY (movieID) REFERENCES Movies(movieID)
);

DROP TABLE IF EXISTS WatchParties;
CREATE TABLE WatchParties(
    partyID INT PRIMARY KEY AUTO_INCREMENT,
    movieID INT, -- FK to Movies
    partyDate DATE,
    FOREIGN KEY (movieID) REFERENCES Movies(movieID)
);

DROP TABLE IF EXISTS WatchPartyMembers;
CREATE TABLE WatchPartyMembers(
    partyID INT,
    userID INT,
    PRIMARY KEY (partyID, userID),
    FOREIGN KEY (partyID) REFERENCES WatchParties(partyID),
    FOREIGN KEY (userID) REFERENCES UserProfiles(userID)
);

DROP TABLE IF EXISTS Lists;
CREATE TABLE Lists (
	listID INT PRIMARY KEY AUTO_INCREMENT,
	listName VARCHAR(100),
	userID INT,
	FOREIGN KEY(userID) REFERENCES UserProfiles(userID)
);

DROP TABLE IF EXISTS MovieLists;
CREATE TABLE MovieLists (
	listID INT,
	movieID INT,
	PRIMARY KEY(listID, movieID),
	FOREIGN KEY(listID) REFERENCES Lists(listID),
	FOREIGN KEY(movieID) REFERENCES Movies(movieID)
);

DROP TABLE IF EXISTS Captions; -- WEAK ENTITY of Movies
CREATE TABLE Captions(
    lang VARCHAR(3), -- partial key
    movieID INT , -- fk to Movies
    captionText CHAR(255),
    PRIMARY KEY (lang, movieID), -- composite key
    FOREIGN KEY (movieID) REFERENCES Movies(movieID)
);

DROP TABLE IF EXISTS Trailers; -- weak entity of Movies
CREATE TABLE Trailers(
    trailerID INT, -- partial key
    movieID INT,   -- FK to Movies (parent)
    trailerLength INT,
    PRIMARY KEY (trailerID, movieID), -- composite key
    FOREIGN KEY (movieID) REFERENCES Movies(movieID)
);

DROP TABLE IF EXISTS Actors;
CREATE TABLE Actors (
	actorID INT,
	firstName VARCHAR(50),
	lastName VARCHAR(50),
	PRIMARY KEY(actorID)
);

DROP TABLE IF EXISTS MovieActors;
CREATE TABLE MovieActors (
	movieID INT,
	actorID INT,
	PRIMARY KEY(movieID, actorID),
	FOREIGN KEY(movieID) REFERENCES Movies(movieID),
	FOREIGN KEY(actorID) REFERENCES Actors(actorID)
);

DROP TABLE IF EXISTS Directors;
CREATE TABLE Directors (
	directorID INT,
	firstName VARCHAR(50),
	lastName VARCHAR(50),
	PRIMARY KEY(directorID)
);

DROP TABLE IF EXISTS MovieDirectors;
CREATE TABLE MovieDirectors (
	movieID INT,
	directorID INT,
	PRIMARY KEY(movieID, directorID),
	FOREIGN KEY(movieID) REFERENCES Movies(movieID),
	FOREIGN KEY(directorID) REFERENCES Directors(directorID)
);

DROP TABLE IF EXISTS Genres;
CREATE TABLE Genres(
    genreID INT PRIMARY KEY,
    name VARCHAR(50)
);

DROP TABLE IF EXISTS MovieGenres;
CREATE TABLE MovieGenres (
	movieID INT,
	genreID INT,
	PRIMARY KEY(genreID , movieID),
	FOREIGN KEY(genreID) REFERENCES Genres(genreID),
	FOREIGN KEY(movieID) REFERENCES Movies(movieID)
);
