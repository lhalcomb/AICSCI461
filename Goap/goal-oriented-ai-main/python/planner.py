"""
planner.py
Planning component for goal-oriented AI modeling.
Created: Chris Branton, 2023-03-07.
Adapted from a techniques presented in AI for Games, 3rd Edition, by Ian Millington
NOTE: in AI literature, discontent (what we call value) is often called "energy metric"

"""

import copy
import heapq


class Planner:

    def __init__(self, world_model):
        self.model = world_model

    def make_plan(self, current_goal):
        pass
 
    # Chooses a goal to pursue based on
    def choose_goal(self):
        # check for empty list
        if not self.model.goal_list:
            return None
        top_goal = self.model.goal_list[0]
        for candidate in self.model.goal_list[1:]:
            if candidate.get_value() > top_goal.get_value():
                top_goal = candidate
        return top_goal


class SimplePlanner(Planner):
    def __init__(self, world_model):
        super(SimplePlanner, self).__init__(world_model)

    def make_plan(self, current_goal):
        plan = []
        current_state = copy.deepcopy(self.model.current_state)

        def precondition_met(preconditions, state):
            """Check if action preconditions are met."""
            return all(state.get(key, False) for key in preconditions)
        
        def find_best_action(goal_name):
            """Find the best action for the given goal."""
            best_actions = []
            for action in self.model.action_list:
                #goal_name_str = goal_name if isinstance(goal_name, str) else goal_name.name
                if goal_name.name in action.results:
                    best_actions.append(action)

            return best_actions

        goal_stack = [current_goal]
        while goal_stack:
            goal_name = goal_stack.pop()
            best_actions = find_best_action(goal_name)
            if not best_actions:
                print(f"No actions found for goal: {goal_name.name}")
                continue

            # Sort actions by cost (optional: can modify to use priority from goal evaluation)
            best_action = min(best_actions, key=lambda x: x.get_cost)

            if precondition_met(best_action.requires, current_state):
                # Apply the action
                plan.append(best_action)
                best_action.execute(current_state)
                print(f"Action {best_action.name} executed.")
                
                # If goal is satisfied, check the next goal
                if goal_name in best_action.results:
                    print(f"Goal {goal_name} achieved.")
                    continue
            else:
                # Add preconditions as new goals if they are not met
                goal_stack.extend(best_action.requires)

        return plan

    

    def evaluate_goal_priority(self, goal_name, state):
        """Dynamically prioritize goals based on need and their value in the config."""
        priority = 0
        goal = next((g for g in self.config['goal_list'] if g['name'] == goal_name), None)

        """ 
        Generator Expression:
            Iterates over self.config['goal_list'] and yields the first goal where g['name'] matches goal_name.
        next():
            Retrieves the first matching goal from the generator, or returns None if no match is found.
        Purpose:
            Used to find a goal in self.config['goal_list` that matches goal_name, safely returning None if no match exists.
        
        """

        if goal:
            # Use the value from config to assign initial priority
            priority += goal['value']
            
            # Specific adjustments based on state
            if goal_name == "increase_population":
                if state.get("food", 0) < 50:
                    priority -= 20  # Discourage population growth if food is low
                elif state.get("housing", 0) < state.get("population", 0) // 5:
                    priority -= 10  # Discourage if housing is insufficient

            elif goal_name == "harvest_resources":
                if state.get("resources", 0) < 20:
                    priority += 10  # Critical need for resources
                elif state.get("resources", 0) < 50:
                    priority += 3  # Moderate need

        return priority
    



class GoapPlanner(Planner):
    def __init__(self, world_model):
        super(GoapPlanner, self).__init__(world_model)
