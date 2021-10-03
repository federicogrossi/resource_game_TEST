from otree.api import *
#is_dropout = models.BooleanField(initial=False)
# Participant.mylist = ["is_dropout"]


cu = Currency

doc = """
Baseline treatment
"""


class Constants(BaseConstants):
    name_in_url = 'resource_game_TEST'
    players_per_group = 2
    num_rounds = 16
    A_value = cu(0.04)
    B_value = cu(0.02)
    Final_number = 10000


class Subsession(BaseSubsession):
    def creating_session(subsession):
        if subsession.round_number == 1:
            subsession.group_randomly()
        else:
            subsession.group_like_round(1)

        for player in subsession.get_players():
            participant = player.participant
            participant.is_dropout = False


class Group(BaseGroup):
    total_harvest = models.IntegerField(
       min=0,
    )
    A_stock_remained = models.IntegerField(
        min=0,
        max=50,
        initial=50,
    )
    B_stock_remained = models.IntegerField(
        min=0,
        max=54,
        initial=50,
    )
    A_growth_rate = models.IntegerField()
    B_growth_rate = models.IntegerField()
    A_new_stock = models.IntegerField(
        min=0,
        max=50,
        initial=50,
    )
    B_new_stock = models.IntegerField(
        min=0,
        max=54,
        initial=50,
    )


# def set_payoffs(group: Group):
#    players = group.get_players()
#    harvests = [p.harvest for p in players]
#    group.total_harvest = sum(harvests)
#    for p in players:
#        if group.total_harvest < group.A_stock_remained:
#            p.payoff = p.harvest * Constants.A_value + group.B_growth_rate * Constants.B_value
#        elif group.total_harvest >= group.A_stock_remained:
#            p.payoff = ((p.harvest / group.total_harvest) * group.A_stock_remained) * Constants.A_value + group.B_growth_rate * Constants.B_value


def stocks_new_and_remained(group: Group):   #  questo potrebbe essere spostato in player e group diventa player, # anche se i gruppi comunque cambiano
    players = group.get_players()
    harvests = [p.harvest for p in players]
    group.total_harvest = sum(harvests)
    if group.round_number == 1:
        group.A_new_stock = 50
    else:
        group.A_new_stock = group.in_round(group.round_number - 1).A_stock_remained + group.in_round(group.round_number - 1).A_growth_rate

    if group.round_number == 1:
        group.B_new_stock = 50
    else:
        group.B_new_stock = group.in_round(group.round_number - 1).B_stock_remained + group.in_round(group.round_number - 1).B_growth_rate  # you can use "result" format (see Lesson 3)

    if group.total_harvest >= group.A_new_stock:
        group.A_stock_remained = 0
    else:
        group.A_stock_remained = group.A_new_stock - group.total_harvest

    if group.in_round(1).total_harvest == 50:
        group.B_stock_remained = 0
    else:
        group.B_stock_remained = group.B_new_stock - group.total_harvest


def growth_rates(group: Group):
    if group.A_stock_remained == range(0, 5):
        group.A_growth_rate = 0
    elif group.A_stock_remained == range(5, 10):
        group.A_growth_rate = 1
    elif group.A_stock_remained == range(10, 15):
        group.A_growth_rate = 2
    elif group.A_stock_remained == range(15, 20):
        group.A_growth_rate = 1
    elif group.A_stock_remained == range(20, 25):
        if group.round_number != 1 and group.in_round(group.round_number - 1).A_growth_rate == 1:
            group.A_growth_rate = 1
        else:
            group.A_growth_rate = 7
    elif group.A_stock_remained == range(25, 30):
        group.A_growth_rate = 9
    elif group.A_stock_remained == range(30, 35):
        group.A_growth_rate = 7
    elif group.A_stock_remained == range(35, 40):
        group.A_growth_rate = 5
    elif group.A_stock_remained == range(40, 45):
        group.A_growth_rate = 3
    elif group.A_stock_remained == range(45, 50):
        group.A_growth_rate = 1
    else:
        group.A_growth_rate = 0

    if group.B_stock_remained == range(0, 5):
        group.B_growth_rate = 1
    elif group.B_stock_remained == range(5, 10):
        group.B_growth_rate = 2
    elif group.B_stock_remained == range(10, 15):
        group.B_growth_rate = 3
    elif group.B_stock_remained == range(15, 20):
        group.B_growth_rate = 4
    elif group.B_stock_remained == range(20, 25):
        if group.round_number != 1 and group.in_round(group.round_number - 1).B_growth_rate == 4:
            group.A_growth_rate = 4
        else:
            group.B_growth_rate = 10
    elif group.B_stock_remained == range(25, 30):
        group.B_growth_rate = 13
    elif group.B_stock_remained == range(30, 35):
        group.B_growth_rate = 12
    elif group.B_stock_remained == range(35, 40):
        group.B_growth_rate = 10
    elif group.B_stock_remained == range(40, 45):
        group.B_growth_rate = 9
    elif group.B_stock_remained == range(45, 50):
        group.B_growth_rate = 5
    elif group.B_stock_remained == 50:
        group.B_growth_rate = 3
    elif group.B_stock_remained >= 51:
        group.B_growth_rate = 0


