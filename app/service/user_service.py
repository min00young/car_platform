import bcrypt, jwt, re

from flask      import jsonify
from exceptions import ValidationError, LoginError

class UserService:
    def __init__(self, user_dao, company_dao, config, database):       
        self.user_dao    = user_dao
        self.company_dao = company_dao        
        self.config      = config
        self.db          = database
        
    def create_new_company(self, new_company):
        #아이디유효성검사(4~12자, 영어대소문자/숫자/사용가능)
        userid_validation = re.compile(r'^[a-zA-Z0-9]{4,20}$')
        if not re.match(userid_validation, new_company['userid']):
            raise ValidationError('USER_ID')

        #비밀번호 유효성검사(최소 8자, 하나의 문자, 하나의 숫자 및 하나의 특수 문자 포함)
        password_validation = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')
        if not re.match(password_validation, new_company['userpassword']):
            raise ValidationError('PASSWORD')

        #핸드폰번호 유효성검사(2,3자리 - 3,4자리 - 4자리)
        phone_validation = re.compile(r'\d{2,3}-\d{3,4}-\d{4}')
        if not re.match(phone_validation, new_company['usernumber']):
            raise ValidationError('PHONE_NUMBER')

        #이메일 유효성검사(@, . 포함여부)
        email_validation = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not re.match(email_validation, new_company['useremail']):
            raise ValidationError('EMAIL')
        
        #비밀번호 암호화
        new_company['userpassword'] = bcrypt.hashpw(  
            new_company['userpassword'].encode('UTF-8'),
            bcrypt.gensalt()
        )
        try:
            connection = self.db.connect()
            trans = connection.begin()

            new_company_id = self.company_dao.create_company(new_company, connection, trans)
            new_company['company_id'] = new_company_id
            result = self.user_dao.create_company(new_company, connection, trans)

            trans.commit()
            return result

        except: 
            trans.rollback()
            return 'Database Rollback'

    def create_new_employee(self, new_employee):
        #아이디유효성검사(6~20자, 영어대소문자/숫자/사용가능)
        userid_validation = re.compile(r'^[a-zA-Z0-9]{6,20}$')
        if not re.match(userid_validation, new_employee['userid']):
             raise ValidationError('USER_ID')

        #비밀번호 유효성검사(최소 8 자, 최대 25자 최소 하나의 문자, 하나의 숫자 및 하나의 특수 문자 포함)
        password_validation = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,25}$')
        if not re.match(password_validation, new_employee['userpassword']):
            raise ValidationError('PASSWORD')

        #핸드폰번호 유효성검사(2,3자리 - 3,4자리 - 4자리)
        phone_validation = re.compile(r'\d{2,3}-\d{3,4}-\d{4}')
        if not re.match(phone_validation, new_employee['usernumber']):
            raise ValidationError('PHONE_NUMBER')

        #이메일 유효성검사(@, . 포함여부)
        email_validation = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not re.match(email_validation, new_employee['useremail']):
            raise ValidationError('EMAIL')

        #비밀번호 암호화
        new_employee['userpassword'] = bcrypt.hashpw(  
            new_employee['userpassword'].encode('utf-8'),
            bcrypt.gensalt()
        )
        try:
            connection = self.db.connect()
            trans = connection.begin()

            new_employee_id = self.user_dao.create_employee(new_employee, connection, trans)
            trans.commit()
            return new_employee_id

        except: 
            trans.rollback()
            raise

    def check_id(self, check_id):      
        check_id = self.user_dao.get_user(check_id)
        
        if check_id == None:
            return True
        return False

    def login(self, id, password):      
        user = self.user_dao.get_user(id)
        
        # 유저 존재여부 확인
        if not user:
            raise LoginError('ID')

        # 비밀번호 확인
        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            raise LoginError('PASSWORD')

        # 탈퇴여부 확인
        if user['removed_at']:
            raise LoginError('REMOVED')

        # 활성화여부 확인
        if user['activation'] != 1:
            raise LoginError('DEACTIVATE')

        # 로그인 성공
        token = jwt.encode({'id': user['id']}, self.config.SECRET_KEY, algorithm=self.config.JWT_ALGORITHM).decode('utf-8')
        return {'token': token}
