I started out setting base_r to 2 and base_inf to 10.

I think the eight measures can generally be separated into two categories: cancellations and rules.

The cancellations can be roughly ordered in the amount of traveling and human contact they prevent. In my opinion, a logical order looks like this:
1. lockdown
2. education
3. events
4. restaurants
5. visitors

Working from home obviously prevents the most human contact, followed by education.
Events and restaurants maybe could be switched around, but if you consider things like amateur sports or theme parks as events, I think it makes sense to put it in front. 
Maybe renaming events to a more general 'leisure' or something would make this more clear.
Visitors mean small-scale events like birthdays and such, so they'll probably feature less than 20 people most of the time, which puts them at the bottom.


The other three measures are rules people have to follow. 
Ordering them by their effect is a bit harder, but it's easy to guess which one will be followed more:
1. quarantine
2. distance
3. masks

Staying home with symptoms is probably the easiest to follow for most people, and wearing masks everywhere is probably the hardest.
Let's say all three of these measures basically prevent you from infecting other if you're already carrying the virus, meaning their effect would be the same if they were all followed to the same degree.
This means we can use the discipline-order as an effect-order!

So, the following two orders can be established:
lockdown > education > events > restaurants > visitors
quarantine > distance > masks

As a base case, I put the weakest measures at 0.95 and every stronger one at 0.05 less. This gave the following list:
1. distance,keep 1.5 meter distance,0.90
2. lockdown,people must work from home,0.75
3. mask,wear a mask in public areas,0.95
4. restaurants,close all restaurants,0.90
5. events,limit the allowed event size,0.85
6. visitors,allow at most 6 visitors at home,0.95
7. quarantine,people with symptoms must stay home,0.85
8. education,education must be taught online,0.80

Using the three best measures gives a reduction of 0,51, which already almost stabilises the infection,
so I decided to raise this to 2.2.

Then, I tried a whole bunch of strategies, which I won't list here, but I came to some interesting conclusions:
The good:
- the adjacency makes isolating a single region very difficult, but not impossible if the surrounding regions go to 0 infections.
- it's hard to go back from code black, so preventing this is better than reacting to it.
The bad:
- simply choosing the beast measures works a bit too well for some of the easier regions like Drenthe
- the weaker measures have very little effect on the more difficult regions

Based on the last two notes, I buffed the weaker measures a bit on nerfed the strong ones. 
I kept doing this several times, eventually deciding not to couple the two categories as strongly anymore (so mask is now more effective than vistors)
As we do not have a score system yet, it's difficult to estimate how many measures we want the player to take, and how many deaths should be acceptable.
As a benchmark, I tried having the 5 strongest measures at the start reduce the infection in most regions, and then deactivating them while trying not to reach code black.
This way, I kept the death toll around 80.000, which is probably a bit too high to be realistic.

Finally, I settled on the following balancing of the measures:
1. distance,keep 1.5 meter distance,0.91
2. lockdown,people must work from home,0.78
3. mask,wear a mask in public areas,0.93
4. restaurants,close all restaurants,0.90
5. events,limit the allowed event size,0.85
6. visitors,allow at most 6 visitors at home,0.94
7. quarantine,people with symptoms must stay home,0.87
8. education,education must be taught online,0.83

Their effect is now a bit stronger than Willem's estimates, but as the effective base R is also higher due to the regional factors, I think that's a fair compromise.

I think some adjustments could still be made for regions reaching zero or a very low amount of infections.
If they're adjacent to a region with a large amount of infected, they should still receive some. 
AKA the exchange should be asymmetruc in such cases, say a traveler infecting someone and returning home.
OR: a small bit of randomness could be introduced, simply adding ten or so infected to a random province every time or something.

As for the score system, I think a 'code white' could be implemented. If a region has a very small amount of infections, 
the score calculation is adjusted to heavily penalise superfluous measures. This would discourage players from taking too many measures,
while also introducing risks if regions can get re-infected.