class Player(BasePlayer):
    harvest = models.IntegerField(
        min=0,
        max=Group.A_new_stock,
        label="How many A-units do you want to harvest?"
    )
    understanding = models.BooleanField(
        choices=[
            [True, 'Yes'],
            [False, 'No'],
        ],
        label="Did you understand the instructions?"
    )
    calculation = models.IntegerField(
        label=" 10 + 27 = ?"
    )
    example = models.FloatField(
        label="If you harvest 5 units and the group harvests a total of 15 units, what is your payoff?"
    )
    A_stock_remained = models.IntegerField(
        min=0,
        max=50,
    )
    B_stock_remained = models.IntegerField(
        min=0,
        max=54,
    )
    A_growth_rate = models.IntegerField()
    B_growth_rate = models.IntegerField()
    A_new_stock = models.IntegerField()
    B_new_stock = models.IntegerField()


# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(group):
        return group.round_number == 1

    timeout_seconds = 45


class Instructions(Page):
    @staticmethod
    def is_displayed(group: Group):
        if group.round_number == 1:
            return True

    timeout_seconds = 240  # after this, you continue, no bots # what if they decide to abandon when they read the instructions? CHECK
    form_model = "player"
    form_fields = ["understanding"]


class Harvest(Page):
    form_model = "player"
    form_fields = ["harvest"]
    timeout_seconds = 120  # https://otree.readthedocs.io/en/latest/multiplayer/waitpages.html?highlight=is_dropout
    after_all_players_arrive = stocks_new_and_remained

    @staticmethod    # try to move this below vars_for_template
    def is_displayed(player: Player):
        group = player.group
        if group.A_new_stock != 0:
            return True
        else:
            return False


class ResultsWaitPage(WaitPage):  # do I have to put group = player.group?
    body_text = "Waiting for other participants to decide."
    after_all_players_arrive = growth_rates


class Results(Page):  # check simple_game for set payoffs --> results-wait-page and result
    timeout_seconds = 30

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        players = group.get_players()
        harvests = [p.harvest for p in players]
        group.total_harvest = sum(harvests)
        for p in players:
            if group.total_harvest < group.A_stock_remained:
                p.payoff = p.harvest * Constants.A_value + group.B_growth_rate * Constants.B_value
            elif group.total_harvest >= group.A_stock_remained:
                p.payoff = ((p.harvest / group.total_harvest) * group.A_stock_remained) * Constants.A_value + group.B_growth_rate * Constants.B_value


class End(Page):
    form_model = "player"
    form_fields = ["calculation"]

    def is_displayed(player: Player):
        group = player.group
        if group.round_number == Constants.num_rounds or group.total_harvest >= 50:
            return True

    def vars_for_template(player: Player):
        all_players = player.in_all_rounds()
        combined_payoff = 0
        for player in all_players:
            combined_payoff += player.payoff
        return dict(combined_payoff=combined_payoff)  #  after this, the questionnaire, the completion code, and the final page



page_sequence = [Introduction, Instructions, Harvest, ResultsWaitPage, Results, End]
