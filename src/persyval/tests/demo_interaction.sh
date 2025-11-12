#!/usr/bin/env bash
# [bash_init]-[BEGIN]
# Exit whenever it encounters an error, also known as a non–zero exit code.
set -o errexit
# Return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status,
#   or zero if all commands in the pipeline exit successfully.
set -o pipefail
# Treat unset variables and parameters other than the special parameters ‘@’ or ‘*’ as an error when performing parameter expansion.
set -o nounset
# Print a trace of commands.
#set -o xtrace
# [bash_init]-[END]

# Note: EOF-style input does not work. So demonstrating only predefined-input style.

# Show help message
uv run persy --show-commands --predefined-input help

# Wrong argument in help command
uv run persy --show-commands --hide-intro --predefined-input "help bla"

# Wrong command
uv run persy --show-commands --hide-intro --predefined-input "he123"

# Exit
uv run persy --show-commands --hide-intro --predefined-input "exit true"

# Show storage stats
uv run persy --show-commands --hide-intro --predefined-input "storage_stats"

# Clear storage
uv run persy --show-commands --hide-intro --predefined-input "storage_clear true"



#echo "----- Restarting -----"
