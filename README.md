# ev-logs
The tool was built to provide ACC EventViewer logs to ULS.
It fetches ACC EventViewer logs from the ACC EventViewer API.

---
## Usage

### ACC EventViewer logs
Setup the .edgerc file as described [here](#authentication)
```bash
akamai-acc events getevents -f
```

## Authentication
To use ACC EventViewer CLI, a proper authentication needs to be provided.
Therefore please create an `.edgerc` file or extend an already existing akamai `.edgerc` file with a new section or use the default as long as the API Client has the proper access rights
The default search location for the edgerc file is `~/.edgerc`. 

---
# Changelog
## v0.0.1(beta)
  - Initial version
---
# Support
Solution is provided as-is, Akamai Support will only be able to help on the ACC Event Viewer.  
For questions or issues with this solution, please raise a GitHub ticket.