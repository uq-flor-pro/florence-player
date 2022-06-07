# [[Florence]] Music Player

*A simple to use music player*

## Version 2
- [x] order new wood for laser cutting #next
- [ ] gaps for heat exchange - rear vents #design 
- [ ] worst case shutdown pin at back #design
- [x] resistors #altronics
- [ ] case picks up finger prints

## Issues
### adafruit bonnet very loud
- [x] #next fix bonnet volume #roadblock 
not going through alsamixer?

https://docs.mopidy.com/en/latest/config/?highlight=audio#audio-section
https://forums.raspberrypi.com/viewtopic.php?t=249758

``` bash
  101  aplay /usr/share/sounds/alsa/Front_Center.wav
  156  aplay /usr/share/sounds/alsa/Front_Center.wav
  157  alsamixer
  158  aplay /usr/share/sounds/alsa/Front_Center.wav
  159  alsamixer
  160  aplay /usr/share/sounds/alsa/Front_Center.wav
  163  sudo vi /usr/share/alsa/alsa.conf 
  164  history | grep alsa
  167  alsactl
  168  alsa-info
  170  sudo vi /usr/share/alsa/alsa.conf 
  171  alsamixer
  173  alsamixer
  174  sudo vi /usr/share/alsa/alsa.conf 
  176  alsamixer
  213  alsamixer
  215  alsamixer
  217  alsamixer
  220  sudo vi /usr/share/alsa/alsa.conf 
  222  alsa-info
  223  sudo alsa-info
  224  alsactl
  225  alsactl --help
  227  speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav
  228  alsamixer 
  229  speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav
  230  alsamixer 
  231  speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav
  232  alsamixer 
  234  sudo vi /usr/share/alsa/alsa.conf 
  237  alsamixer
  238  sudo apt install mopidy-alsamixer
  246  alsamixer
  254  alsamixer
  261  speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav
  265  speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav
  267  speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav
  370  alsamixer
  375  alsamixer
  380  sudo vim /usr/share/alsa/alsa.conf 
  641  alsamixer
  648  alsamixer
  650  sudo vim /usr/share/alsa/alsa.conf 
  652  alsamixer
  653  sudo apt install  python-alsaaudio
  654  sudo apt install  python3-alsaaudio
  656  speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav
  657  sudo vim /usr/share/alsa/alsa.conf 
  658  alsamixer
  660  speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav
  662  speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav
  665  speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav
  667  speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav
  675  sudo vim /usr/share/alsa/alsa.conf 
  676  alsamixer
  677  speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav
  679  speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav
  681  speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav
  682  alsamixer
  684  speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav
  ```
#### no audio
Somewhere along the line the audio is now completely broken.
Nothing plays.
I have tried uncommenting the changes the bonnet made to /boot/config.txt to no avail.
```
gst-launch audiotestsrc ! audioconvert ! audio/x-raw,channels=2 ! alsasink
``` 
should play a sine wave. it doesn't.

making a usb pi image to test from a fresh install.

https://docs.mopidy.com/en/latest/troubleshooting/

## Notes
### push deploy
``` bash
./pummeluff_to_player
./install
```

### startup
gnd -> scl

### ssh
https://pimylifeup.com/raspberry-pi-enable-ssh-boot/

