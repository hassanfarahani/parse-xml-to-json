## Description
Seatmap Availability Exercise:

Our goal is to parse seatmap information from XML files and create a JSON format that our customers can parse so that they can display any airline seatmap by integrating our format.

Desired behavior:

Input: python seatmap_parser.py [FILENAME]

Output: FILENAME_parsed.json

Description:
Write a python script that parses the XML seatmap files included in this folder (seatmap1.xml, seatmap2.xml) into a standardized JSON format that outputs the seatmap (by row) with the following properties at minimum:
	- Seat/Element type (Seat, Kitchen, Bathroom, etc)
	- Seat id (17A, 18A)
	- Seat price
	- Cabin class
	- Availability

## Technologies used
- Python
- Python Element Tree module
