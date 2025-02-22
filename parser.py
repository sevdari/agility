from abc import ABC, abstractmethod
from ticket import Epic, Issue
from typing import Optional

class Parser(ABC):
    @abstractmethod
    def parse(self, raw_output, *args, **kwargs):
        """
        Abstract method to parse input data.
        """
        pass


class EpicParser(Parser):
    def parse(raw_output, epic: Optional[Epic] = None) -> tuple[Epic, str]:
        """
        Parses the LLM output for epic feedback.

        Args:
            raw_output (str): The raw text output produced by the LLM.
            epic (Optional[Epic]): The original epic object, if available.

        Returns:
            tuple: (updated_epic, changes_summary)
                   - updated_epic: An Epic object with 'proposed_content' updated.
                   - changes_summary: A string containing the summary of changes.
        """
        epic_lines = []
        summary_lines = []
        mode = None

        for line in raw_output.splitlines():
            if line.startswith("Epic:"):
                mode = "epic"
                text = line[len("Epic:"):].strip()
                if text:
                    epic_lines.append(text)
            elif line.startswith("Summary:"):
                mode = "summary"
                text = line[len("Summary:"):].strip()
                if text:
                    summary_lines.append(text)
            elif mode == "epic":
                epic_lines.append(line.strip())
            elif mode == "summary":
                summary_lines.append(line.strip())

        proposed_epic_text = "\n".join(epic_lines).strip()
        changes_summary = "\n".join(summary_lines).strip()

        # If the existing epic is not provided, create a new Epic object.
        if epic is None:
            epic = Epic(epic_content=proposed_epic_text)
        else:
            epic.propose_update(proposed_epic_text)

        return epic, changes_summary


class IssueParser(Parser):
    def parse(raw_output) -> tuple[dict, list, str]:
        """
        Parses the LLM output for issue feedback.

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
                        # Updated logic to check inline text as well as subsequent lines.
                        text = line[len("Proposed Body:"):].strip()
                        if text:
                            proposed_body_lines.append(text)
                        # Append any remaining lines in this block.
                        proposed_body_lines.extend([l.strip() for l in lines[idx+1:]])
                        break

                proposed_body = "\n".join(proposed_body_lines).strip()

                # For update action, both title and body are required.
                if action and action.lower() == "update":
                    if not proposed_title or not proposed_body:
                        print(f"Warning: Incomplete update proposal for Issue {issue_id}. Skipping.")
                        continue

                modifications[issue_id] = {
                    "action": action,
                    "proposed_title": proposed_title,
                    "proposed_body": proposed_body,
                }

            elif header.startswith("New Issue:"):
                # For new issues, we include an action of "Add".
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
                if not proposed_title or not proposed_body:
                    print("Warning: Incomplete new issue proposal. Skipping.")
                else:
                    new_proposals.append({
                        "action": action,
                        "proposed_title": proposed_title,
                        "proposed_body": proposed_body
                    })

        return modifications, new_proposals, proposal_summary