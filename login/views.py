from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.views import APIView, Response
from django.views.decorators.csrf import csrf_exempt
from .utils import userLogin
from .models import Education, Portfolio, Project
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated


import json

# Create your views here.

class LoginView(APIView):
    def post(self, request):    
        email = request.data.get("email")
        password = request.data.get("password")
        user = userLogin(email, password)
        if user != None:
            refreshtoken = RefreshToken.for_user(user)
            print("loged in")
            return Response(
                {'refresh': str(refreshtoken),
                 'access': str(refreshtoken.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
            # return Response(str(refreshtoken.access_token))
        else:
            return Response("username or pasword not valid", status=status.HTTP_401_UNAUTHORIZED)
        
class TestView(APIView):
    def post(self, request):
        print(request.user)
        # user = User.objects.get(username=request.user.username)
        # print(user)
        # if user != None:
        #     return Response(User.username)
        return Response("error")
    
class SignUpView(APIView):
    def post(self, request):
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")
        if username and email and password:
            usernameExist = User.objects.filter(username=username).exists()
            usereamilExist = User.objects.filter(email=email).exists()
            if usernameExist and usereamilExist:
                print("username and email already taken")
                return Response("username and email already taken")
            elif usereamilExist:
                print("email already taken")
                return Response("email already taken")
            elif usernameExist:
                print("username already taken")
                return Response("username already taken")
            else:
                user = User.objects.create_user(username= username, email= email, password=password)
                print("user created")
                refreshtoken = RefreshToken.for_user(user)
                print("loged in")
                return Response(
                    {'refresh': str(refreshtoken),
                    'access': str(refreshtoken.access_token),}
                )
                

def home(request):
    return render(request, "homepage.html")


class CreatePortfolioView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, requests):
        # try:
            # if(Portfolio.objects.get(user = requests.user) != None):
            #     Portfolio.objects.get(user = requests.user).delete()
            name = requests.data.get("name")
            user = requests.user
            jobrole = requests.data.get("jobrole")
            description = requests.data.get("description")
            skills = ""
            for skill in requests.data.get("skills"):
                skills += skill + ","
            # social_links = "" 
            # for links in requests.data.get("socialmedia"):
            #     social_links += links + ","

            if(Portfolio.objects.get(user = requests.user) != None):
                print("using old")
                newPorfolio = Portfolio.objects.get(user = requests.user)
                newPorfolio.username = user.username
                newPorfolio.user = user
                newPorfolio.name = name
                newPorfolio.jobrole = jobrole
                newPorfolio.description = description
                newPorfolio.skills = skills
            else:
                newPorfolio = Portfolio(
                    username = user.username,
                    user = user,
                    name = name,
                    jobrole = jobrole,
                    description = description,
                    skills = skills,
                )
            newPorfolio.save()
            print("pk : " + str(newPorfolio.pk))

            return Response("created", status=status.HTTP_201_CREATED)
        # except Exception as exc:
            print(exc)

            return Response("some error occured", status=status.HTTP_404_NOT_FOUND)
    
class AddEducations(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # try:
            user = request.user
            portfolio = Portfolio.objects.get(user=user)
            for education in request.data.get("educations"):
                print(education)
                inst = education["institution"]
                degree = education["degree"]
                sy = education["startyear"]
                ey = education["endyear"]
                if(sy == ""):
                    sy = 0
                if(ey == ""):
                    ey = 0
                edu = Education(
                    institution = inst,
                    degree = degree,
                    startYear = sy,
                    endYear = ey
                )
                edu.save()
                portfolio.educations.add(edu)
            return Response("educations added successfully" ,status=status.HTTP_201_CREATED)
        # except Exception as e:
            print(e)
            return Response("failed to add educations" ,status=status.HTTP_201_CREATED)
class AddProjects(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # try:
            project = request.data
            print("request from the user")
            user = request.user
            print(project)
            portfolio = Portfolio.objects.get(user=user)
            #save image got form the client
            name = project["projectname"]
            img = project["projectimages"]
            desc = project["projectdesc"]
            links = project["projectlinks"]
            proj = Project(
                projectname = name,
                projectdesc = desc,
                projectlinks = links,
                projectimage = img
            )
            proj.save()
            portfolio.projects.add(proj)
            portfolio.save()
            return Response("project added successfully" ,status=status.HTTP_201_CREATED)
        # except Exception as e:
            print(e)
            return Response("failed to add project" ,status=status.HTTP_201_CREATED)

class AddSocialLinks(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            print(request.data.get("socialmedia"))
            social_links = "" 
            for links in request.data.get("socialmedia"):
                social_links += links + ","
            
            portfolio = Portfolio.objects.get(user = request.user)
            portfolio.socialmedia = social_links
            portfolio.save()

            return Response("social links added successfully" ,status=status.HTTP_201_CREATED)
        except:
            return Response("failed to add links" ,status=status.HTTP_201_CREATED)


class PortfolioView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, requests):
        try:
            if(requests.query_params.get("isowner") == "true"):
                user = requests.user
                if(user == None or user.is_anonymous):
                    return Response("Unauthorized acess", status=status.HTTP_401_UNAUTHORIZED)
                user_portfolio = Portfolio.objects.get(user = user.id)
            else:
                print(requests.query_params.get("username"))
                username = requests.query_params.get("username")
                user_portfolio = Portfolio.objects.get(username = username)

            if user_portfolio:
                return Response(portfolioToJson(user_portfolio), status=status.HTTP_200_OK)
            else:
                return Response("no user found", status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(portfolioToJsonBasic(requests.user), status=status.HTTP_200_OK)



def stringToList(inputstr: str):
    out = []
    startIndex = 0
    currIndex = 0
    for s in inputstr:
        if s == ",":
            out.append(inputstr[startIndex:currIndex])
            startIndex = currIndex + 1
        currIndex += 1
    return out

def educationToJSon(edu):
    out = []
    for e in edu:
       out.append({
        "institution" : e.institution,
        "degree" : e.degree,
        "startYear" : e.startYear,
        "endYear" : e.endYear,
        })
       
    return out

def projectToJSon(projects):
    out = []
    for pro in projects:

        out.append({
            "projectname" : pro.projectname,
            "projectimages" : "http://127.0.0.1:8000" + pro.projectimage.url,
            "projectdesc" : pro.projectdesc,
            "projectlinks" : str(pro.projectlinks),
        })

    return out
        

def portfolioToJson(portfolio: Portfolio, ):
    projectToJSon(portfolio.projects.all())
    return {
        "username" : portfolio.user.username,
        "name"  : portfolio.name,
        "email" : portfolio.user.email,
        "jobrole" : portfolio.jobrole,
        "description" : portfolio.description,
        "socialmedia" : stringToList(portfolio.socialmedia),
        "skills"  : stringToList(portfolio.skills),
        "educations" : educationToJSon(portfolio.educations.all()),
        # "projects"  : [],
        "projects"  : projectToJSon(portfolio.projects.all()),
    }

def portfolioToJsonBasic(user: User):
     return {
        "username" : user.username,
        "email" : user.email
    }




testInput = {
   "name" : "bhuvanesh",
   "jobrole" : "app devloper",
   "description" : "some description",
   "skills" : ["app devloper", "django", "restapi"],
   "socialmedia" : ["instagram.com/user","github.com/bhuvaneshcode"],
   "educations" : [{
       "institution" : "instudtion name",
       "startyear" : 2014,
       "endyear" : 2019
   }],
   "projects" : [{
       "projectname" : "app",
       "projectimages" : [],
       "projectdesc" : "description",
       "projectlinks" : []
   }]
}



projects_Demo = {
   "projects": [
      {
         "projectname": "Expense Tracker",
         "projectimages": ["projectimage1.jpg", "projectimage2.jpg"],
         "projectdesc": "A mobile app for tracking daily expenses effortlessly.",
         "projectlinks": ["github.com/user/expensetracker", "example.com/expensetrackerdemo"]
      },
      {
         "projectname": "Task Manager",
         "projectimages": ["taskmanager1.jpg", "taskmanager2.jpg"],
         "projectdesc": "An application to help users manage their tasks and to-dos efficiently.",
         "projectlinks": ["github.com/user/taskmanager", "example.com/taskmanagerdemo"]
      },
      {
         "projectname": "Weather App",
         "projectimages": ["weatherapp1.jpg", "weatherapp2.jpg"],
         "projectdesc": "Get real-time weather updates for your location with this weather app.",
         "projectlinks": ["github.com/user/weatherapp", "example.com/weatherappdemo"]
      },
      {
         "projectname": "E-commerce Website",
         "projectimages": ["ecommerce1.jpg", "ecommerce2.jpg"],
         "projectdesc": "An online shopping website with a wide range of products.",
         "projectlinks": ["github.com/user/ecommerce", "example.com/ecommercedemo"]
      },
      {
         "projectname": "Blog Platform",
         "projectimages": ["blogplatform1.jpg", "blogplatform2.jpg"],
         "projectdesc": "Create and share your blogs with this user-friendly blog platform.",
         "projectlinks": ["github.com/user/blogplatform", "example.com/blogplatformdemo"]
      },
      {
         "projectname": "Recipe Book",
         "projectimages": ["recipebook1.jpg", "recipebook2.jpg"],
         "projectdesc": "Organize and discover new recipes with this recipe book app.",
         "projectlinks": ["github.com/user/recipebook", "example.com/recipebookdemo"]
      },
      {
         "projectname": "Fitness Tracker",
         "projectimages": ["fitnesstracker1.jpg", "fitnesstracker2.jpg"],
         "projectdesc": "Track your workouts and fitness progress with this fitness app.",
         "projectlinks": ["github.com/user/fitnesstracker", "example.com/fitnesstrackerdemo"]
      },
      {
         "projectname": "Social Networking App",
         "projectimages": ["socialapp1.jpg", "socialapp2.jpg"],
         "projectdesc": "Connect with friends and share updates on this social networking app.",
         "projectlinks": ["github.com/user/socialapp", "example.com/socialappdemo"]
      },
      {
         "projectname": "Travel Planner",
         "projectimages": ["travelplanner1.jpg", "travelplanner2.jpg"],
         "projectdesc": "Plan your trips and explore new destinations with this travel app.",
         "projectlinks": ["github.com/user/travelplanner", "example.com/travelplannerdemo"]
      },
      {
         "projectname": "Online Course Platform",
         "projectimages": ["courseplatform1.jpg", "courseplatform2.jpg"],
         "projectdesc": "Learn new skills through online courses with this education platform.",
         "projectlinks": ["github.com/user/courseplatform", "example.com/courseplatformdemo"]
      }
   ]
}
