Some problems with client/ui/config_sharing.py.

1:
If all relevant types for a server are disabled in the visible types list, the panel still shows with nothing inside.
So it should use the same logic of hiding the panel and display a message in that case, just like if the server was not included.
Instead of duplicating code, take the existing code for when the server is not included and turn this into a generalized function with a string parameter for the text that should be displayed in the read only field.

2:
When importing and setting the filter to existing or new, if there are no servers available, it does correctly display the no servers available message, however it also displays the "server not included message".
This server not included message or existing panel if any should be hidden.

3:
I exported a file, and imemdiately tried to import the same exported file.
It only showed one server in the data which is correct since there were no account changes between the data, so only option profiles were able to be updated. Meaning only one server had changed options profile data from defaults, thus it was the only one.
However user accounts still showed up in the visible types lists and in that one server that had the modified options. So i could select both user accounts and options profile. Accounts should have been omitted.
So to clarify, if there are modified options, it doesn't block user accounts when it should for that server.

4:
Always focus the first available item in a list when loading the dialog, the types list and the servers list.