### mcp3008
https://learn.adafruit.com/mcp3008-spi-adc/python-circuitpython
```
sudo pip3 install adafruit-circuitpython-mcp3xxx
```
``` bash
Feb 10 04:36:12 raspberrypi mopidy[647]:   File "/usr/local/lib/python3.9/dist-packages/Mopidy_Pummeluff-2.2.1.dev9+gb5e52eb.d20220210-py3.9.egg/mopidy_pumm>
Feb 10 04:36:12 raspberrypi mopidy[647]:     self.tag_reader   = TagReader(core=core, stop_event=self.stop_event)
Feb 10 04:36:12 raspberrypi mopidy[647]:   File "/usr/local/lib/python3.9/dist-packages/Mopidy_Pummeluff-2.2.1.dev9+gb5e52eb.d20220210-py3.9.egg/mopidy_pumm>
Feb 10 04:36:12 raspberrypi mopidy[647]:     self.rfid       = RFID()
Feb 10 04:36:12 raspberrypi mopidy[647]:   File "/usr/local/lib/python3.9/dist-packages/pirc522/rfid.py", line 50, in __init__
Feb 10 04:36:12 raspberrypi mopidy[647]:     GPIO.setmode(pin_mode)
Feb 10 04:36:12 raspberrypi mopidy[647]: ValueError: A different mode has already been set!
```
tracked down a potential cause in pi
```
pirc522/rfid.py:        GPIO.setmode(pin_mode)
in /usr/local/lib/python3.9/dist-packages
```

https://github.com/adafruit/Adafruit_Python_Extended_Bus/issues/2
Looks like you can't mix rpi.gpio and digitalio :(

RFID tries to set mode as does digitalio I think. Instead switch to gpiozero.

https://raspi.tv/2016/using-mcp3008-to-measure-temperature-with-gpio-zero-and-raspio-pro-hat <- !!

### pins
![[raspberry_pi_gpio-shutdown-pins.webp]]

### static ip
https://www.makeuseof.com/raspberry-pi-set-static-ip/

### pull up/down
**Pull Down**

When you have a circuit that connects 3.3v to a GPIO pin, it'll read HIGH when the circuit is closed. When it's open, it could read anything. You need a "pull down" resistor connecting your circuit to ground, so that it reads LOW when the circuit is open. _(I'll show this in effect later.)

**Pull Up**

Similarly, if you have a circuit connecting your GPIO pin to ground when it's closed, it'll read `LOW`. You need a "pull up" resistor so that, when it's open, it defaults to the `HIGH` state.

In both cases, the button has no resistance (or at least, less resistance), and so when the circuit is closed it short-circuits around the pull up or pull down resistor and reads the other value. Hopefully this will make more sense with a couple demonstrations.
https://grantwinney.com/using-pullup-and-pulldown-resistors-on-the-raspberry-pi/

### resistors
Hello and welcome! It is still noteworthy that it is two different things. 1) the pull-up/-down resistor is required to prevent the floating of the input pin (this resistor could be internal or external). 2) a series resistor between the pin and the switch. The latter is the one that prevents a short if the pin is configured output and the button is pressed. That is a feat the pull-up/-down cannot do.

