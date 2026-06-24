try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    REPORTLAB_AVAILABLE = True
except ModuleNotFoundError:
    SimpleDocTemplate = Paragraph = Spacer = None
    getSampleStyleSheet = None
    REPORTLAB_AVAILABLE = False


def generate_payslip(file_path, payroll):
    if not REPORTLAB_AVAILABLE:
        raise RuntimeError("reportlab is required to generate payslips")

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    content = []
    content.append(Paragraph("Employee Payslip", styles["Title"]))
    content.append(Spacer(1, 20))
    content.append(Paragraph(f"Employee ID: {payroll.employee_id}", styles["Normal"]))
    content.append(Paragraph(f"Gross Salary: {payroll.gross_salary}", styles["Normal"]))
    content.append(Paragraph(f"Deductions: {payroll.total_deductions}", styles["Normal"]))
    content.append(Paragraph(f"Net Salary: {payroll.net_salary}", styles["Normal"]))
    doc.build(content)