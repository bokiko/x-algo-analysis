#!/usr/bin/env python3
"""
X For You Feed Algorithm Simulator

Demonstrates the core scoring mechanics of the X recommendation system:
- Weighted combination of predicted engagement probabilities
- Author diversity decay to prevent feed domination
- Video content bonus scoring

Based on the actual algorithm analysis in this repository.
No external dependencies - pure Python 3.12+

Usage:
    python simulator.py
"""

from dataclasses import dataclass
from typing import Optional
import random


# Action weights for the weighted scorer
# Positive actions have positive weights, negative actions have negative weights
ACTION_WEIGHTS = {
    "favorite": 1.0,
    "reply": 2.0,        # Replies weighted higher (deeper engagement)
    "repost": 1.5,
    "quote": 2.5,        # Quotes weighted highest (creates new content)
    "click": 0.5,
    "profile_click": 0.3,
    "video_view": 0.8,
    "photo_expand": 0.3,
    "share": 1.5,
    "dwell": 0.2,        # Time spent viewing
    "follow_author": 3.0,  # High value signal
    # Negative signals
    "not_interested": -5.0,
    "block_author": -10.0,
    "mute_author": -8.0,
    "report": -15.0,
}


@dataclass
class Post:
    """A candidate post for ranking."""
    id: str
    author_id: str
    text: str
    has_video: bool = False
    video_duration_sec: Optional[float] = None
    is_in_network: bool = True


@dataclass
class EngagementPredictions:
    """Phoenix model predictions for a post."""
    favorite: float = 0.0
    reply: float = 0.0
    repost: float = 0.0
    quote: float = 0.0
    click: float = 0.0
    profile_click: float = 0.0
    video_view: float = 0.0
    photo_expand: float = 0.0
    share: float = 0.0
    dwell: float = 0.0
    follow_author: float = 0.0
    not_interested: float = 0.0
    block_author: float = 0.0
    mute_author: float = 0.0
    report: float = 0.0


def simulate_phoenix_predictions(post: Post, user_follows_author: bool) -> EngagementPredictions:
    """
    Simulate Phoenix transformer predictions.

    In the real system, this is a Grok-based transformer that takes:
    - User's engagement history (what they liked, replied to, shared)
    - Post features (content, author, media)
    And outputs probabilities for each action type.
    """
    # Base predictions with some randomness
    base = random.uniform(0.01, 0.05)

    # In-network posts generally have higher engagement predictions
    network_boost = 1.5 if user_follows_author else 1.0

    # Video content affects certain predictions
    video_boost = 1.3 if post.has_video else 1.0

    return EngagementPredictions(
        favorite=min(0.95, base * 3 * network_boost + random.uniform(0, 0.1)),
        reply=min(0.95, base * 0.5 * network_boost + random.uniform(0, 0.03)),
        repost=min(0.95, base * 0.8 * network_boost + random.uniform(0, 0.05)),
        quote=min(0.95, base * 0.3 * network_boost + random.uniform(0, 0.02)),
        click=min(0.95, base * 2 + random.uniform(0, 0.15)),
        profile_click=min(0.95, base * 0.4 + random.uniform(0, 0.05)),
        video_view=min(0.95, base * 4 * video_boost if post.has_video else 0.01),
        photo_expand=min(0.95, base * 0.6 + random.uniform(0, 0.05)),
        share=min(0.95, base * 0.4 * network_boost + random.uniform(0, 0.03)),
        dwell=min(0.95, base * 5 + random.uniform(0, 0.2)),
        follow_author=min(0.95, base * 0.1 if not user_follows_author else 0.001),
        # Negative signals should be low for good content
        not_interested=max(0.001, random.uniform(0, 0.02)),
        block_author=max(0.001, random.uniform(0, 0.005)),
        mute_author=max(0.001, random.uniform(0, 0.008)),
        report=max(0.001, random.uniform(0, 0.002)),
    )


def compute_weighted_score(predictions: EngagementPredictions) -> float:
    """
    Compute weighted score from predictions.

    Final Score = Σ (weight_i × P(action_i))

    This is the core ranking formula used by X's algorithm.
    """
    score = 0.0
    for action, weight in ACTION_WEIGHTS.items():
        probability = getattr(predictions, action)
        score += weight * probability
    return score


def apply_author_diversity_decay(
    posts_with_scores: list[tuple[Post, float]],
    decay_factor: float = 0.7
) -> list[tuple[Post, float]]:
    """
    Apply author diversity scoring.

    When multiple posts from the same author appear in the feed,
    subsequent posts get their scores attenuated to ensure diversity.

    For each author:
    - 1st post: score * 1.0
    - 2nd post: score * decay_factor
    - 3rd post: score * decay_factor^2
    - etc.
    """
    author_counts: dict[str, int] = {}
    adjusted_results = []

    for post, score in posts_with_scores:
        count = author_counts.get(post.author_id, 0)
        adjusted_score = score * (decay_factor ** count)
        author_counts[post.author_id] = count + 1
        adjusted_results.append((post, adjusted_score))

    return adjusted_results


