REGEX = "regex"
TAG = "tag"
USR = {
		REGEX: [r'^@\S+$'],
		TAG: "USR"
	}
URL = {
		REGEX: [r'^[a-zA-Z]+\.[a-zA-Z]+$'],
		TAG: "USR"
	}

DOT = {
		REGEX: [r'^\.$' ,r'^,[.,-\/#!$%\^&\*;:{}=\-_`~()]+$'],
		TAG: "."
	}

COMMA = {
		REGEX: [r'^,$'],
		TAG: ","
	}

COLON = {
		REGEX: [r'^\.+$', r'^:$'],
		TAG: ":"
	}