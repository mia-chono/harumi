import requests
import datetime


class AnimationDigitalNetworkAPI:
    domain = "animationdigitalnetwork.fr"
    api_domain = 'gw.api.{domain}'.format(domain=domain)

    def __init__(
            self,
            username: str,
            password: str,
            source: str = "Web",
    ) -> None:
        self.username = username
        self.password = password
        self.source = source
        self.http = requests.Session()

    def login(self) -> dict:
        """create a new session with the API, receive json response"""

        json = {
            'username': '{}'.format(self.username),
            'password': '{}'.format(self.password),
            'source': '{}'.format(self.source),
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Referer': 'https://{domain}/'.format(domain=self.domain),
        }

        return self.http.request(
            method='POST',
            url='https://{api}/authentication/login'.format(api=self.api_domain),
            headers=headers,
            json=json,
        ).json()

    def get_profiles(self, access_token: str) -> list[dict]:
        """get the list of profiles"""
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token),
            'Accept': 'application/json',
            'Referer': 'https://{domain}/'.format(domain=self.domain),
        }

        return self.http.request(
            method='GET',
            url='https://{api}/profile'.format(api=self.api_domain),
            headers=headers,
        ).json().get('profiles')

    def select_profile(self, access_token: str, profile_id: int) -> dict:
        """select a profile and allow to use the API"""
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {token}'.format(token=access_token),
            'X-Profile-ID': '{profile_id}'.format(profile_id=profile_id),
            'Referer': 'https://{domain}/'.format(domain=self.domain),
            'DNT': '1',
        }

        return self.http.request(
            method='GET',
            url='https://{api}/user/pincode'.format(api=self.api_domain),
            headers=headers,
        ).json()

    def _get_videos_from_date(self, access_token: str, profile_id: int, date: str) -> list[dict]:
        """retrieves all videos of the provided date"""
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {token}'.format(token=access_token),
            'X-Profile-ID': '{profile_id}'.format(profile_id=profile_id),
            'Referer': 'https://{domain}/'.format(domain=self.domain),
            'DNT': '1',
        }

        return self.http.request(
            method='GET',
            url='https://{api}/video/calendar?date={date}'.format(api=self.api_domain, date=date),
            headers=headers,
        ).json().get('videos')

    def get_videos_from_dates(self, access_token: str, profile_id: int, *dates: str) -> list[dict]:
        """Retrieves all videos of the provided dates

        :parameter dates: is an optionnal param, but when gived it must be in the format YYYY-MM-DD

        :returns: a list of videos, when no dates are provided, it returns all videos of the current day
        """
        videos = []

        if not dates:
            return self._get_videos_from_date(access_token, profile_id, datetime.date.today().strftime("%Y-%m-%d"))

        for date in dates:
            result = self._get_videos_from_date(access_token, profile_id, date)
            videos.extend(result)

        return videos

    def search(self, access_token: str, profile_id: int, query: str) -> list[dict]:
        """search on all shows of adn

        :returns: series or movies that match the query
        """
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {token}'.format(token=access_token),
            'X-Profile-ID': '{profile_id}'.format(profile_id=profile_id),
            'Referer': 'https://{domain}/'.format(domain=self.domain),
            'DNT': '1',
        }

        return self.http.request(
            method='GET',
            url='https://{api}/show/catalog?search={query}'.format(api=self.api_domain, query=query),
            headers=headers,
        ).json().get('shows')

    def get_show_details(self, access_token: str, profile_id: int, url: str) -> dict:
        """get the details of the show

        :parameter url: is the url of the show, it can be found in the search method or copy/paste from the website
        """
        series_name = url.split('/')[-1]
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {token}'.format(token=access_token),
            'X-Profile-ID': '{profile_id}'.format(profile_id=profile_id),
            'Referer': 'https://{domain}/'.format(domain=self.domain),
            'DNT': '1',
        }

        return self.http.request(
            method='GET',
            url='https://{api}/show/{series_name}'.format(api=self.api_domain, series_name=series_name),
            headers=headers,
        ).json().get('show')

    def get_season_from_show(self, access_token: str, profile_id: int, show_id: str) -> list[dict]:
        """get the detail of a season of a show

        :parameter url: is the url of the show, it can be found in the search method or copy/paste from the website
        :parameter season: is the number of the season
        """
        series_name = url.split('/')[-1]
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {token}'.format(token=access_token),
            'X-Profile-ID': '{profile_id}'.format(profile_id=profile_id),
            'Referer': 'https://{domain}/'.format(domain=self.domain),
            'DNT': '1',
        }

        return self.http.request(
            method='GET',
            url='https://{api}/show/{show_id}/season?order=asc'.format(api=self.api_domain, show_id=show_id),
            headers=headers,
        ).json().get('seasons')

    def get_episodes_of_a_show_season(self, access_token: str, profile_id: int, show_id: int, season_number: str) -> \
    list[dict]:
        """get the list of episodes from a show

        :parameter show_id: is the id of the show, it can be found in the search method or copy/paste from the website
        :parameter season_number: received from the get_season_from_show method, use the `season` key ("empty" word works too)
        """
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {token}'.format(token=access_token),
            'X-Profile-ID': '{profile_id}'.format(profile_id=profile_id),
            'Referer': 'https://{domain}/'.format(domain=self.domain),
            'DNT': '1',
        }

        return self.http.request(
            method='GET',
            url='https://{api}/video/show/{show_id}/?season={season_number}&limit=-1&order=asc"'.format(
                api=self.api_domain, show_id=show_id),
            headers=headers,
        ).json().get('videos')

    def get_player_file(self, access_token: str, profile_id: int, video_id: int) -> dict:
        """get the player file name use to read the video"""
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {token}'.format(token=access_token),
            'X-Profile-ID': '{profile_id}'.format(profile_id=profile_id),
            'Referer': 'https://{domain}/'.format(domain=self.domain),
            'DNT': '1',
        }

        return self.http.request(
            method='GET',
            url='https://{api}/player'.format(api=self.api_domain),
            headers=headers,
        ).json().get('player').get('fileName')

    def get_player_configuration_for_the_video(self, access_token: str, profile_id: int, video_id: int) -> dict:
        """get the player configuration for the video"""
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {token}'.format(token=access_token),
            'X-Profile-ID': '{profile_id}'.format(profile_id=profile_id),
            'Referer': 'https://{domain}/'.format(domain=self.domain),
            'DNT': '1',
        }

        return self.http.request(
            method='GET',
            url='https://{api}/player/video/{video_id}/configuration'.format(api=self.api_domain, video_id=video_id),
            headers=headers,
        ).json().get('player').get('options').get('user')

    def player_refresh_token(self, refresh_token: str) -> dict:
        """require to call it before get_video_content method"""
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Referer': 'https://{domain}/'.format(domain=self.domain),
            'X-Player-Refresh-Token': '{refresh_token}'.format(refresh_token=refresh_token),
            'DNT': '1',
        }

        return self.http.request(
            method='POST',
            url='https://{api}/player/refresh/token'.format(api=self.api_domain),
            headers=headers,
            json={'refreshToken': refresh_token},
        ).json()

    def get_video_content(self, access_token: str, profile_id: int, video_id: int) -> dict:
        """get the streaming urls and subtitles of the video

        !!! Require to call the player_refresh_token method before !!!

        :returns: a dict with the following keys:
            - "links" contains "streaming", "subtitles", "nextVideoUrl"
            - "video" is the video details
            - "metadata" of the video

        :informations: the subtitles are crypted, you need to decrypt them with the player file
        """
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {token}'.format(token=access_token),
            'X-Profile-ID': '{profile_id}'.format(profile_id=profile_id),
            'Referer': 'https://{domain}/'.format(domain=self.domain),
            'DNT': '1',
        }

        return self.http.request(
            method='GET',
            url='https://{api}/player/video/{video_id}/link?freeWithAds=true&adaptive=false&withMetadata=true&source=Web'.format(
                api=self.api_domain, video_id=video_id),
            headers=headers,
        ).json()

    def logout(self, access_token: str) -> dict:
        """destroy the current session with the API"""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Referer': 'https://{domain}/'.format(domain=self.domain),
            'X-Access-Token': '{token}'.format(token=access_token),
            'Authorization': 'Bearer {token}'.format(token=access_token),
        }

        return self.http.request(
            method='POST',
            url='https://{api}/authentication/logout'.format(api=self.api_domain),
            headers=headers,
        ).json()
