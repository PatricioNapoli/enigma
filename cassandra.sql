CREATE KEYSPACE "enigma" WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};

USE enigma;
CREATE TABLE btc(time bigint primary key, value float);
CREATE TABLE eth(time bigint primary key, value float);

