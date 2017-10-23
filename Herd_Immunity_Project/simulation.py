"""Simulation Script."""
import random as r
import sys
from person import Person
from logger import Logger

r.seed(42)


class Simulation(object):
    '''
    Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments
    when file is run.

    Simulates the spread of a virus through a given population.
    The percentage of the population that are vaccinated, the size of the
    population, and the amount of initially infected people in a population
    are all variables that can be set when the program is run.

    _____Attributes______

    logger: Logger object.  The helper object that will be responsible for
    writing all logs to the simulation.

    population_size: Int.  The size of the population for this simulation.

    population: [Person].  A list of person objects representing all people in
        the population.

    next_person_id: Int.  The next available id value for all created person
    objects.
        Each person should have a unique _id value.

    virus_name: String.  The name of the virus for the simulation.  This will
    be passed to the Virus object upon instantiation.

    mortality_rate: Float between 0 and 1.  This will be passed
    to the Virus object upon instantiation.

    basic_repro_num: Float between 0 and 1.   This will be passed
    to the Virus object upon instantiation.

    vacc_percentage: Float between 0 and 1.  Represents the total percentage
    of population vaccinated for the given simulation.

    current_infected: Int.  The number of currently people in the population
    currently infected with the disease in the simulation.

    total_infected: Int.  The running total of people that have been infected
    since the simulation began, including any people currently infected.

    total_dead: Int.  The number of people that have died as a result of the
    infection during this simulation.  Starts at zero.


    _____Methods_____

    __init__(population_size, vacc_percentage, virus_name, mortality_rate,
     basic_repro_num, initial_infected=1):
        -- All arguments will be passed as command-line arguments when the file
            is run.
        -- After setting values for attributes, calls self._create_population()
            in order to create the population array that will be used for this
            simulation.

    _create_population(self, initial_infected):
        -- Expects initial_infected as an Int.
        -- Should be called only once, at the end of the __init__ method.
            -- Stores all newly created Person objects in a local variable,
        population.
        -- Creates all infected person objects first.  Each time a new one is
            created, increments infected_count variable by 1.
        -- Once all infected person objects are created, begins creating
            healthy person objects.  To decide if a person is vaccinated or
            not, generates a random number between 0 and 1.  If that number is
            smaller than self.vacc_percentage, new person object will be
            created with is_vaccinated set to True.  Otherwise, is_vaccinated
            will be set to False.
        -- Once len(population) is the same as self.population_size,
            returns population.
    '''

    def __init__(self, population_size, vacc_percentage, virus_name,
                 mortality_rate, basic_repro_num, initial_infected=1):
        """Initialize simulation parameters."""
        self.population_size = population_size
        self.population = []
        self.total_infected = 0
        self.current_infected = 0
        self.next_person_id = 0
        self.virus_name = virus_name
        self.mortality_rate = mortality_rate
        self.basic_repro_num = basic_repro_num
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, population_size, vacc_percentage, initial_infected)

        self.logger = Logger(self.file_name)
        # Create list to hold the newly infected peopel
        self.newly_infected = []

        # Create and save initial population
        self.population = self._create_population(initial_infected,
                                                  vacc_percentage)

        # Begin Log
        self.logger.write_metadata(population_size, vacc_percentage,
                                   virus_name, mortality_rate, basic_repro_num)

    def _create_population(self, initial_infected, vacc_percentage):
        """Create beginning population."""
        population = []
        infected_count = 0
        vaccinated_count = 0
        non_vacc_count = 0
        while len(population) != self.population_size:
            id_number = len(population)
            if infected_count < initial_infected:
                population.append(Person(id_number, False, True))
                infected_count += 1
            else:
                if r.random() < vacc_percentage:
                    population.append(Person(id_number, True, False))
                    vaccinated_count += 1
                else:
                    population.append(Person(id_number, False, False))
                    non_vacc_count += 1
        return population

    def _simulation_should_continue(self):
        """Check if anyone is still alive, then return result."""
        should_end = None
        for person in self.population:
            if not person.is_alive:
                should_end = True
            else:
                if person.infected:
                    should_end = False
                    break
                else:
                    should_end = True

        return not should_end  # Checking if should continue so reverse

    def run(self):
        """Run simulation until everyone is dead or the virus is eradicated."""
        self.time_step_counter = 0

        should_continue = self._simulation_should_continue()

        while should_continue:
            self.time_step_counter += 1
            self.time_step()

            should_continue = self._simulation_should_continue()

        print("The simulation has ended after " + str(self.time_step_counter) +
              " turns.")

    def infected_helper(self, person, alive_list):
        """Validate person."""
        interaction_counter = 0
        if person.infected and person.is_alive:
            while interaction_counter < 100:
                pop_size = len(alive_list) - 1
                random_id = r.randint(0, pop_size)
                if random_id is not person._id:
                    random_person = alive_list[random_id]
                    if random_person.is_alive:
                        self.interaction(person, random_person)
                        interaction_counter += 1
            # After interactions are over, check if person is still alive
            if not person.did_survive_infection(self.mortality_rate):
                alive_list.remove(person)

            self.logger.log_infection_survival(person, not person.is_alive)

    def time_step(self):
        """Iterate step by one."""
        alive_list = list(filter(lambda person: person.is_alive,
                                 self.population))
        for person in self.population:
            self.infected_helper(person, alive_list)
        # Make sure to mark the newly infected peoples as infected
        self._infect_newly_infected()

        self.logger.log_time_step(self.time_step_counter)

    def interaction(self, person, random_person):
        """Check if infected person spreads disease to random."""
        assert person.is_alive is True
        assert random_person.is_alive is True

        did_infect = None

        if not random_person.is_vaccinated:
            if not random_person.infected:
                if r.random() < self.basic_repro_num:
                    self.newly_infected.append(random_person._id)
                    did_infect = True

        # Log interaction
        self.logger.log_interaction(person, random_person, did_infect,
                                    random_person.is_vaccinated,
                                    random_person.infected)

    def _infect_newly_infected(self):
        """Go through population and mark the new infected people."""
        for _id in self.newly_infected:
            self.population[_id].infected = True

        # Clear newly_infected
        self.newly_infected = []


if __name__ == "__main__":
    params = sys.argv[1:]
    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    basic_repro_num = float(params[4])
    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1
    simulation = Simulation(pop_size, vacc_percentage, virus_name,
                            mortality_rate, basic_repro_num,
                            initial_infected)
    simulation.run()
