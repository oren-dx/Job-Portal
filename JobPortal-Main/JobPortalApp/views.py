from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from django.db.models import Count
from JobPortalApp.forms import*
from JobPortalApp.models import*


def register(request):
    form_data = RegisterForm
    if request.method == 'POST':
        form_data = RegisterForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, 'User Created Successfully')
            return redirect('login_page') 
    
    messages.warning(request, 'User Already Exists')
    form_data = RegisterForm()
    context = {
        'form_data':form_data,
        'title':'register page',
        'form_title':'User Register Page ',
        'form_btn':'Register'
    }
    return render(request, 'base-form.html',context)

def login_page(request):
    form_data = AuthenticationForm
    if request.method == 'POST':
        form_data = AuthenticationForm(request, request.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            login(request, user)
            messages.success(request, 'Login successfully')
            return redirect('dashboard')
        
    messages.warning(request, 'Invaild Credentials')
    form_data = AuthenticationForm()
    context = {
        'form_data':form_data,
        'title':'Login page',
        'form_title':'User Login Page',
        'form_btn':'Login'
    }
    return render(request, 'base-form.html',context)

@login_required
def logout_page(request):
    logout(request)
    return redirect('login_page')

@login_required
def dashboard(request):
    job_data = JobPostModel.objects.none()
    seeker_data = None
    recruiter_data = None

    if request.user.user_type == 'Jobseekers':
        try:
            seeker_data = request.user.seeker_profile

        except SeekeerModel.DoesNotExist:
            messages.warning(request,'Please Update your profile first')
            return redirect('update_profile')

        seeker_skill = seeker_data.skill_set

        if seeker_skill:

            for skill in seeker_skill.split(','):

                cleaned_skill = skill.strip()

                if cleaned_skill:

                    job_data |= JobPostModel.objects.filter(
                        skill_set__icontains=cleaned_skill
                    )

        job_data = job_data.distinct()


    elif request.user.user_type == 'Recruiters':

        try:
            recruiter_data = request.user.recruiter_profile

        except RecruitersModel.DoesNotExist:

            messages.warning(request,'Please Update your profile first')

            return redirect('update_profile')

        job_data = JobPostModel.objects.filter(
            post_by=recruiter_data
        ).annotate(
            applicant_count=Count('applied_post_info')
        )


    context = {
        'job_data': job_data,
        'seeker_data': seeker_data,
        'recruiter_data': recruiter_data,
        'title': 'Dashboard',
    }
    return render(request,'dashboard.html',context)


@login_required
def profile_view(request):

    return render(request, 'profile.html')

@login_required
def update_profile(request):
    current_user = request.user
    if current_user.user_type == 'Recruiters':
        try:
            profile_data = RecruitersModel.objects.get(recruiter = current_user)
        except RecruitersModel.DoesNotExist:
            profile_data = None
        if request.method == 'POST':
            form_data = RecruiterProfileUpdateForm(request.POST, request.FILES, instance= profile_data)
            if form_data.is_valid():
                data = form_data.save(commit=False)
                data.recruiter = current_user
                data.save() 
                messages.success(request, 'Profile Update successfully')
                return redirect('profile_view')
        form_data = RecruiterProfileUpdateForm(instance= profile_data)
    elif current_user.user_type == 'Jobseekers':
        try:
            profile_data = SeekeerModel.objects.get(seeker = current_user)
        except SeekeerModel.DoesNotExist:
            profile_data = None
    
        if request.method == 'POST':
            form_data = SeekerProfileUpdateForm(request.POST, request.FILES,instance= profile_data)
            if form_data.is_valid():
                data = form_data.save(commit=False)
                data.seeker = current_user
                data.save() 
                messages.success(request, 'Profile Update successfully')
                return redirect('profile_view')
            
        form_data = SeekerProfileUpdateForm(instance= profile_data)
    
    context = {
        'form_data':form_data,
        'title':'Update page',
        'form_title':'Update Profile info',
        'form_btn':'Update profile'
    }
    return render(request, 'base-form.html',context)


def browse_job(request):
    search_query = request.GET.get('search_query', '').strip()

    # সব Job
    job_data = JobPostModel.objects.all()

    # Recruiter হলে শুধু নিজের posted jobs
    if request.user.is_authenticated and request.user.user_type == 'Recruiters':
        try:
            recruiter_profile = request.user.recruiter_profile
            job_data = job_data.filter(post_by=recruiter_profile)

        except:
            messages.warning(request, 'Please update your profile first.')
            return redirect('update_profile')

    # Search
    if search_query:
        job_data = job_data.filter(
            Q(title__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(post_by__company_name__icontains=search_query) |
            Q(skill_set__icontains=search_query)
        )

    context = {
        'job_data': job_data,
        'search_query': search_query,
    }
    return render(request, 'browse-job.html', context) 

def job_details(request, id):
    job = JobPostModel.objects.get(id=id)

    context = {
        'job': job
    }
    return render(request, 'job-details.html', context)                      

@login_required
def post_job(request):
    try:
        recruiter_data =request.user.recruiter_profile
    except:
        messages.warning(request, 'Please Update your profile first')
        return redirect('update_profile')
    if request.method == 'POST':
        form_data = JobPostForm(request.POST, request.FILES)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.post_by = recruiter_data
            data.save() 
            messages.success(request, 'Job Post successfully')
            return redirect('browse_job')
    form_data = JobPostForm()
    
    context = {
        'form_data':form_data,
        'title':'Job Post page',
        'form_title':'Job Post info Form',
        'form_btn':'Post'
    }
    return render(request, 'base-form.html',context)

@login_required
def update_JobPost(request,id):
    try:
        recruiter_data =request.user.recruiter_profile
        job =JobPostModel.objects.get(id = id)
    except:
        messages.warning(request, 'Please Update your profile first' )
        return redirect('update_profile')
    if request.method == 'POST':
        form_data = JobPostForm(request.POST, request.FILES, instance = job)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.post_by = recruiter_data
            data.save() 
            messages.success(request, 'Job Update successfully')
            return redirect('browse_job')
    form_data = JobPostForm(instance = job)
    
    context = {
        'form_data':form_data,
        'title':'Update Job page',
        'form_title':'Update Job info Form',
        'form_btn':'Update'
    }
    return render(request, 'base-form.html',context)


@login_required
def delete_JobPost(request,id):
    try:
        JobPostModel.objects.get(id = id).delete()
        messages.success(request, 'Job Delete successfully')
        return redirect('browse_job')
    except:
        messages.error(request, 'Job Not Found')
        return redirect('browse_job')
    
@login_required
def apply_job(request, id):
    try :
        seeker_profile = request.user.seeker_profile
        job = JobPostModel.objects.get(id = id)
    except:
        messages.warning(request, 'Please Update your profile first')
        return redirect('update_profile')
    if request.method == 'POST':
        form_data = ApplyJobForm(request.POST, request.FILES)
        if form_data.is_valid():
            data = form_data.save(commit= False)
            data.applied_by = seeker_profile
            data.applied_job = job
            data.save()
            messages.success(request, 'Application Submit Successfully')
            return redirect('browse_job')
    
    form_data = ApplyJobForm()
    context = {
        'form_data':form_data,
        'title':'Apply Job page',
        'form_title':'Apply Job Info Form',
        'form_btn':'Apply'
    }
    return render(request, 'base-form.html',context)
    
@login_required
def my_application(request):

    my_application = ApplyJobModel.objects.filter(
        applied_by=request.user.seeker_profile
    ).select_related(
        'applied_job',
        'applied_job__post_by',
        'applied_job__category'
    )

    context = {
        'application_list': my_application,
        'title': 'My Application Page',
        'form_title': 'Apply Job Info Form',
        'form_btn': 'Apply'
    }
    return render(request,'my_application.html',context)

def candidate_list(request, id):
    job_data = JobPostModel.objects.get(id = id )
    candidate_data = ApplyJobModel.objects.filter(applied_job=job_data)
    
    context = {
        'job_data':job_data,
        'candidate_data':candidate_data,
        'application_list': my_application,
        'title':'Candidate List page',
    }
    return render(request, 'candidate_list.html',context)
@login_required
def accept_application(request, application_id):
    application = get_object_or_404(
        ApplyJobModel,
        id=application_id
    )

    application.status = 'Accepted'
    application.save()

    return redirect('candidate_list',application.applied_job.id)

@login_required
def reject_application(request, application_id):
    application = get_object_or_404(
        ApplyJobModel,
        id=application_id
    )

    application.status = 'Rejected'
    application.save()

    return redirect('candidate_list', application.applied_job.id)

    
    
    


    



