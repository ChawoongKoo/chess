# chess
I made this chess ai bot during the summer after my college graduation. 
I was really bored and wanted something fun to do that could distract me from other work.

Currently at a rating of >1300.
=======
# Chess Engine
>>>>>>> 3e60693 (updated readme)

A from-scratch chess engine written in Python that plays on [Lichess](https://lichess.org) via the Lichess Bot API.

The goal of this project is to build a competitive chess engine the hard way — implementing search, evaluation, and the supporting data structures myself rather than wrapping an existing engine like Stockfish.

## Highlights

- **Negamax search with alpha-beta pruning** for efficient game-tree exploration
- **MVV-LVA move ordering** (Most Valuable Victim / Least Valuable Aggressor) to maximize pruning effectiveness
- **Zobrist hashing** for fast, incrementally-updated position identification — the foundation for an upcoming transposition table
- **Custom evaluation function** combining material balance and mobility, with both absolute and side-relative scoring
- **Perft validator** for verifying move generation correctness against known node counts
- **Pytest test suite** covering evaluation, piece values, search behavior, and external move integration

## How It Works

### Search — [`homemade.py`](homemade.py)

The main engine is the `NegaMax` class. It explores the move tree using the negamax formulation of minimax (one function instead of separate `min`/`max`), with alpha-beta pruning to cut branches that can't influence the final decision. Search depth is configurable in `config.yml`. Each search logs the best move, score, time taken, and positions evaluated.

### Evaluation — [`engines/evaluate.py`](engines/evaluate.py)

Two evaluation functions:

- `basic_evaluate` — absolute scoring (positive = White advantage), useful for analysis and debugging
- `relative_evaluate` — side-to-move scoring (positive = side to move is winning), which is what negamax needs

Both combine weighted piece values ([`engines/piece_value.py`](engines/piece_value.py)) with a mobility term based on legal move counts. Checkmate and draw states are handled explicitly so the search doesn't have to special-case them.

### Move Ordering — [`engines/sort_moves.py`](engines/sort_moves.py)

`MVV_LVA` sorts legal moves so the engine examines the most promising captures first (high-value victim, low-value attacker). Better ordering means alpha-beta prunes sooner, which compounds dramatically as depth grows.

### Position Hashing — [`engines/zobrist.py`](engines/zobrist.py)

The `Zobrist` class maintains a 64-bit hash of the current position that updates incrementally on each move via XOR — castling, promotions, captures, en passant, and castling-rights changes are all handled. The hash is what a transposition table will key on, so repeated positions across the search tree won't need to be re-evaluated.

### Move Generation Validation — [`engines/perft.py`](engines/perft.py)

`perft(board, depth)` counts the number of legal positions reachable at a given depth — a standard sanity check used to verify a chess implementation matches reference move counts.

## Project Structure

```
chess/
├── homemade.py              # Engine entry point (NegaMax, MiniMax, etc.)
├── engines/                 # My engine code
│   ├── evaluate.py          # Position evaluation
│   ├── sort_moves.py        # MVV-LVA move ordering
│   ├── zobrist.py           # Zobrist hashing
│   ├── piece_value.py       # Piece values
│   └── perft.py             # Move generation validator
├── test_bot/                # Pytest suite
├── config.yml               # Bot + engine configuration
└── lichess-bot.py           # Lichess API bridge (provided by lichess-bot)
```

The `lib/`, `lichess-bot.py`, and surrounding scaffolding come from the [lichess-bot](https://github.com/lichess-bot-devs/lichess-bot) project, which handles the Lichess API plumbing. The engine logic in `engines/` and `homemade.py` is mine.

## Running It

```bash
# Install dependencies
pip install -r requirements.txt

# Run the test suite
pytest test_bot/

# Connect to Lichess (requires a Lichess OAuth token in config.yml)
python lichess-bot.py
```

Search depth and engine selection are set under `engine.homemade_options` in `config.yml`. See [`LICHESS_README.md`](LICHESS_README.md) for the full bot setup walkthrough.

## Roadmap

- **Transposition table** — caching evaluated positions keyed by Zobrist hash (hashing is built; cache integration is next)
- **Iterative deepening** — search depth 1, then 2, then 3… so the engine always has a best move ready when time runs out
- **Quiescence search** — extend search through tactical sequences to avoid the horizon effect on captures
- **Neural network evaluation** — train a position evaluator on PGN data (see [`engines/neural_evaluate/`](engines/neural_evaluate/)) to replace or augment the hand-tuned evaluation

## Credits

Built on top of [lichess-bot](https://github.com/lichess-bot-devs/lichess-bot), which provides the Lichess API bridge.

> Pantidis, I., Harrison, M., Choksi, S., & Duplessis, T. *lichess-bot* [Computer software]. https://github.com/lichess-bot-devs/lichess-bot
