-- 유저타입 테이블

SET foreign_key_checks = 0;
DROP TABLE IF EXISTS user_types;
CREATE TABLE user_types
(
    `id`             INT             NOT NULL    AUTO_INCREMENT COMMENT 'pk',
    `name`           VARCHAR(100)    NOT NULL    COMMENT '유저이름',
    PRIMARY KEY (id)
);

/*
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | int          | NO   | PRI | NULL    | auto_increment |
| name  | varchar(100) | NO   |     | NULL    |                |
+-------+--------------+------+-----+---------+----------------+
*/

-- 유저 테이블
DROP TABLE IF EXISTS users;
CREATE TABLE users
(
    `id`             INT              NOT NULL    AUTO_INCREMENT COMMENT 'pk',
    `login_id`       VARCHAR(100)     NOT NULL    COMMENT '유저 아이디',
    `password`       VARCHAR(1000)    NOT NULL    COMMENT '유저 패스워드',
    `user_type_id`   INT              NOT NULL    COMMENT '유저 타입아이디',
    `activation`     BOOLEAN          NOT NULL    DEFAULT False COMMENT '유저 활성상태', 
    `created_at`     TIMESTAMP        NOT NULL    Default NOW() 	COMMENT '등록 일자',
    `updated_at`     TIMESTAMP        NULL        Default NOW() ON UPDATE NOW() COMMENT '수정 일자',
    `removed_at`     TIMESTAMP        NULL        COMMENT '삭제 일자', 
    PRIMARY KEY (id)
);

-- 유저와 유저타입 연결 
-- (다른 테이블의 기본 키를 참조하는 외래 키가 있는 테이블은 MUL로 표시한다고 함..)

