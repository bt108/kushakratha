#!/bin/sh

# Default IP address prefix
DEFAULT_IP_PREFIX="192.168.0."

# Prompting for IP input
echo "IP address: $DEFAULT_IP_PREFIX[input] or full IP adress"
read user_input

# Determine if the input is a full IP address or just the last octet
if echo "$user_input" | grep -E '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$' > /dev/null; then
    # Full IP address provided
    IP_ADDRESS="$user_input"
else
    # Last octet provided; construct the full IP address
    IP_ADDRESS="${DEFAULT_IP_PREFIX}${user_input}"
fi

# SCP command
scp -P 2222 epub/Bhaktivinoda_Thakura_Jaiva_Dharma.epub root@"$IP_ADDRESS":/mnt/onboard/books/Kushakrata/

# Specify the placeholder for the remote folder name
REMOTE_FOLDER_TO_DELETE="/mnt/onboard/books/Kushakrata/Bhaktivinoda_Thakura_Jaiva_Dharma.sdr"

# Prompting for deletion of a remote folder
echo "Do you want to delete $REMOTE_FOLDER_TO_DELETE @ $IP_ADDRESS? (yes/no)"
read delete_folder

if [ "$delete_folder" = "yes" ]; then
    # Remove the remote folder
    ssh -p 2222 root@"$IP_ADDRESS" "rm -rf '$REMOTE_FOLDER_TO_DELETE'"
    echo "The remote folder $REMOTE_FOLDER_TO_DELETE has been removed."
else
    echo "Remote folder was not deleted."
fi
