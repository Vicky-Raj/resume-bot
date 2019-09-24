from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import json
import subprocess
from .models import *
import os
import requests
from fake_useragent import UserAgent
import uuid
from bs4 import BeautifulSoup
import re

date_regex = "[0-9]{4}-[01]((?<=0)[1-9]|(?<=1)[0-2])-[0-3]((?<=3)[01]|(?<=[0-2])[0-9])"
email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

class AmazonView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        name = request.GET.get('name')
        modname = str(name).replace('%20', '+')
        ua = UserAgent()
        bucket = list()

        while len(bucket) == 0:
            response = requests.get(
                f"https://www.amazon.in/s?k={modname}&ref=nb_sb_noss_2",  headers={'User-Agent': str(ua.chrome)})
            soup = BeautifulSoup(response.text, 'lxml')
            for a, b, c, d, e in zip(soup.findAll('span', {'class': 'a-size-medium a-color-base a-text-normal'}), soup.findAll('span', {'class': 'a-price-whole'}), soup.findAll('img', {'class': 's-image'}), soup.findAll('a', {'class': 'a-link-normal a-text-normal'}), soup.findAll('span', {'class': 'a-icon-alt'})):
                # print(f"Name : {a.get_text()} Price :{b.get_text()}  Image url {c['src']}")
                bucket.append(
                    {"name": a.get_text(), 'price': b.get_text(), 'imgurl': c['src'], 'id': d["href"].split("/")[3], 'rating': e.get_text()[0]})
        return Response(bucket)

class DetailsView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request):
        email = request.GET.get("email")
        client,created = Client.objects.get_or_create(email=email)
        if created:
            client.email = email
            client.save()
        return Response({
            "resumes":[resume.name for resume in client.resume_set.all()]
        })
    
class CreateView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.POST.get("email")
        name = request.POST.get("name")
        client,created = Client.objects.get_or_create(email=email)
        if created:
            client.email = email
            client.save()
        if Resume.objects.filter(name=name).exists():
            return Response(400)
        if Resume.objects.all().count() == 9:
            return Response(403)
        resume = Resume()
        resume.client = client
        resume.name = name
        basics = Basics()
        basics.save()
        resume.basics = basics
        resume.save()
        return Response(200)

class BasicsView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        client = Client.objects.get(email=request.POST.get("client_email"))
        resume = client.resume_set.all().filter(name=request.POST.get("res_name")).first()
        fields = ["name","label","email","phone","website","summary","address","country","region"]
        email = request.POST.get("email")
        if email == '' or not bool(re.match(email_regex,email)):
            return Response(400)
        for field in fields:
            setattr(resume.basics,field,request.POST.get(field))
        resume.basics.save()
        resume.save()
        return Response(200)

class ProfilesView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request):
        client = Client.objects.get(email=request.GET.get("email"))
        resume = client.resume_set.all().filter(name=request.GET.get("name")).first()
        return Response({
            "profiles":[
            {
            "network":profile.network,
            "username":profile.username,
            "url":profile.url,
            } for profile in resume.basics.profiles.all()]
        })

    def post(self, request):
        client = Client.objects.get(email=request.POST.get("email"))
        resume = client.resume_set.all().filter(name=request.POST.get("name")).first()
        profile = Profile()
        profile.network = request.POST.get("network")
        profile.username = request.POST.get("username")
        profile.url = request.POST.get("url")
        profile.save()
        resume.basics.profiles.add(profile)
        resume.save()
        return Response()

class WorksView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request):
        client = Client.objects.get(email=request.GET.get("email"))
        resume = client.resume_set.all().filter(name=request.GET.get("name")).first()
        return Response({
            "works":[
            {
            "company":work.company,
            "position":work.position,
            "website":work.website,
            "startDate":work.startDate,
            "endDate":work.endDate,
            "summary":work.summary,
            "highlights":"\n".join([highlight.highlight for highlight in work.highlights.all()])
            } for work in resume.works.all()]
        })
    
    def post(self,request):
        client = Client.objects.get(email=request.POST.get("email"))
        resume = client.resume_set.all().filter(name=request.POST.get("name")).first()
        fields = ["company","position","website","startDate","endDate","summary"]
        startdate = request.POST.get("startDate")
        enddate = request.POST.get("endDate")
        if not bool(re.match(date_regex,startdate)):
            return Response(400)
        if not bool(re.match(date_regex,enddate)):
            return Response(401)
        work = Work()
        for field in fields:
            setattr(work,field,request.POST.get(field))
        work.save()
        highs = request.POST.get("highlights").split("|")
        for high in highs:
            highlight = String()
            highlight.highlight = high
            highlight.save()
            work.highlights.add(highlight)
        work.save()
        resume.works.add(work)
        resume.save()
        return Response(200)

