from sqlalchemy import text

class UserDao:
    def __init__(self, database):
        self.db = database

    def create_company(self, user, connection, trans):
        connection.execute(text("""
        INSERT INTO users (
            login_id,
            password,
            user_type_id,
            activation
        ) VALUES (
            :userid,
            :userpassword,
            :user_type_id,
            :activation
        )
    """), user)

        connection.execute(text("""
            INSERT INTO user_details (
                name,
                phone_number,
                position,
                email,
                company_id
            ) VALUES (
                :username,
                :usernumber,
                :userposition,
                :useremail,
                :company_id
            )
        """), user)
        return 'success'

    def create_employee(self, user, connection, trans):
        connection.execute(text("""
            INSERT INTO users (
                login_id,
                password,
                user_type_id,
                activation
            ) VALUES (
                :userid,
                :userpassword,
                :user_type_id,
                :activation
            )
        """), user)

        connection.execute(text("""
            INSERT INTO user_details (
                name,
                phone_number,
                position,
                email,
                company_id
            ) VALUES (
                :username,
                :usernumber,
                :userposition,
                :useremail,
                :company_id
            )
        """), user)

        return 'success'

    def get_user(self, login_id):
        result = self.db.execute(text("""
            SELECT
                id,
                login_id,
                password,
                user_type_id,
                activation,
                created_at,
                updated_at,
                removed_at
            FROM users
            WHERE login_id = :login_id
        """), {'login_id' : login_id}).fetchone()

        return result

    def search_company(self, search_company):
        rows = self.db.execute(text("""    
            SELECT
                name,
                address1,
                address2,
                state,
                city
            FROM rental_companies
            WHERE name = :search_company
        """), {'search_company' : search_company}).fetchall()

        return rows
