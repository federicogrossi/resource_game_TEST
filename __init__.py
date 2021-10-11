from otree.api import *

cu = Currency

doc = """
BASELINE test
"""


def creating_session(subsession):
    if subsession.round_number != 1:
        subsession.group_like_round(1)


class Constants(BaseConstants):
    name_in_url = 'resource_game_TEST'
    players_per_group = 2
    num_rounds = 12
    A_value = cu(0.04)
    B_value = cu(0.02)
    Final_number = 10000


class Subsession(BaseSubsession):
    pass


class Player(BasePlayer):
    harvest = models.IntegerField(
        min=0,
        max=50,
        initial=0,
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
    is_dropout = models.BooleanField(initial=False)


class Group(BaseGroup):
    total_harvest = models.IntegerField()
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
    )
    B_new_stock = models.IntegerField(
        min=0,
        max=54,
    )


def stocks_new_and_remained(group: Group):   # questo potrebbe essere spostato in player e group diventa player, # anche se i gruppi comunque cambiano
    players = group.get_players()
    harvests = [p.harvest for p in players]
    group.total_harvest = sum(harvests)

    if group.round_number == 1:
        group.A_new_stock = 50
    elif group.round_number == 2:
        group.A_new_stock = 50 - group.in_round(group.round_number - 1).total_harvest + group.in_round(group.round_number - 1).A_growth_rate
    elif group.round_number >= 3:
        group.A_new_stock = group.in_round(group.round_number - 1).A_stock_remained + group.in_round(group.round_number - 1).A_growth_rate

    if group.round_number == 1:
        group.B_new_stock = 50
    elif group.round_number == 2:
        group.B_new_stock = 50 - group.in_round(group.round_number - 1).total_harvest + group.in_round(group.round_number - 1).B_growth_rate
    elif group.round_number >= 3:
        group.B_new_stock = group.in_round(group.round_number - 1).B_stock_remained + group.in_round(group.round_number - 1).B_growth_rate  # in past round

    if group.round_number == 1:
        group.A_stock_remained = 50
    if group.round_number == 2:
        group.A_stock_remained = 50 - group.in_round(group.round_number - 1).total_harvest
    if group.round_number >= 3:
        group.A_stock_remained = group.A_new_stock - group.in_round(group.round_number - 1).total_harvest

    if group.round_number == 1:
        group.B_stock_remained = 50
    if group.round_number == 2:
        group.B_stock_remained = 50 - group.in_round(group.round_number - 1).total_harvest
    if group.round_number >= 3:
        group.B_stock_remained = group.B_new_stock - group.in_round(group.round_number - 1).total_harvest


