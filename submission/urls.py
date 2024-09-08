from django.urls import path
from submission import views


urlpatterns = [
    path('hackathons/', views.HachathonListCreateView.as_view(), name='hackathon-list-create'),
    path('hackathons/<int:pk>/', views.HackathonRetriveUpdateDestory.as_view(), name='hackathon-retrieve-update-destroy'),
    
    path('hackathons/<int:pk>/participants/', views.HackathonParticipantListAPIView.as_view(), name='hackathon-participants-list'),
    
    path('hackathons/<int:pk>/submissions/', views.HackathonSubmissionListCreateView.as_view(), name='hackathon-submissions-list-create'),
    
    path('hackathons/enrolled/', views.EnrollUserHackathonList.as_view(), name='enrolled-hackathons-list'),
]
