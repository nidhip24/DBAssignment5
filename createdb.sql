CREATE DATABASE order_db;
USE order_db;
CREATE USER 'dbowner'@'127.0.0.1' IDENTIFIED BY 'Secret5555';
GRANT ALL PRIVILEGES ON order_db.* TO 'dbowner'@'127.0.0.1'