def video_quality_bonus(post: Post) -> float:
    """
    Apply video quality bonus.

    Videos within an optimal duration range get a score boost.
    Very short or very long videos get less boost.
    """
    if not post.has_video or post.video_duration_sec is None:
        return 0.0

    duration = post.video_duration_sec

    # Optimal range: 15-60 seconds
    if 15 <= duration <= 60:
        return 0.5
    # Good range: 5-15 or 60-180 seconds
    elif 5 <= duration < 15 or 60 < duration <= 180:
        return 0.3
    # Acceptable: other durations
    else:
        return 0.1


def rank_posts(
    posts: list[Post],
    user_following: set[str]
) -> list[tuple[Post, float, EngagementPredictions]]:
    """
    Full ranking pipeline simulation.

    1. Get Phoenix ML predictions for each post
    2. Compute weighted scores
    3. Apply video bonus
    4. Apply author diversity decay
    5. Sort by final score
    """
    scored_posts: list[tuple[Post, float, EngagementPredictions]] = []

    # Step 1-3: Score each post
    for post in posts:
        user_follows = post.author_id in user_following
        predictions = simulate_phoenix_predictions(post, user_follows)
        base_score = compute_weighted_score(predictions)
        video_bonus = video_quality_bonus(post)
        score = base_score + video_bonus
        scored_posts.append((post, score, predictions))

    # Sort by score for diversity calculation
    scored_posts.sort(key=lambda x: x[1], reverse=True)

    # Step 4: Apply author diversity
    posts_scores = [(p, s) for p, s, _ in scored_posts]
    adjusted = apply_author_diversity_decay(posts_scores)

    # Rebuild with predictions
    final_results = []
    for i, (post, adjusted_score) in enumerate(adjusted):
        _, _, predictions = scored_posts[i]
        final_results.append((post, adjusted_score, predictions))

    # Step 5: Final sort
    final_results.sort(key=lambda x: x[1], reverse=True)
    return final_results


def print_ranking_breakdown(post: Post, score: float, predictions: EngagementPredictions):
    """Print detailed scoring breakdown for a post."""
    print(f"\n{'='*60}")
    print(f"Post: {post.text[:50]}...")
    print(f"Author: {post.author_id} | In-Network: {post.is_in_network}")
    if post.has_video:
        print(f"Video: {post.video_duration_sec}s")
    print(f"\nPredictions -> Weighted Contributions:")
    print(f"{'-'*60}")

    total = 0.0
    for action, weight in sorted(ACTION_WEIGHTS.items(), key=lambda x: -abs(x[1])):
        prob = getattr(predictions, action)
        contribution = weight * prob
        total += contribution
        if abs(contribution) > 0.001:  # Only show significant contributions
            sign = "+" if weight > 0 else ""
            print(f"  {action:20} P={prob:.4f} × w={weight:+.1f} = {sign}{contribution:.4f}")

    print(f"{'-'*60}")
    print(f"  Base Score: {total:.4f}")
    video_bonus = video_quality_bonus(post)
    if video_bonus > 0:
        print(f"  Video Bonus: +{video_bonus:.4f}")
    print(f"  Final Score: {score:.4f}")


def main():
    """Run the simulator with sample data."""
    print("=" * 60)
    print("X For You Feed Algorithm Simulator")
    print("=" * 60)

    # Sample posts
    posts = [
        Post("1", "alice", "Just shipped a new feature! Thread on what we learned...", is_in_network=True),
        Post("2", "alice", "Follow-up: here's the technical deep dive", is_in_network=True),
        Post("3", "bob", "Hot take: tabs are better than spaces", is_in_network=True),
        Post("4", "viral_account", "This video will change how you think about productivity",
             has_video=True, video_duration_sec=45, is_in_network=False),
        Post("5", "news_org", "Breaking: major announcement in tech industry", is_in_network=False),
        Post("6", "viral_account", "Another banger video for you",
             has_video=True, video_duration_sec=120, is_in_network=False),
    ]

    # User follows alice and bob
    user_following = {"alice", "bob"}

    print(f"\nUser follows: {', '.join(user_following)}")
    print(f"Ranking {len(posts)} candidate posts...")

    # Run the ranking
    random.seed(42)  # For reproducible demo
    results = rank_posts(posts, user_following)

    # Show results
    print("\n" + "=" * 60)
    print("FINAL RANKED FEED")
    print("=" * 60)

    for rank, (post, score, predictions) in enumerate(results, 1):
        network = "IN" if post.author_id in user_following else "OUT"
        video = " [VIDEO]" if post.has_video else ""
        print(f"\n#{rank} (score: {score:.4f}) [{network}]{video}")
        print(f"   @{post.author_id}: {post.text[:45]}...")

    # Show detailed breakdown for top post
    print("\n" + "=" * 60)
    print("DETAILED BREAKDOWN: Top Ranked Post")
    top_post, top_score, top_predictions = results[0]
    print_ranking_breakdown(top_post, top_score, top_predictions)

    # Demonstrate author diversity effect
    print("\n" + "=" * 60)
    print("AUTHOR DIVERSITY EFFECT")
    print("=" * 60)
    alice_posts = [(p, s) for p, s, _ in results if p.author_id == "alice"]
    if len(alice_posts) >= 2:
        print(f"\n@alice has {len(alice_posts)} posts in results:")
        for i, (post, score) in enumerate(alice_posts):
            decay = 0.7 ** i
            print(f"  Post {i+1}: score={score:.4f} (decay factor: {decay:.2f})")
        print("\nDiversity decay ensures no single author dominates the feed.")


if __name__ == "__main__":
    main()
