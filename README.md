# Evolve_Tweets_2.0

My second attempt at generating meaningful sentences using a genetic algorithm. This time, instead of evolvinng grammar structure, 
it is evolving word type combinations. 

It starts with a template

The SUBJECT had to VERB

Then, each individual in a population has a subject type and a verb type. The individual will randomly pick of subject and a verb of 
that type. For example, subject type ANIMALS could pick "hamsters". It then fills in the template with its words.

The hamsters had to party.

There are 5 individuals in a population, so 5 sentences total. A user then ranks each sentence based on how funny or suitable they are. 
That rank gives each indivudal a fitness, making them more likely to crossover into the next generations.

Individuals crossover word types, and mutate word types to get a random new word type. 
