# Elementary-Finance
Elementary financial programs while I learn the subject.
Currently there are 3 Auxiliary programs.
DataCollector is a collection of programs that can take data from uk yahoo finance to evaluate stocks.
FinancialStats is a collection of useful stats programs, means, covariance matrices...
Holiday Logic is a basic program for determining if a day is a holiday in the UK during 2019.

There are two trading programs.
Yesterdays winner uses a once a day rebalancing strategy of selling everything and buying the the most recent best performed of the Big 4 banks. It's trades are stored here https://docs.google.com/spreadsheets/d/14oI_ZUOpXOfWaD8FnwYualJLqitZXWCJh5S20huaAHI/edit?usp=sharing
CERV uses the CER model as outlined in http://faculty.washington.edu/ezivot/econ424/portfolioTheoryMatrix.pdf and the data can be found in https://docs.google.com/spreadsheets/d/1V4-ibttRKCvFJyOrqVu6AIjGC0FWr7Qb8kB0lq6e7tk/edit#gid=0

There is a Derivatives folder, in this will go all the programs related to options pricing.
Currently their is a file, this deals with pricing the most vanilla of options, Europeans and digitals.
It prices them using the Black Scholes formula, there are also two check functions using put call parity, this was so I could check that they were giving sensible answers.
There are also a few greek functions, one uses a finite difference method and can calculate the greek of all previous options and the most common greeks.
There are also some specific greek functions for European call options from the formulas. These were used to check that the finite difference method was giving sensible answers.
