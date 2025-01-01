# imports 
import decimal
from io import BytesIO
import requests
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render , redirect
from .models import User_reg , Transactions , Supports
from django.contrib.auth import login , logout , authenticate 
from django.contrib.auth.models import User
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime

# homepage 
def homepage(request):
    return render(request,'./homepage.html',)

# User profile page
def User_profile(request):
    user = User_reg.objects.get(user=request.user)

    context = {
        "User" : user ,
    }
    
    return render(request,'./user.html',context)

# Login page
def loginpg(request):
    if request.method == 'POST':
        username_user = str(request.POST['name'])
        password_user = str(request.POST['password'])
        user = authenticate(username=username_user, password=password_user)
        if user :
            login(request,user)
            messages.success(request,"You are now logged in")
            return redirect("Dashboard")
        else:
            messages.error(request,"invalid Credentials")
            return redirect("login page")
    
    return render(request,"./loginpg.html")

# customer support page
def support(request):
    if request.method == 'POST':
        Name = request.POST['name']
        email = request.POST['email']
        issue = request.POST['issue']
        support = Supports.objects.create(name=Name,email=email,issue=issue)
        support.save()
    return render(request,'./support.html')

# Transaction page
def transaction(request):
    if request.user.is_anonymous: 
        messages.error(request,"login in order to access Transaction")
        return redirect("login page")
    user = User_reg.objects.get(user=request.user)
    transactions = Transactions.objects.filter(user=user)
    context={
        "User" : user,
        "Transactions" : transactions,
    }
    if request.method=='POST':
        user_profile = User_reg.objects.get(user=request.user)
        start_date = request.POST.get("start_date","2024-01-01")
        end_date = request.POST.get("end_date","2024-12-31")

        pdfmetrics.registerFont(TTFont('ArialUnicodeMS', 'C:\\Windows\\Fonts\\ARIALUNI.TTF'))

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="Bank-Statement.pdf"'
        
        
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

    # Add Bank Header with logo
        styles = getSampleStyleSheet()
        styles["Normal"].fontName = "ArialUnicodeMS"
        styles["Heading2"].fontName = "ArialUnicodeMS"
        logo_url = "https://clipartcraft.com/images/bank-logo-icon-9.png"  # Replace with the actual logo URL
        try:
            logo_response = requests.get(logo_url, stream=True)
            if logo_response.status_code == 200:
                logo_image = Image(BytesIO(logo_response.content), width=50, height=50)
                elements.append(logo_image)
            else:
                print("Failed to fetch the logo")
        except Exception as e:
            print(f"Error fetching logo: {e}")

        header = Paragraph("<b>CHD Bank</b><br/>Bank Statement", styles["Title"])
        elements.append(header)

        account_info = Paragraph(
            f"Account Number: <b>{user_profile.account_number}</b><br/>"
            f"Date : {start_date} to {end_date}",
            styles["Normal"]
        )
        elements.append(account_info)
        elements.append(Spacer(1, 12))

        # Add transaction history header
        elements.append(Paragraph("<b>Transaction History:</b>", styles["Heading2"]))

        # Fetch transactions within the date range
        transactions = Transactions.objects.filter(
            user=user_profile,
            timestamp__date__gte=datetime.strptime(start_date, "%Y-%m-%d").date(),
            timestamp__date__lte=datetime.strptime(end_date, "%Y-%m-%d").date()
        ).order_by("-timestamp")

        # Create table data
        data = [["Date", "Transaction Type", "Amount", "Recipient Account"]]
        for transaction in transactions:
            data.append([
                transaction.timestamp.date().strftime("%Y-%m-%d"),
                transaction.transaction_type,
                f"\u20B9{transaction.amount:,.2f}",
                transaction.receiptent_no or "N/A"
            ])

        # Create Table Style
        table = Table(data, colWidths=[100, 150, 100, 150])
        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),  
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),      
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),             
                ("FONTNAME", (0, 0), (-1, -1), "ArialUnicodeMS"),   
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),           
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),    
                ("GRID", (0, 0), (-1, -1), 1, colors.black),       
            ])
        )

        elements.append(table)

        # Add Footer
        def footer(canvas, doc):
            canvas.saveState()
            footer_text = f"CHD Bank \u00a9 {datetime.now().year} | Page {doc.page}"
            canvas.drawString(100, 30, footer_text)
            canvas.restoreState()

        # Build the PDF
        doc.build(elements, onFirstPage=footer, onLaterPages=footer)

        return response

    return render(request,'./transaction.html',context)

