from django.shortcuts import render,HttpResponse, redirect
from .models import Account
from .forms import AccountForm
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def home(request):
    return render(request,'index.html')

def create(request):
    form = AccountForm()
    if request.method == "POST":
        form = AccountForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            print('successfull')
            
            receiver_email = form.data['email']
            data = Account.objects.get(email= receiver_email)
            acc = data.account_no
            try:
                send_mail(
                    'Thanks for Registration', # subject
                    f'Thank you for registrating with our proBank. We are excited to have you on board! Your account number is {acc}, \n thank you \n regards \n proBank manager', #body
                    settings.EMAIL_HOST_USER,
                    [receiver_email],
                    fail_silently=False,
                )
                print('Mail sent')
                return redirect('home')
            
            except Exception as e:
                return HttpResponse(f'Error sending email: {e}')
            
    return render(request,'create.html', {'form':form})


def pin(request):
    if request.method == "POST":
        acc = request.POST.get('acc')
        mobile = request.POST.get('phone')
        pin = int(request.POST.get('pin'))
        cpin = int(request.POST.get('cpin'))
        print(acc,mobile,pin,cpin)
        try:
            account = Account.objects.get(account_no=acc)
        except:
            return HttpResponse("Account Not Found :(")
        finally:
            print('Exception is Handled')
        if account.Mobile_number == int(mobile):
            if pin == cpin:
                pin += 111
                account.pin = pin
                account.save()
                receiver_email = account.email
                print('PIN ADDED')
                try:
                    send_mail(
                        'Pin has Successfully Added', # subject
                        f'Horraay! PIN has been generated, \n Thank you, \n Regards, \n proBank manager.', #body
                        settings.EMAIL_HOST_USER,
                        [receiver_email],
                        fail_silently=False,
                    )
                    print('Mail sent')
                    return redirect('home')
            
                except Exception as e:
                    return HttpResponse(f'Error sending email: {e}')
            else:
                print("BOTH PINS DOESN'T MATCH ")
        else:
            print('MOBILE NUMBER NOT FOUND :(')
    
    return render(request,'pin.html')



def balance(request):
    bal = 0
    flag = False
    if request.method ==  "POST":
        flag = True
        acc= request.POST.get('acc')
        pin = int(request.POST.get('pin'))
        print(acc,pin)
        try:
            account = Account.objects.get(account_no= acc)
            # print(account)
        except:
            return HttpResponse('Entered Account Number is Not Found :(')
        encpin = account.pin - 111
        if pin == encpin:
            print('Pin Matched')
            bal = account.balance
            receiver_email = account.email
            try:
                send_mail(
                    'Balance Enquiry', # subject
                    f'You Have Enquired the Balance of You Account.\n Tha Balance is RS. {bal}/- \n Thank you, \n Regards, \n proBank manager.', #body
                    settings.EMAIL_HOST_USER,
                    [receiver_email],
                    fail_silently=False,
                )
                print('Mail sent')
                # return redirect('home')
            
            except Exception as e:
                return HttpResponse(f'Error sending email: {e}')       
        else:
            return HttpResponse('Enter Valid Pin')   
    return render(request, 'balance.html', {'bal': bal,'flag':flag})


def deposit(request):
    if request.method == "POST":
        acc = request.POST.get('acc')
        phone = int(request.POST.get('mobile'))
        amt = int(request.POST.get('amt'))
        
        try:
            account = Account.objects.get(account_no=acc)
        except:
            return HttpResponse('ACCOUNT NOT FOUND')
        finally:
            print('Exception is Handled')
        if account.Mobile_number == phone:
            print('Account is Verified')
            if amt >= 100 and amt <= 10000:
                account.balance += amt
                account.save()
                receiver_email = account.email
                try:
                    send_mail(
                        'Deposited Succesfully', # subject
                        f'Credited Amount in Your Account {acc} is RS.{amt}/- \n Total Balance in Your Account{acc} is RS.{account.balance}/- \n Thank you, \n Regards, \n proBank manager.', #body
                        settings.EMAIL_HOST_USER,
                        [receiver_email],
                        fail_silently=False,
                    )
                    print('Mail sent')
                    return redirect('home')
            
                except Exception as e:
                    return HttpResponse(f'Error sending email: {e}')
            else:
                return HttpResponse('Amount should be in a range of 100 to 10000 ')
        else:
            return HttpResponse('Entered Mobile Number is Not Valid, Kindly Enter a Valid Mobile Number')
    
    return render(request,'deposit.html')


