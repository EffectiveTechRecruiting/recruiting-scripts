from string import Template
import os
import webbrowser
import datetime
import requests

def create_coderpad( candidate_first_name, candidate_last_name ):
	question_contents = """/*

QUESTION 1: Write a function GetPowerset that accepts a set of strings - encoded as a List - and returns that set's powerset (https://en.wikipedia.org/wiki/Power_set).  For example, GetPowerset( new List<int>( { "a", "b" } ) ) would return a list containing {}, { "a" }, { "b" }, and { "a", "b" }.  The order of the elements does not matter.  You are welcome and encouraged to do this problem prior to the interview.

*/

using System;
using System.Collections.Generic;

class Solution {
  static List<List<string>> GetPowerset( List<string> setElements )
  {
      // Put your solution here
  }    
     
  static void Main(string[] args) {
    var mySet = new List<string>{ "a", "b" };
      
    var myPowerSet = GetPowerset( mySet );
    
    foreach ( var s in myPowerSet ) {
      var concatenation = string.Join( ", ", s );
      if ( concatenation.Length > 0 ) {
        concatenation = " " + concatenation + " ";
      }
      Console.WriteLine( "{" + concatenation + "}" );
    }
  }
}"""

	url = 'https://coderpad.io/api/pads'
	response = requests.get( url, headers={ 'Authorization' : 'Token token="<<YOURTOKENHERE>>"' } )
	if response.status_code != 200:
	    raise Exception( "unable to authenticate" )

	candidate_coderpad_title = candidate_first_name + " " + candidate_last_name + " (1)"

	payload = { 'title' : candidate_coderpad_title, 'language' : 'csharp', 'contents' : question_contents }
	response = requests.post( url, headers={ 'Authorization' : 'Token token="<<YOURTOKENHERE>>"' }, data=payload )
	if response.status_code != 200:
	    print response.status_code
	    raise Exception( "unable to create pad" )

	response_json = response.json()
	coderpad_url = response_json[ 'url' ]
	#coderpad_hangout_url = response_json[ 'hangout' ]

	print coderpad_url
	#print coderpad_hangout_url

	return coderpad_url

def generate_email( candidate_first_name, candidate_last_name, interview_date, coderpad_url ):
	interview_date_string = interview_date.strftime("%A") + ", " + interview_date.strftime("%B") + " " + str( interview_date.day )
	interview_time_string = str(interview_date.strftime("%-I")) + ":" + str(interview_date.strftime("%M")) + " " + interview_date.strftime("%p")

	email_template = Template( """<font face="verdana" size="2">
<p/><h2>Subj: CompanyName: Phone Screening Details for $candidate_first_name $candidate_last_name</h2>
<hr/>
<p/>Dear $candidate_first_name:
<p/>Our interview is scheduled for <b>$interview_date</b> at <b>$interview_time Eastern</b>. Please allot about ninety minutes for the interview. We may not use all of that time, but we like to allocate it just in case.
<p/>During the call please direct your browser to a CoderPad instance we have set up: <a href="$coderpad_url">$coderpad_url</a> .  Please confirm that you can access this application prior to the interview.  I strongly encourage you to read the short <a href="https://coderpad.io/howto.pdf">coderpad.io HowTo guide</a> to familiarize yourself with that application.  We will ask you a few simple programming/technical questions, and this is a good collaborative notepad/execution space to do so.  You are welcome and encouraged to solve the first question, which is already provided, prior to the interview.
<p/>Do you have a Skype account? If not, please create one, and send me your Skype ID so we can get the communication infrastructure all set up. My own Skype ID is <b>MySkypeUserName</b> . We'll be doing a voice chat only, so don't worry about setting up your camera.
<p/>If you'd like to know a little more about what we do, I encourage you to visit our recruiting portal at <b>MyRecruitingPortal.com</b> to get a bit more flavor about our vision, culture, and practices.
<p/>If you have any problems, please don't hesitate to call me at <b>555-123-4567</b>. We look forward to speaking with you!
<p/>Regards,<br/>
John
</font>
""" )

	email_content = email_template.substitute( candidate_first_name = candidate_first_name,
			candidate_last_name = candidate_last_name,
			interview_date = interview_date_string,
			interview_time = interview_time_string,
			coderpad_url = coderpad_url )
	path = os.path.abspath('./temp_interview_details.html')
	url = 'file://' + path
	with open(path, 'w') as f:
		f.write( email_content )
	webbrowser.open(url)

if __name__ == "__main__":
	candidate_first_name = "Frank"
	candidate_last_name = "Jones"
	interview_date = datetime.datetime( 2016, 8, 5, 15, 30, 0, 0 )

	coderpad_url = create_coderpad( candidate_first_name, candidate_last_name )
	generate_email( candidate_first_name, candidate_last_name, interview_date, coderpad_url )