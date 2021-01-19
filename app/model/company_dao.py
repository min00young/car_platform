from sqlalchemy import text

class CompanyDao:
  def __init__(self, database):
      self.db = database

  def create_company(self, user, connection, trans):
    new_company_id = connection.execute(text("""
    INSERT INTO rental_companies (
        name,
        address1,
        address2,
        city,
        state,
        zip_code,
        intro
    ) VALUES (
        :companyname,
        :companyaddress1,
        :companyaddress2,
        :companycity,
        :companystate,
        :companyzipcode,
        :companyintro
    )
"""), user).lastrowid
    return new_company_id

  def get_company(self, id):
    row = self.db.execute(text("""    
      SELECT
          id,
          name,
          address1,
          address2,
          state,
          city
      FROM rental_companies
      WHERE id = :id
  """), {'id' : id}).fetchone()
    return row

  def get_all_companies(self):
    rows = self.db.execute(text("""    
      SELECT
          id,
          name,
          address1,
          address2,
          state,
          city
      FROM rental_companies
  """)).fetchall()

    return rows