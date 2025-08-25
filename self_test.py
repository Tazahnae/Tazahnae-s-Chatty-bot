from bot_core import respond

tests = [
    "hello",
    "time",
    "joke",
    "remember share in TKH Slack",
    "notes",
    "math: 2*(3+4)",
    "weather Newark",
]

for q in tests:
    print(f"> {q}")
    print(respond(q))
