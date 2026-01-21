# How the X "For You" Feed Works

A simple explanation for everyone - no tech knowledge required.

---

## What is the "For You" Feed?

When you open X (formerly Twitter), the "For You" tab shows you posts. But how does X decide which posts to show you first? That's what this guide explains.

---

## The Basic Idea

X tries to show you posts you'll **actually enjoy** - posts you might like, reply to, or share. It learns what you like by watching what you do.

Think of it like a friend who knows your taste in movies. After watching enough movies together, they can predict what you'll enjoy next.

---

## Where Do the Posts Come From?

X pulls posts from two places:

### 1. People You Follow
Posts from accounts you already follow. X calls this "in-network" content.

### 2. Discovery
Posts from people you *don't* follow, but X thinks you'll like. These are found by looking at what similar users enjoy.

```
Your Feed = Posts from people you follow
          + Posts X thinks you'll discover and love
```

---

## How X Ranks Posts

Every post gets a **score**. Higher score = shown higher in your feed.

The score is based on predictions: "How likely is this person to..."

- **Like** this post?
- **Reply** to it?
- **Repost** it?
- **Share** it?
- **Watch the video** (if it has one)?
- **Click** on it?
- **Follow** the author?

Each action has a different **weight**:
- Replies and quotes matter more (you're really engaged)
- Likes matter, but less than replies
- Following someone is a strong signal

### Negative Signals Too

X also predicts if you might:
- Click "Not Interested"
- Block or mute the author
- Report the post

These **lower** the score. If X thinks you'll hate something, it pushes it down.

---

## The Scoring Formula

In simple terms:

```
Post Score = (Chance you'll like it × Like weight)
           + (Chance you'll reply × Reply weight)
           + (Chance you'll repost × Repost weight)
           + ... and so on for each action
           - (Chance you'll block × Block penalty)
           - (Chance you'll report × Report penalty)
```

The post with the highest score appears first.

---

## Why You See Variety (Author Diversity)

Ever notice you don't see 10 posts in a row from the same person?

X intentionally mixes things up. If someone posts a lot, their second post gets a lower score than their first, their third even lower, and so on.

This keeps your feed interesting and prevents any single account from taking over.

---

## Video Posts

Videos in the "sweet spot" (15-60 seconds) get a small boost. X has found these tend to be most engaging.

Very short clips or very long videos get less of a boost.

---

## What X Removes

Before showing you posts, X filters out:
- Posts you've already seen
- Your own posts (you don't need to see them again)
- Posts from people you blocked or muted
- Posts with keywords you've muted
- Duplicate reposts of the same content
- Very old posts
- Spam and rule-breaking content

---

## The AI Behind It

X uses a large AI model (based on Grok) to make all these predictions. It learns from:

- **Your history**: What you've liked, replied to, shared, and scrolled past
- **The post itself**: What it says, who wrote it, whether it has media
- **Patterns**: What millions of other users do

The AI doesn't use hand-written rules like "show sports to sports fans." Instead, it learns patterns automatically from behavior.

---

## Key Takeaways

1. **Your actions shape your feed** - Like, reply, and share content you enjoy. X will show you more of it.

2. **Negative signals matter** - If you often block accounts or click "Not Interested," X learns to avoid similar content.

3. **Engagement depth matters** - Replies and quotes signal stronger interest than likes.

4. **Discovery is intentional** - X deliberately shows you posts from outside your network to help you find new voices.

5. **No one person dominates** - The diversity system ensures your feed stays varied.

---

## Common Questions

**Q: Why do I see posts from people I don't follow?**
A: X mixes in "discovery" content it thinks you'll like, based on what similar users enjoy.

**Q: Why did a post I don't like appear?**
A: The AI isn't perfect. Use "Not Interested" or mute/block to teach it.

**Q: Does posting time matter?**
A: Newer posts generally score higher, but a great older post can still appear if X thinks you'll love it.

**Q: Are some accounts "boosted"?**
A: The algorithm doesn't manually boost accounts. Scores come from predicted engagement, which naturally favors accounts whose content resonates with users.

---

## Want to Go Deeper?

- **[README.md](README.md)** - Full technical documentation
- **[simulator.py](simulator.py)** - Run `python simulator.py` to see the scoring in action

---

*This guide simplifies a complex system. The actual algorithm has many more details, but these are the core concepts that determine what you see.*
