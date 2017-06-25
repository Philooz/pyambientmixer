# pyAmbientMixer - a Python player with Pygame to play ambient-mixer.com mixes locally.

This little hacked script is here to allow people to download and play ambient mixes stored on ambient-mixer.com. It's not really "out for all users", but it works enough to be public.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You'll need python3 installed on your system, with the python packages untangle, pygame, requests and docopt.

If you're on a 'bian system, you can install python3 and pip with

```sudo apt install python3 python3-pip```

I recommend pip to install the required modules. Install them with

```sudo pip3 install requests pygame untangle docopt```

You'll also need an OGG encoder, as I went with pygame (and because it's a free format).
I recommend the easy-to-use dir2ogg utility, which encodes a whole directory into ogg.
If you're a 'bian, you can install it with

```sudo apt install dir2ogg```

### Installing

Just store ```ambient.py``` and ```ambient_downloader.py``` anywhere on your system.

## Downloading a mix

Easy. Get to the mix you'd like to keep. In this example, I went with "**Night in a Medieval Monastery**".

Just run ```ambient_downloader.py``` with the url.

In our example :

```python3 ambient_downloader.py http://religion.ambient-mixer.com/night-in-a-medieval-monastery```

which will give us

```Saved http://xml.ambient-mixer.com/audio-template?player=html5&id_template=48152 as presets/night-in-a-medieval-monastery.xml.
Saved http://xml.ambient-mixer.com/audio/9/5/7/957298df7abb5d7e94e6323c45d94063.mp3 as sounds/3677.mp3.
Saved http://xml.ambient-mixer.com/audio/d/3/3/d33c249dc7497e59091fab0ef08ee283.mp3 as sounds/529.mp3.
Saved http://xml.ambient-mixer.com/audio/a/0/1/a015edfc739fd3c7d942823511ba869d.mp3 as sounds/329.mp3.
Saved http://xml.ambient-mixer.com/audio/4/9/a/49a0e9aef698b60cf2c43312225778b9.mp3 as sounds/5745.mp3.
Saved http://xml.ambient-mixer.com/audio/3/b/6/3b64e0b6dffd39bd239e8071c25a4f37.mp3 as sounds/4583.mp3.
Saved http://xml.ambient-mixer.com/audio/7/8/e/78ece9cbea4fe23031c07ce15278f84a.mp3 as sounds/3354.mp3.
Saved http://xml.ambient-mixer.com/audio/7/5/e/75e7d0a3c6c6ef6ed69b26e7098b208c.mp3 as sounds/6432.mp3.
Saved http://xml.ambient-mixer.com/audio/1/6/8/168498dfdf8743eefb46dfebfd09c9eb.mp3 as sounds/6773.mp3.
```

Once the downloads are complete, you'll get two folders inside the current directory : ```sounds```, which contains all the sounds files you've downloaded; and ```presets``` which holds all the .xml files corresponding to the presets.

### Convert mp3s to oggs

If you're using dir2ogg, the command is

```dir2ogg -r sounds```

### Playing the mix

Once you downloaded your mix, and you've converted the files, just play it with ```ambient.py``` as such :
```python3 ambient.py presets/night-in-a-medieval-monastery.xml```

You should see 
```Loaded Channel 0 : Gregorian Chant 2 (looping), 3677.ogg (volume 21, balance 0).
Loaded Channel 1 : old Castle Background (looping), 529.ogg (volume 100, balance 0).
Loaded Channel 2 : Burning Torches (looping), 329.ogg (volume 71, balance 0).
Loaded Channel 3 : Door open with creak and close (random 1 per 10m), 5745.ogg (volume 21, balance 0).
Loaded Channel 4 : Flipping through large book (random 1 per 1m), 4583.ogg (volume 71, balance 0).
Loaded Channel 5 : Small Group Whispering (random 5 per 10m), 3354.ogg (volume 61, balance 0).
Loaded Channel 6 : echoing steps (looping), 6432.ogg (volume 100, balance 0).
Loaded Channel 7 : Writing with a quill (looping), 6773.ogg (volume 96, balance 0).```

Relax and enjoy your mix! :)

### TODOS and possible bugs

So far, everything should work fine, except Crossfade (which is a TODO).
The random playing times can act funny.
There is no GUI, and no possibility of changing files "on the fly". Feel free to fork and continue this project. ^^

## Authors

* **Philooz** - *Initial work* - [Philooz](https://github.com/Philooz)

## License

This project is licensed under the GPL License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to ambient-mixer.com website
* Huge thanks to the makers of the awesome python modules
* You for downloading this!
