DROP TABLE IF EXISTS `COMPANY`;

CREATE TABLE `COMPANY` (
   `TICKER` VARCHAR(10) PRIMARY KEY,
   `NAME` VARCHAR(200) DEFAULT NULL,
   `DESCRIPTION` TEXT DEFAULT NULL,
   `INDUSTRY` VARCHAR(50) DEFAULT NULL,
   `SECTOR` VARCHAR(50) DEFAULT NULL,
   `REVENUE` VARCHAR(50) DEFAULT NULL,
   `NET_INCOME` VARCHAR(50) DEFAULT NULL,
   `EMPLOYEES` BIGINT DEFAULT 0,
   `RESOURCE_URL` VARCHAR(200) DEFAULT NULL,
   `LAST_RETRIEVED` DATE DEFAULT NULL,
   `CLASS` VARCHAR(10) DEFAULT NULL, -- stock or fund
   `FORWARD_PE` VARCHAR(50) DEFAULT NULL,
   `TRAILING_PE` VARCHAR(50) DEFAULT NULL,
   `PRICE_TO_BOOK` VARCHAR(50) DEFAULT NULL,
   `COUNTRY` VARCHAR(50) DEFAULT NULL,
   `LAST_TARGET_PRICE` VARCHAR(50) DEFAULT NULL
);

DROP TABLE IF EXISTS `AV_CACHE`;

CREATE TABLE `AV_CACHE` (
    `TICKER` VARCHAR(10) NOT NULL,
    `CLASS` VARCHAR(10) NOT NULL,
    `PAYLOAD` VARCHAR(10000) NOT NULL,
    `DATE` DATE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`TICKER`, `CLASS`)
);

DROP TABLE IF EXISTS `API_META`;

CREATE TABLE `API_META` (
    `API_KEY` VARCHAR(100) PRIMARY KEY,
    `USAGES` INT DEFAULT 0,
    `META_DATE` DATE DEFAULT CURRENT_DATE
);

DROP TABLE IF EXISTS `HISTORIC_META_DATA`;

CREATE TABLE `HISTORIC_META_DATA`(
    `TICKER` VARCHAR(10) PRIMARY KEY,
    `LAST_RETRIEVED` INT DEFAULT 0
);

DROP TABLE IF EXISTS `HISTORIC_DATA`;

CREATE TABLE `HISTORIC_DATA`(
     `TICKER` VARCHAR(10) NOT NULL,
     `DATE` INT DEFAULT 0,
     `OPEN` VARCHAR(10) NOT NULL,
     `HIGH` VARCHAR(10) NOT NULL,
     `LOW` VARCHAR(10) NOT NULL,
     `CLOSE` VARCHAR(10) NOT NULL,
     `VOLUME` VARCHAR(10) NOT NULL,
     PRIMARY KEY (`TICKER`, `DATE`)
);