def withdrawl(request):
    if request.method == "POST":
        acc = request.POST.get('acc')
        pin = int(request.POST.get('pin'))
        amt =  int(request.POST.get('amt'))
        print(acc,pin,amt)
        try:
            account = Account.objects.get(account_no= acc)
        except:
            return HttpResponse('Account Not Found :(')
        finally:
            print('Exception Handled')    
        check_pin = account.pin - 111
        if check_pin == pin:
            print('Pin Matched')   
            if account.balance > amt and amt <=10000 and amt >=500:
                account.balance -= amt
                account.save()
                receiver_email = account.email
                try:
                    send_mail(
                        'Withdraw Succesfull ', # subject
                        f'Debited Amount from Your Account {acc} is RS.{amt}/- \n Total Balance in Your Account{acc} is RS.{account.balance}/- \n Thank you, \n Regards, \n proBank manager.', #body
                        settings.EMAIL_HOST_USER,
                        [receiver_email],
                        fail_silently=False,
                    )
                    print('Mail sent')
                    return redirect('home')
            
                except Exception as e:
                    return HttpResponse(f'Error sending email: {e}')
            else:
                return HttpResponse('Please Enter Valid Amount')
        else:
            return HttpResponse('Please Enter Valid Pin')
    return render(request,'withdrawl.html')


def acc_transfer(request):
    if request.method == 'POST':
        sender_acc = request.POST.get('sender_acc')
        receiver_acc = request.POST.get('receiver_acc')
        pin = int(request.POST.get('pin'))
        amt = int(request.POST.get('amt'))
        
        try:
            sender_account = Account.objects.get(account_no= sender_acc)
        except:
            return HttpResponse('Sender_account is Not Found :(')
        finally:
            print('Exception Handled ')
        try:
            receiver_account = Account.objects.get(account_no=receiver_acc)
        except:
            return HttpResponse('Receiver_account is Not Found :(')
        finally:
            print('Exception handled')
        encpin = sender_account.pin - 111
        if pin == encpin:
            print('Pin Matched :)')
            if sender_account.balance >= amt:
                sender_account.balance -= amt
                receiver_account.balance += amt
                sender_account.save()
                receiver_account.save()
                receiver_email = receiver_account.email
                sender_email = sender_account.email
                try:
                    send_mail(
                        'Account Transfer Succesfull ', # subject
                        f'Debited Amount from Your Account {sender_acc} to {receiver_acc} is RS.{amt}/-  \n Total Balance in Your Account{sender_acc} is RS.{sender_account.balance}/- \n Thank you, \n Regards, \n proBank manager.', #body
                        settings.EMAIL_HOST_USER,
                        [sender_email],
                        fail_silently=False,
                    )
                    print('Mail sent')
                    return redirect('home')
            
                except Exception as e:
                    return HttpResponse(f'Error sending email: {e}')
                try:
                    send_mail(
                        'Account Transfer Succesfull ', # subject
                        f'Credited Amount In Your Account {receiver_acc} from {sender_acc} is RS.{amt}/-  \n Total Balance in Your Account {receiver_acc} is RS.{receiver_account.balance}/- \n Thank you, \n Regards, \n proBank manager.', #body
                        settings.EMAIL_HOST_USER,
                        [receiver_email],
                        fail_silently=False,
                    )
                    print('Mail sent')
                    return redirect('home')
            
                except Exception as e:
                    return HttpResponse(f'Error sending email: {e}')
            else:
                return HttpResponse('Insufficient Balance :(')
        else:
            return HttpResponse('Incorrect PIN ')
    
    return render(request,'acc_transfer.html')