### Applet to sync play counts between iTunes and Windows Media Player

This is an applet that lets the user sync the play counts of their iTunes and Windows Media Player libraries. 

It is now available on Gumroad (at a dirt cheap price). 
[Check it out](https://jrsousa2.gumroad.com/l/Plays_Sync)

A trial version has been added to this repo as well.<br>
[https://github.com/jrsousa2/Plays_Sync/releases/tag/v1.1.0](https://github.com/jrsousa2/Plays_Sync/releases/tag/v1.1.0)

Unlike others I've seen this one runs very fast, because it relies on the iTunes library XML file, which is much faster to load than scanning the entire iTunes music database. Unfortunately there is no such file for WMP, but reading the WMP library is a little faster anyway. Speed performance is more critical for very large music collections.

This time around I've used wxFormBuilder to create a more native-looking GUI than the first applet I created, which used TkInter. 

A feature that was challenging to add was a "progress bar" (actually, a completion percentage) that could be refreshed timely and that wouldn't cause the GUI to freeze as data from the WMP library is being read and loaded, so the user knows the program is still running and not stalled. (Some professional applications actually don't give the user that benefit when they run a command (like Wolfram Cloud, for example)). This is only a problem for users who have too many music files anyway.

**Here is a snapshot that illustrates how the program works:**<br>
(Please note Github can be terrible at managing hyperlinks, so don't blame me if the links fail -- they can be viewed above anyway). Even better, you can run the trial version, which is free and available right here under Releases (right frame).

#### Current version:
![Latest](https://raw.githubusercontent.com/jrsousa2/Plays_Sync/main/Snapshot1.png)

**Below images of test runs:**<br>

##### Updating iTunes from WMP (if WMP>iTunes → iTunes:=WMP)
![Screenshot 1](https://raw.githubusercontent.com/jrsousa2/Plays_Sync/main/Snapshot2.png)

##### Updating WMP from iTunes (if iTunes>WMP → WMP:=iTunes)
![Screenshot 2](https://raw.githubusercontent.com/jrsousa2/Plays_Sync/main/Snapshot3.png)

Reason why not all files were updated is because these are snapshots of test runs, and I was careful to not update all the files.

Of course the program will only work if the user has both iTunes and WMP installed on Windows (no Mac version for now).

<i>PS Please feel free to reach out to me with any questions you may have.</i>

