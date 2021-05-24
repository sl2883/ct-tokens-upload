### From a user profile, create a CT profile with identify and device token
<mark>Make sure you've updated the constants at the top of file - ct-token-uploads</mark>

- PROJECT ID should match to your account's project id
- PASSCODE should match to your account's passcode
- Ensure that your CSV file name is profiles.csv
- Column names are 
	- user_id (user identifier)
	- idfa (iOS identifier)
	- adid (Android identifier)
	- type (fcm/apns etc.)
	- token (device token)
- At least one of user id or (idfa/adid) must be present for a profile.

### To run

 ```javascript
  python3 ct-token-uploads.py
  ```