from redis import Redis 
import time
import sys

# Connect to the Redis
r_client = Redis(
    host="localhost", 
    port=6379, 
    db=1
)

KEY = "messageboard:5:online_users"

def main(): 
    check_connection()

    login_user("Alice")
    login_user("Bob")
    time.sleep(10)
    login_user("Priti")
    login_user("Swati")

    print("Before Wating for 20 seconds")
    log_online_users()
    online_users_count()
    time.sleep(20)
    remove_inactive_users()

    print("After removing inactive users:")
    log_online_users()
    online_users_count()

    r_client.delete(KEY)

def check_connection(): 
    try: 
        response = r_client.ping()
        print("Connection to redis is successful!!")
        print(f"Response: {response}")

    except Exception as ex: 
        print("Some Error Ocurred")
        print("Could not connect to redis server")
        print(f"Error: {ex}")
        sys.exit()

def login_user(username): 
    expiration_time = int(time.time()) + 30

    r_client.zadd(KEY, {
        username: expiration_time
    })

def remove_inactive_users(): 
    current_time  = int(time.time())
    removed_elements = r_client.zremrangebyscore(KEY, 0, current_time)
    
    print(f"{removed_elements} are removed")

def log_online_users():
    users = r_client.zrange(KEY, 0, -1, withscores=True)

    for user, score in users:
        print(f"{user.decode('utf-8')}: {int(score)}")

def online_users_count(): 
    users = r_client.zcard(KEY)
    
    print(f"Online users: {users}")


if __name__ == '__main__': 
    main()



