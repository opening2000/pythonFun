CREATE
    TABLE url_cache
    (
        url VARCHAR(1000),
        urlmd5 VARCHAR(40) NOT NULL,
        content mediumtext,
        inserttime DATETIME,
        updatetime DATETIME,
        PRIMARY KEY (urlmd5),
        CONSTRAINT idx_url_cache_urlmd5 UNIQUE (urlmd5)
    )
    ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE
    TABLE url_error
    (
        urlmd5 VARCHAR(40) NOT NULL,
        url VARCHAR(1000),
        righturl VARCHAR(1000),
        errormessage VARCHAR(255),
        solveFlag VARCHAR(2) DEFAULT '0',
        solution VARCHAR(255),
        inserttime DATETIME,
        updatetime DATETIME,
        PRIMARY KEY (urlmd5),
        CONSTRAINT idx_url_error_uelmd5 UNIQUE (urlmd5)
    )
    ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE
    TABLE url_from_to
    (
        fromurldm5 VARCHAR(40) NOT NULL,
        fromurl VARCHAR(1000),
        tourlmd5 VARCHAR(40) NOT NULL,
        tourl VARCHAR(1000),
        COUNT INT,
        PRIMARY KEY (fromurldm5, tourlmd5),
        CONSTRAINT idx_url_from_to_tourlmd5 UNIQUE (tourlmd5),
        INDEX idx_url_from_to_fromurlmd5 (fromurldm5)
    )
    ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE
    TABLE url_main
    (
        urlmd5 VARCHAR(40) NOT NULL,
        parenturlmd5 VARCHAR(40),
        url VARCHAR(1000),
        name VARCHAR(255),
        level INT,
        isvisited VARCHAR(2),
        VALIDATE VARCHAR(2) DEFAULT '1',
        inserttime DATETIME,
        updatetime DATETIME,
        PRIMARY KEY (urlmd5),
        CONSTRAINT idx_url_main_urlmd5 UNIQUE (urlmd5),
        INDEX idx_url_main_parenturlmd5 (parenturlmd5)
    )
    ENGINE=InnoDB DEFAULT CHARSET=utf8;



