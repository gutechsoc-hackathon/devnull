BEGIN TRANSACTION;
CREATE TABLE Users(UId integer primary key autoincrement, Email text, SId text, LastAccess text, password text);
COMMIT