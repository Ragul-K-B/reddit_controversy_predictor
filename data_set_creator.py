import praw
import pandas as pd
import time

client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
user_agent = 'controversy-analyzer by u/YOUR_USERNAME'
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

subreddits = [
    # 🔥 Serious / News / Opinion
    'politics',
    'worldnews',
    'news',
    'unpopularopinion',
    'changemyview',
    'technology',
    'askscience',
    'askphilosophy',
    'AskHistorians',
    'science',

    # 🎭 Entertainment / Culture
    'movies',
    'television',
    'gaming',
    'music',
    'books',
    'Documentaries',

    # 🏀 Sports
    'sports',
    'nba',
    'soccer',
    'formula1'
]
posts_per_sub = 400
all_posts = []

for sub in subreddits:
    subreddit = reddit.subreddit(sub)
    print(f"📥 Fetching from r/{sub}...")

    sub_posts = []
    for post in subreddit.top(limit=1500, time_filter='all'):
        if len(sub_posts) >= posts_per_sub:
            break

        # ✅ Text-only, not stickied, selftext must exist and be longer than 100 chars
        if (
            post.is_self and
            not post.stickied and
            post.selftext and
            len(post.selftext.strip()) > 100
        ):
            score = post.score
            upvote_ratio = post.upvote_ratio
            num_comments = post.num_comments
            controversy_score = (num_comments / (score + 1)) * (1 - upvote_ratio)

            post_data = {
                'subreddit': sub,
                'title': post.title,
                'selftext': post.selftext[:1000],
                'score': score,
                'upvote_ratio': upvote_ratio,
                'num_comments': num_comments,
                'controversy_score': round(controversy_score, 4),
                'post_url': post.url,
                'permalink': f"https://www.reddit.com{post.permalink}"
            }

            sub_posts.append(post_data)

            if len(sub_posts) % 100 == 0:
                print(f"🔄 Collected {len(sub_posts)} from r/{sub}")
                time.sleep(1)

    print(f"✅ Finished r/{sub}: {len(sub_posts)} collected.")
    all_posts.extend(sub_posts)

# 📊 Final check
df = pd.DataFrame(all_posts)
print("\n🔥 Final subreddit distribution:")
print(df['subreddit'].value_counts())

# 💾 Save to file
df.to_csv(r'R:\Python\reddit\reddit_conterversy_analyser\dataset.csv', index=False)
print("\n📁 Saved as 'balanced_dataset.csv'")