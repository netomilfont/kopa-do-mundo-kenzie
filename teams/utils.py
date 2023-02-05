from datetime import datetime

class DataErrors(Exception):
    def __init__(self, message=None, status_code=500):
        self.message = message
        self.status_code = status_code


def data_processing(team_dict: dict):
    now = datetime.now()
    ano = team_dict['first_cup'].split('-')
    ano_atual = now.year
    number_of_possib_titles = (ano_atual - int(ano[0])) / 4 

    if team_dict['titles'] < 0:
        raise DataErrors("titles cannot be negative", 400)

    if int(ano[0]) < 1930:
        raise DataErrors("there was no world cup this year", 400)    

    if number_of_possib_titles < team_dict['titles']:
        raise DataErrors("impossible to have more titles than disputed cups", 400)
    
    cup_year = 1930
    while cup_year <= ano_atual:
        if cup_year < int(ano[0]):
            cup_year = cup_year + 4        
        elif cup_year == int(ano[0]):
            return team_dict
        elif cup_year > int(ano[0]):
            raise DataErrors("there was no world cup this year", 400)