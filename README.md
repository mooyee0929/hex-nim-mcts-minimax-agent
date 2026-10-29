# Hex Nim MCTS + Minimax Agent

This is a game-playing agent for a two-player misère "cross-out" game on a hexagonal board. On each turn a player crosses out one, two or three free cells that lie next to each other along a straight line, and the player who crosses out the last remaining cell loses. The agent is written in Python and talks to a game server over TCP. It uses Monte Carlo Tree Search (UCT) while the board is large and switches to alpha-beta minimax once few cells remain.

## The game

- The board is a 12 x 12 grid of hexagonally offset cells. Only a random connected subset of cells is playable, and the rest are walls (`-1`).
- A move is `[(x, y), length, direction]`. It covers `length` (1 to 3) free cells, starting at `(x, y)` and continuing in one of six hex directions.
- Crossing out the last free cell loses, and so does an illegal move. If a player does not answer within the server's timeout, the server plays a random legal move for it.

## Agent design (`agent/hybrid_agent.py`)

- **Move generation.** `getLegalSteps` lists every single free cell, plus every 2- and 3-cell straight line of free cells. Direction `d` and its opposite `7 - d` trace the same line from the other end, so only directions 1 to 3 are generated. This halves the branching factor compared with using all six directions.
- **Hybrid search.** `Getstep` picks the search method by how many free cells remain:
  - **16 or more free cells: MCTS.** A search tree with UCT selection (exploration constant 1.414) runs 600 iterations with random playouts and returns the child with the best UCT value.
  - **Fewer than 16 free cells: minimax** with alpha-beta pruning to depth 6. A position with exactly one free cell left is scored as a forced loss for the player to move. At the depth limit, the evaluation rewards positions where the number of free cells is congruent to 1 mod 4, the losing count in take-1-to-3 misère Nim.
- **Networking.** `agent/STcpClient_1.py` connects to the server at `localhost:8888`, sends the player ID (`idTeam`), receives the 12 x 12 board state as 32-bit integers, and sends back the chosen move.

### Earlier versions

`agent/` also keeps the two single-strategy agents that were compared before settling on the hybrid:

- `minimax.py`: alpha-beta minimax only (depth 6, directions 1 to 3).
- `mcst.py`: MCTS only, generating moves in all six directions.

The write-up (`report.pdf`, in Chinese) reports these findings:

- Minimax alone could only search about 4 plies before the direction reduction was added.
- MCTS moved faster but lost to minimax in head-to-head tests.
- In the hybrid, the first move searched with minimax can still exceed the per-move time limit.

## Repository structure

```
.
├── agent/
│   ├── hybrid_agent.py         # hybrid MCTS + minimax agent (entry point)
│   ├── STcpClient_1.py         # TCP client used by the agents
│   ├── minimax.py, mcst.py     # single-strategy agents
│   ├── hybrid_agent.spec, minimax.spec, mcst.spec, mix.spec   # PyInstaller specs
│   ├── build/                  # PyInstaller intermediates
│   └── dist/                   # built executables: hybrid_agent.exe, minimax.exe, mcst.exe, mix.exe
├── server/
│   ├── AI_game.py              # match driver: reads input.txt, runs a game, opens the replay UI
│   ├── STcpServer.py           # TCP server on port 8888, launches player executables
│   ├── gameRule.py             # board generation, move validation, random fallback move
│   └── gameUI.py               # Tkinter replay viewer
├── sample/                     # prebuilt opponent executables (Windows)
├── t.py                        # unfinished MCTS draft
├── input.txt                   # match configuration read by the server
├── Sample_1.spec               # PyInstaller spec for a sample opponent
├── hybrid_agent_bundle.zip     # packaged copy of the agent executable, source, client and report
├── report.pdf                  # write-up of the approach (Chinese)
├── specification.pdf           # game rules and environment description
└── specification-slides.pptx   # environment setup guide (Chinese)
```

## Requirements

- Agent: Python 3 with `numpy` (it uses only the standard library otherwise).
- Server: Python 3 with `numpy` and `tkinter`. The server is Windows-only, because it launches players as `.exe` files and stops them with `taskkill`.
- Building executables: `pyinstaller`.

## Usage

1. Set `idTeam` in `agent/STcpClient_1.py` to your player ID. The server rejects clients whose ID does not match the one in `input.txt`. The committed executables were built with the ID that `input.txt` lists for them.
2. Build the agent executable from its spec:

   ```bash
   cd agent
   pyinstaller hybrid_agent.spec
   ```

   This produces `agent/dist/hybrid_agent.exe`.
3. Edit `input.txt`. It has six lines: player 1 ID, path to player 1's executable, player 2 ID, path to player 2's executable, number of playable cells (`0` for random), and random seed (`0` for random). The committed file pits `sample/third_party_opponent.exe` against `agent/dist/hybrid_agent.exe`.
4. From the repository root, start a match:

   ```bash
   python server/AI_game.py
   ```

   The server launches both executables, plays one game, and opens a Tkinter replay window with `back` / `next` buttons to step through the moves.

## Acknowledgements

The game server (`server/`, with `AI_game.py` credited to LAB639), the TCP client template (`agent/STcpClient_1.py`) and the sample opponents (`sample/Sample_1.exe`, `sample/Sample_2.exe`, `sample/Sample_1_C++.exe`) came with the game environment and are not original to this repository. `sample/third_party_opponent.exe` is another player's opponent build that was used for testing. The agents (`agent/hybrid_agent.py`, `agent/minimax.py`, `agent/mcst.py`, `t.py`) are the work in this repository.