def growth_rates(group: Group):
    players = group.get_players()
    harvests = [p.harvest for p in players]
    group.total_harvest = sum(harvests)
    if group.round_number == 1:
        if group.total_harvest == 0:
            group.A_growth_rate = 0
        elif group.total_harvest in range(1, 6):
            group.A_growth_rate = 1
        elif group.total_harvest in range(6, 11):
            group.A_growth_rate = 3
        elif group.total_harvest in range(11, 16):
            group.A_growth_rate = 5
        elif group.total_harvest in range(16, 21):
            group.A_growth_rate = 7
        elif group.total_harvest in range(21, 26):
            group.A_growth_rate = 9
        elif group.total_harvest in range(26, 31):
            group.A_growth_rate = 7
        elif group.total_harvest in range(31, 36):
            group.A_growth_rate = 1
        elif group.total_harvest in range(31, 41):
            group.A_growth_rate = 2
        elif group.total_harvest in range(41, 46):
            group.A_growth_rate = 1
        elif group.total_harvest in range(46, 50):
            group.A_growth_rate = 0
        else:
            group.A_growth_rate = 0

        if group.total_harvest == 0:
            group.B_growth_rate = 3
        elif group.total_harvest in range(1, 6):
            group.B_growth_rate = 5
        elif group.total_harvest in range(6, 11):
            group.B_growth_rate = 9
        elif group.total_harvest in range(11, 16):
            group.B_growth_rate = 10
        elif group.total_harvest in range(16, 21):
            group.B_growth_rate = 12
        elif group.total_harvest in range(21, 26):
            group.B_growth_rate = 13
        elif group.total_harvest in range(26, 31):
            group.B_growth_rate = 10
        elif group.total_harvest in range(31, 36):
            group.B_growth_rate = 4
        elif group.total_harvest in range(36, 41):
            group.B_growth_rate = 3
        elif group.total_harvest in range(41, 46):
            group.B_growth_rate = 2
        elif group.total_harvest in range(46, 50):
            group.B_growth_rate = 1
        elif group.total_harvest == 50:  # yes, change to include group.round_number == 1, put upwards
            group.B_growth_rate = 0

    else:
        if group.A_stock_remained in range(0, 5):
            group.A_growth_rate = 0
        elif group.A_stock_remained in range(5, 10):
            group.A_growth_rate = 1
        elif group.A_stock_remained in range(10, 15):
            group.A_growth_rate = 2
        elif group.A_stock_remained in range(15, 20):
            group.A_growth_rate = 1
        elif group.A_stock_remained in range(20, 25):
            if group.round_number != 1 and group.in_round(group.round_number - 1).A_growth_rate == 1:
                group.A_growth_rate = 1
            else:
                group.A_growth_rate = 7
        elif group.A_stock_remained in range(25, 30):
            group.A_growth_rate = 9
        elif group.A_stock_remained in range(30, 35):
            group.A_growth_rate = 7
        elif group.A_stock_remained in range(35, 40):
            group.A_growth_rate = 5
        elif group.A_stock_remained in range(40, 45):
            group.A_growth_rate = 3
        elif group.A_stock_remained in range(45, 50):
            group.A_growth_rate = 1
        else:
            group.A_growth_rate = 0

        if group.B_stock_remained in range(0, 5):
            group.B_growth_rate = 1
        elif group.B_stock_remained in range(5, 10):
            group.B_growth_rate = 2
        elif group.B_stock_remained in range(10, 15):
            group.B_growth_rate = 3
        elif group.B_stock_remained in range(15, 20):
            group.B_growth_rate = 4
        elif group.B_stock_remained in range(20, 25):
            if group.round_number != 1 and group.in_round(group.round_number - 1).B_growth_rate == 4:
                group.B_growth_rate = 4
            else:
                group.B_growth_rate = 10
        elif group.B_stock_remained in range(25, 30):
            group.B_growth_rate = 13
        elif group.B_stock_remained in range(30, 35):
            group.B_growth_rate = 12
        elif group.B_stock_remained in range(35, 40):
            group.B_growth_rate = 10
        elif group.B_stock_remained in range(40, 45):
            group.B_growth_rate = 9
        elif group.B_stock_remained in range(45, 50):
            group.B_growth_rate = 5
        elif group.B_stock_remained == 50:  # yes, change to include group.round_number == 1, put upwards
            group.B_growth_rate = 3
        elif group.B_stock_remained >= 51:
            group.B_growth_rate = 0

    for p in players:
        if group.total_harvest < group.A_stock_remained:
            p.payoff = p.harvest * Constants.A_value + group.B_growth_rate * Constants.B_value
        elif group.total_harvest >= group.A_stock_remained:
            p.payoff = ((p.harvest / group.total_harvest) * group.A_stock_remained) * Constants.A_value + group.B_growth_rate * Constants.B_value


# PAGES
class Grouping(WaitPage):
    body_text = "Please wait a few seconds so that other participants can join your group."
    group_by_arrival_time = True

    @staticmethod
    def is_displayed(group):
        return group.round_number == 1


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

    timeout_seconds = 240 
    form_model = "player"
    form_fields = ["understanding"]


class Example(Page):   # the correct calculation is: (0.04 * 5) + (0.02 * 10) = 0.40$
    form_model = "player"
    form_fields = ["example"]
    timeout_seconds = 60

    @staticmethod
    def is_displayed(group: Group):
        if group.round_number == 1:
            return True


class Calculating(WaitPage):
    after_all_players_arrive = stocks_new_and_remained


class Harvest(Page):
    form_model = "player"
    form_fields = ["harvest"]
    timeout_seconds = 120      # https://otree.readthedocs.io/en/latest/multiplayer/waitpages.html?highlight=is_dropout

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        if group.A_new_stock != 0:
            return True
        else:
            return False

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.harvest = 0  # 0 or 2?
            player.is_dropout = True

    def custom_export(players):  # this is for custom data export
        # header row
        yield ['session', 'participant_code', 'round_number', 'id_in_group', 'payoff', 'harvest']  # I added harvest
        for p in players:
            participant = p.participant
            session = p.session
            yield [session.code, participant.code, p.round_number, p.id_in_group, p.payoff, p.harvest]


class ResultsWaitPage(WaitPage):
    body_text = "Waiting for other participants to decide."
    after_all_players_arrive = growth_rates


class Results(Page):
    timeout_seconds = 30


class ByeDropout(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.is_dropout

    @staticmethod
    def error_message(player: Player, values):
        return "Sorry, you cannot proceed past this page"


class End(Page):
    form_model = "player"
    form_fields = ["calculation"]

    def is_displayed(player: Player):
        group = player.group
        if group.round_number == Constants.num_rounds or group.total_harvest >= group.A_new_stock:
            return True

    def vars_for_template(player: Player):
        all_players = player.in_all_rounds()
        combined_payoff = 0
        for player in all_players:
            combined_payoff += player.payoff
        return dict(combined_payoff=combined_payoff)

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.calculation <= Constants.Final_number:
            return upcoming_apps[0]    # go to QUESTIONNAIRE


page_sequence = [Grouping, Introduction, Instructions, Example, Calculating, Harvest, ResultsWaitPage, Results, ByeDropout, End]
