from dataclasses import dataclass


@dataclass(frozen=True)
class ProcessRundownFile:  # Command
    name: str  # The name of the rundown file to process.
    created_at: str  # The timestamp when the action was created.


@dataclass(frozen=True)
class RundownFileProcessed:  # Event
    name: str  # The name of the processed rundown file.
    created_at: str  # The timestamp when the event was created.
