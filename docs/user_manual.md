# PandemicPanic User Manual
## Introduction
PandemicPanic&trade; places you, the player, at the helm of the Dutch Cabinet at the start of a global pandemic.

About two hundred cases have already been confirmed in the Netherlands, spread over every one of the twelve provinces. 
The virus is very infectious and patients will quickly overwhelm hospitals if it is allowed to spread freely.
 
However, because the death rate is low and most infected don't experience any symptoms outside of a runny nose or a mild fever,
there is much skepticism about whether the government should take strict measures to contain the infection.

## Goal
It is your job find a balance between letting the virus run wild, potentially killing more than a million inhabitants, and
calling a full lockdown, destroying the economy and leading to civil unrest.

To do this, you need to take the right measures in the right place at the right time. You have the following eight measures available to you:
1. distance: people must keep 1.5 meter distance between themselves and other in public spaces.
2. lockdown: people must work from home as much as possible.
3. mask: people must wear a face mask in public spaces.
4. restaurants: close all restaurants, cafes, and hotels.
5. events: limit events and leisure activities to small groups.
6. visitors: allow at most 6 visitors from different households per day.
7. quarantine: people experiencing any symptoms must stay at home.
8. education: all forms of education must be taught online as much as possible.

All these measures will reduce the reproduction number (R-factor), which signifies how many people a single patient will infect while carrying the virus.

Because very little is known about the virus, the exact effect of these measures is unknown, and neither as the base R-factor if none of them are taken.
What is known, however, is that the virus spreads easier in densely populated regions with many young, active inhabitants. 
It also has a higher death rate in regions with an older population, which will increase even more if the hospitals are full.

Keep in mind that all measures will be unpopular, and that this unpopularity is increased if
they are taken when the number of infections is still very low or when they are active for too long.

## Instruction
Start the game by running the 'game.py' file in the project-folder.

When the game is started, you'll be asked if you want to play in terminal mode or visual mode. 
Visual mode is recommended, so input a 'v' and hit enter,

When the game is started, a week has already passed since the first confirmed cases, and more have appeared since.
You'll see three main objects on your screen: 

On the left: a map displaying the current status of every province. The redder, the more infections per 100,000 inhabitants there are. 
If a warning sign appears on province, that means the hospitals are full.

Top-right: a matrix allowing you to choose which measures (rows) to take in which province (columns) for the following week. 
Simply click a square to turn a measure on (green) or off (red), click the abbreviation of a province to activate every measure there,
or click on the number of a measure to activate it in every province. 
You can also activate every measure, everywhere by clicking the button in the top-left cell.

Bottom-right: a table with more detailed information on new and current infected and deaths caused by the virus.
Use this to estimate the effect of your measures.

Once you have decided which measures to take, click the 'next turn'-button to advance to the next week and see their effects.
After 52 weeks, the game will end and you will see your final death count, as well as your score, which is influenced by
both the amount of deaths and the measures you've taken.
If you then exit the game, you'll be presented with plotted data of the number of infections and the death count.

If you wish to play in terminal mode, input 't' after starting the game. 
In this mode, there is only one region and you can only take or remove one measure each week, but you'll get more data, 
including the amount of recoveries made and the R-value.

# Controls
In visual mode, everything can be done with your mouse. However, there are a few shortcuts:
- to view a short description of the measures in the matrix, press [SPACE].
- to advance to the next week, press [ENTER]
- to end the game, press [ESC]. You won't get a score, but you will see your death count and plots.

# Hints
The game can be quite hard, so here are some hints to help you on your way:

- Once a person is infected, they'll be sick for two weeks, in which they infect others according to the R-factor.
After two weeks, they either die or recover and stay immume to the virus (forever!).

- As said before, your score is influenced by both the amount of deaths and the measures you've taken.
Measures are always unpopluar, and will always cost you points, but they will cost you more if they are viewed as
too strict or if people are growing tired of them.
More specifically, you will get a larger penalty if:
    - They are active while less than 0.1% of the population of that region is infected. 
When this is the case, the region will appear green on the map.
    - They have been active for more than 10 weeks. You'll have to keep track of this on your own, 
so you might want to vary your measures over time*.

- You'll get penalized for every death that occurs. Every death counts equally, 
but there will be more deaths if the hospitals are full, which happens once 2% of the population gets infected.

- Provinces aren't isolated. If a province has much less infected than their neighbour, 
some of that neighbour's infections will 'leak' over the border.

*also, cheesing the system by applying a measure for 9 weeks, lifting it for one, and then reapplying it won't work.