# Sign-up page
def sign_up(request):

    if request.method == 'POST':
        username = request.POST["username"]
        Email = request.POST["email"]
        password = request.POST['password']
        ac_number = request.POST['account_number']
        phone = request.POST['phone']
        ac_type = request.POST['account-type']
        gender = request.POST['Gender']
        address = request.POST['address']
        Photo = request.FILES['photo']
        pan = request.POST['pan']
        Aadhaar = request.POST['aadhaar']
        dob = request.POST['dob']
        
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username exists")
            return redirect("Sign-up")
        else:
                user = User.objects.create(username=username,password=password)
                User_reg.objects.create(user=user,account_number=ac_number,phone=phone,email=Email,account_type=ac_type,gender=gender,image=Photo,address=address,Pan=pan,aadhaar=Aadhaar,DoB=dob)
                login(request,user)
                messages.success(request,"Your account was successfully created!!")
                return redirect("Dashboard")
    
    return render(request,"./signup.html")

# DashBoard page
def dashboard(request):
    if request.user.is_anonymous: 
        messages.error(request,"login in order to access Dashboard")
        return redirect("login page")

    user_profile = User_reg.objects.get(user=request.user)
    funds = Transactions.objects.filter(user=user_profile)[4:]

    label = ['Withdrawal','Deposit','Transfer']
    value = [
        Transactions.objects.filter(user=user_profile,transaction_type="WITHDRAW").count(),
        Transactions.objects.filter(user=user_profile,transaction_type="DEPOSIT").count(),
        Transactions.objects.filter(user=user_profile,transaction_type="TRANSFER").count()
    ]

    assert len(label) == len(value)
    assert all(isinstance(v, (int, float)) for v in value)

    plt.figure(figsize=(4, 4))
    plt.pie(value, labels=label, autopct='%1.1f%%', startangle=140, colors=["red", "green", "blue"])

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()


    context = {
        "User" : user_profile,
        "Transactions":funds,
        "chart": image_base64,
    }


    return render(request,"./dashboard.html",context)

# Deposit page
def deposit(request):
    if request.method=="POST":
        amount = float(request.POST["deposit-amount"])
        account = request.POST["account-number"]
        user = User_reg.objects.get(account_number=account)
        user.balance += decimal.Decimal(amount)
        user.save()

        Transactions.objects.create(user=user,transaction_type="DEPOSIT",amount=amount,receiptent_no="Self",receiptent=amount,about="Deposit")
        messages.success(request,f"Deposit of {amount} is Successful !!")
        return redirect("Dashboard")

    return render(request,"./deposit.html")

# Withdrawal page
def withdrawal(request):
    if request.method=="POST":
        amount = decimal.Decimal(request.POST["withdrawal-amount"])
        account = request.POST["account-number"]
        user = User_reg.objects.get(account_number = account)

        if user.balance < amount :
            messages.error(request,"Balance Low")
            return redirect("Dashboard")
        
        else:
            user.balance -= amount
            user.save()

        Transactions.objects.create(user=user,transaction_type="WITHDRAW",amount=amount,receiptent_no="Self",receiptent=amount,about="WithDraw")
        messages.success(request,f"Withdrawal of {amount} is Successful !!")
        return redirect("Dashboard")
    return render(request,"./Withdrawal.html")

# Transfer page
def Transfer(request):
    if request.method == "POST":
        user_account = request.POST["user-account"]
        receiptent_ac = request.POST["Receiptent-account"]
        amount = decimal.Decimal(request.POST["transfer-amount"])
        discription = request.POST["transaction-description"]
        user = User_reg.objects.get(user=request.user)
        
        try:
            receiptent_transfer = User_reg.objects.get(account_number=receiptent_ac)
        except User_reg.DoesNotExist:
            messages.error(request,"User does not exist")
            return redirect("Transfer")
        
        if amount > user.balance:
            messages.error(request,"Balance insufficient")
            return redirect("Transfer")
        
        else:
            user.balance -= amount
            receiptent_transfer.balance += amount
            user.save()
            receiptent_transfer.save()
            

        Transactions.objects.create(user=user,transaction_type="TRANSFER",amount=amount,receiptent_no=receiptent_ac,receiptent=receiptent_transfer.balance,about=discription)
        messages.success(request,f"{amount} is transferred to {receiptent_transfer.user.username}")
        return redirect("Dashboard")
    return render(request,"./transfer.html")


def change_password(request):
    if request.method == 'POST':
        user_name = str(request.POST.get('name'))
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        
        if password != confirm_password :
            messages.error(request, "Passwords do not match")
            return redirect('Change Password')
        
        elif not User.objects.filter(username=user_name):
            messages.error(request, "Enter correct name")
            return redirect('Change Password')
        
        else:
            user = User.objects.get(username=user_name)
            user.set_password(password)
            user.save()
            messages.success(request, "Password changed successfully")
            return redirect('login page')
    
    return render(request, "./password.html")

# Log-out function 
def user_logout(request):
    logout(request)
    messages.success(request,"You are now logged out")
    return redirect('login page')