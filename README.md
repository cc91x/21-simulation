
Add Readme here
Did we ever get betting size to be variable? 

Link to one or two basic blackjack calculators - https://outplayed.com/blackjack-strategy-calculator
https://wizardofodds.com/games/blackjack/strategy/calculator/
https://wizardofodds.com/games/blackjack/calculator/

As well as the order of operations, etc,. https://www.youtube.com/watch?v=XP3PcptUP8w

- Just checked out, so far, done nothing
Steps to setup:
Add a section with all the csvs...?

Check if Aces become hard once it HAS to be a 1 ... (i.e. if the Ace being 11 would make it > 21, then it's no longer soft)


# Introduction 

link ideas, existing online calculators, reference materials for rules and flow of play 

### Defining player decisions

Blackjack layer decisions can be famously predefined. You may be familair with basic strategy charts [like this](link) that define an optimal play style. These charts are effective, however, they only define the basic hit or stand decision, and exclude other player decisions such as splitting, double, bet sizing, counting. This project allows these decisions to be predefined in the following CSVs.

#### 2d CSVs - these are simple one to one mappings

- BET_SIZING_MAPPING.csv - the bet unit size to make dependening on the pre-hand true count. Useful when the count is favorable. 
- COUNT_CARD_VALUES.csv - the value assigned to each card when counting.
- SHOULD_TAKE_INSURANCE_MATRIX.csv - if the player should take insurance depending on true count.

#### 3d CSVs - these are 3d mappings, defined as multiple 2d grids. Before each 2d grid, the accompanying count is defined 

- HARD_SHOULD_DOUBLE_DOWN_MATRIX.csv - if the player should double down depending on hand total, count and the dealer's up card, with a hard hand.
- SOFT_SHOULD_DOUBLE_MATRIX.csv - if the player should double down depending on hand total, count, and the dealer's up card, with a soft hand.
- HARD_SHOULD_HIT_MATRIX.csv - if the player should hit (or stand) depending on hand total, count and the dealer's up card, with a hard hand.
- SOFT_SHOULD_HIT_MATRIX.csv - if the player should hit (or stand) depending on hand total, count and the dealer's up card, with a soft hand.
- SHOULD_SPLIT_MATRIX.csv - if the player should split depending on pair and the dealer's up card. 

Notes: A 'hard' hand is a hand either without any aces or aces whose value must be 1 to stay under 21, while a 'soft' hand has an ace that could be played high or low and still be under 21.

# Setup

All setup happens in the [config file](config/blackjackConfig.ini)

### Setting simulation specifics  

Under `SETUP` in the config file, we configure parameters for the simulation. Most important is `COUNTING_STRATEGY_DIRECTORY`, which specifies the directory name under [strategies](strategies/) for a strategy to use. If this variable is set incorrectly, the simulation won't work. We use `basic-strategy` by default.

### Setting table rules 

Under `RULES` in the config file, we configure the table specific rules that can vary from game to game. Things like the blackjack payout, number of decks, dealer specific rules, etc.

### Adding a new counting strategy.

Create a new directory under [strategies](strategies/), and create the CSV files (which can be copied over from [templates](strategies/templates/)) to define the strategy specifics. The CSV files, and their functions, are:
For strategies that do not involve counting, see how the CSVs are populated under [basicStrategy](strategies/basicStrategy/)

Note: the CSV file names are hardcoded and need to be exactly as above.

### Running the simulation

After updating the config file, run the [main script](python/main.py). Results are logged. 

## Blackjack reference materials

add links here and their use 
