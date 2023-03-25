# CELLO-3.0

CELLO-3.0 is a software package for designing and simulating genetic circuits. It includes a core cell-logic synthesis process, an interactive shell interface, and a Python package that can be used as a component in other software. CELLO-3.0 is designed to be lightweight, error-proof, and capable of handling both inter-cellular partitioning and intra-cellular partitioning.

## Installation

To install CELLO-3.0, simply follow these steps:

First, install [Redis](https://redis.io/docs/getting-started/installation/) on your computer

On MacOS:
```
brew install redis
```
(for other platforms, please check Redis installation guide)


Get ready to run run Cello-v3!
```
git clone https://github.com/your-username/cello-3.0.git
cd CELLO-3.0/
```

It's always a good idea to set up a python virtual environment first, venv is fine.
```
python -m venv venv
source venv/bin/activate
```

Last step, and now you are ready!
```
pip install -r req.txt
```


## Usage

CELLO-3.0 can be used in a variety of ways, depending on your needs:

- As a standalone tool: Use the interactive shell interface to design and simulate genetic circuits.
- As a Python package: Import the core CELLO code as a Python library and use it as a component in your own software.
- As a website: Use the Cello3.0 website, built in Python, to run CELLO-3.0.

CELLO-3.0 includes a proprietary UCF formatter tool that can modify or create UCF files from a website, allowing for intuitive editing of the data inside. Users can also download UCF files from the website.

#### Running CELLO:

[COMING SOON!]()

#### Running UCFormatter tool:

```
cd UCFormatter/
python UCFormatter.py
```
Navigate to [localhost:8050]() to see use UCFormatter.

## Features

* Core cell-logic synthesis process from genetic or logic circuits.
* Capable of handling both inter-cellular partitioning and intra-cellular partitioning
* Transform design to SBOL format for universtal transport

## UCF

The Cello software designs the DNA sequences for programmable circuits based on a high-level software description and a library of characterized DNA parts representing Boolean logic gates. The user constraints file (UCF) is a JavaScript Object Notation (JSON) file that describes a part and gate library for a particular organism.

## Future Work

CELLO-3.0 is an ongoing project, and future work may include:

* Optimizing Yosys commands for logic synthesis
* Develop more compatibility with any genetic circuit designs
* Integrating with other genetic engineering tools and databases

## Contributing

We welcome contributions from the community! If you'd like to contribute to CELLO-3.0, please follow the guidelines in the CONTRIBUTING.md file.

## Credits

CELLO-3.0 was developed by Weiqi Ji and [other contributors]() at [CIDAR LAB](https://www.cidarlab.org) under Douglas Densmore. It was inspired by the original CELLO software package developed by [CIDAR LAB](https://www.cidarlab.org) and [other contributors]().

## License

CELLO-3.0 is released under the [license name] license. See the LICENSE file for more information.

## Troubleshoot:

If You get the error that port 8050 is already running, you can try to shut it down this way:

```
redis-cli shutdown
```
(Ignore if it takes forever, use 'ctrl+c')

```
lsof -i :8050
```

This will show you as list of PIDs running on port 8050

```
kill PID
```
(use the PIDs that listed from the last step, repeat if needed)

**Now, you are able to restart Cello again!**

If that doesn't work, just restart your computer, all your cache will be reset this way.

