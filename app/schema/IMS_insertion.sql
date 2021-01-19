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
(4, 'lee', 'lee123', 2, False),
(5, 'son', '12341234', 2, False);

/*
# users 테이블 removed_at 칼럼 값 수정가능여부 체크
UPDATE users
SET removed_at = '2020-12-20 20:01:11'
WHERE id = 4;
*/

-- rental_companies 테이블
INSERT INTO rental_companies 
(`id`,`name`,`intro`,`address1`,`address2`,`state`,`city`,`zip_code`)
VALUES 
(1, 'wecode', 'hello world!', 'Wework', '427 Teheran-ro', 'Gangnam-gu', 'Seoul', '06159'); 

-- user_details 테이블
INSERT INTO user_details 
(`id`,`name`,`phone_number`,`position`,`email`,`company_id`)
VALUES 
(1, '송은우', '010-1234-5678', 'CEO', 'song@wecode.co.kr', '1'),
(2, '신재훈', '010-4321-8765', 'director', 'shin@wecode.co.kr', '1'),
(3, '장규석', '010-1003-3463', 'developer', 'jang@wecode.co.kr', '1'),
(4, '이민영', '010-5717-6080', 'designer', 'lee@wecode.co.kr', '1');  

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
(`id`,`car_id`,`car_number`,`phone_number`,`state`,`city`)
VALUES
(1, 1,'15허2843','010-3018-4632','California', 'LA'),
(2, 8,'16호3523','010-6723-1162','Oregon', 'Portland'),
(3, 6,'13허2584','010-1218-5665','Illinoi', 'Chicago'),
(4, 3,'14호9235','010-3362-4234','New York', 'NYC'),
(5, 10,'12호7563','010-6713-1612','Washington', 'Seattle');

-- 추가 요청사항
UPDATE requests
SET 
additional_info = '멘솔냄새나는 차량으로 부탁드립니다'
WHERE id = 1;

-- 렌카쪽에서 제안들을 보고, 이 차로 하겠다, 라고 예약확정시 status = 1

-- 배차 하였을 시, drive_date & status 수정
UPDATE requests
SET 
drive_date = '2020-12-19 20:01:11', status = 2
WHERE id = 1;

-- 반납 하였을 시, checkout_date & status 수정
UPDATE requests
SET 
checkout_date = '2020-12-20 15:22:00', status = 3
WHERE id = 1;

/*
INSERT INTO requests
(`id`,`cars_id`,`car_number`,`phone_number`,`state`,`city`,`additional_info`,`drive_date`,`checkout_date`,`status`)
VALUES
(1, '1','11허2343','010-3018-4633','California', 'LA','멘솔냄새나는 차량으로 부탁드립니다','2020-12-19 20:01:11','2020-12-20 15:22:00', 3),
(1, '8','12호7563','010-6713-1612','Washington', 'Seattle','새차같은 렌트카 차량으로 부탁드립니다','2020-12-21 20:01:11','2020-12-25 14:12:00', 3),
(1, '6','13허2584','010-1218-5665','Illinoi', 'Chicago','2인분같은 1인분 차량으로 부탁드립니다','2020-12-20 20:01:11','2020-12-26 13:51:00', 3),
(1, '3','14호9235','010-3362-4234','New York', 'NYC','벤츠같은 아반떼로 부탁드립니다','2020-12-25 20:01:11','2020-12-27 12:11:00', 3);
*/

INSERT INTO suggestions
(`id`,`first_car_id`,`request_id`,`user_id`)
VALUES
(1, 1, 1, 1),
(2, 2, 2, 2),
(3, 3, 3, 3),
(4, 4, 4, 4),
(5, 5, 5, 5);

-- 두 번째 후보차량 모델을 제안할 때 
UPDATE suggestions
SET
second_car_id = 2
WHERE id = 1;

-- 추가 제안정보 입력
UPDATE suggestions
SET
additional_info = '멘솔냄새나는 차량으로 모시겠습니다~'
WHERE id = 1;