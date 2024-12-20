""" A class which performs most of the unique actions required during
    a game of blackjack """

from constants import HandResult
from custom_logging import global_logger as logger
from dealer_hand import DealerHand 
from decision_engine import DecisionEngine
from gameplay_config import GameplayConfig as cfg
from player_hand import PlayerHand
from util_functions import get_win_amount


class GameplayEngine():

    def __init__(self, bankroll, count, shoe, hand_analyzer):
        self._bankroll = bankroll 
        self._count = count
        self._decision_engine = DecisionEngine(count)
        self._shoe = shoe
        self._hand_analyzer = hand_analyzer

    def _check_for_blackjacks(self, player_hands, dealer_hand):
        player_hand = player_hands[0]
        return player_hand.is_blackjack() or dealer_hand.is_blackjack()
    
    def _deal_opening_cards(self, player_hands, dealer_hand):
        player_hand = player_hands[0]
        player_hand.deal_card_face_up(self._shoe, self._count, logger)
        dealer_hand.deal_card_face_up(self._shoe, self._count, logger)
        player_hand.deal_card_face_up(self._shoe, self._count, logger)
        dealer_hand.deal_card_face_down(self._shoe)
        logger.card(player_hand.get_hand_string())
        logger.card(f'Dealer up card: {dealer_hand.get_face_up_card().get_card_string()}')

    def _determine_bet_size(self, count):
        return self._decision_engine.determine_bet_size(count)
    
    def _determine_blackjacks(self, player_hand, dealer_hand):
        if not player_hand.is_blackjack() and not dealer_hand.is_blackjack():
            return (False, None)
        elif player_hand.is_blackjack() and dealer_hand.is_blackjack():
            return (True, HandResult.PUSH)
        elif player_hand.is_blackjack():
            return (True, HandResult.BLACKJACK_WIN)
        else:
            return (True, HandResult.LOSE)

    def _determine_hand_results(self, player_hands, dealer_hand, pre_hand_count):
        round_pnl = 0
        dealer_score = dealer_hand.get_dealer_score()
        for hand in player_hands:
            hand_score = hand.get_optimal_score()
    
            blackjack_exists, blackjack_result = self._determine_blackjacks(hand, dealer_hand)  
            if blackjack_exists:
                result = blackjack_result
            elif hand.is_surrendered:
                result = HandResult.SURRENDER
            elif (hand_score > 21) or (dealer_score <= 21 and dealer_score > hand_score):
                result =  HandResult.LOSE 
            elif dealer_score > 21 or hand_score > dealer_score:
                result = HandResult.WIN 
            else:
                result = HandResult.PUSH
            
            logger.card(f'Hand Complete. Result for player: {result.name} with {hand.get_hand_string()} and {dealer_hand.get_hand_string()}')
            hand_win_amount = get_win_amount(result, hand, dealer_hand.is_blackjack())
            hand.bankroll.add(hand_win_amount)

            hand_pnl = hand_win_amount - hand.bet_value
            stake = self._determine_bet_size(pre_hand_count)
            self._hand_analyzer.analyze_hand(hand, dealer_hand.get_face_up_card(), hand_pnl, pre_hand_count, stake)
            round_pnl += hand_pnl 

        logger.card(f'Round complete. PNL from hands: {round_pnl}')

    def _double_down_on_hands_if_applicable(self, player_hands, dealer_up_card, pre_hand_count):
        if len(player_hands) == 1 or cfg.DOUBLE_AFTER_SPLIT:
            for hand in player_hands:
                if not hand.is_surrendered and self._decision_engine.should_double_down_func(hand, dealer_up_card, pre_hand_count):
                    logger.card(f'Doubling down with {hand.get_hand_string()} and dealer up card {dealer_up_card.get_card_string()}')
                    hand.double_down()
                    hand.limit_to_one_hit()        

    def _play_hand_as_dealer(self, player_hands, dealer_hand):
        dealer_hand.reveal_face_down_card(self._count)
        player_has_under_21 = any(hand.get_optimal_score() <= 21 for hand in player_hands)

        while player_has_under_21 and self._decision_engine.should_dealer_hit(dealer_hand):
            dealer_hand.deal_card_face_up(self._shoe, self._count, logger)

    def _play_hands_as_player(self, player_hands, dealer_up_card, pre_hand_count):
        for hand in player_hands:
            while hand.is_allowed_to_hit and self._decision_engine.should_player_hit(hand, dealer_up_card, pre_hand_count):
                hand.deal_card_face_up(self._shoe, self._count, logger)
                hand.count_hit()
        
    def _split_player_hands_if_applicable(self, player_hands, dealer_up_card, pre_hand_count):
        should_split = not player_hands[0]._is_surrendered
        
        while len(player_hands) < cfg.SPLIT_MAX_TIMES + 1 and should_split:
            new_hands = []
            should_split = False
            
            for hand in player_hands:
                if not hand.has_insurance and self._decision_engine.should_split_func(hand, dealer_up_card, pre_hand_count):
                    should_split = True
                    logger.card(f'Splitting hand {hand.get_hand_string()}')
                    hand1, hand2 = hand.split_hand()
                    
                    if hand1.cards[0].is_ace():
                        hand1.limit_to_one_hit()
                        hand2.limit_to_one_hit()

                    hand1.deal_card_face_up(self._shoe, self._count, logger)
                    hand1.count_hit()
                    hand2.deal_card_face_up(self._shoe, self._count, logger)
                    hand2.count_hit()
                    new_hands.extend([hand1, hand2])
                
                else:
                    new_hands.append(hand)
            
            player_hands = new_hands

        return player_hands

    def _surrender_hands_if_applicable(self, player_hands, dealer_hand, pre_hand_count):
        if not cfg.SURRENDER_ALLOWED:
            return 
        else:
            dealer_up_card = dealer_hand.get_face_up_card()
            for hand in player_hands:
                if self._decision_engine.should_surrender_func(hand, dealer_up_card, pre_hand_count):
                    hand.surrender()
                    dealer_hand.reveal_face_down_card(self._count)
                    logger.card(f'Surrendering {hand.get_hand_string()}')
    
    def _take_insurance_if_applicable(self, player_hands, dealer_up_card, pre_hand_count):
        player_hand = player_hands[0]
        if self._decision_engine.should_take_insurance_func(dealer_up_card, pre_hand_count):
            logger.card(f'Taking insurance for {player_hand.bet_value / 2}')
            player_hand.take_insurance()

        
    def play_hand(self, player_hands, dealer_hand, pre_hand_count):
        """ Logic to run a hand  """

        dealer_up_card = dealer_hand.get_face_up_card()
        self._take_insurance_if_applicable(player_hands, dealer_up_card, pre_hand_count)

        if not self._check_for_blackjacks(player_hands, dealer_hand):
            self._surrender_hands_if_applicable(player_hands, dealer_hand, pre_hand_count)
            player_hands = self._split_player_hands_if_applicable(player_hands, dealer_up_card, pre_hand_count)
            
            self._double_down_on_hands_if_applicable(player_hands, dealer_up_card, pre_hand_count)
            self._play_hands_as_player(player_hands, dealer_up_card, pre_hand_count)
            self._play_hand_as_dealer(player_hands, dealer_hand)

        self._determine_hand_results(player_hands, dealer_hand, pre_hand_count)
        logger.card(f'Hands played: {self._hand_analyzer.hands_played} PNL so far: {self._bankroll.balance}')

    def play_blackjack(self):
        """ The main gameplay logic """
        
        while self._hand_analyzer.hands_played < cfg.HANDS_TO_PLAY and (
            self._shoe.num_shuffles - 1) < cfg.SHUFFLES_TO_PLAY: 
            
            if self._shoe.should_reshuffle():
                logger.card(f'Reshuffling self._shoe. Dealt: {len(self._shoe.dealt)}/{self._shoe.num_cards} cards.')
                logger.card(f'Total hands played: {self._hand_analyzer.hands_played}. Bankroll: {self._bankroll.balance}')
                self._shoe.shuffle()
                self._count.reset()

            bet_size = self._determine_bet_size(self._count.count)
            player_hands = [PlayerHand(self._bankroll, bet_size, [])]
            dealer_hand = DealerHand([])
            pre_hand_count = self._count.count
            self._deal_opening_cards(player_hands, dealer_hand)
            self.play_hand(player_hands, dealer_hand, pre_hand_count)
