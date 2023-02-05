from rest_framework.views import APIView, Response, Request, status
from .models import Team
from django.forms.models import model_to_dict
from .utils import DataErrors, data_processing
import ipdb

class TeamView(APIView):
    def post(self, req: Request) -> Response:
        try:
            valid_team = data_processing(req.data)
        except DataErrors as error:
            return Response(
                {"error": error.message},
                error.status_code
            )


        team = Team.objects.create(**req.data)
        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_201_CREATED)


    def get(self, req: Request) -> Response:
        teams = Team.objects.all()
        teams_list = []
        
        for team in teams:
            teams_dict = model_to_dict(team)
            teams_list.append(teams_dict)
        
        return Response(teams_list, status.HTTP_200_OK)

class TeamDetailView(APIView):
    def get(self, req: Request, team_id: str) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team_dict = model_to_dict(team)
        
        return Response(team_dict, status.HTTP_200_OK)
    

    def patch(self, req: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        for key, value in req.data.items():
            setattr(team, key, value)

        team.save()

        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_200_OK)

    
    def delete(self, req: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)