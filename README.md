# pulse-launch

A simple python script to launch a command when a pulseaudio sink changes

## Usage

```
usage: pulse-launch.py [-h] [--other_cmd OTHER_CMD] sink_name cmd

positional arguments:
  sink_name             name of the sink you want to launch smth for
  cmd                   the cmd you want to launch if sink-name is default

optional arguments:
  -h, --help            show this help message and exit
  --other_cmd OTHER_CMD
                        the cmd you want to launch if sink-name is not default
```
