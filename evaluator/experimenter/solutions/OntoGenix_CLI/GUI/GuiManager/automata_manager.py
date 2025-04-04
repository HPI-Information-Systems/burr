from evaluator.experimenter.solutions.OntoGenix_CLI.GUI.OntoGenixExceptions import AutomataException

class State:
    def __init__(self, name):
        self.name = name

class Transition:
    def __init__(self, from_state, to_state, action, requires_confirmation):
        self.from_state = from_state
        self.to_state = to_state
        self.action = action
        self.requires_confirmation = requires_confirmation

    def is_valid(self, reached_states):
        # TODO: check if this condition is neccessary
        if self.from_state.name == "PROMPT_CRAFT" and self.to_state.name == "ONTOLOGY_ENTITY":
            # Check if ONTOLOGY has been reached previously
            return "ONTOLOGY" in [state.name for state in reached_states]
        return True

class Automaton:
    def __init__(self):
        self.states = {}
        self.transitions = []
        self._reached_states = list()

        # Set the automaton initial states
        self.last_state = None
        self.current_state = None
        self.action = None

    @property
    def reached_states(self):
        return list(self._reached_states)

    def add_state(self, name):
        state = State(name)
        self.states[name] = state
        return state

    def add_transition(self, from_state, to_state, action, requires_confirmation):
        transition = Transition(from_state, to_state, action, requires_confirmation)
        self.transitions.append(transition)

    def can_transition(self, from_state, to_state):
        print("can_transition ->", ' from_state ', from_state.name, ' to_state ', to_state.name )
        for transition in self.transitions:
            if (
                transition.from_state.name == from_state.name
                and transition.to_state.name == to_state.name
            ):
                if not transition.is_valid(self.reached_states):
                    return False  # Transition is not valid based on conditions
                return True
        return False

    def perform_transition(self, to_state):
        if self.can_transition(self.current_state, to_state):
            self._reached_states.append(to_state) # TODO: change to list of states to add backtracking
            self.last_state = self.current_state
            self.current_state = to_state
            return True
        else:
            raise AutomataException.InvalidTransitionException(
                f"{self.current_state.name} -> {to_state.name}"
            )
        #return False

    def rollback_transition(self):
        # TODO: maybe put an option to rollback to more than one state or to a particular state
        # self.current_state = self.last_state
        # self._reached_states.remove(self.current_state)
        try:
            if not self._reached_states:
                self.current_state = None
                self.last_state = None 
            else:
                self.current_state = self._reached_states.pop()
                self.last_state = self._reached_states[-1] if self._reached_states else None
        except IndexError:
            # IndexError: pop from empty list
            self.last_state = None
        return True

    def possible_next_states(self):
        possible_states = []
        for transition in self.transitions:
            if transition.from_state.name == self.current_state.name:
                possible_states.append(transition.to_state.name)
        return possible_states

#TODO: add enum with possible states (?)
class Automata_Manager:

    def __init__(self):
        # Create the automaton
        self.droid = Automaton()

        # Define states
        PROMPT_CRAFT = self.droid.add_state("PROMPT_CRAFT")
        HIGH_LEVEL_STRUCTURE = self.droid.add_state("HIGH_LEVEL_STRUCTURE")
        ONTOLOGY = self.droid.add_state("ONTOLOGY")
        ONTOLOGY_ENTITY = self.droid.add_state("ONTOLOGY_ENTITY")
        MAPPING = self.droid.add_state("MAPPING")
        NONE = self.droid.add_state("None")

        # Set initial states
        self.droid.current_state = NONE

        # Define transitions
        self.droid.add_transition(NONE, PROMPT_CRAFT, "prompt_crafting", False)
        self.droid.add_transition(NONE, HIGH_LEVEL_STRUCTURE, "data_description", False)

        self.droid.add_transition(PROMPT_CRAFT, PROMPT_CRAFT, "prompt_crafting", True)
        self.droid.add_transition(PROMPT_CRAFT, HIGH_LEVEL_STRUCTURE, "data_description", True)
        # self.droid.add_transition(PROMPT_CRAFT, ONTOLOGY_ENTITY, "ontology_building", True)

        self.droid.add_transition(HIGH_LEVEL_STRUCTURE, PROMPT_CRAFT, "prompt_crafting", False)
        self.droid.add_transition(HIGH_LEVEL_STRUCTURE, HIGH_LEVEL_STRUCTURE, "data_description", False)
        self.droid.add_transition(HIGH_LEVEL_STRUCTURE, ONTOLOGY, "ontology_building", False)
        self.droid.add_transition(HIGH_LEVEL_STRUCTURE, MAPPING, "mapping", False)

        # self.droid.add_transition(ONTOLOGY, PROMPT_CRAFT, "prompt_crafting", False)
        self.droid.add_transition(ONTOLOGY, HIGH_LEVEL_STRUCTURE, "data_description", False)
        self.droid.add_transition(ONTOLOGY, ONTOLOGY, "data_description", False)
        self.droid.add_transition(ONTOLOGY, ONTOLOGY_ENTITY, "ontology_entity_enrichment", False)
        self.droid.add_transition(ONTOLOGY, MAPPING, "mapping", False)

        # self.droid.add_transition(ONTOLOGY_ENTITY, PROMPT_CRAFT, "prompt_crafting", False)
        self.droid.add_transition(ONTOLOGY_ENTITY, HIGH_LEVEL_STRUCTURE, "data_description", False)
        self.droid.add_transition(ONTOLOGY_ENTITY, ONTOLOGY, "data_description", False)
        self.droid.add_transition(ONTOLOGY_ENTITY, ONTOLOGY_ENTITY, "ontology_entity_enrichment", False)
        self.droid.add_transition(ONTOLOGY_ENTITY, MAPPING, "mapping", False)

        self.droid.add_transition(MAPPING, PROMPT_CRAFT, "prompt_crafting", False)
        self.droid.add_transition(MAPPING, HIGH_LEVEL_STRUCTURE, "data_description", False)
        self.droid.add_transition(MAPPING, ONTOLOGY_ENTITY, "ontology_entity_enrichment", False)
        self.droid.add_transition(MAPPING, MAPPING, "mapping", False)
