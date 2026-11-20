from pydantic import BaseModel


class Incident(BaseModel):
    incident_date: str
    incident_time: str
    location: str
    units_responded: int
    reporting_officer: str