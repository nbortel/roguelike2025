# Automaton: Not Alone
Automaton is a traditional roguelike built in Python using the tcod libray.

Development is in the early stages. Everything subject to change.

You are a lone automaton awoken deep in the depths of a broken vault. Scavenge 
for parts and build an army of robot companions in order to climb out of the 
deep. Learn about the events that transpired in the past leading to the 
extinction of you human precursors.

## Design
I want to build a tight experience that should take no more than an hour to 
complete as a minimum product. This project is inspired by other heavyweights 
in the genre, but I want to keep the scope small at first.

The player should be able to increase strength through acquiring parts, but 
the focus is on building and upgrading your allies. Fallen allies should be 
able to be scavenged in order to recoup some of the parts used in building 
them.

I don't want there to be quite as much pressure as more difficult games such 
as Cogmind, but there should still be the risk of failure. Minimizing damage to 
your allies while maximizing the amount of parts acquired should be the key to 
success.

### Game World
The entirety of the core experience takes place in a derlict post-apocalyptic 
vault inhabited by rogue machines and mutant creatures. To start I will aim for 
six floors, each taking 10-20 minutes to clear, for an experience of 1-2 hours 
per run.

These six floors will be divided into 3 zones, with 2 floors each.

#### Maintenance
The maintenance zone is where the player first awakens. The enemies within are 
mostly of a weaker variety, and common parts are plentiful. Enemies include 
corrupt custodians, mechanics, etc. No mutant enemies encountered at this 
depth.

#### Residential
The residential zone will have fewer parts, but the ones encountered will 
generally be of higher quality. Dedicated caches of more common parts can be 
found as well. Enemies will mostly still be of mechanical variety, but there is 
potential to encounter rarer mutated enemies in these levels.

#### Administrative
The administrative zone closest to the surface will include offices and 
laboratories. Common parts are the least plentiful here, rare parts can be 
found frequently, and legendary parts can be occasionally acquired. Enemies 
here are the most dangerous and include wrathful automatons, mutated beasts, 
and more. The game is won when the player successfully ascends from this zone.

### Mechanics
Game mechanics center around the assembly of mechanical allies by the player 
automaton in order to explore, scavenge, and fight their way out of the depths.
The status of allies should be determined by which parts the player uses to 
construct them. The player should have some ability to dictate the ai behavior 
of allies as well.

When the player levels up, they should be able to integrate a part, permenantly 
increasing their strength. The number of parts they can use to create allies 
should also increase.
