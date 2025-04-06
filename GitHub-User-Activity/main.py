# import sys
# import json
# import http.client
# def get_latest_events(username):
#     conn = http.client.HTTPSConnection("api.github.com")
#     headers = {
#         'User-Agent': 'Python GitHub Events Script'
#     }
#     conn.request("GET", f"/users/{username}/events", headers=headers)

#     response = conn.getresponse()
#     if response.status == 200 :
#         events = json.load(response)
#         for e in events :
#             event_type = e['type']
#             if event_type == 'PushEvent' :
#                 commits_count = len(e['payload']['commits'])
#                 print(f'- Pushed {commits_count} commits to {e["repo"]["url"]}')
#             elif event_type == 'IssuesEvent' :
#                 print(f'- Opened a new issue in {e["repo"]["url"]}')
#             elif event_type =='WatchEvent' :
#                 print(f'- Starred {e["repo"]["url"]}')
#             elif event_type == 'PullRequestEvent' :
#                 print(f'- pulled from {e["repo"]["url"]}')
#             elif event_type == 'ForkEvent' :
#                 print(f'- forked {e["repo"]["url"]}')
#             elif event_type == 'CreateEvent' :
#                 print(f'- created {e["payload"]["ref_type"]} {e["payload"]["ref"]} in {e["repo"]["url"]}')
#             elif event_type == 'DeleteEvent' :
#                 print(f'- deleted {e["repo"]["url"]}')

#     else :
#         print(response.status)
#     conn.close()

# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         username = sys.argv[1]
#         get_latest_events(username)
#     else:
#         print("Please provide a GitHub username and a personal access token as command line arguments.")

import cmd
import json
import http.client

class GitHubEventsCLI(cmd.Cmd):
    intro = 'Welcome to the GitHub Events CLI. Type help or ? to list commands.'
    prompt = '(github) '

    def get_latest_events(self, username):
        conn = http.client.HTTPSConnection("api.github.com")
        headers = {
            'User-Agent': 'Python GitHub Events Script'
        }
        conn.request("GET", f"/users/{username}/events", headers=headers)

        response = conn.getresponse()
        if response.status == 200:
            events = json.load(response)
            for e in events:
                event_type = e['type']
                if event_type == 'PushEvent':
                    commits_count = len(e['payload']['commits'])
                    print(f'- Pushed {commits_count} commits to {e["repo"]["url"]}')
                elif event_type == 'IssuesEvent':
                    print(f'- Opened a new issue in {e["repo"]["url"]}')
                elif event_type == 'WatchEvent':
                    print(f'- Starred {e["repo"]["url"]}')
                elif event_type == 'PullRequestEvent':
                    print(f'- Pulled from {e["repo"]["url"]}')
                elif event_type == 'ForkEvent':
                    print(f'- Forked {e["repo"]["url"]}')
                elif event_type == 'CreateEvent':
                    print(f'- Created {e["payload"]["ref_type"]} {e["payload"]["ref"]} in {e["repo"]["url"]}')
                elif event_type == 'DeleteEvent':
                    print(f'- Deleted {e["repo"]["url"]}')
        else:
            print(f"Error: {response.status}")
        conn.close()
    def default(self, line):
        """Handle commands with hyphens."""
        if line.startswith("github-activity "):
            username = line[len("github-activity "):].strip()
            self.get_latest_events(username)
        else:
            print(f"Unknown command: {line}")
    def do_exit(self, arg):
        """Exit the CLI."""
        print("Goodbye!")
        return True

if __name__ == "__main__":
    GitHubEventsCLI().cmdloop()