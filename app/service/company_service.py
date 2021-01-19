
class CompanyService:
    def __init__(self, company_dao):       
        self.company_dao = company_dao
        
    def get_company(self, company):
        company = self.company_dao.get_company(company)
        return company

    def get_all_companies(self):
        companies = self.company_dao.get_all_companies()
        return companies
