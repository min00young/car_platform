-- user_types 테이블
INSERT INTO user_types 
(`id`,`name`)
VALUES 
(1,'company'), 
(2,'employee');

-- users 테이블
INSERT INTO users 
(`id`,`login_id`,`password`,`user_type_id`, `activation`)
VALUES 
(1, 'song', 'song123', 1, True),
(2, 'shin', 'shin123', 2, False),
(3, 'jang', 'jang123', 2, False),
(4, 'lee', 'lee123', 2, False);

-- rental_companies 테이블
INSERT INTO rental_companies 
(`id`,`name`,`intro`,`address1`,`address2`,`state`,`city`,`zip_code`)
VALUES 
(1, 'wecode', 'hello world!', 'Wework', '427 Teheran-ro', 'Gangnam-gu', 'Seoul', '06159'),
(2, 'rencar', 'hello world!', 'rencar', '100 Pennsylvania Avenue', 'NY', 'NY', '06345');

-- user_details 테이블
INSERT INTO user_details 
(`id`,`name`,`phone_number`,`position`,`email`,`company_id`)
VALUES
(1, '송은우', '010-1234-5678', 'CEO', 'song@wecode.co.kr', 1),
(2, '신재훈', '010-4321-8765', 'director', 'shin@wecode.co.kr', 1),
(3, '장규석', '010-1003-3463', 'developer', 'jang@wecode.co.kr', 1),
(4, '이민영', '010-5717-6080', 'designer', 'lee@wecode.co.kr', 1);

-- 차량 테이블
INSERT INTO cars
(`id`,`brand`,`model`)
VALUES
(1, '현대',   '소나타'),
(2, '현대',   '그렌져'),
(3, '현대',   '아반떼'),
(4, '현대',   '코나'),
(5, '현대',   '싼타페'),
(6, '기아',   'K3'),
(7, '기아',   'K5'),
(8, '기아',   'K7'),
(9, '기아',   '레이'),
(10, '기아',   '스팅어'),
(11, '아우디',  'A3'),
(12, '아우디',  'A4'),
(13, '아우디',  'A6'),
(14, '아우디',  'Q3'),
(15, '아우디',  'R8'),
(16, 'BMW',   'X1'),
(17, 'BMW',   'M3'),
(18, 'BMW',   'M5'),
(19, '벤츠',   'C클래스'),
(20, '벤츠',   'E클래스'),
(21, '벤츠',   'S클래스'),
(22, '포르쉐',  '911'),
(23, '포르쉐', '카이엔');

-- 최소조건의 요청
INSERT INTO requests
(`id`,`car_id`,`car_number`,`phone_number`,`state`,`city`, `status`)
VALUES

( 1,  3, '111가1111','010-1111-1111','California', 'LA', 0),
( 2,  7, '222가2222','010-1111-1111','California', 'LA', 0),
( 3,  3, '111가1111','010-1111-1111','California', 'LA', 1),
( 4,  7, '222가2222','010-1111-1111','California', 'LA', 1),
( 5,  3, '222가2222','010-1111-1111','California', 'LA', 2),
( 6,  7, '222가2222','010-1111-1111','California', 'LA', 2),
( 7,  3, '111가1111','010-1111-1111','California', 'LA', 3),
( 8,  7, '222가2222','010-1111-1111','California', 'LA', 3);

INSERT INTO suggestions
(`first_car_id`, `second_car_id`, `request_id`,`user_id`)
VALUES
(3, 7, 1, 1),
(3, 7, 2, 1),
(3, 7, 3, 1),
(3, 7, 4, 1),
(3, 7, 5, 1),
(3, 7, 6, 1),
(3, 7, 7, 1),
(3, 7, 8, 1);
