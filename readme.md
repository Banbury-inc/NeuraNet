├── contracts/
│   ├── FileStorage.sol          # Smart contract code
│   ├── Migrations.sol           # Truffle migration code
│   └── ...
├── web/
│   ├── api/                     # API layer
│   │   ├── handlers/           # API request handlers
│   │   ├── models/             # Structs and types used by the API
│   │   ├── routes/             # API routes and endpoints
            ├── routes.go        # web routes are defined 
│   │   ├── main.go             # Entry point for the API
│   │   └── ...
│   ├── ipfs/                    # IPFS integration
│   │   ├── ipfs.go             # IPFS API client code
│   │   └── ...
│   ├── ui/                      # User interface layer
│   │   ├── assets/             # Static assets like CSS and JS
│   │   ├── templates/          # HTML templates rendered by Go
            ├── base.html         # Base HTML template for all pages
            ├── home.html         # Home page template
            ├── upload.html       # File upload page template
            ├── file.html         # File details page template
            ├── account.html      # User account page template
            ├── login.html        # Login page template
            ├── signup.html       # Signup page template
            ├── error.html        # Error page template
            └── partials/         # HTML partials used by the templates
                ├── header.html   # Header partial
                ├── footer.html   # Footer partial
│   │   ├── controllers/        # Go controllers for UI actions
│   │   ├── main.go             # Entry point for the UI
│   │   └── ...
│   ├── main.go                 # Entry point for the web server
│   └── ...
├── db/
│   ├── migrations/             # Database migration scripts
│   ├── models/                 # Database models and types
│   ├── repository/             # Database access layer
│   ├── main.go                 # Entry point for the database
│   └── ...
├── tests/                       # Unit and integration tests
│   ├── api/                     # API endpoint tests
│   ├── ipfs/                    # IPFS integration tests
│   ├── db/                      # Database tests
│   ├── main_test.go            # Entry point for the tests
│   └── ...
├── config/
│   ├── config.yaml             # App configuration file
│   ├── secrets.yaml            # App secrets file
│   └── ...
├── Dockerfile                  # Docker container configuration
├── README.md                   # Project documentation
└── ...
