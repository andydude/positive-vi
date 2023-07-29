# Let us start with the complicated commands

class CommandReader:

    def read(self):

        pass

@dataclass
class ReplaceFromShell:
    """
    vi.html:
      *Synopsis*
        [count] ! motion shell-commands <newline>
    """
    count: int
    _exclToken: str
    motion: Motion
    shellCommands: str

