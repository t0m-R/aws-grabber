import requests
import argparse
import platform
import os
import subprocess

def getOS():
    return os.platform.system()

def awspath(os):
    if os == "Windows":
        path = "~\\.aws"
    else:
        path = '~/.aws'
    return os.path.expanduser(path)

def arg_parser(os):
    parser = argparse.ArgumentParser(description='Grabber for credentials of AWS Student Pack')
    parser.add_argument('--user', '-u', metavar="user@mail.com", required=True)
    parser.add_argument('--passwd', '-p', metavar='passwd', required=True)
    parser.add_argument('--awspath', '-a', metavar='.aws/ folder PATH ', default=awspath(os))
    parser.add_argument('--output', '-f', metavar='aws output type', default='json')
    parser.add_argument('--region', '-r', metavar='aws region', default='us-east-1')
    parser.add_argument('--profile', metavar='aws profile name', default='default')
    args = parser.parse_args()
    return args

def main():
    os = getOS()
    args = arg_parser(os)
    credentials = get_credentials(args.user, args.passwd)
    config = get_config(args.region, args.output)
    if check_path(os, args.awspath, 'credentials'):
        write(args.awspath, 'credentials', args.profile, credentials)
    if check_path(os, args.awspath, 'config'):
        write(args.awspath, 'config', args.profile, config)

def get_config(region, output):
    config = []
    config.append('region=' + region)
    config.append('output=' + output)
    return config

def get_credentials(user, passwd):
    ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    url  = "https://labs.vocareum.com"
    url2 = url + "/util/vcauth.php"
    payload = { 'sender': 'home', 'loginid': user, 'passwd': passwd}
    headers = {'User-Agent':ua, 'Accept-Language': 'en-GB,en;q=0.5'}
    url3 = url + '/main/main.php?m=course&code=vc_2_0_AWS'
    url4 = url + '/main/main.php?m=editor&nav=1&asnid=14334&stepid=14335'
    url5 = url + "/util/vcput.php?a=getaws&nores=0&stepid=14335&mode=s&type=0&vockey="
    with requests.session() as s:
        s.get(url, proxies=burp, headers=headers, stream=True)
        s.post(url2,data=payload, headers=headers, stream=True)
        s.get(url3, headers=headers, stream=True)
        s.get(url4, headers=headers, stream=True)
        url5 += s.cookies['logintoken']
        aws = s.get(url5, headers=headers, stream=True)
        text = aws.text.split('\n')[1:4]
        return text

def check_path(os, path, fname):
    if os.path.exists(path):
        if os.path.exists(os.path.join(path, fname)):
            print("Found an existing {0} file! Moved to {0}.old".format(fname))
            if os == "Windows":
                continue
            else:
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
