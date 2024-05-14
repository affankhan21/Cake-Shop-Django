from django.shortcuts import render,redirect
from django.http import HttpResponse
from AdminApp.models import Category,Cake
from UserApp.models import UserInfo,MyCart,Payment,Status,Order_Master
from datetime import datetime

def home(request):
    cats = Category.objects.all()
    cakes = Cake.objects.all()
    return render(request,"homepage.html",{"cats":cats,"cakes":cakes})

def viewCakes(request,cid):
    cats = Category.objects.all()
    category = Category.objects.get(id=cid)
    cakes = Cake.objects.filter(category=category)
    return render(request,"homepage.html",{"cats":cats,"cakes":cakes})


def ViewDetails(request,id):
    pass
    if(request.method == "GET"):
        cats = Category.objects.all()
        cake = Cake.objects.get(id=id)
        return render(request,"ViewDetails.html",{"cats":cats,"cake":cake})
    else:
        #User is logged in
        if "uname" in request.session:
            uname = request.session["uname"]
            user = UserInfo.objects.get(username=uname)
            cake = Cake.objects.get(id=request.POST["cake_id"])
            status = Status.objects.get(status_name='Cart')
            qty = request.POST["qty"]
            #check if item already present in Cart
            try:
                item = MyCart.objects.get(user=user,cake=cake,status=status)
            except:
                #We can insert the item in cart
                item = MyCart(user=user,cake=cake,qty=qty,status=status)
                item.save()            
            return redirect(showAllCartItems)            
        else:
            return redirect(login)

def showAllCartItems(request):
    pass
    if(request.method == "GET"):
        if "uname" in request.session:
            uname = request.session["uname"]
            user = UserInfo.objects.get(username=uname)
            status = Status.objects.get(status_name='Cart')
            items = MyCart.objects.filter(user=user,status=status)            
            cats = Category.objects.all()
            total = 0
            for item in items:
                total += item.cake.price * item.qty
            request.session["total"]=total
            return render(request,"ShowAllCartItems.html",{"items":items,"cats":cats})
        else:
            return redirect(login)
    else:
        action = request.POST["action"]
        id = request.POST["item_id"]
        item = MyCart.objects.get(id=id)
        if action == "delete":            
            item.delete()
        else:
            qty = request.POST["qty"]
            item.qty = qty
            item.save()
        return redirect(showAllCartItems)

def login(request):
    if(request.method=="GET"):
        return render(request,"login.html",{})
    else:        
        username = request.POST["uname"]
        password = request.POST["pwd"]
        try:
            user = UserInfo.objects.get(username = username,password =password)            
        except:
            #Invalid credentials
            return redirect(login)
        else:
            request.session["uname"]=username            
            return redirect(home)


def register(request):
    if(request.method=="GET"):
        return render(request,"register.html",{})
    else:        
        username = request.POST["uname"]
        password = request.POST["pwd"]
        email = request.POST["email"]
        try:            
            user = UserInfo.objects.get(username = username)
        except:
            #If match not found, then this user is new user
            #So we can create user account
            user = UserInfo(username=username,password=password,email=email)
            user.save()
            return redirect(login)
        else:
            #This user already exists
            return redirect(register)
            
    
def logout(request):
    request.session.clear()
    return redirect(home)

            
def makepayment(request):
    if request.method == "GET":
        return render(request,"makepayment.html",{})
    else:
        card_no = request.POST["card_no"]
        cvv = request.POST["cvv"]
        expiry = request.POST["expiry"]
        #check if valid
        try:
            user = Payment.objects.get(card_no=card_no,cvv=cvv,expiry=expiry)
        except:
            return redirect(makepayment)
        else:
            #Proceed to make payment
            amount = request.session["total"]
            if(amount <  user.balance):
                user.balance -= amount
                owner =Payment.objects.get(card_no='22222',cvv='5678',expiry='12/2030') 
                owner.balance += amount
                owner.save()
                user.save()
                #Insert record in order_master
                uname = request.session["uname"]
                user = UserInfo.objects.get(username=uname)
                order = Order_Master(date_of_order=datetime.now(),amount = amount,user = user)
                order.save()
                #Modify the status of cart items
                status = Status.objects.get(status_name='Cart')
                items = MyCart.objects.filter(user=user,status=status)    
                status1 = Status.objects.get(status_name='Order')
                for item in items:
                    item.status = status1
                    item.order_id = order
                    item.save()
            else:
                return HttpResponse("Insufficient balance")
            return redirect(home)
        
                
def MyOrders(request):
    user = UserInfo.objects.get(username = request.session["uname"])
    orders = Order_Master.objects.filter(user=user)
 
    items = {}

    for order in orders:
        items[order]=MyCart.objects.filter(order_id = order,user=user)

    return render(request,"MyOrder.html",{"items":items})



