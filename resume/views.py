from django.shortcuts import render, redirect
from .models import Resume
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
# Create your views here.


@login_required
def accept(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        summary = request.POST.get("summary", "")
        degree = request.POST.get("degree", "")
        school = request.POST.get("school", "")
        university = request.POST.get("university", "")
        previous_work = request.POST.get("previous_work", "")
        skills = request.POST.get("skills", "")

        resume = Resume(name=name, email=email, phone=phone, summary=summary, degree=degree,
                        school=school, university=university, previous_work=previous_work, skills=skills)
        resume.save()
        return redirect('resume', id=resume.id)
    return render(request, 'resume/accept.html')


@login_required
def generate_pdf(request, id):
    # Model data
    user_resume = Resume.objects.get(pk=id)
    
    # Rendered
    html_string = render_to_string('resume/resume.html', {'user_resume': user_resume})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=resume.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response
