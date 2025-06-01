# Roadmaps

1. Log user activities
2. Save user response
3. Create leader board 
4. Create score + trophies 
5. Email 
6. password reset 


🏆 1. Score System
Track and reward quiz participation and correctness.

Event	Points
Completing a quiz	+10
Correct answer	+2
Finishing quiz with 100%	+20
Finishing under 1 min	+5
Streak of 5 correct answers	+10
First quiz of the day	+3

✅ Track total score in UserProfile model.

🥇 2. Badges / Trophies
Assign digital badges when users achieve certain milestones.

🎖 Badge Ideas:
Badge Name	Criteria
Bookworm	Finish all quizzes in one book
Quiz Champion	Score 90%+ on 10 quizzes
Streak Master	Get 20 correct answers in a row
Fast Thinker	Complete 5 quizzes in under a minute each
Night Owl	Finish 3 quizzes after 10 PM
Early Bird	Finish 3 quizzes before 8 AM
Perfect Score	Score 100% on any quiz
Persistent Learner	Play daily for 7 days in a row

✅ Store badges in a separate Badge model and associate via UserProfile.badges.

📈 3. Leaderboards
Show top users globally, per book, or per week/month.

Type	Description
Global	All-time top scorers
Per Book	Top scorers per book
Weekly	Resets every 7 days
Friends Only	If you support following/friends

🔄 4. Progression Levels
Create levels based on cumulative score:

Level	Score Range
Beginner	0–99
Learner	100–299
Explorer	300–699
Achiever	700–1499
Scholar	1500+

✅ Automatically promote users as score increases.

🧩 5. Challenge Mode
Daily Quiz Challenge: Limited-time quiz per day

Weekly Boss Quiz: Tough, longer quiz for extra points and rare badges

Time Attack: Earn points based on speed

💬 6. Achievements / Activity Feed
Let users:

Post quiz completions as a “status”

View friend or public activity feed: “Yosmi earned the Fast Thinker badge!”

🔒 7. Unlockables
Gamify content access:

Some quizzes, books, or badges can only be accessed after completing prerequisites.

🔍 8. Analytics for Learners
Let users track their:

Accuracy per topic

Daily improvement graph

Badges and next milestones