class EducationView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request):
        client = Client.objects.get(email=request.GET.get("email"))
        resume = client.resume_set.all().filter(name=request.GET.get("name")).first()
        return Response({
           "educations":[
               {
                   "institute":ed.institute,
                    "area":ed.area,
                    "studyType":ed.studyType,
                    "startDate":ed.startDate,
                    "endDate":ed.endDate,
                    "gpa":ed.gpa,
                    "courses": "\n".join([course.highlight for course in ed.courses.all()])
               }for ed in resume.education.all()
           ]
        })
    def post(self,request):
        client = Client.objects.get(email=request.POST.get("email"))
        resume = client.resume_set.all().filter(name=request.POST.get("name")).first()
        fields = ["institute","area","studyType","startDate","endDate","gpa"]
        startdate = request.POST.get("startDate")
        enddate = request.POST.get("endDate")
        if not bool(re.match(date_regex,startdate)):
            return Response(400)
        if not bool(re.match(date_regex,enddate)):
            return Response(401)
        ed = Education()
        for field in fields:
            setattr(ed,field,request.POST.get(field))
        ed.save()
        courses = request.POST.get("courses").split("|")
        for course in courses:
            courseObj = String()
            courseObj.highlight = course
            courseObj.save()
            ed.courses.add(courseObj)
        ed.save()
        resume.education.add(ed)
        resume.save()
        return Response(200)

class PublicationView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request):
        client = Client.objects.get(email=request.GET.get("email"))
        resume = client.resume_set.all().filter(name=request.GET.get("name")).first()
        return Response({
            "publications":[
                {
                    "name":pub.name,
                    "publisher":pub.publisher,
                    "releaseDate":pub.releaseDate,
                    "website":pub.website,
                    "summary":pub.summary

                }for pub in resume.publications.all()
            ]
        })

    def post(self,request):
        client = Client.objects.get(email=request.POST.get("email"))
        resume = client.resume_set.all().filter(name=request.POST.get("res_name")).first()
        fields = ["name","publisher","releaseDate","website","summary"]
        re_date = request.POST.get("releaseDate")
        if not bool(re.match(date_regex,re_date)):
            return Response(400)
        pub = Publications()
        for field in fields:
            setattr(pub,field,request.POST.get(field))
        pub.save()
        resume.publications.add(pub)
        resume.save()
        return Response(200)

class AwardsView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request):
        client = Client.objects.get(email=request.GET.get("email"))
        resume = client.resume_set.all().filter(name=request.GET.get("name")).first()
        return Response({
            "awards":[
                {
                    "title":award.title,
                    "date":award.date,
                    "awarder":award.awarder,
                    "summary":award.summary
                }for award in resume.awards.all()
            ]
        })
    def post(self,request):
        client = Client.objects.get(email=request.POST.get("email"))
        resume = client.resume_set.all().filter(name=request.POST.get("name")).first()
        fields = ["title","date","awarder","summary"]
        date = request.POST.get("date")
        if not bool(re.match(date_regex,date)):
            return Response(400)
        award = Awards()
        for field in fields:
            setattr(award,field,request.POST.get(field))
        award.save()
        resume.awards.add(award)
        resume.save()
        return Response(200)

class ReferenceView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request):
        client = Client.objects.get(email=request.GET.get("email"))
        resume = client.resume_set.all().filter(name=request.GET.get("name")).first()
        return Response({
            "references":[
                {
                    "name":ref.name,
                    "reference":ref.reference
                }for ref in resume.references.all()
            ]
        })
    def post(self,request):
        client = Client.objects.get(email=request.POST.get("email"))
        resume = client.resume_set.all().filter(name=request.POST.get("res_name")).first()
        ref = References()
        ref.name = request.POST.get("name")
        ref.reference = request.POST.get("reference")
        ref.save()
        resume.references.add(ref)
        resume.save()
        return Response()

class SkillsView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        client = Client.objects.get(email=request.POST.get("email"))
        resume = client.resume_set.all().filter(name=request.POST.get("name")).first()
        resume.skills.clear()
        skills = request.POST.get("skills").split("|")
        for skill in skills:
            skillObj = String()
            skillObj.highlight = skill
            skillObj.save()
            resume.skills.add(skillObj)
            resume.save()
        return Response({
            "skills":[skill.highlight for skill in resume.skills.all()]
        })

class InterestsView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        client = Client.objects.get(email=request.POST.get("email"))
        resume = client.resume_set.all().filter(name=request.POST.get("name")).first()
        resume.interests.clear()
        ints = request.POST.get("interests").split("|")
        for interest in ints:
            intObj = String()
            intObj.highlight = interest
            intObj.save()
            resume.interests.add(intObj)
            resume.save()
        return Response({
            "interests":[inte.highlight for inte in resume.interests.all()]
        })

