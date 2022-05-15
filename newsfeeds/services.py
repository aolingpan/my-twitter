from newsfeeds.models import NewsFeed
from friendships.services import FriendshipService


class NewsFeedService:

    def fanout_to_followers(self, tweet):
        # followers = FriendshipService.get_followers(tweet.user)
        # 不可以将数据库操作放在for循环里面，效率会非常低
        # for follower in followers:
        #     NewsFeed.objects.create(user=follower, tweet=tweet)
        newsfeeds = [
            NewsFeed(user=follower, tweet=tweet)
            for follower in FriendshipService.get_followers(tweet.user)
        ]
        newsfeeds.append(NewsFeed(user=tweet.user, tweet=tweet))
        NewsFeed.object.bulk_create(newsfeeds)




