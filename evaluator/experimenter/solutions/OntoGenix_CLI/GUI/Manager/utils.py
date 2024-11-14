def _manage_action(self, prompt: str) -> None:
        """Manage the user's prompt based on the current ontology state."""
        # TODO: read about @corountine (asyncio ones) vs Future. Task is subclass of Future
        try:
            self.LLManswer_textedit.setEnabled(False)
            self.log.append_log(message="\n\n------------- GUI MANAGER ----------------", level="manager", end="\n\n")
            # TODO: separate the following chunk into a separate method (it's common to every method)
            msg = ""
            #print("User's prompt: ", prompt)
            for chunk in self.genie.interaction(prompt=prompt):
                self.log.append_log(chunk, level="manager", end="")
                msg += chunk
                if self.isStopped: break
            #print("Response by Toolkit: ", msg)
        except GeneratorExit as ge:
            print(f"Process stopped/cancelled by user: {ge}")
            # Rollback to the previous step of the automaton
            self.genie.automata.droid.rollback_transition()
            self.log.append_log(message="INFO: Rolling back to previous state", level="warning", end="\n")
        except InvalidTransitionException as ite:
            print(ite)
            self.genie.automata.droid.rollback_transition()
            self.log.append_log(message="\nTransición inválida", level="manager", end="\n")
        finally:
            # TODO: self.genie.automata.droid.rollback_transition()
            self.isStopped = False
            self.log.append_log(message="", level="manager", end="\n")
            self.LLManswer_textedit.setEnabled(True)