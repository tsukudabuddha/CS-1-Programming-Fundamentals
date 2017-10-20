class Logger(object):
    '''
    Utility class responsible for logging all interactions of note during the
    simulation.


    _____Attributes______

    file_name: the name of the file that the logger will be writing to.

    _____Methods_____

    __init__(self, file_name):

    write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
        basic_repro_num):
        - Writes the first line of a logfile, which will contain metadata on the
            parameters for the simulation.

    log_interaction(self, person1, person2, did_infect=None, person2_vacc=None, person2_sick=None):
        - Expects person1 and person2 as person objects.
        - Expects did_infect, person2_vacc, and person2_sick as Booleans, if passed.
        - Between the values passed with did_infect, person2_vacc, and person2_sick, this method
            should be able to determine exactly what happened in the interaction and create a String
            saying so.
        - The format of the log should be "{person1.ID} infects {person2.ID}", or, for other edge
            cases, "{person1.ID} didn't infect {person2.ID} because {'vaccinated' or 'already sick'}"
        - Appends the interaction to logfile.

    log_infection_survival(self, person, did_die_from_infection):
        - Expects person as Person object.
        - Expects bool for did_die_from_infection, with True denoting they died from
            their infection and False denoting they survived and became immune.
        - The format of the log should be "{person.ID} died from infection" or
            "{person.ID} survived infection."
        - Appends the results of the infection to the logfile.

    log_time_step(self, time_step_number):
        - Expects time_step_number as an Int.
        - This method should write a log telling us when one time step ends, and
            the next time step begins.  The format of this log should be:
                "Time step {time_step_number} ended, beginning {time_step_number + 1}..."
        - STRETCH CHALLENGE DETAILS:
            - If you choose to extend this method, the format of the summary statistics logged
                are up to you.  At minimum, it should contain:
                    - The number of people that were infected during this specific time step.
                    - The number of people that died on this specific time step.
                    - The total number of people infected in the population, including the newly
                        infected
                    - The total number of dead, including those that died during this time step.
    '''

    def __init__(self, file_name):
        """Initialize logger with file_name as the file name."""
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name,
                       mortality_rate, basic_repro_num):
        """Write metadata to file."""
        parameters = [pop_size, vacc_percentage, virus_name, mortality_rate,
                      basic_repro_num]
        parameter_string = ""
        for param in parameters:
            parameter_string += (str(param) + "\t")

        with open(self.file_name, "w") as f:
            f.write(parameter_string + "\n")

    def log_interaction(self, person1, person2, did_infect=None,
                        person2_vacc=None, person2_sick=None):
        """Log interactions between infected person and random person."""
        print("Person for log id: %s" % person1._id)
        print("Random for log id: %s" % person2._id)
        with open(self.file_name, "a") as f:
            if did_infect:
                f.write(str(person1._id) + " infects " + str(person2._id) + "\n")
            elif person2_sick:
                f.write(str(person1._id) + " didn't infect " + str(person2._id) +
                        " because they were already sick\n")
            elif person2_vacc:
                f.write(str(person1._id) + " didn't infect " + str(person2._id) +
                        " because they were vaccinated\n")

    def log_infection_survival(self, person, did_die_from_infection):
        """Log whether or not the person died."""
        with open(self.file_name, 'a') as f:
            if did_die_from_infection:
                f.write(str(person._id) + " died from infection\n")
            else:
                f.write(str(person._id) + " survived infection.\n")

    def log_time_step(self, time_step_number):
        """Log time step event."""
        with open(self.file_name, 'a') as f:
            f.write("Time step %i ended, beginning " % time_step_number +
                    "%i...\n" % (time_step_number + 1))
        # NOTE: Stretch challenge opportunity! Modify this method so that at
        # the end of each time step, it also logs a summary of what happened
        # in that time step, including the number of people infected, the
        # number of people dead, etc.  You may want to create a helper class
        #  to compute these statistics for you,
        #  as a Logger's job is just to write logs!
