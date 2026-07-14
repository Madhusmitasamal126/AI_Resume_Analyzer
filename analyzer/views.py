import fitz

from django.shortcuts import render
from django.core.files.storage import default_storage

from .forms import ResumeUploadForm
from .utils import extract_text_from_pdf
from .skill_match import calculate_similarity, compare_skills


def home(request):
    form = ResumeUploadForm()
    return render(request, "home.html", {"form": form})


def analyze_resume(request):
    if request.method == "POST":

        form = ResumeUploadForm(request.POST, request.FILES)

        if form.is_valid():

            pdf = request.FILES["resume"]
            jd = request.POST.get("job_description", "")

            path = default_storage.save(pdf.name, pdf)
            full_path = default_storage.path(path)

            resume_text = extract_text_from_pdf(full_path)

            similarity = calculate_similarity(
                resume_text,
                jd
            )

            skills = compare_skills(
                resume_text,
                jd
            )

            return render(
                request,
                "result.html",
                {
                    "similarity": similarity,
                    "skills": skills,
                    "resume_text": resume_text,
                },
            )

    return render(
        request,
        "home.html",
        {"form": ResumeUploadForm()},
    )