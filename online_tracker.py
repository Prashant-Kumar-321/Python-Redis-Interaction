import redis

# Connect to Redis 
r = redis.Redis(host='localhost', port=6379, db=0)

def main(): 
    login_user("Prashant")
    login_user("John")
    login_user("Alice")

    show_online_users()
    online_users_count()

    logout_user("John")

    show_online_users()
    online_users_count()

    delete_online_users()

def login_user(username): 
    r.lpush("online_users", username)
    print(f"{username} loged In")

def logout_user(username): 
    r.lrem("online_users", 1, username)
    print(f"{username} loged Out")

def show_online_users(): 
    users = r.lrange("online_users", 0, -1)
    users = [user.decode("utf-8") for user in users]
    
    print("Online Users:")
    id = 1
    for user in users: 
        print(f"{id}) {user}")
        id += 1
    
def online_users_count(): 
    count = r.llen("online_users")
    print(f"{count} users are currently online.") 

def delete_online_users(): 
    r.delete("online_users")





if __name__ == "__main__": 
    main()