#!/usr/bin/env python
import argparse
from app import app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-cfg",
                        "--config_name",
                        default="default_settings",
                        dest="cfg",
                        action='store',
                        required=False,
                        help="the settings config file in ./conf")
    args, unk = parser.parse_known_args()
    # load default settings
    app.config.from_object('conf.{0}'.format(args.cfg))
    # using 0.0.0.0 instead of 127.0.0.1 makes this server open to
    # other machines on the network.
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    main()