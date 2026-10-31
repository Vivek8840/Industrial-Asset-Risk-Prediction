
from pydantic import BaseModel, ConfigDict, Field


class SensorReadings(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    machine_type: str = Field(alias="Type", pattern="^[LMH]$")

    air_temperature: float = Field(
        alias="Air temperature [K]", gt=0
    )
    process_temperature: float = Field(
        alias="Process temperature [K]", gt=0
    )
    rotational_speed: float = Field(
        alias="Rotational speed [rpm]", gt=0
    )
    torque: float = Field(alias="Torque [Nm]", ge=0)
    tool_wear: float = Field(alias="Tool wear [min]", ge=0)

    def to_model_input(self) -> dict:
        """Convert validated readings to the model's expected columns."""
        return {
            "Type": self.machine_type,
            "Air temperature [K]": self.air_temperature,
            "Process temperature [K]": self.process_temperature,
            "Rotational speed [rpm]": self.rotational_speed,
            "Torque [Nm]": self.torque,
            "Tool wear [min]": self.tool_wear,
        }


class PredictionResponse(BaseModel):
    failure_probability: float
    decision_threshold: float
    predicted_failure: bool
    risk_level: str
    model_status: str
