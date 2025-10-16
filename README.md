# Movie Skeeter

A tool to help me post my movie reviews on BlueSky

## Prerequisites
- [uv](https://docs.astral.sh/uv/)
- [direnv](https://direnv.net/)

## Usage

- Clone this repo
- Create a `.envrc` file or environment variables with your BlueSky login info
```
export BSKY_USER="Your BSky username"
export BSKY_PASS="Your BSky password"
```
- Edit `data/movies.csv`
- Run `uv run main.py`
