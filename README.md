# python_p2p_chat
Player to player desktop GUI chat application where one user becomes the host/server and other users can join the room as clients. Made in Python 3.4 and Tkinter.

Just run "python p2p_chat.py" in the same directory as p2p_chat.py using Python 3. You might need X server if using Windows.

Note: You can't use this app to communicate with your friends outside of your network if the host is using a router (behind a NAT) as this app doesn't support NAT hole punching, yet.

### Features good to be added:
- Aggregate messages from the same user
- Different colored user names for each user
- Time of messages sent
- List showing joined users
- Complete Korean support (Needs to upgrade Tkinter version)
- Connect to host behind NAT (Needs a broker for NAT hole punching)
- Mutual authentication and encryption of data


### Possible code improvements:
- Use message header to indicate how many bytes are being sent
- When pasting into ip and port entry while the content is selected, the validation logic should pass it if the resulting string is within the limit


First practice Python project inspired by https://github.com/chprice/Python-Chat-Program
