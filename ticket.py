# Abstract base class for tickets.
from abc import ABC, abstractmethod

class Ticket(ABC):
    _next_id = 0

    def __init__(self, current_content: dict, state: str = "APPROVED"):
        self.id = Ticket._next_id
        Ticket._next_id += 1
        self.current_content = current_content
        self.proposed_content = {}
        self.state = state

    def get_id(self):
        return self.id
    
    def get_state(self):
        pass

    def set_state(self, state: str):
        self.state = state

    def get_current_content(self):
        return self.current_content
    
    def get_proposed_content(self):
        return self.proposed_content
    
    # Setter methods
    def set_current_content(self, current_content: str):
        self.current_content = current_content

    def set_proposed_content(self, proposed_content: str):
        self.proposed_content = proposed_content

    @abstractmethod
    def accept_proposal(self):
        pass

    @abstractmethod
    def reject_proposal(self):
        pass

    @abstractmethod
    def modify_proposal(self, proposed_content: str):
        pass

    @abstractmethod
    def __str__(self):
        pass


class Epic(Ticket):
    _valid_states = ["APPROVED", "UPDATE"]
    def __init__(self, epic_content: str, state: str = "APPROVED"):
        super().__init__({"epic_content": epic_content}, state)

    def get_current_content(self) -> dict:
        return self.current_content
    
    def get_proposed_content(self) -> dict:
        return self.proposed_content

    def set_current_content(self, epic_content: str) -> None:
        self.current_content = {"epic_content": epic_content}

    def set_proposed_content(self, proposed_content: str) -> None:
        self.proposed_content = {"epic_content": proposed_content}

    def propose_update(self, proposed_content: str) -> None:
        self.state = "UPDATE"
        self.set_proposed_content(proposed_content)
        
    def accept_proposal(self) -> None:
        if self.state == "UPDATE":
            self.state = "APPROVED"
            self.current_content = self.proposed_content
            self.proposed_content = None

    def reject_proposal(self) -> None:
        if self.state == "UPDATE":
            self.state = "APPROVED"
            self.proposed_content = None

    def modify_proposal(self, epic_content: str):
        self.current_content = {"epic_content": epic_content}
        self.proposed_content = None
        self.state = "APPROVED"

    def __str__(self) -> str:
        return f"""
        Epic ID: {self.id}
        Current Content: {self.current_content}
        Proposed Content: {self.proposed_content}
        State: {self.state}
        """


class Issue(Ticket):
    _valid_states = ["APPROVED", "UPDATE", "DELETE", "ADD"]
    def __init__(self, current_title: str, current_body: str, state: str = "APPROVED", epic_id: int = None):
        super().__init__({"issue_title": current_title, "issue_body": current_body}, state)
        # Link to the epic that this issue belongs to
        self.epic_id = epic_id

    def get_current_content(self) -> dict:
        return self.current_content
    
    def get_proposed_content(self) -> dict:
        return self.proposed_content
    
    def get_epic_id(self) -> int | None:
        return self.epic_id

    def set_current_content(self, current_title: str, current_body: str) -> None:
        self.current_content = {"issue_title": current_title, "issue_body": current_body}

    def set_proposed_content(self, proposed_title: str, proposed_body: str) -> None:
        self.proposed_content = {"issue_title": proposed_title, "issue_body": proposed_body}

    def propose_update(self, proposed_title: str, proposed_body: str, state: str = "UPDATE") -> None:
        self.state = state
        self.set_proposed_content(proposed_title, proposed_body)
    
    def set_epic_id(self, epic_id: int) -> None:
        self.epic_id = epic_id

    def accept_proposal(self) -> None:
        match self.state:
            case "UPDATE":
                self.state = "APPROVED"
                self.current_content = self.proposed_content
                self.proposed_content = None
            case "ADD":
                self.state = "APPROVED"
                self.current_content = self.proposed_content
                self.proposed_content = None
            case "DELETE":
                # delete the issue object completely
                pass
            case "APPROVED":
                raise ValueError("Cannot accept a proposal for an approved issue")

    def reject_proposal(self) -> None:
        if self.state == "APPROVED":
            raise ValueError("Cannot reject a proposal for an approved issue")
        self.state = "APPROVED"
        self.proposed_content = None

    def modify_proposal(self, proposed_title: str, proposed_body: str) -> None:
        self.current_content = {"issue_title": proposed_title, "issue_body": proposed_body}
        self.proposed_content = None
        self.state = "APPROVED"

    def __str__(self) -> str:
        return f"""
        Issue ID: {self.id}
        Linked Epic ID: {self.epic_id}
        Current Content: {self.current_content}
        Proposed Content: {self.proposed_content}
        State: {self.state}
        """