# Copyright (c) 2021 Philipp Hochkamp
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import threading
from subprocess import Popen

import pulsectl

def second_thread(args):
    with pulsectl.Pulse('name-fetcher') as pulse:
        print(pulse.server_info().default_sink_name)
        if pulse.server_info().default_sink_name == args.sink_name:
            Popen(args.cmd, shell=True)
        else:
            Popen(args.other_cmd, shell=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "sink_name",
        help="name of the sink you want to launch smth for")
    parser.add_argument(
        "cmd", help="the cmd you want to launch if sink-name is default")
    parser.add_argument(
        "--other_cmd",
        help="the cmd you want to launch if sink-name is not default")
    args = parser.parse_args()

    with pulsectl.Pulse('event-printer') as pulse:
        def handle_event(ignore):
            threading.Thread(target=second_thread, args=(args,)).run()
        handle_event(False)
        pulse.event_mask_set('sink')
        pulse.event_callback_set(handle_event)
        pulse.event_listen()


if __name__ == "__main__":
    main()
