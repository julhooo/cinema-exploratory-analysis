CREATE TABLE films (
    tconst VARCHAR(20) PRIMARY KEY,
    primaryTitle VARCHAR(200) NOT NULL,
    releaseYear INT NOT NULL,
    runtimeMinutes INT NOT NULL,
    averageRating FLOAT NOT NULL,
    numVotes INT NOT NULL
);

CREATE TABLE financial (
    tconst VARCHAR(20) PRIMARY KEY,
    budget INT NOT NULL,
    boxoffice INT NOT NULL,
    profit INT NOT NULL,
    FOREIGN KEY (tconst) REFERENCES Films(tconst)
);

CREATE TABLE crew (
    nconst VARCHAR(20) PRIMARY KEY,
    crewName VARCHAR(100) NOT NULL,
    birthYear INT, 
    deathYear INT
);

CREATE TABLE directors (
    tconst VARCHAR(20),
    nconst VARCHAR(20),
    PRIMARY KEY(tconst, nconst),
    FOREIGN KEY (tconst) REFERENCES Films(tconst),
    FOREIGN KEY (nconst) REFERENCES Crew(nconst)
);

CREATE TABLE writers (
    tconst VARCHAR(20),
    nconst VARCHAR(20),
    PRIMARY KEY(tconst, nconst),
    FOREIGN KEY (tconst) REFERENCES Films(tconst),
    FOREIGN KEY (nconst) REFERENCES Crew(nconst)
);

CREATE TABLE genres (
    tconst VARCHAR(20),
    genres VARCHAR(20),
    PRIMARY KEY(tconst, genres),
    FOREIGN KEY (tconst) REFERENCES Films(tconst)
);