– [Ghanima](https://raspberrypi.stackexchange.com/users/19949/ghanima "15,379 reputation") ♦

[Feb 9 2018 at 17:46](https://raspberrypi.stackexchange.com/questions/51142/wire-button-without-resistor#comment124721_79027)

## Feedback
### Jacki
- should look like familiar radio
- simplify over time if needed but not prematurely
- not arcade buttons

### Janet
- operate from the top, via a knuckle
- hanging on wall
### Altronics attendant
- tough buttons
### Pete


## install again
first adafruit speaker bonnet!
update/upgrade
then mopidy (WARNING re apt-key)
```
pi@raspberrypi:~ $ wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
Warning: apt-key is deprecated. Manage keyring files in trusted.gpg.d instead (see apt-key(8)).
OK
```
(change mirrors to Japan - slower dl?)
enable, start
mopidy-spotify # sudo pip install mopidy-spotify
python3-pip
mopidy-iris #use sudo
mopidy-local #why isn't audio working through mopidy?
git
	

## adc

## network issues
https://forums.raspberrypi.com/viewtopic.php?p=1670096&hilit=transfer+disconnects#p1670096

Re: Copying a lot of files to the Raspberry Pi fails and leads to minute-long unresponsiveness

Sat May 30, 2020 5:54 pm
Wondering if this is the old Wifi dropping problem. Well, not so old, I'm still seeing it. Does your WiFi drop every 5 or 6 minutes, regardless of whether you're doing a copy to the Pi or not? What do you see if you grep the log for 'wlan0: carrier lost'?

#### limiting throughput on wlan help?
wondershaper, slower mirror (japan)

### computer took pi ip
```
sudo dhclient -r #release 
sudo dhclient # negotiate new ip
```

## speakers not producing sound on mopidy
was working using gstreamer:
```
  114  gst-launch-1.0 audiotestsrc ! audioresample ! autoaudiosink
  118  gst-launch-1.0 audiotestsrc ! audioresample ! oss4sink
```
now not working this way.

### checking soldering
desolder wick

## using two SPI devices at once
edit /boot/config.txt to enable SPI1
change gpiozero to use other SPI1 Hardware pins
change mcp_watcher to new pins
????
Failure to read

*Works with SPI0 and CS as CE0. but that means that RFID reader is not usable at same time.*

### pummeluff not loading
```
Mar 09 15:42:05 raspberrypi mopidy[766]:   Starting Mopidy 3.2.0
Mar 09 15:42:05 raspberrypi mopidy[766]: WARNING  2022-03-09 15:42:05,221 [766:MainThread] mopidy_pummeluff.registry
Mar 09 15:42:05 raspberrypi mopidy[766]:   Registry not existing yet on "/var/lib/mopidy/pummeluff/tags.json"
Mar 09 15:42:05 raspberrypi mopidy[766]: ERROR    2022-03-09 15:42:05,223 [766:MainThread] mopidy.ext
Mar 09 15:42:05 raspberrypi mopidy[766]:   Failed to load extension pummeluff: cannot import name 'MCPWatcher' from 'mopidy_pummeluff.threads' (/usr/local/lib/python3.9/dist-packages/Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg/mopidy_pummeluff/threads/__init__.py)
Mar 09 15:42:05 raspberrypi mopidy[766]: Traceback (most recent call last):
Mar 09 15:42:05 raspberrypi mopidy[766]:   File "/usr/lib/python3/dist-packages/mopidy/ext.py", line 221, in load_extensions
Mar 09 15:42:05 raspberrypi mopidy[766]:     extension_class = entry_point.resolve()
Mar 09 15:42:05 raspberrypi mopidy[766]:   File "/usr/lib/python3/dist-packages/pkg_resources/__init__.py", line 2456, in resolve
Mar 09 15:42:05 raspberrypi mopidy[766]:     module = __import__(self.module_name, fromlist=['__name__'], level=0)
Mar 09 15:42:05 raspberrypi mopidy[766]:   File "/usr/local/lib/python3.9/dist-packages/Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg/mopidy_pummeluff/__init__.py", line 9, in <module>
Mar 09 15:42:05 raspberrypi mopidy[766]:     from .frontend import PummeluffFrontend
Mar 09 15:42:05 raspberrypi mopidy[766]:   File "/usr/local/lib/python3.9/dist-packages/Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg/mopidy_pummeluff/frontend.py", line 15, in <module>
Mar 09 15:42:05 raspberrypi mopidy[766]:     from .threads import GPIOHandler, TagReader, MCPWatcher
Mar 09 15:42:05 raspberrypi mopidy[766]: ImportError: cannot import name 'MCPWatcher' from 'mopidy_pummeluff.threads' (/usr/local/lib/python3.9/dist-packages/Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg/mopidy_pummeluff/threads/__init__.py)
```

### festiboxes doesn't like 4.3mm instead of 4mm
Change diameter of triangles to 30mm

### full log
```
1  curl -sS https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2samp.sh | bash
    2  alsamixer
    3  wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
    4  sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/buster.list
    5  sudo apt update
    6  sudo apt-get upgrade
    7  sudo apt install mopidy
    8  sudo apt install wondershaper
    9  ip a
   10  wondershaper wlan0 100 100
   11  sudo wondershaper wlan0 100 100
   12  sudo apt install mopidy
   13  sudo wondershaper wlan0 remove
   14  sudo apt install mopidy
   15  vim /etc/apt/sources.list
   16  vi /etc/apt/sources.list
   17  sudo vi /etc/apt/sources.list
   18  sudo apt install mopidy
   19  sudo apt install --fix-broken 
   20  sudo apt udpate
   21  sudo apt update
   22  sudo vi /etc/apt/sources.list
   23  sudo apt update
   24  sudo vi /etc/apt/sources.list
   25  sudo apt update
   26  sudo vi /etc/apt/sources.list
   27  sudo apt update
   28  fg
   29  sudo vi /etc/apt/sources.list
   30  sudo apt update
   31  sudo reboot
   32  sudo apt update
   33  sudo apt install mopidy
   34  sudo systemctl start mopidy.service 
   35  sudo apt install python3-pip
   36  sudo pip install mopidy-iris
   37  sudo systemctl restar mopidy
   38  sudo systemctl restart mopidy
   39  vim /etc/mopidy/mopidy.conf 
   40  vi /etc/mopidy/mopidy.conf 
   41  sudo vi /etc/mopidy/mopidy.conf 
   42  sudo apt install vim
   43  sudo vim /etc/mopidy/mopidy.conf 
   44  sudo systemctl restart mopidy
   45  ip a
   46  journalctl -fe
   47  sudo vim /etc/mopidy/mopidy.conf 
   48  sudo systemctl restart mopidy
   49  journalctl -fe
   50  vls
   51  ls
   52  ls -lart
   53  unzip dragons.zip -d music
   54  sudo vim /etc/mopidy/mopidy.conf 
   55  sudo mopidy-ctl local scan
   56  sudo mopidyctl local scan
   57  sudo mopidyctl scan local
   58  sudo mopidyctl --help
   59  sudo systemctl restart mopidy
   60  gst-launch-1.0 audiotestsrc ! audioresample ! autoaudiosink
   61  vim /etc/mopidy/mopidy.conf 
   62  sudo vim /etc/mopidy/mopidy.conf 
   63  sudo systemctl restart mopidy
   64  sudo journalctl -fe
   65  sudo systemctl enable mopidy
   66  sudo systemctl start mopidy
   67  sudo vim /etc/mopidy/mopidy.conf 
   68  gst-launch-1.0 audiotestsrc ! audioresample ! autoaudiosink
   69  sudo vim /etc/mopidy/mopidy.conf 
   70  sudo mopidyctl config
   71  fg
   72  sudo systemctl start mopidy
   73  sudo systemctl restart mopidy
   74  cd music
   75  ls -lart
   76  cd in_league/
   77  ls -lart
   78  su mopidy
   79  sudo su mopidy
   80  sudo vim /etc/mopidy/mopidy.conf 
   81  gst-launch-1.0 audiotestsrc ! audioresample ! autoaudiosink
   82  sudo vim /etc/mopidy/mopidy.conf 
   83  fg
   84  sudo systemctl restart mopidy
   85  sudo journalctl -fe
   86  sudo systemctl restart mopidy
   87  sudo shutdown now
   88  sudo apt install git
   89  sudo su -
   90  ./install 
   91  cd /usr/src
   92  ls
   93  cd mopidy-pummeluff/
   94  ls
   95  cd ..
   96  chmod -R 777 mopidy-pummeluff/
   97  sudo chmod -R 777 mopidy-pummeluff/
   98  cd
   99  ./install 
  100  journalctl -fe
  101  sudo vim /etc/mopidy/mopidy.conf 
  102  sudo systemctl restart mopidy
  103  journalctl -fe
  104  sudo raspi-config 
  105  journalctl -fe
  106  sudo systemctl restart mopidy
  107  journalctl -fe
  108  sudo usermod -a -G spi,gpio mopidy
  109  echo "mopidy ALL = NOPASSWD: /sbin/shutdown" > /etc/sudoers.d/mopidy
  110  sudo systemctl restart mopidy
  111  journalctl -fe
  112  sudo pip install spidev
  113  journalctl -fe
  114  vim mopidy_transfer.zip 
  115  sudo reboot
  116  journalctl -fe
  117  vim mopidy_transfer.zip 
  118  ./install 
  119  journalctl -fe
  120  fg
  121  vim mopidy_transfer.zip 
  122  ./install 
  123  journalctl -fe
  124  vim install 
  125  cd /usr/src
  126  ls
  127  cd mopidy-pummeluff/
  128  ls
  129  cd ..
  130  sudo chmod -R 700
  131  sudo chmod -R 700 *
  132  ls
  133  sudo chown -R mopidy *
  134  ls
  135  cd
  136  vim install 
  137  ./install 
  138  cd /usr/src
  139  chmod o+rwx mopidy-pummeluff/
  140  sudo chmod o+rwx mopidy-pummeluff/
  141  cd
  142  ./install 
  143  vim install 
  144  cd -
  145  ls
  146  ls -lart
  147  chmod -R 777 mopidy-pummeluff/
  148  sudo chmod -R 777 mopidy-pummeluff/
  149  cd -
  150  ./install 
  151  journalctl -fe
  152  vim /usr/local/lib/python3.9/dist-packages/Mopidy_Pummeluff-2.2.1.dev9+gb5e52eb.d20220309-py3.9.egg/mopidy_pummeluff/frontend.py
  153  vim install 
  154  cd /usr/src/mopidy-pummeluff/mopidy_pummeluff/
  155  vim frontend.py
  156  cd mopidy-pummeluff/
  157  ls
  158  cd ..
  159  ls
  160  ls -lart
  161  cd
  162  vim install 
  163  vim mopidy_transfer.zip 
  164  vim install 
  165  vim mopidy_transfer.zip 
  166  vim install 
  167  ./install 
  168  journalctl -fe
  169  vim mopidy_transfer.zip 
  170  ./install 
  171  journalctl -fe
  172  ./install 
  173  journalctl -fe
  174  vim mopidy_transfer.zip 
  175  vim /etc/mopidy/mopidy.conf 
  176  sudo vim /etc/mopidy/mopidy.conf 
  177  sudo systemctl restart mopidy
  178  journalctl -fe
  179  sudo vim /etc/mopidy/mopidy.conf 
  180  vim mopidy_transfer.zip 
  181  sudo pip install gpiozero
  182  vim mopidy_transfer.zip 
  183  journalctl -fe
  184  sudo systemctl restart mopidy
  185  journalctl -fe
  186  sudo vim /usr/local/lib/python3.9/dist-packages/Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg/mopidy_pummeluff/threads/
  187  vim /usr/local/lib/python3.9/dist-packages/Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg/mopidy_pummeluff/threads/
  188  cdm /usr/local/lib/python3.9/dist-packages/Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg/mopidy_pummeluff/threads/
  189  cd /usr/local/lib/python3.9/dist-packages/Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg/mopidy_pummeluff/threads/
  190  ls
  191  ls -lart
  192  chmod +x mcp_watcher.py 
  193  sudo chmod +x mcp_watcher.py 
  194  cd
  195  ./install 
  196  journalctl -fe
  197  cd /usr/src/mopidy-pummeluff/
  198  ls
  199  cd mopidy_pummeluff/
  200  ls
  201  ls -lart
  202  cd threads/
  203  ls -lart
  204  cd ..
  205  chmod 777 -R *
  206  sudo chmod 777 -R * mopidy-pummeluff/
  207  journalctl -fe
  208  cd
  209  ./install 
  210  journalctl -fe
  211  cd /usr/local/lib/python3.9/dist-packages/Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg/mopidy_pummeluff/threads/
  212  ls -lart
  213  cd ..
  214  ls -lart
  215  sudo systemctl restart mopidy
  216  journalctl -fe
  217  cd /usr/local/lib/python3.9/dist-packages/Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg/mopidy_pummeluff/threads/
  218  ls -lart
  219  cd
  220  cd /usr/src/mopidy-pummeluff/
  221  ls
  222  ls -lart
  223  cd th
  224  cd mopidy_pummeluff/threads/
  225  ls -lart
  226  cd
  227  vim install 
  228  ./install 
  229  journalctl -fe
  230  sudo shutdown now
  231  sudo vim /etc/mopidy/mopidy.conf 
  232  find / * -name "pummeluff"
  233  sudo find / * -name "pummeluff"
  234  vim mopidy_transfer.zip 
  235  sudo find / * -name "*pummeluff*"
  236  sudo vim /etc/mopidy/mopidy.conf 
  237  journalctl -fe
  238  cd /usr/local/lib/python3.9/dist-packages/Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg
  239  ls
  240  cd ..
  241  ls -lart
  242  mv Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg.b
  243  sudo mv Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg.b
  244  sudo systemctl restart mopidy
  245  journalctl -fe
  246  cd 
  247  ./install 
  248  journalctl -fe
  249  vim mopidy_transfer.zip 
  250  find / * -name "gpiozero"
  251  sudo find / * -name "gpiozero"
  252  vim /usr/lib/python3/dist-packages/gpiozero
  253  vim mopidy_transfer.zip 
  254  vim install 
  255  ./install 
  256  journalctl -fe
  257  vim mopidy_transfer.zip 
  258  ./install 
  259  journalctl -fe
  260  sudo shutdown now
  261  ls
  262  ls -lart
  263  cd Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg
  264  ls
  265  sudo systemctl restart mopidy
  266  journaltctl -fe
  267  journalctl -fe
  268  ls
  269  ls -lart
  270  cd ..
  271  ls
  272  ls -lart
  273  cd ..
  274  ls
  275  cd ..
  276  ls
  277  cd -
  278  ls
  279  cd dist-packages/
  280  ls
  281  vim easy-install.pth 
  282  vim setuptools.pth 
  283  sudo shutdown
  284  sudo shutdownnow
  285  sudo shutdown now
  286  history
  287  cd /usr/local/lib/python3.9/dist-packages/
  288  ls
  289  ls -lart
  290  cd Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg
  291  ls -lart
  292  cd ..
  293  ls -lart
  294  journalctl -fe
  295  ls -lart
  296  journalctl -fe
  297  ls -lart
  298  cd -
  299  ls -lart
  300  cd mopidy_pummeluff/
  301  ls -lart
  302  ls -lart threads/
  303  vim threads/mcp_watcher.py 
  304  ls
  305  cd ..
  306  ls
  307  ls -lart
  308  cd Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg
  309  ls -lart
  310  cd mopidy_pummeluff/
  311  ls
  312  vim threads/mcp_watcher.py 
  313  python -m mopidy_pummeluff 
  314  journalctl -fe
  315  cd ..
  316  cd ,,
  317  cd ..
  318  mv Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg.b.b
  319  sudo mv Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg Mopidy_Pummeluff-2.2.1.dev19+g67a9e20.d20220309-py3.9.egg.b.b
  320  sudo systemct restart mopidy
  321  sudo systemctl restart mopidy
  322  journalctl -fe
  323  ls -lart
  324  journalctl -fe
  325  ls -lart
  326  tmux
  327  sudo apt install tmux
  328  tmux
  329  cd /usr/src
  330  ls
  331  cd mopidy-pummeluff/
  332  ls
  333  sudo python setup.py install
  334  ./install 
  335  cd 
  336  vim install 
  337  cd -
  338  cd /usr/src
  339  vim mopidy-pummeluff/setup.
  340  vim mopidy-pummeluff/setup.py 
  341  ip a
  342  ping abc.net.au
  343  ping duckduckgo.com
  344  ip a
  345  ping duckduckgo.com
  346  sudo apt update
  347  nmtui
  348  sudo apt install nmtui
  349  ifconfig
  350  nmcli
  351  sudo apt install nmcli
  352  vim /etc/mopidy/mopidy.conf 
  353  sudo vim /etc/mopidy/mopidy.conf 
  354  sudo systemctl restart mopidy
  355  journalctl -fe
  356  sudo vim /etc/mopidy/mopidy.conf 
  357  sudo systemctl restart mopidy
  358  journalctl -fe
  359  fg
  360  sudo systemctl restart mopidy
  361  journalctl -fe
  362  sudo apt install Mopidy-Spotify
  363  sudo python3 -m pip install Mopidy-Spotify
  364  sudo apt install liibspotify12 pyspotify
  365  sudo apt install libspotify12 python3-spotify
  366  sudo reboot
  367  sudo apt install libspotify12 python3-spotify
  368  journalctl -fe
  369  sudo systemctl restart mopidy
  370  journalctl -fe
  371  sudo python3 -m pip install Mopidy-Spotify
  372  sudo systemctl restart mopidy
  373  journalctl -fe
  374  fg
  375  vim /etc/mopidy/mopidy.conf 
  376  sudo vim /etc/mopidy/mopidy.conf 
  377  vim /etc/mopidy/mopidy.conf 
  378  sudo vim /etc/mopidy/mopidy.conf 
  379  vim mopidy_transfer.zip 
  380  vim test.py
  381  python test.py 
  382  vim mopidy_transfer.zip 
  383  cd /usr/src
  384  python mopidy-pummeluff/mopidy_pummeluff/threads/mcp_watcher.py 
  385  cd /usr/src
  386  python mopidy-pummeluff/mopidy_pummeluff/threads/mcp_watcher.py 
  387  python
  388  ls
  389  cd mopidy-pummeluff/
  390  ls
  391  python -m mopidy_pummeluff 
  392  python mopidy_pummeluff/threads/mcp_watcher.py 
  393  history
```

```
# Florence player install script
# 

set -e
sudo mkdir -p /usr/local/share/keyrings
sudo wget -q -O /usr/local/share/keyrings/mopidy-archive-keyring.gpg \
  https://apt.mopidy.com/mopidy.gpg
sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/buster.list
sudo apt update 
sudo apt-get upgrade
echo "Press enter to edit sources.list and choose an alternative mirror or Esc :q! to quit"
read
sudo vi /etc/apt/sources.list
sudo apt install mopidy vim git
sudo systemctl start mopidy.service 
sudo systemctl enable mopidy.service 
sudo apt install python3-pip
sudo pip install mopidy-iris
echo "Testing speaker"
gst-launch-1.0 audiotestsrc ! audioresample ! autoaudiosink
echo "Press enter to continue"
read

sudo pip install spidev
sudo python setup.py install
sudo usermod -a -G spi,gpio mopidy
echo "mopidy ALL = NOPASSWD: /sbin/shutdown" > /etc/sudoers.d/mopidy


sudo apt install libspotify12 python3-spotify
sudo python3 -m pip install Mopidy-Spotify


echo "Editing mopidy.conf. Save your config here now."
read
sudo vim /etc/mopidy/mopidy.conf 
sudo systemctl restart mopidy


cd
./install
```

### GStreamer fails after everything installed
https://forums.raspberrypi.com/viewtopic.php?t=196744
![[output.pdf]]

### tried sudo rpi-update
successful but also disabled mopidy, on restarting gpio stealing i2s

#### something to do with pummeluff
works without it

/I stole it's I2S GPIO!!!!/ Change the GPIO for the station selector and boom! music!

### network drops out still 
why?
not a problem on ether

when large amount of traffic occurs seems to drop out. comes back up after a few minutes.
iris stays going because it's not polling obviously.