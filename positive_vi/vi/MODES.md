# Modes
- 'command mode' (after ':', ex default, vi default, 15 in ex.html, 6 in vi.html)
  - == CMD_MODE
  - 'ex mode' (16 in ex.html, 3 in vi.html)
  - 'ex command mode' (9 in ex.html, 3 in vi.html)
    - After [Q]
  - 'vi command mode' (0)
  - 'command-line mode' (0)
    - == CMD_LINE_MODE
  - 'operator-pending mode'
- 'text input mode' (after 'i', 36 in ex.html, 42 in vi.html)
  - == IN_MODE
  - After [aci]
  - 'vi text input mode' (1 in ex.html)
  - 'ex text input mode' (9 in ex.html)
  - 'input mode' (4 in ex.html, 21 in vi.html)
  - 'select mode'
  - 'insert mode'
    - == IN_INSERT_MODE
    - 'replace mode' in text input mode
      - == IN_REPLACE_MODE (unimplemented)
    - 'virtual replace mode' in text input mode
      - requires "gR" which is unimplemented
    - 'insert normal mode' in text input mode
    - 'insert visual mode' in text input mode
    - 'insert select mode' in text input mode
- 'visual mode' (after 'v|<escape>', 45 in ex.html, 10 in vi.html)
  - == VI_MODE
  - After [v]
  - 'normal mode' (0, not posix-compliant)
  - 'open mode' (4 in ex.html, 22 in vi.html)
  - 'open and visual mode' (16 in ex.html, 3 in vi.html)
    - 'characterwise visual mode'
      - 'character mode buffer' (2 in ex.html, 29 in vi.html)
      - == VI_MODE
    - 'linewise visual mode'
      - 'line-mode buffer' (1 in ex.html, 1 in vi.html)
      - 'line mode buffer' (6 in ex.html, 33 in vi.html)
      - == VI_LINE_MODE
    - 'blockwise visual mode'
      - == VI_BLOCK_MODE

# Misc Modes
- 'standout mode' (errorbells)
- 'terminal-normal mode'
- 'terminal-job mode'


# The states
states=[
    'CMD',
    'CMD/LINE',
    'IN',
    'VI',
]

# And some transitions between states. We're lazy, so we'll leave out
# the inverse phase transitions (freezing, condensation, etc.).
transitions = [
    { 'trigger': 'visual', 'source': 'EX', 'dest': 'VI' },
    { 'trigger': 'Q', 'source': 'VI', 'dest': 'EX' }
    
    { 'trigger': 'startinsert', 'source': 'CMD', 'dest': 'IN_S' }
    { 'trigger': 'stopinsert', 'source': 'IN_S', 'dest': 'CMD' }

    { 'trigger': 'startreplace', 'source': 'CMD', 'dest': 'IN_R' }
    { 'trigger': 'stopreplace', 'source': 'IN_R', 'dest': 'CMD' }
]

CMD_SUBMODE = 'extended'
CMD_SUBMODE = 'visual'

IN_SUBMODE = 'insert'
IN_SUBMODE = 'replace'

[buffer][count] d motion
