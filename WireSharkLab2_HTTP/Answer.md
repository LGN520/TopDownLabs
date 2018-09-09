- 1. The Basic HTTP GET/response interaction
    + Q: Is your browser running HTTP version 1.0 or 1.1? What version of HTTP is the server running?
        * A: HTTp 1.1
    + Q: What languages (if any) does your browser indicate that it can accept to the server?
        * A: zh-CN, zh
    + Q: What is the IP address of your computer? Of the gaia.cs.umass.edu server?
        * A: (1)Source, 124.16.112.223 (2)Dest, 128.119.245.12
    + Q: What is the status code returned from the server to your browser?
        * A: (1)For HTTP-wireshark-file1.html, 200 (2)For favicon.ico, 404
    + Q: When was the HTML file that you are retrieving last modified at the server?
        * A: (1)For HTTP-wireshark-file1.html, Sat, 08 Sep 2018 05:59:01 GMT (2)For favicon.ico, null
    + Q: How many bytes of content are being returned to your browser?
        * A: (1)For HTTP-wireshark-file1.html, 128 (2)For favicon.ico, 209
    + Q: By inspecting the raw data in the packet content window, do you see any headers within the data that are not displayed in the packet-listing window? If so, name one.
        * A: No
- 2. The HTTP CONDITIONAL GET/response interaction
    + Q: Inspect the contents of the first HTTP GET request from your browser to the server. Do you see an “IF-MODIFIED-SINCE” line in the HTTP GET?
        *  A: No
    + Q: Inspect the contents of the server response. Did the server explicitly return the contents of the file? How can you tell?
        * A: Yes, there are line-based text data after blank line
    + Q: Now inspect the contents of the second HTTP GET request from your browser to the server. Do you see an “IF-MODIFIED-SINCE:” line in the HTTP GET? If so, what information follows the “IF-MODIFIED-SINCE:” header?
        * A: Yes, the last modified time of the previous request
    + Q: What is the HTTP status code and phrase returned from the server in response tothis second HTTP GET? Did the server explicitly return the contents of the file? Explain.
        * A: 304, No
- 3. Retrieving Long Documents
    + Q: How many HTTP GET request messages did your browser send? Which packet number in the trace contains the GET message for the Bill or Rights?
        * A: 1, No.72
    + Q: Which packet number in the trace contains the status code and phrase associated with the response to the HTTP GET request?
        * A: No.168
    + Q: What is the status code and phrase in the response?
        * A: 200 OK
    + Q: How many data-containing TCP segments were needed to carry the single HTTP response and the text of the Bill of Rights?
        * A: 4
- 4. HTML Documents with Embedded Objects