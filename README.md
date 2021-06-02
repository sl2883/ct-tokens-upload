<mark>Make sure you've updated the constants at the top of file - ct-token-uploads</mark>

- PROJECT ID should match to your account's project id
- PASSCODE should match to your account's passcode
- Ensure that your CSV file name is profiles.csv
- Column names are 
	- Name
	- Email Address
	- User Id
	- Device ID
	- Device OS
	- Token
	- Email Opt In?
	- Push Opt In?
- At least one of user id or device-id must be present for a profile.

### To run

 ```javascript
  python3 ct-token-uploads.py
  ```