ALTER TABLE users
    ADD CONSTRAINT FK_users_user_type_id FOREIGN KEY (user_type_id)
        REFERENCES user_types (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- 유저_렌탈회사 테이블
DROP TABLE IF EXISTS rental_companies;
CREATE TABLE rental_companies
(
    `id`               INT             NOT NULL    AUTO_INCREMENT COMMENT 'pk',
    `name`             VARCHAR(200)    NOT NULL    COMMENT '이름',
    `intro`            VARCHAR(200)    NOT NULL    COMMENT '유형',
    `address1`         VARCHAR(100)    NOT NULL    COMMENT '동/번지',
    `address2`         VARCHAR(100)    NOT NULL    COMMENT '상세주소',
    `state`            VARCHAR(100)    NOT NULL    COMMENT '주이름',
    `city`             VARCHAR(100)    NOT NULL    COMMENT '도시이름',
    `zip_code`         VARCHAR(200)    NOT NULL    COMMENT '우편번호',
    PRIMARY KEY (id)
);

-- 유저_렌탈회사직원 테이블
DROP TABLE IF EXISTS user_details;
CREATE TABLE user_details
(
    `id`             INT             NOT NULL    AUTO_INCREMENT COMMENT 'pk',
    `name`           VARCHAR(100)    NOT NULL    COMMENT '유저 이름',
    `phone_number`   VARCHAR(50)     NOT NULL    COMMENT '유저 전화번호',
    `position`       VARCHAR(50)     NOT NULL    COMMENT '유저 직급',
    `email`          VARCHAR(200)    NOT NULL    COMMENT '유저 이메일',
    `company_id`     INT             NOT NULL    COMMENT '유저타입 아이디', 
    PRIMARY KEY (id)
);

-- 렌탈회사직원과 렌탈회사 연결
ALTER TABLE user_details
    ADD CONSTRAINT FK_user_details_company_id FOREIGN KEY (company_id)
        REFERENCES rental_companies (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- 차량 테이블
DROP TABLE IF EXISTS cars;
CREATE TABLE cars
(
    `id`     INT             NOT NULL    AUTO_INCREMENT,
    `name`   VARCHAR(100)    NOT NULL    COMMENT '차량명',
    `brand`  VARCHAR(100)    NOT NULL    COMMENT '브랜드',
    PRIMARY KEY (id)
);

-- 요청 테이블
DROP TABLE IF EXISTS requests;
CREATE TABLE requests
(
    `id`               INT              NOT NULL    AUTO_INCREMENT,
    `car_id`           INT              NOT NULL    COMMENT '차량정보(FK)',
    `car_number`       VARCHAR(100)     NOT NULL    COMMENT '차량번호',
    `phone_number`     VARCHAR(100)     NOT NULL    COMMENT '핸드폰번호',
    `state`            VARCHAR(100)     NOT NULL    COMMENT '이용지역',
    `city`             VARCHAR(100)     NOT NULL    COMMENT '이용지역',
    `additional_info`  VARCHAR(1000)    NULL        COMMENT '추가요청사항',
    `drive_date`       TIMESTAMP        NULL        COMMENT '배차일자',
    `checkout_date`    TIMESTAMP        NULL        COMMENT '반납일자',
    `status`           INT              NOT NULL    DEFAULT 0     COMMENT '매칭 진행상태',
    `created_at`       TIMESTAMP        NOT NULL    Default NOW() COMMENT '요청일자',
    `removed_at`       TIMESTAMP        NULL        COMMENT '삭제일자',
    PRIMARY KEY (id)
);

ALTER TABLE requests
    ADD CONSTRAINT FK_requests_cars_id FOREIGN KEY (car_id)
        REFERENCES cars (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- 제안 테이블
DROP TABLE IF EXISTS suggestions;
CREATE TABLE suggestions
(
    `id`               INT             NOT NULL    AUTO_INCREMENT,
    `first_car_id`     INT             NOT NULL    COMMENT '제안차량1',
    `second_car_id`    INT             NULL        COMMENT '제안차량2',
    `additional_info`  VARCHAR(1000)   NULL        COMMENT '추가요청사항',
    `request_id`       INT             NOT NULL    COMMENT '요청 아이디',
    `user_id`          INT             NOT NULL    COMMENT '렌트카',
    `created_at`       TIMESTAMP       NOT NULL    Default NOW() COMMENT '요청일자',
    `removed_at`       TIMESTAMP       NULL        COMMENT '삭제일자',
    PRIMARY KEY (id)
);

ALTER TABLE suggestions
    ADD CONSTRAINT FK_suggestions_request_id FOREIGN KEY (request_id)
        REFERENCES requests (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE suggestions
    ADD CONSTRAINT FK_suggestions_user_id FOREIGN KEY (user_id)
        REFERENCES users (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE suggestions
    ADD CONSTRAINT FK_suggestions_first_car_id FOREIGN KEY (first_car_id)
        REFERENCES cars (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE suggestions
    ADD CONSTRAINT FK_suggestions_second_car_id FOREIGN KEY (second_car_id)
        REFERENCES cars (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

/*
+--------------+--------------+------+-----+---------+----------------+
| Field        | Type         | Null | Key | Default | Extra          |
+--------------+--------------+------+-----+---------+----------------+
| id           | int          | NO   | PRI | NULL    | auto_increment |
| name         | varchar(100) | NO   |     | NULL    |                |
| phone_number | varchar(50)  | NO   |     | NULL    |                |
| position     | varchar(50)  | NO   |     | NULL    |                |
| email        | varchar(200) | NO   |     | NULL    |                |
| company_id   | int          | NO   | MUL | NULL    |                |
+--------------+--------------+------+-----+---------+----------------+
*/
DROP TABLE IF EXISTS cars;
CREATE TABLE cars
(
    `id`     INT             NOT NULL    AUTO_INCREMENT, 
    `brand`  VARCHAR(100)    NOT NULL    COMMENT '브랜드', 
    `model`  VARCHAR(100)    NOT NULL    COMMENT '모델명', 
    PRIMARY KEY (id)
);


DROP TABLE IF EXISTS requests;
CREATE TABLE requests
(
    `id`               INT              NOT NULL    AUTO_INCREMENT, 
    `car_id`           INT              NOT NULL    COMMENT '차량정보(FK)', 
    `car_number`       VARCHAR(100)     NOT NULL    COMMENT '차량번호', 
    `phone_number`     VARCHAR(100)     NOT NULL    COMMENT '핸드폰번호', 
    `state`            VARCHAR(100)     NOT NULL    COMMENT '이용지역', 
    `city`             VARCHAR(100)     NOT NULL    COMMENT '이용지역', 
    `additional_info`  VARCHAR(1000)    NULL        COMMENT '추가요청사항', 
    `drive_date`       TIMESTAMP        NULL        COMMENT '배차일자', 
    `checkout_date`    TIMESTAMP        NULL        COMMENT '반납일자', 
    `status`           INT              NOT NULL    DEFAULT 0     COMMENT '매칭 진행상태', 
    `created_at`       TIMESTAMP        NOT NULL    Default NOW() COMMENT '요청일자',
    `removed_at`       TIMESTAMP        NULL        COMMENT '삭제일자', 
    PRIMARY KEY (id)
);

ALTER TABLE requests
    ADD CONSTRAINT FK_requests_car_id FOREIGN KEY (car_id)
        REFERENCES cars (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

DROP TABLE IF EXISTS suggestions;
CREATE TABLE suggestions
(
    `id`               INT             NOT NULL    AUTO_INCREMENT, 
    `first_car_id`     INT             NOT NULL    COMMENT '제안차량1', 
    `second_car_id`    INT             NULL        COMMENT '제안차량2', 
    `additional_info`  VARCHAR(1000)   NULL        COMMENT '추가요청사항', 
    `request_id`       INT             NOT NULL    COMMENT '요청 아이디', 
    `user_id`          INT             NOT NULL    COMMENT '렌트카', 
    `created_at`       TIMESTAMP       NOT NULL    Default NOW() COMMENT '요청일자', 
    `removed_at`       TIMESTAMP       NULL        COMMENT '삭제일자', 
    PRIMARY KEY (id)
);

ALTER TABLE suggestions
    ADD CONSTRAINT FK_suggestions_request_id FOREIGN KEY (request_id)
        REFERENCES requests (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE suggestions
    ADD CONSTRAINT FK_suggestions_user_id FOREIGN KEY (user_id)
        REFERENCES users (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE suggestions
    ADD CONSTRAINT FK_suggestions_first_car_id FOREIGN KEY (first_car_id)
        REFERENCES cars (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE suggestions
    ADD CONSTRAINT FK_suggestions_second_car_id FOREIGN KEY (second_car_id)
        REFERENCES cars (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

SET foreign_key_checks = 1;
