from django.shortcuts import render,redirect,get_object_or_404
from jobs.models import Jobs,Sectors,Applications,Profile,Notification
from jobs.forms import JobForm,ProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import send_mail

from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
# Create your views here.

#custom decorator
def admin_permission(fun):
    def wrapper(request,*args,**kwargs):
        if request.user.is_superuser:
            return fun(request,*args,**kwargs)
        else:
            messages.error(request,"Permission denied!")
            return redirect("all_jobs")
    return wrapper

def home(request):
    return render(request,'home.html')

@login_required
def allJobs(request, sector=None):
    if sector:
        job_posts = Jobs.objects.select_related("sector").filter(sector_id=sector,is_active=True)
    else:
        job_posts = Jobs.objects.select_related("sector").filter(is_active=True)
    for job in job_posts:
        job.has_applied = Applications.objects.filter(job=job,user=request.user).exists()
    return render(request, "all-jobs.html",{"jobs": job_posts}) 

def jobDetail(request, job_id): #used optimization: selected_related
    job = get_object_or_404(Jobs.objects.select_related("sector"),id=job_id) #404 insead of exception
    has_applied = Applications.objects.filter(job_id=job_id, user_id=request.user.id).exists()
    return render(request,"job-detail.html",{"job": job,"has_applied": has_applied})

@admin_permission
def addJob(request):
    if request.POST:
        form=JobForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("all_jobs")
        else:
            print("Not valid form",form.errors)
    else:
        form=JobForm()
    return render(request,"add-jobs.html",{"form":form})

def updateJob(request, job_id):
    try:
        job = Jobs.objects.get(id=job_id)
        if request.method == "POST":
            form = JobForm(request.POST, instance=job)
            if form.is_valid():
                form.save()
                messages.success(request, "Job updated successfully!")
                return redirect("job_detail", job_id)
        else:
            form = JobForm(instance=job)
        return render(request, "update-job.html", {"form": form})
    except Jobs.DoesNotExist:
        messages.error(request, "Job not found!")
        return redirect("all_jobs")

@login_required(login_url="login")
def applyJob(request, job_id):
    job = get_object_or_404(Jobs, id=job_id)
    if request.method == "POST":
        resume = request.FILES.get("resume")
        Applications.objects.create(user=request.user,job=job,resume=resume)
        messages.success(request,"Application submitted successfully!")
        return redirect("all_jobs")
    return render(request,"apply-job.html",{"job": job})

def signIn(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if request.user.is_superuser:
                auth.login(request,user)
                return redirect('admin_dashboard')
            else:
                auth.login(request,user)
                return redirect('user_dashboard')
        else:
            messages.error(request,'Invalid username or password!')
            return redirect('login')
    return render(request,'login.html')

def signUp(request):
    if request.method=="POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=email).exists():
            messages.info(request,'User already exist! Please login!')
            return redirect('login')
        else:
            user=User.objects.create_user(username=email,first_name=first_name,last_name=last_name,email=email,password=password)
            Profile.objects.create(user=user)
            messages.success(request,'Welcome to JobsPortal! Please login to contonue!')
            send_mail(
                subject="Welcome To JobPortal",
                message=f"Hi {first_name} {last_name},\n   Get ready to step into your dream job with JobPortal . ",
                from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings.py
                recipient_list=[email],
                fail_silently=False,
            )
            return redirect('login')
    return render(request,'register.html')

def signOut(request):
    auth.logout(request)
    return redirect('home')

@login_required
def userDashboard(request):
    if request.user.is_superuser:
        return redirect("admin_dashboard")
    profile = Profile.objects.get(user__id=request.user.id)
    applied_jobs = Applications.objects.select_related("job").filter(user_id=request.user.id)
    return render(request,"user-dashboard.html",{"applied_jobs": applied_jobs,"p": profile})

@login_required
def editProfile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = ProfileForm(instance=profile)
        return render(request,'edit-profile.html',{'form': form} )

@login_required
def viewProfile(request):
    p=Profile.objects.get(user=request.user)
    return render(request,'view-profile.html',{'p':p})

@admin_permission
def adminDashboard(request,sector=None):
    if not request.user.is_superuser:
        return redirect("user_dashboard")
    data={
    "total_users":User.objects.filter(is_superuser=False).count(),
    "total_jobs":Jobs.objects.count(),
    "total_applications":Applications.objects.count(),
    }
    applications=Applications.objects.all()
    search = request.GET.get("search")
    if search:
        applications = applications.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__username__icontains=search) |
            Q(user__email__icontains=search) |
            Q(job__title__icontains=search)
        )
    if sector:
        job=Jobs.objects.filter(sector__id=sector,is_active=True)
    else:
        job=Jobs.objects.filter(is_active=True) 
    return render(request,"admin-dashboard.html",{'data':data,"applications":applications,"search":search,"job":job})

@admin_permission
def adminApplications(request):
    applications = Applications.objects.select_related("user","job").all()
    return render(request,"admin-applications.html",{"applications": applications})

@admin_permission
def applicationDetails(request, application_id):
    application = Applications.objects.select_related("user","job").get(id=application_id)
    return render(request,"application-details.html",{"application": application})

@admin_permission
def viewUsers(request):
    users=User.objects.filter(is_superuser=False)
    return render(request, "view-users.html", {"users": users})

@admin_permission
def adminJob(request):
    jobs = Jobs.objects.select_related("sector","company")
    search = request.GET.get("search")
    if search:
        jobs = jobs.filter(Q(title__icontains=search) | Q(company__name__icontains=search))
    sector = request.GET.get("sector")
    if sector:
        jobs = jobs.filter(sector_id=sector)
    status = request.GET.get("status")
    if status == "active":
        jobs = jobs.filter(is_active=True)
    elif status == "inactive":
        jobs = jobs.filter(is_active=False)
    context = {
        "jobs": jobs,
        "search": search,
        "selected_sector": sector,
        "selected_status": status,
    }
    return render(request,"admin-jobs.html",context)

@login_required(login_url="login")
def notifications(request):
    if request.user.is_superuser:
        return redirect("all_jobs")
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request,"notifications.html",{"notifications": notifications})

@login_required(login_url="login")
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification,id=notification_id,user=request.user)
    notification.is_read = True
    notification.save()
    return redirect("notifications")

#class based view for sector
class SectorListView(ListView):
    model = Sectors
    template_name = 'sector-list.html'
    context_object_name = 'sectors'

class SectorCreateView(ListView):
    model = Sectors
    field = ['name']
    template_name = 'sector-create.html'
    success_url = reverse_lazy('sector_list')

class SectorUpdateView(UpdateView):
    model = Sectors
    field = ['name']
    template_name = 'sector-update.html'
    success_url = reverse_lazy('sector_list')

class SectorDeleteView(DeleteView):
    model = Sectors
    template_name = 'sector-delete.html'
    success_url = reverse_lazy('sector_list')
    pk_url_kwarg="sector_id"
    

