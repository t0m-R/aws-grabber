import requests
import argparse
import platform
import os
import subprocess

def awspath():
    if platform.platform().startswith("Windows"):
        path = "~\\.aws"
    else:
        path = '~/.aws'
    return os.path.expanduser(path)

def arg_parser():
    parser = argparse.ArgumentParser(description='Grabber for credentials of AWS Student Pack')
    parser.add_argument('--user', '-u', metavar="user@mail.com", required=True)
    parser.add_argument('--passwd', '-p', metavar='passwd', required=True)
    parser.add_argument('--awspath', '-a', metavar='.aws/ folder PATH ', default=awspath())
    parser.add_argument('--output', '-f', metavar='aws output type', default='json')
    parser.add_argument('--region', '-r', metavar='aws region', default='us-east-1')
    parser.add_argument('--profile', metavar='aws profile name', default='default')
    args = parser.parse_args()
    return args

def main():
    args = arg_parser()
    credentials = get_credentials(args.user, args.passwd)
    config = get_config(args.region, args.output)
    if check_path(args.awspath, 'credentials'):
        write(args.awspath, 'credentials', args.profile, credentials)
    if check_path(args.awspath, 'config'):
        write(args.awspath, 'config', args.profile, config)

def get_config(region, output):
    config = []
    config.append('region=' + region)
    config.append('output=' + output)
    return config

def get_credentials(user, passwd):
    url  = "https://labs.vocareum.com"
    url2 = url + "/util/vcauth.php"
    payload = { 'sender': 'home', 'loginid': user, 'passwd': passwd}
    url3 = url + "/util/vcput.php?a=getaws&type=0&stepid=14335&vockey="
    with requests.session() as s:
        s.get(url)
        s.post(url2,data=payload)
        url3 += s.cookies['logintoken']
        aws = s.get(url3)
        text = aws.text.split('\n')[1:4]
        return text

def check_path(path, fname):
    if os.path.exists(path):
        if os.path.exists(os.path.join(path, fname)):
            print("Found an existing {0} file! Moved to {0}.old".format(fname))
            subprocess.run(['mv', fname, str(fname+'.old')],cwd=path)
        return True
    else:
        print("Error, path do not exists:")
        print(path + '\n')
        return False

def write(path, fname, profile, text):
    with open(os.path.join(path, fname,),'w') as f:
        text.insert(0,'[' + profile + ']')
        for line in text:
            f.write(line + '\n')


if __name__ == '__main__':
    main()
