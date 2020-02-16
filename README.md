# aws-grabber
Python Script to grab the AWS Educate credentials so students can use aws-cli v1.

## About
This command will update the configuration files of `aws-cli` with new credentials.
It will grab for you `aws_access_key`, `aws_secret_acces_key` and `aws_session_token` from [Vocareum Labs](https://labs.vocareum.com) and write them in `~/.aws/credentials` and `~/.aws/config`.
Basic usage:
```
python3 grabber.py -u user@mail.com -p passwd
```

## Installation

Download and extract this repo as a zip file or clone it using HTTPS:

```
git clone https://github.com/t0m-R/aws-grabber.git
```

## Dependencies
This script modifies config files of `aws-cli` and **suppose that you have it already installed**, for more information see [Installing the AWS CLI version 1](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv1.html).

`aws-grabber` use `requests` module for making https requests. You can install it with:
```
pip install requests
```

The other modules are part of the Python Standard Library and are built-in with python.

## Usage

`grabber.py` need username and password to work:
```
python3 grabber.py -u user@mail.com -p passwd
```
It will update the config files in the default installation path for aws cli with new credentials.
Existing files will be renamed with a trailing `.old`.
For more information see [Installing the AWS CLI version 1](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv1.html).



If you have installed `aws-cli` somewhere else use the flag `--awspath` or `-a` to the location of your `.aws` folder using absolute path notation:
```
python3 grabber.py -u user@mail.com -p passwd -a /your/custom/absolute/path
```



The default output for `aws-cli` is JSON. You can change it with the flag `--output`, `-o`:
```
python3 grabber.py -u user@mail.com -p passwd -o text
```
For more information of accepted formats see [How to Select the Output Format](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-output.html).



At the moment AWS Students have a `default` profile name and can use only `us-east-1` region.
If this behaviour changes you can modify these parameters with   `--region`, `-r` flag for region, and `--profile`, `-p` for profile:
```
python3 grabber.py -u user@mail.com -p passwd -p MyProfile -r eu-central-1
```
For more information of accepted region see [AWS Service Endpoints](https://docs.aws.amazon.com/general/latest/gr/rande.html).


## License

[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html)
