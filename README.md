UNIVERSAL CUSTOM DISCORD RPC!! HECK YEAH!!

A simple Python script that gives you a custom Discord Rich Presence for literally any app or game. I originally built this to get Ship of Harkinian (Ocarina of Time PC port) showing up on my Discord profile on Arch Linux, but I’ve tweaked it so it works for any OS on Windows, Mac, Linux and probably BSD too! 

-lightweight virtually 0 cpu
-only shows up when the game is open
-it works for any program
-it's persistent and will work even if discord crashes or closes
-easy to use

SET UP!!
install python, pypresence and psutil :p

if there isn't an application for your program then make an application but if there is just lookup the application id
https://discord.com/developers/applications <-- link to make application id
copy the application id into the .py script (btw the whole thing is annotated)
(optional) upload icons to that application on the discord website

then run the program and open your app, if you did it right things should work

i like to make mine an executable but you can just run `python discord_rpc.py` too
