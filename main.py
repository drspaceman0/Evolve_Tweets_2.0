import random
import copy
import os
__author__ = 'eric'

POP_SIZE = 5
SUBJECT_CATEGORY_FILE = os.getcwd() + "subject_types.txt"
VERB_CATEGORY_FILE = os.getcwd() + "verb_types.txt"
TEMPLATE_FILE = os.getcwd() + "templates.txt"
SUBJECT_FILE = os.getcwd() + "subjects.txt"
VERB_FILE = os.getcwd() + "verbs.txt"


class Individual:

    def __init__(self, template):

        # Type of subject. Retrieved from subject types list
        self.subject_type = get_rand_type(SUBJECT_CATEGORY_FILE)

        # The subject. Randomly grabbed from the list of its type
        self.subject = get_word(self.subject_type, SUBJECT_FILE)

        # Type of verb. Retrieved from verb types list
        self.verb_type = get_rand_type(VERB_CATEGORY_FILE)

        # The verb. Randomly grabbed from the list of its type
        self.verb = get_word(self.verb_type, VERB_FILE)

        self.sentence = ""
        self.fitness = 0
        self.fill_template(template)

    def fill_template(self, template):
        """
        Fill in sentence template with the individual's subject and verb

        """
        template = template.replace("SUBJECT", self.subject)
        self.sentence = template.replace("VERB", self.verb)

    def change_type(self, category, new_type, template):
        """
        Change individuals subject or verb category. Then fill in sentence template

        """
        if category == "SUBJECT":
            self.subject_type = new_type
            self.subject = get_word(new_type, SUBJECT_FILE)
        elif category == "VERB":
            self.verb_type = new_type
            self.verb = get_word(new_type, VERB_FILE)
        self.fill_template(template)

    def increment_fitness(self, x):
        self.fitness = self.fitness + x

    def reset_words(self):
        self.subject = get_word(self.subject_type, SUBJECT_FILE)
        self.verb = get_word(self.verb_type, VERB_FILE)

    def get_sentence(self):
        return self.sentence

    def get_fitness(self):
        return self.fitness


def get_rand_type(file):
    size = sum(1 for _ in open(file))
    fo = open(file, "r")
    rand_num = random.randint(0, size)
    for x in xrange(rand_num):
        fo.readline()
    word = fo.readline()
    fo.close()
    word = word.rstrip()
    return word


def get_word(type, file):
    """
    Grab word randomly from list of that type

    """
    type_length = -1
    start = 0
    found_type = False
    with open(file) as myFile:
        # search file for type
        for num, line in enumerate(myFile, 1):
            if type in line:
                start = num # location of type
                type_length = -3
                found_type = True
            if found_type:
                type_length += 1
            if found_type and '#' in line:
                break
    rand_num = random.randint(start, start+type_length)
    i = 0
    f = open(file)
    for line in f:
        if i == rand_num:
            return line.rstrip()
        i += 1


def assign_fitness(population):
    sentences = []
    for indiv in population:
        sentences.append(indiv.get_sentence())
    count = 0
    while count != len(sentences):
        for x in xrange(len(sentences)):
            print str(x+1) + ".) " + sentences[x]
        print "Input favorite tweet's number"
        choice = raw_input()
        while not choice.isdigit():
            choice = raw_input()
        choice = int(choice) - 1
        while int(choice) >= len(sentences) or sentences[choice] == "xxx":
            choice = int(raw_input()) - 1
        population[choice].increment_fitness(count)
        sentences[choice] = "xxx"
        count += 1


def return_best_individual(population):
    best_indiv = population[0]
    for x in population:
        if best_indiv.fitness > x.fitness:
            best_indiv = x
    return best_indiv


def initial_population(size):
    population = []
    template = get_rand_type("TEMPLATE")
    for _ in xrange(size):
        population.append(Individual(template))
    assign_fitness(population)
    return population


