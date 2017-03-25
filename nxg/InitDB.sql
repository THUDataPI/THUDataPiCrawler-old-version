DROP TABLE IF EXISTS `lagou`.`company`;
CREATE TABLE  `lagou`.`company` (
  `companyId` varchar(20) NOT NULL,
  `companyShortName` varchar(100) DEFAULT NULL,
  `companyFullName` varchar(200) DEFAULT NULL,
  `financeStage` varchar(45) DEFAULT NULL,
  `city` varchar(30) DEFAULT NULL,
  `industryField` varchar(45) DEFAULT NULL,
  `companySize` varchar(20) DEFAULT NULL,
  `Dealed` varchar(5) DEFAULT '0',
  PRIMARY KEY (`companyId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='¹«Ë¾Ö÷±í';
