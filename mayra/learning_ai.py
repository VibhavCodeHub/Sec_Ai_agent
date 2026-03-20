# Deprecated: LearningMayra logic merged into assistant.py
# Use `python mayra/main.py --daemon` for live responsive AI

"""
Legacy standalone learning loop. Now integrated with streaming daemon.
"""

if __name__ == '__main__':
    print("Use main.py --daemon for live mode!")
    from assistant import respond
    query = input("Query: ")
    print(respond(query))
