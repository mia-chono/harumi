import time
import random

from animation_digital_network_api import AnimationDigitalNetworkAPI


def wait(time_to_wait: int) -> None:
    print("Waiting for {} seconds".format(time_to_wait))
    time.sleep(time_to_wait)


api = AnimationDigitalNetworkAPI("username", "password")

user_access_token = api.login()
print(user_access_token)
access_token = user_access_token.get("accessToken")

profiles = api.get_profiles(access_token)
print(profiles)
wait(random.randint(5, 10))

print(api.select_profile(access_token, profiles[0].get("id")))
wait(random.randint(8, 15))

print(api.get_videos_from_dates(access_token, profiles[0].get("id")))
print(api.get_videos_from_dates(access_token, profiles[0].get("id"), "2022-09-03", "2022-09-04"))
wait(random.randint(10, 200))

logout_result = api.logout(access_token)
print(logout_result)
