import subprocess

# Initialize IPFS by running 'ipfs init' command
def ipfs_init():
    try:
        subprocess.run(['ipfs', 'init'], check=True)
        print("IPFS initialized.")
    except subprocess.CalledProcessError as e:
        print("Failed to initialize IPFS:", e)

# Add a file to IPFS by running 'ipfs add' command with the file path
def ipfs_add(file_path):
    try:
        result = subprocess.run(['ipfs', 'add', file_path], capture_output=True, text=True, check=True)
        # Get the output of the 'ipfs add' command
        output = result.stdout.strip()

        # Extract the CID from the output
        cid = output.split()[-2]

        print("File added to IPFS with CID:", cid)
        return cid
    except subprocess.CalledProcessError as e:
        print("Failed to add file to IPFS:", e)
        return None

# Retrieve the content of a file from IPFS by running 'ipfs cat' command with the file's hash
def ipfs_cat(hash):
    try:
        result = subprocess.run(['ipfs', 'cat', hash], capture_output=True, text=True, check=True)
        print("File content from IPFS:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Failed to retrieve file content from IPFS:", e)

# List the contents of a directory in IPFS by running 'ipfs ls' command with the directory's hash
def ipfs_ls(hash):
    try:
        result = subprocess.run(['ipfs', 'ls', hash], capture_output=True, text=True, check=True)
        print("Contents of the directory from IPFS:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Failed to retrieve directory contents from IPFS:", e)

# Pin a file or directory to IPFS by running 'ipfs pin add' command with the file/directory's hash
def ipfs_pin(hash):
    try:
        subprocess.run(['ipfs', 'pin', 'add', hash], check=True)
        print("File or directory pinned to IPFS.")
    except subprocess.CalledProcessError as e:
        print("Failed to pin file or directory to IPFS:", e)

# Start the IPFS daemon using 'ipfs daemon' command
def ipfs_daemon():
    try:
        subprocess.Popen(['ipfs', 'daemon'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("IPFS daemon started.")
        # You may want to add a delay here or use other methods to ensure the daemon is fully ready before proceeding.
    except subprocess.CalledProcessError as e:
        print("Failed to start IPFS daemon:", e)

# Connect to a peer in the IPFS swarm by running 'ipfs swarm connect' command with the peer's address
def ipfs_swarm_connect(peer_address):
    try:
        subprocess.run(['ipfs', 'swarm', 'connect', peer_address], check=True)
        print(f"Connected to {peer_address} in IPFS swarm.")
    except subprocess.CalledProcessError as e:
        print("Failed to connect to peer in IPFS swarm:", e)

# Get the list of connected peers in the IPFS swarm by running 'ipfs swarm peers' command
def ipfs_swarm_peers():
    try:
        result = subprocess.run(['ipfs', 'swarm', 'peers'], capture_output=True, text=True, check=True)
        print("Connected peers in IPFS swarm:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Failed to retrieve connected peers in IPFS swarm:", e)

# Get the list of bootstrap nodes in IPFS by running 'ipfs bootstrap list' command
def ipfs_bootstrap_list():
    try:
        result = subprocess.run(['ipfs', 'bootstrap', 'list'], capture_output=True, text=True, check=True)
        print("Bootstrap nodes in IPFS:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Failed to retrieve bootstrap nodes from IPFS:", e)

# Create a new IPFS object with given data by running 'ipfs object new unixfs-dir' command
def ipfs_object_new(data):
    try:
        result = subprocess.run(['ipfs', 'object', 'new', 'unixfs-dir'], input=data.encode(), capture_output=True, text=True, check=True)
        hash = result.stdout.strip()
        print(f"New IPFS object created with hash: {hash}")
        return hash
    except subprocess.CalledProcessError as e:
        print("Failed to create new IPFS object:", e)
        return None

# Get the data of an IPFS object by running 'ipfs object get' command with the object's hash
def ipfs_object_get(hash):
    try:
        result = subprocess.run(['ipfs', 'object', 'get', hash], capture_output=True, text=True, check=True)
        print(f"IPFS object data for hash {hash}:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Failed to retrieve IPFS object data:", e)

# Remove pin from a file or directory in IPFS by running 'ipfs pin rm' command with the object's hash
def ipfs_pin_rm(hash):
    try:
        subprocess.run(['ipfs', 'pin', 'rm', hash], check=True)
        print(f"File or directory with hash {hash} unpinned from IPFS.")
    except subprocess.CalledProcessError as e:
        print("Failed to unpin file or directory from IPFS:", e)

# Run IPFS garbage collection by running 'ipfs repo gc' command
def ipfs_repo_gc():
    try:
        subprocess.run(['ipfs', 'repo', 'gc'], check=True)
        print("IPFS garbage collection completed.")
    except subprocess.CalledProcessError as e:
        print("Failed to run IPFS garbage collection:", e)
