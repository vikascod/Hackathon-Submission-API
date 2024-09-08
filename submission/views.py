from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from submission.models import Hackathon, Submission, HackathonParticipant
from submission.serializers import HackathonSerializer, SubmissionSerializer, HackathonParticipantSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView


# Create your views here.
class HachathonListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        hackathons = Hackathon.objects.all()
        serializer = HackathonSerializer(hackathons, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = HackathonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({'Response': serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response({"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class HackathonRetriveUpdateDestory(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, pk, *args, **kwargs):
        try:
            hackathon = Hackathon.objects.get(pk=pk)
        except Hackathon.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serlaizer = HackathonSerializer(hackathon)
        return Response({"Response": serlaizer.data}, status=status.HTTP_200_OK)
    
    def put(self, request, pk, *args, **kwargs):
        try:
            hackathon = Hackathon.objects.get(pk=pk)
        except Hackathon.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serlaizer = HackathonSerializer(hackathon, data=request.data)
        if serlaizer.is_valid():
            serlaizer.save()
            return Response({"Response": serlaizer.data}, status=status.HTTP_200_OK)
        
        return Response({"Response": serlaizer.errors}, status=status.HTTP_304_NOT_MODIFIED)

    def delete(self, request, pk):
        try:
            hackathon = Hackathon.objects.get(pk=pk)
        except Hackathon.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        hackathon.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class HackathonParticipantListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            hackathon = Hackathon.objects.get(pk=pk)
        except Hackathon.DoesNotExist:
            return Response({"Error": "Hackathon not found."}, status=status.HTTP_404_NOT_FOUND)
        
        participants = HackathonParticipant.objects.filter(hackathon=hackathon)
        serializer = HackathonParticipantSerializer(participants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk, *args, **kwargs):
        try:
            hackathon = Hackathon.objects.get(pk=pk)
        except Hackathon.DoesNotExist:
            return Response({"Error": "Hackathon not found."}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user

        # user is already a participant
        if HackathonParticipant.objects.filter(hackathon=hackathon, user=user).exists():
            return Response({"Error": "User is already enrolled in this hackathon."}, status=status.HTTP_400_BAD_REQUEST)

        participant = HackathonParticipant(
            hackathon=hackathon,
            user=user
        )
        participant.save()

        serializer = HackathonParticipantSerializer(participant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HackathonSubmissionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            hackathon = Hackathon.objects.get(pk=pk)
        except Hackathon.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = self.request.user
        submissions = Submission.objects.filter(hackathon=hackathon,
                                                user=user)
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        try:
            hackathon = Hackathon.objects.get(pk=pk)
        except Hackathon.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = self.request.user
        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.hackathon = hackathon
            serializer.user = user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EnrollUserHackathonList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        participanted_hackathons = HackathonParticipant.objects.filter(user=request.user)
        
        if not participanted_hackathons.exists():
            return Response({"Error": "No hackathons found for this user."}, status=status.HTTP_404_NOT_FOUND)

        hackathons = [participant.hackathon for participant in participanted_hackathons]
        serializer = HackathonSerializer(hackathons, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    