class LanguageView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        client = Client.objects.get(email=request.POST.get("email"))
        resume = client.resume_set.all().filter(name=request.POST.get("name")).first()
        resume.languages.clear()
        languages = request.POST.get("languages").split("|")
        for language in languages:
            langObj = String()
            langObj.highlight = language
            langObj.save()
            resume.languages.add(langObj)
            resume.save()
        return Response({
            "languages":[lang.highlight for lang in resume.languages.all()]
        })

def add_basics(resume,res_map):
    res_map["basics"] = {}
    fields = ["name","label","email","phone","website","summary"]
    for field in fields:
        res_map["basics"].update({field:getattr(resume.basics,field)})

    res_map["basics"]["location"] = {}
    res_map["basics"]["location"].update({"address":resume.basics.address})
    res_map["basics"]["location"].update({"countryCode":resume.basics.country})
    res_map["basics"]["location"].update({"region":resume.basics.region})

    res_map["basics"]["profiles"] = []

    for profile in resume.basics.profiles.all():
        res_map["basics"]["profiles"].append({
            "network":profile.network,
            "username":profile.username,
            "url":profile.url
        })
   

def add_work(resume,res_map):
    res_map["work"] = []
    for work in resume.works.all():
        res_map["work"].append({
            "company":work.company,
            "position":work.position,
            "website":work.website,
            "startDate":work.startDate,
            "endDate":work.endDate,
            "summary":work.summary,
            "highlights":[highlight.highlight for highlight in work.highlights.all()]
        })


    
def add_education(resume,res_map):
    res_map["education"] = []
    for edu in resume.education.all():
        res_map["education"].append({
            "institute":edu.institute,
            "area":edu.area,
            "studyType":edu.studyType,
            "startDate":edu.startDate,
            "endDate":edu.endDate,
            "gpa":edu.gpa,
            "courses":[course.highlight for course in edu.courses.all()]  
        })

def add_awards(resume,res_map):
    res_map["awards"] = []
    for award in resume.awards.all():
        res_map["awards"].append({
            "title":award.title,
            "date":award.date,
            "awarder":award.awarder,
            "summary":award.summary
        })

def add_pubs(resume,res_map):
    res_map["publications"] = []
    for pub in resume.publications.all():
        res_map["publications"].append({
            "name":pub.name,
            "publisher":pub.publisher,
            "releaseDate":pub.releaseDate,
            "website":pub.website,
            "summary":pub.summary
        })

def add_skills(resume,res_map):
    res_map["skills"] = []
    res_map["skills"].append({"keywords":[skill.highlight for skill in resume.skills.all()]})

def add_lang(resume,res_map):
    res_map["languages"] = [
        {
            "language":lang.highlight
        }for lang in resume.languages.all()
    ]

def add_ints(resume,res_map):
    res_map["interests"] = [
        {
            "name":inte.highlight
        }for inte in resume.interests.all()
    ]

def add_refs(resume,res_map):
    res_map["references"] = [
        {
            "name":ref.name,
            "reference":ref.reference
        }for ref in resume.references.all()
    ]

def compile_resume(resume,theme):
    dir_name = os.path.join(os.getcwd(),"media")
    if resume.file != None and os.path.exists(os.path.join(dir_name,resume.file)):
        os.remove(os.path.join(dir_name,resume.file))
    res_map = {}
    add_basics(resume,res_map)
    add_work(resume,res_map)
    add_education(resume,res_map)
    add_awards(resume,res_map)
    add_pubs(resume,res_map)
    add_skills(resume,res_map)
    add_lang(resume,res_map)
    add_ints(resume,res_map)
    add_refs(resume,res_map)
    with open("resume.json","w") as res:
        json.dump(res_map,res)
    file_name = f"{str(uuid.uuid4())}.pdf"
    os.system(f"resume export {os.path.join(dir_name,file_name)} --theme {theme}")
    if os.path.exists(os.path.join(dir_name,file_name)):
        os.remove("resume.json")
        resume.file = file_name
        resume.save()
        return file_name
    return False

class CompileResumeView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        client = Client.objects.get(email=request.POST.get("email"))
        resume = client.resume_set.all().filter(name=request.POST.get("name")).first()
        if resume.basics.email == "":
            return Response(400)
        
        name = compile_resume(resume,request.POST.get("theme"))

        if not resume:
            return Response(401)

        return Response({
            "name":name
        })

class DeleteView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        client = Client.objects.get(email=request.POST.get("email"))
        resume = client.resume_set.all().filter(name=request.POST.get("name")).first()
        if resume.file != None and os.path.exists(os.path.join(os.getcwd(),"media",resume.file)):
            os.remove(os.path.join(os.getcwd(),"media",resume.file))
        resume.delete()
        return Response()

