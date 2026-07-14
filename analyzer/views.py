import fitz

from django.shortcuts import render
from .forms import ResumeUploadForm


def home(request):

    extracted_text = ""

    if request.method == "POST":

        form = ResumeUploadForm(request.POST, request.FILES)

        if form.is_valid():

            pdf = request.FILES["resume"]

            document = fitz.open(stream=pdf.read(), filetype="pdf")

            for page in document:
                extracted_text += page.get_text()

    else:

        form = ResumeUploadForm()

    return render(
        request,
        "home.html",
        {
            "form": form,
            "text": extracted_text
        }
    )