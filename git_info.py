import subprocess
import os

commands = [
    ['git', 'status'],
    ['ls', '-la'],
    ['git', 'log', '--oneline', '-n', '5'],
    ['git', 'remote', '-v'],
    ['git', 'config', '--get', 'user.name'],
    ['git', 'config', '--get', 'user.email']
]

for command in commands:
    result = subprocess.run(command, capture_output=True, text=True)
    print(f'Command: {" ".join(command)}')
    print(f'Output:\n{result.stdout}')
    print(f'Error (if any):\n{result.stderr}')
    print('---')

# Read README.md if it exists
if os.path.exists('README.md'):
    print('Contents of README.md:')
    with open('README.md', 'r') as f:
        print(f.read())
    print('---')
else:
    print('README.md does not exist.')
    print('---')
