## Feature: State Manager for Silent Mode
-DIsplays "Currently in Silent Mode" message to users.
-Stores silent mode status in the database.
-Reads status when app starts and update UI accordingly.

## Technologies and Tools
-Java(Android)
-Firebase Realtime Database
-SharedPreferences(for local caching, optional)

## Specifications
-When user enters a scheduled class time:
 -Automatically switch to silent mode.
 -Show "Currently in Silent Mode" message on screen.
-When user exits class time:
 -Switch back tk normal mode.
 -Message disappears
-Silent status should be stored in Firebase DB as:
'''json
{"userID": "abc123",
 "status": "silent",
 "timestamp": "2025-05-23T11:20:00"
}