def selection(population, degree):
    selected_indiv = copy.copy(population[random.randint(0,len(population)-1)])
    for x in xrange(3):
        rand_indiv = copy.copy(population[random.randint(0,len(population)-1)])
        if degree == "high":
            if rand_indiv != selected_indiv and rand_indiv.fitness < selected_indiv.fitness:
                selected_indiv = rand_indiv
        if degree == "low":
            if rand_indiv != selected_indiv and rand_indiv.fitness > selected_indiv.fitness:
                selected_indiv = rand_indiv
    return selected_indiv


def next_generation(population):
    next_pop = []
    template = get_rand_type("TEMPLATE")
    elite_indiv = return_best_individual(population)
    elite_indiv.fill_template(template)
    next_pop.append(elite_indiv)
    for x in xrange(0, len(population)-1, 2):
        indiv1 = copy.copy(selection(population, "high"))
        indiv2 = copy.copy(selection(population, "high"))
        while indiv1.get_sentence() == indiv2.get_sentence():
            indiv2 = selection(population, "high")

        # crossover
        if random.randint(0,100) >= 30:
            if random.randint(0,100) <= 50:
                temp = copy.copy(indiv1.subject_type)
                indiv1.change_type("SUBJECT", indiv2.subject_type, template)
                indiv2.change_type("SUBJECT", temp, template)
            else:
                temp = copy.copy(indiv1.verb_type)
                indiv1.change_type("VERB", indiv2.verb_type, template)
                indiv2.change_type("VERB", temp, template)
        # mutation
        if random.randint(0,100) <= 50:
            indiv1.change_type("SUBJECT", get_rand_type("SUBJECT"), template)
            indiv2.change_type("SUBJECT", get_rand_type("SUBJECT"), template)
        else:
            indiv1.change_type("VERB", get_rand_type("VERB"), template)
            indiv2.change_type("VERB", get_rand_type("VERB"), template)

        next_pop.append(indiv1)
        next_pop.append(indiv2)

    print len(next_pop)
    assign_fitness(next_pop)
    return next_pop


def next_generation_more_crossover(population):
    next_pop = []
    template = get_rand_type("TEMPLATE")
    elite_indiv = return_best_individual(population)
    elite_indiv.fill_template(template)
    next_pop.append(elite_indiv)
    for x in xrange(0, len(population)-1,):
        indiv = copy.copy(selection(population, "high"))

        # crossover
        if random.randint(0,100) <= 30:
            crossover_buddy = copy.copy(selection(population, "high"))
            if random.randint(0,100) <= 50:
                temp = copy.copy(indiv.subject_type)
                indiv.change_type("SUBJECT", crossover_buddy.subject_type, template)
            else:
                temp = copy.copy(indiv.verb_type)
                indiv.change_type("VERB", crossover_buddy.verb_type, template)
        # mutation
        if random.randint(0,100) <= 50:
            indiv.change_type("SUBJECT", get_rand_type("SUBJECT"), template)
        else:
            indiv.change_type("VERB", get_rand_type("VERB"), template)
        indiv.reset_words()
        next_pop.append(indiv)

    print len(next_pop)
    assign_fitness(next_pop)
    for x in next_pop:
        print x.get_fitness()
    return next_pop


def check_for_repeats(population, template):
    for x in xrange(len(population)):
        for y in xrange(x+1, len(population)):
            while population[x].get_sentence() == population[y].get_sentence():

                print "blooo"
                print str(x) + "     " + str(y)
                print population[x].get_sentence()
                print population[y].get_sentence()
                if random.randint(0,100) <= 50:
                    if random.randint(0,100) <= 50:
                        population[x].change_type("SUBJECT", get_rand_type("SUBJECT"), template)
                    else:
                        population[x].change_type("VERB", get_rand_type("VERB"), template)

pop = initial_population(POP_SIZE)
for _ in xrange(3):
    npop = next_generation_more_crossover(pop)
for x in npop:
    print x.fitness