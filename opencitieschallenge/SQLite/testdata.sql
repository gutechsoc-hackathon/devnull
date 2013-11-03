BEGIN TRANSACTION;
INSERT INTO Users VALUES (1, 'guteamdevnull@gmail.com', '000001', '2013-11-02 17:22:35', 'password');
INSERT INTO Visited_Venues VALUES (1, '6bj8shjks9p74637', 'Kelvingrove Gallery', 2, 1200);
INSERT INTO Locations VALUES (1, -4.290698, 55.868509, '2013-11-02 17:22:35', 1200);
COMMIT;
