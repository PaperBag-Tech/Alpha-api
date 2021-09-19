from enum import Enum

class UserRole(str, Enum):
	Admin = "Admin"
	Editor = "Editor"
	Agent = "Agent"
	Others = "Others"

class LeadStauts(str, Enum):
	open = "Open"
	scheduled = "Scheduled"
	rescheduled = "Rescheduled"
	pendingCustomerConfirmation = "Pending Customer Confirmation"
	pendingAgentConfirmation = "Pending Agent Confirmation"
	closed = "Closed"
	