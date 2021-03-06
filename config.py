config = {
    # Site Name will be shown in page titles and in navbar
    "site-name": "Quotes Database",

    # MOTD will be shown as header text on the homepage
    "MOTD": "Welcome to the quotes database",

    # Show random quote on homepage
    "random-quote": True,

    # Length of nanoid quote IDs
    "quote-id-length": 12,

    # Used to protect against session data tampering
    "secret-key": "This should be a complex random value",

    # For approving or removing quotes
    "administrator-password": "This should be a different complex random value",

    # Database connection info
    "db": {
        "server": "mongodb://localhost:27017/",

        "database": "smash",

        "collection": "quotes",
    },
}
