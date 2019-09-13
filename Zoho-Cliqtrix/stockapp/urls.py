from django.urls import path 
from . import views
urlpatterns = [
    # path('stock/<str:code>/',views.StockView.as_view()),
    # path('amazon/',views.AmazonView.as_view()),
    # path("medium/",views.MediumView.as_view()),
    # path('wiki/',views.WikipediaView.as_view()),
    # path('weather/',views.WeatherView.as_view()),
    # path('news/<str:country>/',views.NewsView.as_view()),
    # path('convert/<str:from_code>/',views.ConvertView.as_view()),
    # path('domain/<str:domain>/',views.DomainView.as_view()),
    # path('pix/<str:term>/',views.PixView.as_view()),
    # path('zone/<str:code>/',views.ZoneView.as_view()),
    # path('time/',views.TimeView.as_view()),
    # path('getbook/',views.BookmarkGetView.as_view()),
    # path('newbook/',views.BookmarkCreateView.as_view()),

    path("resume/create/",views.CreateView.as_view()),
    path("resume/details/",views.DetailsView.as_view()),
    path("resume/basics/",views.BasicsView.as_view()),
    path("resume/profiles/",views.ProfilesView.as_view()),
    path("resume/works/",views.WorksView.as_view()),
    path("resume/education/",views.EducationView.as_view()),
    path("resume/publications/",views.PublicationView.as_view()),
    path("resume/awards/",views.AwardsView.as_view()),
    path("resume/references/",views.ReferenceView.as_view()),
    path("resume/skills/",views.SkillsView.as_view()),
    path("resume/interests/",views.InterestsView.as_view()),
    path("resume/languages/",views.LanguageView.as_view()),
    path("resume/compile/",views.CompileResumeView.as_view()),
    path("resume/delete/",views.DeleteView.as_view()),
    path("amazon/",views.AmazonView.as_view())
]
