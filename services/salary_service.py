from datetime import date
from sqlalchemy.orm import Session
from models.salary_structure_model import SalaryStructure
from models.payroll_model import Payroll

def create_salary_structure(db: Session, payload):
    structure = SalaryStructure(**payload.model_dump())
    db.add(structure)
    db.commit()
    db.refresh(structure)
    return structure

def get_salary_structure(db: Session, employee_id: int):
    return (db.query(SalaryStructure).filter(SalaryStructure.employee_id == employee_id).first())

def generate_payroll(db: Session, employee_id: int):
    salary = get_salary_structure(db, employee_id)
    if not salary:
        return None
    gross_salary = (salary.basic_salary + salary.hra + salary.allowances)
    net_salary = (gross_salary - salary.deductions)
    payroll = Payroll(employee_id=employee_id, payroll_month=date.today(), gross_salary=gross_salary, total_deductions=salary.deductions, net_salary=net_salary)
    db.add(payroll)
    db.commit()
    db.refresh(payroll)
    return payroll

def payroll_history(db: Session, employee_id: int):
    return (db.query(Payroll).filter(Payroll.employee_id == employee_id).all())

def payroll_statistics(db: Session):
    payrolls = db.query(Payroll).all()
    total_payroll = sum(
        p.net_salary
        for p in payrolls)
    return {"total_records":len(payrolls), "total_payroll":total_payroll}