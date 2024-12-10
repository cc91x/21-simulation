# Background

### Introduction

Blackjack has become one of the most popular casino games in the world, and unlike most other games, is consistently beatable - as long as the player is counting cards and using a winning strategy. This has led to the creation of a subfield of study for these various card counting strategies. A quirk of blackjack is that many casinos employ slightly different variations of the rules, specifically around edge cases. There do exist many online blackjack calculators ([see references](#blackjack-reference-materials)), but these are often limited, excluding game specific rules, and only allowing predefined strategies, leaving players unable to experiment.  
  
This project is intended to give players a way to build and test card counting strategies, using a monte carlo simulations, where all aspects of the game - including rules, number of hands, counting strategy and decision strategy - are all defined. 

### Defining player decisions

In blackjack, optimal play style can be simplified to a series of decisions (hit vs. stand, doubling down, splitting) defined in a grid with the player's hand and dealer's up card, [like this one](https://www.blackjackapprenticeship.com/blackjack-strategy-charts/). These charts are effective, but often limited, excluding most count based variations. This project adds support for these count based decisions through the [following CSVs](#csv-files), each one specifying a boolean action based on the in game scenario. The '1d' array CSVs are basic one to one mappings, and the '3d' array CSVs contain a range of true counts and a 2d grid for each one. Each CSV has column headers to help clarify their function.

# Setup

All setup happens in the [config file](config/blackjackConfig.ini)

### Setting simulation specifics  

Under `SETUP` in the config file, we configure parameters for the simulation. Most important is `COUNTING_STRATEGY_DIRECTORY`, which specifies the directory name under [strategies](strategies/) for a strategy to use. If this variable is set incorrectly, the simulation won't work. We use `basic-strategy` by default.

### Setting table rules 

Under `RULES` in the config file, we configure the table specific rules that can vary from game to game. Things like the blackjack payout, number of decks, dealer specific rules, etc.

### Adding a new counting strategy.

Create a new directory under [strategies](strategies/), and create the CSV files (which can be copied over from [templates](strategies/templates/)) to define the strategy specifics. Update the [config file](config/blackjackConfig.ini) with the name of the newly created directory. To understand how to fill out define CSVs, see [basic-strategy](strategies/basic-strategy/), and see [hi-lo](strategies/hi-lo/) for the popular hi-lo strategy.

Note: the CSV file names are hardcoded and need to be exactly as above.

### Running the simulation

After updating the config file, run the [main script](python/main.py). Results of the simulation are [logged](/logs). 

## CSV files

#### 1d CSVs - simple one to one mappings

- BET_SIZING_MAPPING.csv - the bet unit size to make dependening on the pre-hand true count. Define larger bet size when the count is favorable
- COUNT_CARD_VALUES.csv - the value assigned to each card when counting
- SHOULD_TAKE_INSURANCE_MATRIX.csv - if the player should take insurance depending on true count

#### 3d CSVs - 3d mappings, defined as multiple 2d grids. Before each 2d grid, the accompanying count is defined 

- HARD_SHOULD_DOUBLE_DOWN_MATRIX.csv - if the player should double down depending on hand total, count and the dealer's up card, with a hard hand
- SOFT_SHOULD_DOUBLE_MATRIX.csv - if the player should double down depending on hand total, count, and the dealer's up card, with a soft hand
- HARD_SHOULD_HIT_MATRIX.csv - if the player should hit (or stand) depending on hand total, count and the dealer's up card, with a hard hand
- SOFT_SHOULD_HIT_MATRIX.csv - if the player should hit (or stand) depending on hand total, count and the dealer's up card, with a soft hand
- SHOULD_SPLIT_MATRIX.csv - if the player should split depending on pair and the dealer's up card
- SHOULD_SURRENDER_MATRIX.csv - if the player should surrender given hand total and the dealer's up card

Note: Some matrices do not include full ranges of rows, like the hit matrices, which only have hand totals from 11 - 17. By default rows beyond this range will extend the nearest defined row, so a hand total from 1-10 would use 11, and 18+ would use 17.   
Note: A 'hard' hand is a hand either without any aces or aces whose value must be 1 to stay under 21, while a 'soft' hand has an ace that could be played high or low and still be under 21.  
Note: The value of 11 is used for Aces anytime it refers to a single card


# Future Enhancements 

Though the customizability is extensive, there are still elements to the game and counting strategies that are unsupported and ideally will be added in the future. For counting strategies, not included are aces side counts (used to keep a separate count for aces) and suit based strategies (some strategies, like red 7s, differentiate cards based on suit). For gameplay, most side bets, like pairs, royals, flushes, etc., are not included. Many of the common game conditions/rules were added, but there countless casinos out there which may use their own bespoke rules - and if it's not in the config file, it's not included. Other enhancements center around user features, such as providing a better output for data analysis than raw print statements, and more in depth scenario evaluation.  

## Blackjack reference materials

Rules and basic strategy  
https://bicyclecards.com/how-to-play/blackjack/  
https://www.blackjackapprenticeship.com/blackjack-strategy-charts/  

Blackjack calculators  
https://outplayed.com/blackjack-strategy-calculator  
https://wizardofodds.com/games/blackjack/strategy/calculator/  
https://wizardofodds.com/games/blackjack/calculator/ - this is for determining the house's edge, excellent for debugging here

Advanced strategy sources  
https://www.qfit.com/card-counting.htm  
https://www.youtube.com/@laytheodds9362  

YouTubers documenting their blackpack experiences  
https://www.youtube.com/@QuattroAP  
https://www.youtube.com/@stevenbridges
