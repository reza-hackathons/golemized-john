# golemized-john
A golemized docker image for cracking some passwd file in a distributed manner!
## Steps
1. Make sure you have docker installed.  
- `cd golem-john-docker`  
- `docker build -t YOUR-USERNAME/golem-john:YOUR-TAG .`  
- `docker push YOUR-USERNAME/golem-john:YOUR-TAG`  
2. Golemize the docker image.  
- `python3 -m venv SOME-VIRTUAL-ENV-NAME`  
- `source SOME-VIRTUAL-ENV-NAME/bin/activate`  
- `pip3 install -U pip`  
- `pip3 install yapapi certifi gvmkit-build`  
- `gvmkit-build YOUR-USERNAME/golem-john:YOUR-TAG`  
- `gvmkit-build YOUR-USERNAME/golem-john:YOUR-TAG --push`
- `Save the returned hash and put it into the script.py`   
3. Ask the providers to compile.  
- Open a new terminal: `yagna service run`  
- Open a new terminal: `export YAGNA-APPKEY = YOUR-YAGNA-APPKEY`  
- `yagna payment init -r`  
- `python script.py`  
4. Inspect the contents of the `out` folder to see which nodes have cracked the passwd. 
- `cd out`  
- `cat cracked_*`  

## Demo  
[https://youtu.be/L1ht9E93I_0](https://youtu.be/L1ht9E93I_0)  

## Caveat
Some nodes may fail to crack the passwd.  
