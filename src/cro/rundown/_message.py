from dataclasses import dataclass


@dataclass(frozen=True)
class ProcessFile: # Command
    name: str  # The name of the file to process.
    timestamp: str  # The timestamp when the action was created.


@dataclass(frozen=True)
class FileProcessed: # Event
    name: str  # The name of the processed file.
    timestamp: str  # The timestamp when the event was created
