# python_p2p_chat
Player to player desktop gui chat application where one user becomes the host/server and other users can join the room as clients. Made using Python and Tkinter.


Featurs good to be added:
- Aggregate messages from the same user
- Different colored user names for each user
- Time of messages sent
- Complete Korean support (Needs to upgrade Tkinter version)
- Connect to host behind NAT (Needs a broker for NAT hole punching)
- Mutual authentication and encryption of data


Possible code improvements:
- Use message header to indicate how many bytes are being sent
- When pasting into ip and port entry while the content is selected, the validation logic should pass it if the resulting string is within the limit


First practice Python project inspired by https://github.com/chprice/Python-Chat-Program
