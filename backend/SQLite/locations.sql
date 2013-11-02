BEGIN TRANSACTION;
CREATE TABLE Locations(UId integer foreign key, Long real primary key, Lat real primary key, Time text primary key, Duration integer);
COMMIT