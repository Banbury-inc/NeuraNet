## Things to consider when designing a multiple knapsack algorithm

### Devices
* Number of devices
* Total Storage of the devices
* Average amount of time the device is online (how reliable) 
* Power consumption per unit storage
* Cost for each unit capacity and power consumption
* Average Upload and Download speed of device
* The current Upload and Download speed of the device 
### Files

* File index
* File Name
* Size of file
* File type
* File priority
* Frequency file visited
* File Location
* CID (Content Identifier in the decentralized network)
* File access permissions (private, public, read-only)
* File replication factor
* File versioning and update frequency
* File Encryption and security measures
* File owner and sharing permissions
### To run the server 
Start the backend server
* pip install flask
* python app.py
Start the frontend server
* npm install
* npm start


### File Structure

decentralized_file_sharing/
│
├── backend/
│   ├── app.py                  # Main backend application file (Flask or FastAPI)
│   ├── api/
│   │   ├── __init__.py         # API package initializer
│   │   ├── devices.py          # API endpoints for managing devices
│   │   ├── files.py            # API endpoints for managing files
│   │   └── knapsack.py         # API endpoint for the knapsack algorithm
│   ├── models/
│   │   ├── __init__.py         # Models package initializer
│   │   ├── device.py           # Device data model
│   │   └── file.py             # File data model
│   └── utils/
│       ├── __init__.py         # Utility package initializer
│       └── auth.py             # Authentication and security utilities
│
├── frontend/
│   ├── public/
│   │   ├── index.html          # Main HTML file
│   │   └── ...                 # Other public files (e.g., images, icons)
│   └── src/
│       ├── components/         # React components
│       │   ├── Device.js       # Component for device management
│       │   ├── File.js         # Component for file management
│       │   └── ...             # Other components
│       ├── App.js              # Main App component
│       └── index.js            # Entry point for the frontend
│
├── algorithms/
│   ├── __init__.py             # Algorithms package initializer
│   ├── knapsack.py             # Core implementation of the Multiple Knapsack Algorithm
│   └── ...                     # Other algorithm implementations (e.g., priority-based)
│
├── decentralized_storage/
│   └── ipfs.py                 # IPFS integration module
│
├── config/
│   ├── config.py               # Configuration settings for the project
│   └── ...
│
├── tests/                      # Unit tests for backend and algorithms
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── test_devices.py
│   │   └── ...
│   └── algorithms/
│       ├── __init__.py
│       ├── test_knapsack.py
│       └── ...
│
├── requirements.txt            # Dependencies for the project
├── .gitignore                  # Git ignore file
├── README.md                   # Project documentation
└── ...

