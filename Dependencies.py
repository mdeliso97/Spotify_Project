import subprocess

# Run pip freeze command to get a list of installed packages
result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)

# Check if the command executed successfully
if result.returncode == 0:
    # Get the output and split it into individual lines
    output = result.stdout
    packages = output.split('\n')

    # Write the packages to a text file
    with open('dependencies.txt', 'w') as file:
        file.write('\n'.join(packages))
        print('Dependencies written to dependencies.txt')
else:
    print('Error occurred while fetching dependencies:', result.stderr)