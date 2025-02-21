class Epic:
    """
    Represents an epic with its original content and an optional proposed update.
    """
    def __init__(self, epic_id, epic_content, proposed_content=None):
        self.epic_id = epic_id
        self.epic_content = epic_content      # The original epic statement.
        self.proposed_content = proposed_content  # The proposed updated epic, if any.

    def __str__(self):
        s = f"Epic ID: {self.epic_id}\nEpic Content:\n{self.epic_content}\n"
        if self.proposed_content:
            s += f"Proposed Content:\n{self.proposed_content}\n"
        return s

    def to_dict(self):
        return {
            "epic_id": self.epic_id,
            "epic_content": self.epic_content,
            "proposed_content": self.proposed_content,
        }


class Issue:
    """
    Represents an issue with its current state and an optional proposed update.
    """
    def __init__(self, issue_id, issue_title, issue_body,
                 proposed_issue_title=None, proposed_issue_body=None,
                 proposed_action=None):
        self.issue_id = issue_id
        self.issue_title = issue_title        # The current title.
        self.issue_body = issue_body          # The current body/description.
        self.proposed_issue_title = proposed_issue_title  # Proposed updated title.
        self.proposed_issue_body = proposed_issue_body    # Proposed updated body.
        self.proposed_action = proposed_action  # Proposed action: "Update", "Delete", or "Add".

    def __str__(self):
        s = (f"Issue ID: {self.issue_id}\n"
             f"Title: {self.issue_title}\n"
             f"Body: {self.issue_body}\n")
        if self.proposed_action or self.proposed_issue_title or self.proposed_issue_body:
            s += "Proposed Change:\n"
            if self.proposed_action:
                s += f"  Action: {self.proposed_action}\n"
            if self.proposed_issue_title:
                s += f"  Title: {self.proposed_issue_title}\n"
            if self.proposed_issue_body:
                s += f"  Body: {self.proposed_issue_body}\n"
        return s

    def to_dict(self):
        return {
            "issue_id": self.issue_id,
            "issue_title": self.issue_title,
            "issue_body": self.issue_body,
            "proposed_issue_title": self.proposed_issue_title,
            "proposed_issue_body": self.proposed_issue_body,
            "proposed_action": self.proposed_action,
        }


class Parser:
    @staticmethod
    def parse_epic_feedback(raw_output, existing_epic):
        """
        Parses the LLM output for epic feedback.

        Expected format:
        
        Proposed Epic:
        <updated epic statement>

        Changes Summary:
        <summary of changes and reasoning>

        Args:
            raw_output (str): The raw text output produced by the LLM.
            existing_epic (Epic): The original epic object.

        Returns:
            tuple: (updated_epic, changes_summary)
                   - updated_epic: An Epic object with 'proposed_content' updated.
                   - changes_summary: A string containing the summary of changes.
        """
        epic_lines = []
        summary_lines = []
        mode = None

        for line in raw_output.splitlines():
            if line.startswith("Proposed Epic:"):
                mode = "epic"
                text = line[len("Proposed Epic:"):].strip()
                if text:
                    epic_lines.append(text)
            elif line.startswith("Changes Summary:"):
                mode = "summary"
                text = line[len("Changes Summary:"):].strip()
                if text:
                    summary_lines.append(text)
            elif mode == "epic":
                epic_lines.append(line.strip())
            elif mode == "summary":
                summary_lines.append(line.strip())

        proposed_epic_text = "\n".join(epic_lines).strip()
        changes_summary = "\n".join(summary_lines).strip()

        # Create a new Epic object with the updated (proposed) content.
        updated_epic = Epic(existing_epic.epic_id, existing_epic.epic_content,
                            proposed_content=proposed_epic_text)
        return updated_epic, changes_summary

    @staticmethod
    def parse_issue_feedback(raw_output):
        """
        Parses the LLM output for issue feedback.

        Expected format (each block separated by a blank line):

        For existing issues:
        ---------------------
        Issue <ID>:
        Action: <Update/Delete>
        If Action is Update, then include:
        Proposed Title: <revised title>
        Proposed Body:
        <revised description>
        
        For new issues:
        ---------------------
        New Issue:
        Action: Add
        Proposed Title: <title>
        Proposed Body:
        <description>

        Proposal Summary:
        <summary of proposed changes to the issues>

        Returns:
            tuple: (modifications, new_proposals, proposal_summary)
                  - modifications: dict mapping issue IDs (int) to dict:
                        { "action": "Update" or "Delete",
                          "proposed_title": <value> (if applicable),
                          "proposed_body": <value> (if applicable) }
                  - new_proposals: list of dicts, each with keys:
                        { "action": "Add",
                          "proposed_title": <value>, 
                          "proposed_body": <value> }
                  - proposal_summary: a string containing the summary.
        """
        modifications = {}
        new_proposals = []
        proposal_summary = ""

        # Split the output into blocks by double newlines.
        blocks = [block.strip() for block in raw_output.split("\n\n") if block.strip()]

        for block in blocks:
            lines = block.splitlines()
            if not lines:
                continue

            header = lines[0].strip()

            # Handle the proposal summary block.
            if header.startswith("Proposal Summary:"):
                summary_lines = [line.strip() for line in lines[1:]]
                proposal_summary = "\n".join(summary_lines).strip()
                continue

            if header.startswith("Issue"):
                # Parse an update or deletion proposal for an existing issue.
                try:
                    # Expected header format: "Issue <ID>:"
                    issue_id = int(header.split()[1].replace(":", ""))
                except Exception as e:
                    print(f"Error parsing issue id in proposal: {e}")
                    continue

                action = None
                proposed_title = None
                proposed_body_lines = []

                for idx, raw_line in enumerate(lines[1:], start=1):
                    line = raw_line.strip()
                    if line.startswith("Action:"):
                        action = line.split("Action:")[1].strip()
                    elif line.startswith("Proposed Title:"):
                        proposed_title = line.split("Proposed Title:")[1].strip()
                    elif line.startswith("Proposed Body:"):
                        # Check inline text as well as subsequent lines.
                        text = line[len("Proposed Body:"):].strip()
                        if text:
                            proposed_body_lines.append(text)
                        proposed_body_lines.extend([l.strip() for l in lines[idx+1:]])
                        break

                proposed_body = "\n".join(proposed_body_lines).strip()

                modifications[issue_id] = {
                    "action": action,
                    "proposed_title": proposed_title,
                    "proposed_body": proposed_body,
                }

            elif header.startswith("New Issue:"):
                # Handle a new issue proposal.
                action = "Add"
                proposed_title = None
                proposed_body_lines = []

                for idx, raw_line in enumerate(lines[1:], start=1):
                    line = raw_line.strip()
                    if line.startswith("Proposed Title:"):
                        proposed_title = line.split("Proposed Title:")[1].strip()
                    elif line.startswith("Proposed Body:"):
                        text = line[len("Proposed Body:"):].strip()
                        if text:
                            proposed_body_lines.append(text)
                        proposed_body_lines.extend([l.strip() for l in lines[idx+1:]])
                        break

                proposed_body = "\n".join(proposed_body_lines).strip()
                if proposed_title and proposed_body:
                    new_proposals.append({
                        "action": action,
                        "proposed_title": proposed_title,
                        "proposed_body": proposed_body
                    })

        return modifications, new_proposals, proposal_summary 