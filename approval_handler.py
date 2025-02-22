from ticket import Epic, Issue
from multipledispatch import dispatch

# Create a class to handle approval logic for proposed epics and issues.

class ApprovalHandler:
    """
    A class to handle approval logic for proposed epics and issues.
    """
    def __init__(self):
        # Store the current state of the tickets
        self.tickets = {}
        self.new_tickets = {}

    @dispatch(Epic)
    def add_ticket(self, ticket: Epic):
        print(f"Adding epic {ticket.id}")
        if isinstance(ticket, Epic):
            # Check if the epic is already in the tickets dictionary
            if f"epic_{ticket.id}" in self.tickets:
                raise ValueError(f"Epic with ID {ticket.id} already exists in tickets")
            else:
                self.tickets[f"epic_{ticket.id}"] = ticket

    @dispatch(Issue)
    def add_ticket(self, ticket: Issue):
        print(f"Adding issue {ticket.id}")
        if isinstance(ticket, Issue):
            # Check if the issue is already in any dictionary
            if f"issue_{ticket.id}" in self.tickets or f"issue_{ticket.id}" in self.new_tickets:
                raise ValueError(f"Issue with ID {ticket.id} already exists in tickets or new_tickets")
            else:
                if ticket.state == "ADD":
                    self.new_tickets[f"issue_{ticket.id}"] = ticket
                else:
                    self.tickets[f"issue_{ticket.id}"] = ticket
        
    def remove_ticket(self, ticket: Epic | Issue):
        if isinstance(ticket, Epic):
            if f"epic_{ticket.id}" in self.tickets:
                del self.tickets[f"epic_{ticket.id}"]
            else:
                raise ValueError(f"Epic with ID {ticket.id} not found in tickets")
        elif isinstance(ticket, Issue):
            if f"issue_{ticket.id}" in self.new_tickets:
                del self.new_tickets[f"issue_{ticket.id}"]
            if f"issue_{ticket.id}" in self.tickets:
                del self.tickets[f"issue_{ticket.id}"]
            else:
                raise ValueError(f"Issue with ID {ticket.id} not found in tickets")

    @dispatch(Epic)
    def approve_ticket(self, ticket: Epic):
        # Epic tickets will only be in the tickets dictionary
        # Check if the epic is in the tickets dictionary
        if f"epic_{ticket.id}" in self.tickets:
            ticket.accept_proposal()
        else:
            raise ValueError(f"Epic with ID {ticket.id} not found in tickets")

    @dispatch(Issue)
    def approve_ticket(self, ticket: Issue):
        # Existing issue tickets will be in the tickets dictionary
        # New proposed issue tickets will be in the new_tickets dictionary (with the state "ADD")
        
        # Move the new proposed issue ticket from the new_tickets dictionary to the tickets dictionary
        if f"issue_{ticket.id}" in self.new_tickets:
            self.tickets[f"issue_{ticket.id}"] = self.new_tickets[f"issue_{ticket.id}"]
            del self.new_tickets[f"issue_{ticket.id}"]
        
        # Check if the issue is in the tickets dictionary
        if f"issue_{ticket.id}" in self.tickets:
            ticket.accept_proposal()
        else:
            raise ValueError(f"Issue with ID {ticket.id} not found in tickets")
        
    @dispatch(Epic)
    def reject_ticket(self, ticket: Epic):
        # Epic tickets will only be in the tickets dictionary
        # Check if the epic is in the tickets dictionary
        if f"epic_{ticket.id}" in self.tickets:
            ticket.reject_proposal()
        else:
            raise ValueError(f"Epic with ID {ticket.id} not found in tickets")
        
    @dispatch(Issue)
    def reject_ticket(self, ticket: Issue):
        # Existing issue tickets will be in the tickets dictionary
        # New proposed issue tickets will be in the new_tickets dictionary (with the state "ADD")
        
        # If the issue is in the new_tickets dictionary, delete it
        if f"issue_{ticket.id}" in self.new_tickets:
            del self.new_tickets[f"issue_{ticket.id}"]
        # If the issue is in the tickets dictionary, reject the proposal
        elif f"issue_{ticket.id}" in self.tickets:
            ticket.reject_proposal()
        else:
            raise ValueError(f"Issue with ID {ticket.id} not found in tickets")

    @dispatch(Epic)
    def modify_ticket(self, ticket: Epic, proposed_content: str):
        # Epic tickets will only be in the tickets dictionary
        # Check if the epic is in the tickets dictionary
        if f"epic_{ticket.id}" in self.tickets:
            ticket.modify_proposal(proposed_content)
        else:
            raise ValueError(f"Epic with ID {ticket.id} not found in tickets")

    @dispatch(Issue)
    def modify_ticket(self, ticket: Issue, proposed_title: str, proposed_body: str):
        # Existing issue tickets will be in the tickets dictionary
        # New proposed issue tickets will be in the new_tickets dictionary (with the state "ADD")
        
        # If the issue is in the new_tickets dictionary, modify the proposal and move it to the tickets dictionary
        if f"issue_{ticket.id}" in self.new_tickets:
            self.tickets[f"issue_{ticket.id}"] = self.new_tickets[f"issue_{ticket.id}"]
            del self.new_tickets[f"issue_{ticket.id}"]

        # Check if the issue is in the tickets dictionary
        if f"issue_{ticket.id}" in self.tickets:
            ticket.modify_proposal(proposed_title, proposed_body)
        else:
            raise ValueError(f"Issue with ID {ticket.id} not found in tickets")
        
    def __str__(self):
        return f"""
        --------------------------------
        Tickets:
        {''.join([str(ticket) for ticket in self.tickets.values()])}
        New Tickets:
        {''.join([str(ticket) for ticket in self.new_tickets.values()])}
        --------------------------------
        """
    

if __name__ == "__main__":
    approval_handler = ApprovalHandler()
    print(approval_handler)

    # Test adding a new epic
    epic = Epic(epic_content="This is a new epic")
    approval_handler.add_ticket(epic)
    print(approval_handler)

    # Test adding a new issue
    issue = Issue(current_title="New Issue", current_body="This is a new issue", epic_id=1)
    approval_handler.add_ticket(issue)
    print(approval_handler)

    # Test removing an epic
    approval_handler.remove_ticket(epic)
    print(approval_handler)

    # Test removing an issue
    approval_handler.remove_ticket(issue)
    print(approval_handler)

    # Add a new epic
    epic = Epic(epic_content="This is a new epic")
    approval_handler.add_ticket(epic)
    print(approval_handler)
    
    # Propose an update to the epic
    epic.propose_update(proposed_content="This is an updated epic")
    print(approval_handler)

    # Approve the update to the epic
    approval_handler.approve_ticket(epic)
    print(approval_handler)

    # # Add a new issue
    # issue = Issue(current_title="New Issue", current_body="This is a new issue", epic_id=2)
    # approval_handler.add_ticket(issue)
    # print(approval_handler)

    # # Propose an update to the issue
    # issue.propose_update(proposed_title="Updated Issue", proposed_body="This is an updated issue", state="UPDATE")
    # print(approval_handler)

    # # Approve the update to the issue
    # approval_handler.approve_ticket(issue)
    # print(approval_handler)
    
    # Test modifying an epic
    approval_handler.modify_ticket(epic, proposed_content="This is a modified epic")
    print(approval_handler)

