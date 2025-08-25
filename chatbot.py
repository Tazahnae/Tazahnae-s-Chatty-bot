#!/usr/bin/env python3
from bot_core import BOT_NAME, respond

def main():
    print(f"Hi Tazahnae 👋, I’m {BOT_NAME}. Ready to help!")
    print("Type 'help' for commands. Type 'exit' to quit.")
    while True:
        try:
            user = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Bye!")
            break
        if user.lower() in {"exit", "quit"}:
            print("👋 Bye!")
            break
        print(respond(user))

if __name__ == "__main__":
    main()
