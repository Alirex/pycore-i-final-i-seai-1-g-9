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


PERSY_STORAGE_PATH=$(mktemp --directory -t persy-demo-XXXXXX)

echo "Using storage path: ${PERSY_STORAGE_PATH}"
echo "-------------------------------------"

persy_exec() {
  persy \
    --storage-dir "${PERSY_STORAGE_PATH}" \
    --show-commands \
    --non-interactive \
    --raise-sys-exit-on-error \
    --hide-intro \
    "$1"
}

persy_exec_plain() {
  persy \
    --storage-dir "${PERSY_STORAGE_PATH}" \
    --show-commands \
    --non-interactive \
    --raise-sys-exit-on-error \
    --hide-intro \
    --plain-render \
    "$1"
}


# Show help message
persy --show-commands --non-interactive help

# Wrong argument in help command
persy_exec "help bla" || true

# Wrong command
persy_exec "he123" || true

# Exit
persy_exec "exit true"

# Show storage stats
persy_exec "storage_stats"

# Clear storage
persy_exec "storage_clear true"

persy_exec "contact_add Some"

# Add multiple contacts
for i in {1..3}; do
  birthday="1990-0$((i))-0$((i))"

  persy_exec "contact_add x$((i)) address-$((i)) ${birthday} +38073000000$((i)),+38097000001$((i)),+38097000001$((i)) user_$((i))@example.com,user_$((i))@gmail.com"
done

# Show storage stats
persy_exec "storage_stats"

# Show all contacts
persy_exec "contacts_list all"

# Show filtered
persy_exec_plain "contacts_list filter name=x2"

# Get last line from output
last_line=$(persy_exec_plain "contacts_list filter name=x2" | tail --lines 1)

# Remove contact based on last line
persy_exec "contact_delete ${last_line} true"

# Show all contacts
persy_exec "contacts_list all"


#echo "----- Restarting -----"
