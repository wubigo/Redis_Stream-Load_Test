# Redis Stream Performance Testing :

The purpose of this repository is to create a way to evaluate the performance of redis stream. Because Redis Benchmark doesn't allow to test the Redis Stream.

To do that we will use Locust.

## Dependencies

There are not so much dependencies

```bash
$ pip3 install -r requirments.txt
```


## Usage

You have to update your configuration of redis in the `settins.py` file.

```python
redis_host="localhost"
redis_port=6379
redis_password='PASSWORD'
```
Then you just to have to run th program :

```bash
$ locust -f redis_stream.py
```

If you need to have lots of clients and benefit the multi cores of your computer you will have to open as much as terminals you want/have cores.   

And lauch in one termianl : 

```bash
$ locust -f redis_stream.py --master --expect-workers=X
```
With X the number of slaves

and in others terminal :

```bash
locust -f Scripts/redis_get_set.py --worker
```


And then in a browser open :

__http://localhost:8089/__